import os
from flask import Flask, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# Constants
API_BASE_URL = "https://api.onegov.nsw.gov.au"
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
AUTH_HEADER = os.getenv("AUTH_HEADER")


# Function to get access token
def get_access_token():
    url = f"{API_BASE_URL}/oauth/client_credential/accesstoken"
    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/json",
    }
    payload = {"grant_type": "client_credentials"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]


# Route to fetch contracts list
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
    return jsonify(response.json())


# Route to fetch contract details
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


# Route to fetch planned procurement list
@app.route("/plannedprocurementlist", methods=["GET"])
def get_planned_procurement_list():
    start_row = request.args.get("startRow", 0)
    token = get_access_token()
    url = f"{API_BASE_URL}/etender/v1/plannedprocurementlist"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json",
    }
    params = {"startRow": start_row}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())


# Route to fetch planned procurement details
@app.route("/plannedprocurementdetails", methods=["GET"])
def get_planned_procurement_details():
    procurement_id = request.args.get("PlannedProcurementUUID")
    if not procurement_id:
        return jsonify({"error": "PlannedProcurementUUID is required"}), 400
    token = get_access_token()
    url = f"{API_BASE_URL}/etender/v1/plannedprocurementdetails"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json",
    }
    params = {"PlannedProcurementUUID": procurement_id}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())


# Route to fetch standing offer notice details
@app.route("/standingoffernoticedetails", methods=["GET"])
def get_standing_offer_notice_details():
    son_id = request.args.get("SONUUID")
    if not son_id:
        return jsonify({"error": "SONUUID is required"}), 400
    token = get_access_token()
    url = f"{API_BASE_URL}/etender/v1/standingoffernoticedetails"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json",
    }
    params = {"SONUUID": son_id}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())


# Route to fetch standing offer notice list
@app.route("/standingoffernoticelist", methods=["GET"])
def get_standing_offer_notice_list():
    start_row = request.args.get("startRow", 0)
    token = get_access_token()
    url = f"{API_BASE_URL}/etender/v1/standingoffernoticelist"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json",
    }
    params = {"startRow": start_row}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())


# Root endpoint
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "API is running"})


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
