"""
test_student_api.py
-------------------
Test script for LLM Code Deployment Student API.
Simulates both Round 1 and Round 2 requests, prints evaluation JSON.
"""

import requests
import json
import base64
from pathlib import Path
from uuid import uuid4

# ---------------- CONFIG ----------------
API_URL = "https://llm-code-deployment-6om1.onrender.com/api-endpoint"  # Your deployed Render URL
EVAL_MOCK_URL = "https://webhook.site/c7bcc38a-d1fa-4c2f-9e5d-a8dc8775df32"  # Your webhook.site URL
STUDENT_SECRET = "21f3001995-P1"  # Must match your config.py
TASK_ID = "test-task-1-4-R1"
EMAIL = "21f3001995@ds.study.iitm.ac.in"

# ---------------- MOCK ATTACHMENTS ----------------
attachments_dir = Path("./sample_attachments")
attachments_dir.mkdir(exist_ok=True)

# Sample CSV for testing
(sample_csv := attachments_dir / "data.csv").write_text("product,sales\nA,100\nB,200")

def encode_attachments():
    """Convert attachment files to base64 URLs."""
    files = []
    for f in attachments_dir.iterdir():
        if f.is_file():
            with open(f, "rb") as fp:
                b64 = base64.b64encode(fp.read()).decode()
            mime = "text/csv" if f.suffix == ".csv" else "application/octet-stream"
            files.append({"name": f.name, "url": f"data:{mime};base64,{b64}"})
    return files

# ---------------- BRIEFS ----------------
BRIEF_R1 = "Generate a simple HTML page that displays the sum of sales in #total-sales."
BRIEF_R2 = "Update the page to show a table #product-sales with all products and their sales."

# ---------------- HELPER ----------------
def send_task(round_num: int, brief: str):
    """Send a POST request to the Student API."""
    nonce = str(uuid4())
    payload = {
        "email": EMAIL,
        "secret": STUDENT_SECRET,
        "task": TASK_ID,
        "round": round_num,
        "nonce": nonce,
        "brief": brief,
        "evaluation_url": EVAL_MOCK_URL,
        "attachments": encode_attachments(),
        "checks": ["Repo has MIT license", "README.md is professional"]
    }

    print(f"\n🚀 Sending Round {round_num} request...")
    try:
        resp = requests.post(API_URL, json=payload, timeout=60)
        print("Status:", resp.status_code)
        try:
            print(json.dumps(resp.json(), indent=2))
        except Exception:
            print("Response content (not JSON):", resp.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")


if __name__ == "__main__":
    # Test Round 1: Create new repo
    send_task(1, BRIEF_R1)

    # Test Round 2: Update existing repo
    #send_task(2, BRIEF_R2)

    print("\n✅ Testing finished. Check webhook.site for evaluation payloads.")
