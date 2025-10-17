"""
test_student_api_r2.py
----------------------
Sends Round 2 task to Student API.
Includes logging for debugging interactive features (currency conversion, filtering, markdown).
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
attachments_dir = Path("./sample_attachments_r2")
attachments_dir.mkdir(exist_ok=True)

(sample_csv := attachments_dir / "sales.csv").write_text("product,sales\nA,100\nB,200\nC,150")
(sample_json := attachments_dir / "rates.json").write_text(json.dumps({"USD": 1, "EUR": 0.9}))
(sample_md := attachments_dir / "input.md").write_text("# Title\n\nThis is **bold** text.")

def encode_attachments():
    files = []
    for f in attachments_dir.iterdir():
        if f.is_file():
            b64 = base64.b64encode(f.read_bytes()).decode()
            mime = "text/csv" if f.suffix == ".csv" else \
                   "application/json" if f.suffix == ".json" else \
                   "text/markdown"
            files.append({"name": f.name, "url": f"data:{mime};base64,{b64}"})
    return files

# ---------------- BRIEF ----------------
BRIEF_R2 = """
Update the HTML page:
1. Add table #product-sales listing each product and its sales
2. Add currency selector #currency-picker that converts #total-sales using rates.json
3. Filter products by region #region-filter and update #total-sales accordingly
4. Render Markdown content from input.md in #markdown-output
5. Include console.log statements to debug CSV parsing, currency conversion, filtering, and markdown rendering
"""

DEFAULT_CHECKS = [
    "Repo has MIT license",
    "README.md is professional",
    "Page displays total sales in #total-sales",
    "Page shows product table #product-sales",
    "Currency conversion works via #currency-picker",
    "Markdown rendered in #markdown-output"
]

# ---------------- HELPER ----------------
def send_task():
    nonce = str(uuid4())
    payload = {
        "email": EMAIL,
        "secret": STUDENT_SECRET,
        "task": TASK_ID,
        "round": 2,
        "nonce": nonce,
        "brief": BRIEF_R2,
        "evaluation_url": EVAL_MOCK_URL,
        "attachments": encode_attachments(),
        "checks": DEFAULT_CHECKS
    }
    print("\n🚀 Sending Round 2 request...")
    try:
        resp = requests.post(API_URL, json=payload, timeout=60)
        print("Status:", resp.status_code)
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    send_task()
    print("\n✅ Round 2 test finished. Check console.logs in deployed page for debugging.")
