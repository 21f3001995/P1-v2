"""
test_student_api_r1.py
----------------------
Sends Round 1 task to Student API.
Includes logging for debugging LLM-generated HTML/JS.
"""

import requests
import json
import base64
from pathlib import Path
from uuid import uuid4

# ---------------- CONFIG ----------------
API_URL = "https://llm-code-deployment-6om1.onrender.com/api-endpoint"
EVAL_MOCK_URL = "https://webhook.site/c7bcc38a-d1fa-4c2f-9e5d-a8dc8775df32"
STUDENT_SECRET = "21f3001995-P1"
TASK_ID = "test-task-llm-X"
EMAIL = "21f3001995@ds.study.iitm.ac.in"

# ---------------- ATTACHMENTS ----------------
attachments_dir = Path("./sample_attachments_r1")
attachments_dir.mkdir(exist_ok=True)
(sample_csv := attachments_dir / "sales.csv").write_text("product,sales\nA,100\nB,200\nC,150")

def encode_attachments():
    files = []
    for f in attachments_dir.iterdir():
        if f.is_file():
            b64 = base64.b64encode(f.read_bytes()).decode()
            mime = "text/csv" if f.suffix == ".csv" else "application/octet-stream"
            files.append({"name": f.name, "url": f"data:{mime};base64,{b64}"})
    return files

# ---------------- BRIEF ----------------
BRIEF_R1 = """
Generate a single-page HTML app:
1. Display total sales from sales.csv in element #total-sales
2. Load Bootstrap 5 from jsdelivr
3. Include console.log statements for debugging values (CSV content, parsed numbers, final total)
4. Include README.md with MIT License
"""

DEFAULT_CHECKS = [
    "Repo has MIT license",
    "README.md is professional",
    "Page displays total sales in #total-sales",
    "Page includes Bootstrap CSS"
]

# ---------------- HELPER ----------------
def send_task():
    nonce = str(uuid4())
    payload = {
        "email": EMAIL,
        "secret": STUDENT_SECRET,
        "task": TASK_ID,
        "round": 1,
        "nonce": nonce,
        "brief": BRIEF_R1,
        "evaluation_url": EVAL_MOCK_URL,
        "attachments": encode_attachments(),
        "checks": DEFAULT_CHECKS
    }
    print("\n🚀 Sending Round 1 request...")
    try:
        resp = requests.post(API_URL, json=payload, timeout=60)
        print("Status:", resp.status_code)
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    send_task()
    print("\n✅ Round 1 test finished. Check console.logs in deployed page for debugging.")
