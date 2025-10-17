"""
Enhanced test_student_api.py
----------------------------
Simulates Round 1 and Round 2 task requests for LLM Code Deployment Student API.
Includes realistic briefs and attachments that mimic evaluation checks.
"""

import requests
import json
import base64
from pathlib import Path
from uuid import uuid4

# ---------------- CONFIG ----------------
API_URL = "https://llm-code-deployment-6om1.onrender.com/api-endpoint"  # Your deployed Render URL
EVAL_MOCK_URL = "https://webhook.site/c7bcc38a-d1fa-4c2f-9e5d-a8dc8775df32"  # Mock evaluator URL
STUDENT_SECRET = "21f3001995-P1"
TASK_ID = "test-task-llm-enhanced-2"
EMAIL = "21f3001995@ds.study.iitm.ac.in"

# ---------------- MOCK ATTACHMENTS ----------------
attachments_dir = Path("./sample_attachments")
attachments_dir.mkdir(exist_ok=True)

# Sample CSV for sales data
(sample_csv := attachments_dir / "sales.csv").write_text("product,sales\nA,100\nB,200\nC,150")
# Sample JSON for currency rates
(sample_json := attachments_dir / "rates.json").write_text(json.dumps({"USD": 1, "EUR": 0.9}))
# Sample Markdown
(sample_md := attachments_dir / "input.md").write_text("# Title\n\nThis is **bold** text.")

def encode_attachments():
    """Convert attachment files to base64 URLs."""
    files = []
    for f in attachments_dir.iterdir():
        if f.is_file():
            with open(f, "rb") as fp:
                b64 = base64.b64encode(fp.read()).decode()
            mime = "text/csv" if f.suffix == ".csv" else \
                   "application/json" if f.suffix == ".json" else \
                   "text/markdown"
            files.append({"name": f.name, "url": f"data:{mime};base64,{b64}"})
    return files

# ---------------- BRIEFS ----------------
BRIEF_R1 = """
Generate a single-page HTML app:
1. Display total sales from sales.csv in element #total-sales
2. Load Bootstrap 5 from jsdelivr
3. Include README.md with MIT License
"""

BRIEF_R2 = """
Update the page to:
1. Add a table #product-sales listing each product and its sales
2. Add a currency selector #currency-picker that converts #total-sales using rates.json
3. Filter products by region #region-filter and update #total-sales accordingly
4. Show Markdown content from input.md in #markdown-output
"""

# ---------------- CHECKS SIMULATION ----------------
DEFAULT_CHECKS = [
    "Repo has MIT license",
    "README.md is professional",
    "Page displays total sales in #total-sales",
    "Page includes Bootstrap CSS",
    "Page shows product table #product-sales after Round 2",
    "Currency conversion works via #currency-picker",
    "Markdown rendered in #markdown-output",
]

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
        "checks": DEFAULT_CHECKS
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
    # Round 1: Basic app creation
    send_task(1, BRIEF_R1)

    # Round 2: Feature updates with interactivity
    #send_task(2, BRIEF_R2)

    print("\n✅ Testing finished. Check webhook.site for evaluation payloads.")
