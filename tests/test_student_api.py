import requests
import json
import uuid

# ----------------------------
# Configuration
# ----------------------------
API_URL = "https://llm-code-deployment-6om1.onrender.com/api-endpoint"  # your Render URL
EVAL_URL = "http://127.0.0.1:9000/notify"  # local mock evaluation
SECRET = "21f3001995-P1"
EMAIL = "21f3001995@ds.study.iitm.ac.in"
TASK_ID = "test-task-1.1"

# Sample attachment (can be empty or a small dummy file)
ATTACHMENTS = [
    {"name": "sample.txt", "url": "data:text/plain;base64,SGVsbG8gd29ybGQh"}  # "Hello world!"
]

CHECKS = [
    "Repo has MIT license",
    "README.md is professional",
    "Page displays captcha URL passed at ?url=...",
    "Page displays solved captcha text within 15 seconds"
]

BRIEF = "Create a minimal app for testing Round 1"

# ----------------------------
# Helper function
# ----------------------------
def send_task(round_num, brief):
    nonce = str(uuid.uuid4())
    payload = {
        "email": EMAIL,
        "secret": SECRET,
        "task": TASK_ID,
        "round": round_num,
        "nonce": nonce,
        "brief": brief,
        "evaluation_url": EVAL_URL,
        "attachments": ATTACHMENTS,
        "checks": CHECKS
    }

    print(f"\n🚀 Sending Round {round_num} request...")
    resp = requests.post(API_URL, json=payload)
    print("Status:", resp.status_code)
    print(resp.json())

# ----------------------------
# Run tests
# ----------------------------
if __name__ == "__main__":
    # Round 1: build
    send_task(1, BRIEF)

    # Round 2: revision
    BRIEF2 = "Update the app for Round 2 testing"
    send_task(2, BRIEF2)
