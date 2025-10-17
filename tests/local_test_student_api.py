# local_test_full.py
import threading
import time
import json
from fastapi import FastAPI, Request
import uvicorn
import requests

# ---------- MOCK EVALUATION SERVER ----------
eval_app = FastAPI()

received_evals = []

@eval_app.post("/mock-eval")
async def mock_eval(request: Request):
    data = await request.json()
    print(f"\n📨 Evaluation received:\n{json.dumps(data, indent=2)}\n")
    received_evals.append(data)
    return {"status": "ok"}

def start_eval_mock():
    uvicorn.run(eval_app, host="127.0.0.1", port=8001, log_level="info")

# Run mock evaluation server in background
threading.Thread(target=start_eval_mock, daemon=True).start()
time.sleep(1)  # wait for server to start

# ---------- CONFIG ----------
STUDENT_API_URL = "http://127.0.0.1:8000/api-endpoint"
evaluation_url = "http://127.0.0.1:8000/eval-mock"
SECRET = "21f3001995-P1"  # must match what app.py expects
EMAIL = "21f3001995@ds.study.iitm.ac.in"

# ---------- TASK TEMPLATES ----------
round1_task = {
    "email": EMAIL,
    "secret": SECRET,
    "task": "test-task-1",
    "round": 1,
    "nonce": "nonce-123",
    "brief": "Create a test page displaying Hello World",
    "checks": ["Page loads", "Displays Hello World"],
    "evaluation_url": evaluation_url,
    "attachments": []
}

round2_task = {
    "email": EMAIL,
    "secret": SECRET,
    "task": "test-task-1",
    "round": 2,
    "nonce": "nonce-123",
    "brief": "Update page to display Hello Render",
    "checks": ["Page loads", "Displays Hello Render"],
    "evaluation_url": evaluation_url,
    "attachments": []
}

# ---------- SEND TASKS ----------
def send_task(task):
    print(f"🚀 Sending Round {task['round']} request...")
    r = requests.post(STUDENT_API_URL, json=task)
    print(f"Status: {r.status_code}")
    try:
        print(r.json())
    except Exception:
        print(r.text)

send_task(round1_task)
time.sleep(5)  # wait for Round 1 processing

send_task(round2_task)
time.sleep(5)  # wait for Round 2 processing

print("\n✅ Local test finished.")
print("Check:")
print(" - repos/ directory for generated repo folders")
print(" - GitHub account for new/updated repository")
print(" - FastAPI logs for internal actions")
print(" - Evaluation server console for received POSTs")
