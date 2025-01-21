import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import logging
import time

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Constants
API_BASE_URL = "https://api.onegov.nsw.gov.au"
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
AUTH_HEADER = os.getenv("AUTH_HEADER")

# Token caching
cached_token = None
token_expiry = 0

# Logging setup
logging.basicConfig(level=logging.INFO)


# Function to get access token
def get_access_token():
    global cached_token, token_expiry
    if cached_token and time.time() < token_expiry:
        return cached_token
    try:
        url = f"{API_BASE_URL}/oauth/client_credential/accesstoken"
        headers = {
            "Authorization": AUTH_HEADER,
            "Content-Type": "application/json",
        }
        payload = {"grant_type": "client_credentials"}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        token_expiry = time.time() + int(response.json()["expires_in"])
        cached_token = response.json()["access_token"]
        return cached_token
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching token: {e}")
        return jsonify({"error": "Failed to fetch access token", "details": str(e)}), 500


# API routes
@app.route("/contractlist", methods=["GET"])
def get_contract_list():
    start_row = request.args.get("startRow", 0)
    token = get_access_token()
    url = f"{API_BASE_URL}/etender/v1/contractlist"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json",
    }
    params = {"startRow": start_row}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 429:
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    return jsonify(response.json())


@app.route("/contractdetails", methods=["GET"])
def get_contract_details():
    contract_id = request.args.get("CNUUID")
    if not contract_id:
        return jsonify({"error": "CNUUID is required"}), 400
    token = get_access_token()
    url = f"{API_BASE_URL}/etender/v1/contractdetails"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json",
    }
    params = {"CNUUID": contract_id}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())


@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "API is running"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
