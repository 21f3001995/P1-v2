"""
Project: LLM Code Deployment (Student API)
------------------------------------------
FastAPI app for student-side workflow:
1. Receives task requests (Round 1/2)
2. Generates/upgrades apps using LLM
3. Pushes to GitHub and deploys GitHub Pages
4. Notifies evaluation API
"""

from fastapi import FastAPI, Request, HTTPException
from config import STUDENT_SECRET, BASE_REPO_DIR, GITHUB_USERNAME
from github_utils import create_or_update_repo
from llm_generator import generate_app_from_brief
from attachment_utils import save_attachments

from pathlib import Path
from uuid import uuid4
import asyncio
import shutil
import traceback
import requests
import json

app = FastAPI(title="LLM Code Deployment - Student API", version="1.0.0")

# ---------------------------------------------------------------------
# 1️⃣ POST /api-endpoint : receive task
# ---------------------------------------------------------------------
@app.post("/api-endpoint")
async def receive_task(request: Request):
    try:
        data = await request.json()

        # Secret verification
        if data.get("secret") != STUDENT_SECRET:
            raise HTTPException(status_code=403, detail="Invalid secret")

        # Async process task
        asyncio.create_task(process_task(data))

        return {
            "status": "ok",
            "message": "Request received and processing started.",
            "task": data.get("task"),
            "round": data.get("round", 1),
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------------------------------
# 2️⃣ process_task(): core logic
# ---------------------------------------------------------------------
async def process_task(data: dict):
    try:
        email = data["email"]
        task_id = data["task"]
        round_num = int(data.get("round", 1))
        nonce = data.get("nonce", str(uuid4()))
        brief = data.get("brief", "")
        evaluation_url = data["evaluation_url"]
        attachments = data.get("attachments", [])
        checks = data.get("checks", [])

        print(f"\n🚀 Starting Round {round_num} for {task_id} ({email})")

        # Create workspace
        repo_folder = BASE_REPO_DIR / f"{task_id}_{nonce}_app"
        if repo_folder.exists():
            shutil.rmtree(repo_folder)
        repo_folder.mkdir(parents=True, exist_ok=True)

        # Save attachments
        attachments_dir = repo_folder / "attachments"
        saved_files = save_attachments(attachments, attachments_dir)
        print(f"📎 Saved {len(saved_files)} attachments.")

        # Generate/update project files
        generate_app_from_brief(brief, attachments_dir, repo_folder, round_num=round_num)
        print("✨ LLM generation completed.")

        # Add LICENSE + README.md
        (repo_folder / "LICENSE").write_text("MIT License\n")
        readme_text = f"# {task_id}\n\n## Brief\n{brief}\n\n## Checks\n" + \
                      "\n".join([f"- {c}" for c in checks]) + "\n\nMIT License."
        (repo_folder / "README.md").write_text(readme_text)

        # Create/update repo on GitHub
        repo_name, commit_sha, pages_url = create_or_update_repo(task_id, repo_folder, round_num)
        print(f"✅ GitHub push complete: {repo_name} @ {commit_sha}")

        # Notify instructor evaluation_url
        await notify_evaluation_api(
            evaluation_url=evaluation_url,
            email=email,
            task_id=task_id,
            round_num=round_num,
            nonce=nonce,
            repo_name=repo_name,
            commit_sha=commit_sha,
            pages_url=pages_url,
        )

        print(f"🏁 Round {round_num} completed successfully.\n")

    except Exception as e:
        print("❌ process_task() failed:", e)
        traceback.print_exc()

# ---------------------------------------------------------------------
# 3️⃣ Notify instructor evaluation_url
# ---------------------------------------------------------------------
async def notify_evaluation_api(evaluation_url, email, task_id, round_num, nonce,
                                repo_name, commit_sha, pages_url):
    payload = {
        "email": email,
        "task": task_id,
        "round": round_num,
        "nonce": nonce,
        "repo_url": f"https://github.com/{GITHUB_USERNAME}/{repo_name}",
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    delay = 1
    for attempt in range(5):
        try:
            print(f"📤 POST → {evaluation_url} (attempt {attempt + 1})")
            print(json.dumps(payload, indent=2))

            response = await asyncio.to_thread(
                lambda: requests.post(evaluation_url, json=payload, timeout=15)
            )

            if response.status_code == 200:
                print("✅ Evaluation API acknowledged.")
                return
            else:
                print(f"⚠️ Evaluation API returned {response.status_code}: {response.text}")

        except Exception as e:
            print(f"⚠️ Notify attempt {attempt + 1} failed:", e)

        await asyncio.sleep(delay)
        delay *= 2  # exponential backoff

    print("❌ All notify attempts failed.")

# ---------------------------------------------------------------------
# 4️⃣ Mock evaluation endpoint (local testing)
# ---------------------------------------------------------------------
@app.post("/eval-mock")
async def eval_mock(request: Request):
    data = await request.json()
    print("\n🧪 Eval mock received:")
    print(json.dumps(data, indent=2))
    return {"status": "received", "round": data.get("round", "N/A")}

# ---------------------------------------------------------------------
# 5️⃣ Health check
# ---------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "project": "LLM Code Deployment"}

@app.get("/")
def root():
    return {"status": "ok", "project": "LLM Code Deployment"}
