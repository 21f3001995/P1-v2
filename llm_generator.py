from llm_client import generate_files_from_brief
from pathlib import Path
import os
import base64
import shutil

def generate_app_from_brief(brief: str, attachments_dir: Path, repo_dir: Path, round_num: int = 1):
    """
    Generates or updates project files using LLM, considering round number.
    - Round 1: initial creation
    - Round 2: incremental updates / modifications
    """
    # Convert attachments folder into JSON objects with base64 URLs
    attachments = []
    for f in os.listdir(attachments_dir):
        path = attachments_dir / f
        with open(path, "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode()
        mime = "application/octet-stream"
        if f.endswith(".csv"):
            mime = "text/csv"
        elif f.endswith(".json"):
            mime = "application/json"
        attachments.append({"name": f, "url": f"data:{mime};base64,{b64}"})

    if round_num == 1:
        # Round 1: initial generation
        files = generate_files_from_brief(brief, attachments)
    else:
        # Round 2: incremental updates
        # Backup current repo
        backup_dir = repo_dir / f"_backup_round{round_num-1}"
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(repo_dir, backup_dir, dirs_exist_ok=True)

        # Call LLM with previous repo context for incremental updates
        files = generate_files_from_brief(
            brief,
            attachments,
            previous_repo_dir=repo_dir
        )

    # Save/update files to repo_dir
    for file in files:
        path = repo_dir / file["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(file["content"])
