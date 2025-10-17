"""
LLM Generator for LLM Code Deployment
-------------------------------------
Generates project files based on task brief + attachments.
Supports round_num for Round 1 vs Round 2 variations.
"""

from llm_client import generate_files_from_brief
from pathlib import Path
import os
import base64

def generate_app_from_brief(brief: str, attachments_dir: Path, repo_dir: Path, round_num: int = 1):
    """
    Generates all files for the project using LLM and saves them to repo_dir.
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

    # Generate files via LLM
    files = generate_files_from_brief(brief, attachments, round_num=round_num)

    # Save files to repo_dir
    for file in files:
        path = repo_dir / file["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(file["content"])

    # Log generated files
    print("✨ Generated files:")
    for file in files:
        print(f"- {file['path']} ({len(file['content'])} chars)")
