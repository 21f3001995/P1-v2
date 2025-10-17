"""
Project: LLM Code Deployment (Student API)
------------------------------------------
This FastAPI app implements the student-side server that:
1. Receives and verifies task requests (Round 1 or 2)
2. Uses an LLM generator to build or update an app
3. Pushes to GitHub and deploys GitHub Pages
4. Notifies the instructor’s evaluation_url with repo metadata
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
import time

app = FastAPI(title="LLM Code Deployment - Student API", version="1.0.0")


# ---------------------------------------------------------------------
# 🧩 1. POST /api-endpoint : receive task
# ---------------------------------------------------------------------
@app.post("/api-endpoint")
async def receive_task(request: Request):
    """
    Accepts POST JSON with fields:
      email, secret, task, round, nonce, brief, evaluation_url, attachments, checks
    Verifies secret and starts async build/update job.
    """
    try:
        data = await request.json()

        # 🔒 Secret verification
        if data.get("secret") != STUDENT_SECRET:
            raise HTTPException(status_code=403, detail="Invalid secret")

        # Spawn async job so the HTTP response returns immediately
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
# 🧠 2. process_task(): core logic
# ---------------------------------------------------------------------
async def process_task(data: dict):
    """
    Handles building or updating the app based on round number.
    Steps:
      1. Save attachments
      2. Generate or update project using LLM
      3. Push to GitHub and enable Pages
      4. Notify instructor via evaluation_url
    """
    try:
        email = data["email"]
        secret = data["secret"]
        task_id = data["task"]
        round_num = int(data.get("round", 1))
        nonce = data.get("nonce", str(uuid4()))
        brief = data.get("brief", "")
        evaluation_url = data["evaluation_url"]
        attachments = data.get("attachments", [])
        checks = data.get("checks", [])

        print(f"\n🚀 Starting Round {round_num} for {task_id} ({email})")

        # Step 1: create workspace
        repo_folder = BASE_REPO_DIR / f"{task_id}_{nonce}_app"
        if repo_folder.exists():
            shutil.rmtree(repo_folder)
        repo_folder.mkdir(parents=True, exist_ok=True)

        # Step 2: save attachments
        attachments_dir = repo_folder / "attachments"
        saved_files = save_attachments(attachments, attachments_dir)
        print(f"📎 Saved {len(saved_files)} attachments.")

        # Step 3: generate or update project files
        generate_app_from_brief(brief, attachments_dir, repo_folder, round_num=round_num)
        print("✨ LLM generation completed.")

        # Step 4: add LICENSE + README.md
        (repo_folder / "LICENSE").write_text("MIT License\n")
        readme_text = f"# {task_id}\n\n## Brief\n{brief}\n\n## Checks\n" + \
                      "\n".join([f"- {c}" for c in checks]) + "\n\nMIT License."
        (repo_folder / "README.md").write_text(readme_text)

        # Step 5: create or update repo on GitHub
        repo_name, commit_sha, pages_url = create_or_update_repo(task_id, repo_folder, round_num)
        print(f"✅ GitHub push complete: {repo_name} @ {commit_sha}")

        # Step 6: notify instructor’s evaluation_url
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
# 📨 3. Notify instructor evaluation_url
# ---------------------------------------------------------------------
async def notify_evaluation_api(evaluation_url, email, task_id, round_num, nonce,
                                repo_name, commit_sha, pages_url):
    """
    Sends repo + commit metadata to instructor evaluation API.
    Retries on failure with exponential backoff.
    """
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
# 🧪 4. Mock evaluation endpoint (local testing)
# ---------------------------------------------------------------------
@app.post("/eval-mock")
async def eval_mock(request: Request):
    """
    Local mock of the instructor’s evaluation_url.
    Prints payload and returns HTTP 200.
    """
    data = await request.json()
    print("\n🧪 Eval mock received:")
    print(json.dumps(data, indent=2))
    return {"status": "received", "round": data.get("round", "N/A")}


# ---------------------------------------------------------------------
# ❤️ 5. Health check
# ---------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok", "project": "LLM Code Deployment"}
