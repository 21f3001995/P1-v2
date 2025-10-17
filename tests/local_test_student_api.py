"""
Local test script for student LLM Code Deployment API.
------------------------------------------------------
This script simulates professor requests for Round 1 and Round 2.
Ensure your FastAPI app is running locally at http://127.0.0.1:8000

Usage:
    python local_test_student_api.py
"""

import base64
import json
import requests
import time
from pathlib import Path

# -------------------------------
# CONFIGURATION
# -------------------------------
API_URL = "http://127.0.0.1:8000/api-endpoint"   # local FastAPI endpoint
STUDENT_SECRET = "21f3001995-P1"      # must match .env
EVALUATION_URL = "http://127.0.0.1:9999/dummy"    # dummy callback endpoint
TEST_FILE = "sample_for_LocalTesting.txt"

# -------------------------------
# HELPER: Base64 encode file
# -------------------------------
def encode_file(filepath: str):
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:text/plain;base64,{b64}"

# -------------------------------
# 1️⃣ CREATE A DUMMY ATTACHMENT
# -------------------------------
Path(TEST_FILE).write_text("This is a dummy file for local Round 1 test.\n")

# -------------------------------
# 2️⃣ PREPARE ROUND 1 PAYLOAD
# -------------------------------
round1_payload = {
    "secret": STUDENT_SECRET,
    "round": 1,
    "email":"21f3001995@ds.study.iitm.ac.in",
    "task_id": "local_task_001",
    "evaluation_url": EVALUATION_URL,
    "brief": "Create a simple HTML page with a blue title 'Hello Local Test'.",
    "attachments": [encode_file(TEST_FILE)]
}

print("\n🚀 Sending Round 1 request...")
r1 = requests.post(API_URL, json=round1_payload)
print(f"Status: {r1.status_code}")
try:
    print(json.dumps(r1.json(), indent=2))
except Exception:
    print(r1.text)

# -------------------------------
# 3️⃣ WAIT THEN DO ROUND 2 UPDATE
# -------------------------------
time.sleep(3)

round2_payload = {
    "secret": STUDENT_SECRET,
    "round": 2,
    "email":"21f3001995@ds.study.iitm.ac.in",
    "task_id": "local_task_001",
    "evaluation_url": EVALUATION_URL,
    "brief": "Update the HTML to include current time and a random quote.",
    "attachments": []
}

print("\n🔁 Sending Round 2 request...")
r2 = requests.post(API_URL, json=round2_payload)
print(f"Status: {r2.status_code}")
try:
    print(json.dumps(r2.json(), indent=2))
except Exception:
    print(r2.text)

# -------------------------------
# ✅ RESULT SUMMARY
# -------------------------------
print("\n✅ Local test finished.")
print("Check:")
print(" - repos/ directory for generated repo folders")
print(" - GitHub account for new/updated repository")
print(" - FastAPI logs for internal actions")
