from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.onegov.nsw.gov.au"
API_KEY = "GAOTu9pI4uFD3tjp8wJv4i8AHlb2p6SP"
API_SECRET = "hAfxSmMepBMn5iIX"
AUTH_HEADER = "Basic R0FPVHU5cEk0dUZEM3RqcDh3SnY0aThBSGxiMnA2U1A6aEFmeFNtTWVwQk1uNWlJWA=="

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

@app.route("/contractlist", methods=["GET"])
def get_contract_list():
    token = get_access_token()
    start_row = request.args.get("startRow", 0)
    url = f"{API_BASE_URL}/etender/v1/contractlist"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
    }
    params = {"startRow": start_row}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

@app.route("/contractdetails", methods=["GET"])
def get_contract_details():
    token = get_access_token()
    cn_uuid = request.args.get("CNUUID")
    url = f"{API_BASE_URL}/etender/v1/contractdetails"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
    }
    params = {"CNUUID": cn_uuid}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

@app.route("/plannedprocurementlist", methods=["GET"])
def get_planned_procurement_list():
    token = get_access_token()
    start_row = request.args.get("startRow", 0)
    url = f"{API_BASE_URL}/etender/v1/plannedprocurementlist"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
    }
    params = {"startRow": start_row}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

@app.route("/plannedprocurementdetails", methods=["GET"])
def get_planned_procurement_details():
    token = get_access_token()
    pp_uuid = request.args.get("PlannedProcurementUUID")
    url = f"{API_BASE_URL}/etender/v1/plannedprocurementdetails"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
    }
    params = {"PlannedProcurementUUID": pp_uuid}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

@app.route("/standingoffernoticedetails", methods=["GET"])
def get_standing_offer_notice_details():
    token = get_access_token()
    son_uuid = request.args.get("SONUUID")
    url = f"{API_BASE_URL}/etender/v1/standingoffernoticedetails"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
    }
    params = {"SONUUID": son_uuid}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

@app.route("/standingoffernoticelist", methods=["GET"])
def get_standing_offer_notice_list():
    token = get_access_token()
    start_row = request.args.get("startRow", 0)
    url = f"{API_BASE_URL}/etender/v1/standingoffernoticelist"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
    }
    params = {"startRow": start_row}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run()
