"""
test_student_api_debug.py
-------------------------
Enhanced testing script for your Student API.
✅ Supports Round 1 / Round 2 selection
✅ Sends realistic briefs and attachments
✅ Displays LLM logs and generated code (if DEBUG_MODE=true on backend)
✅ Prints evaluation payloads & HTTP response info
"""

import requests
import json
import base64
from pathlib import Path
from uuid import uuid4

# ---------------- CONFIG ----------------
API_URL = "https://llm-code-deployment-6om1.onrender.com/api-endpoint"   # your deployed API
EVAL_MOCK_URL = "https://webhook.site/c7bcc38a-d1fa-4c2f-9e5d-a8dc8775df32"  # webhook for eval payloads
STUDENT_SECRET = "21f3001995-P1"
EMAIL = "21f3001995@ds.study.iitm.ac.in"

# Change task ID for each new test to avoid GitHub conflicts
TASK_ID = "test-task-llm-debug-X2"

# ---------------- ATTACHMENTS ----------------
attachments_dir = Path("./debug_attachments")
attachments_dir.mkdir(exist_ok=True)

# Example CSV and JSON attachments
(sample_csv := attachments_dir / "sales.csv").write_text("product,sales\nA,100\nB,200\nC,150")
(sample_json := attachments_dir / "rates.json").write_text(json.dumps({"USD": 1, "EUR": 0.9}))
(sample_md := attachments_dir / "readme.md").write_text("# Hello\n\nThis is a debug markdown sample.")

def encode_attachments():
    """Convert files in attachments_dir into base64-encoded data URLs."""
    files = []
    for f in attachments_dir.iterdir():
        if f.is_file():
            mime = {
                ".csv": "text/csv",
                ".json": "application/json",
                ".md": "text/markdown"
            }.get(f.suffix, "application/octet-stream")
            with open(f, "rb") as fp:
                b64 = base64.b64encode(fp.read()).decode()
            files.append({"name": f.name, "url": f"data:{mime};base64,{b64}"})
    return files

# ---------------- BRIEFS ----------------
BRIEF_R1 = """
Generate a single-page HTML app that:
1. Reads sales.csv and computes total sales.
2. Displays total in element #total-sales.
3. Include console.log for parsed CSV, numeric values, and computed sum.
4. Load Bootstrap 5 via jsDelivr.
5. Include MIT License and README.md.
"""

BRIEF_R2 = """
Update previous page to:
1. Add a product table (#product-sales).
2. Add currency selector (#currency-picker) using rates.json.
3. Display converted total in #total-sales dynamically.
4. Include console.log for conversion rates and events.
5. Show Markdown (readme.md) in #markdown-output section.
"""

DEFAULT_CHECKS = [
    "Repo has MIT license",
    "README.md is professional",
    "Page displays total sales in #total-sales",
    "Page includes Bootstrap CSS",
    "Displays product table and conversion selector",
]

# ---------------- HELPER ----------------
def send_task(round_num: int, brief: str):
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
        response = requests.post(API_URL, json=payload, timeout=90)
        print("\n📩 Response received:")
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(json.dumps(data, indent=2))

            # ✅ Print LLM logs if backend DEBUG_MODE is ON
            if "llm_generated_files" in data:
                print("\n🧠 LLM Generated Files:")
                for fname, content in data["llm_generated_files"].items():
                    print(f"\n--- {fname} ---\n{content[:2000]}\n{'...' if len(content) > 2000 else ''}")
            else:
                print("\n(No LLM debug logs — set DEBUG_MODE=true in backend to enable)")
        except Exception:
            print("Response content (non-JSON):", response.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("Select Round:")
    print("1. Round 1 (new app)")
    print("2. Round 2 (update existing repo)")
    try:
        choice = int(input("Enter 1 or 2: ").strip())
    except ValueError:
        choice = 1

    if choice == 1:
        send_task(1, BRIEF_R1)
    else:
        send_task(2, BRIEF_R2)

    print("\n✅ Test finished. Check webhook.site for evaluation payloads & console logs on GitHub Pages.")
