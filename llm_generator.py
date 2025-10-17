from llm_client import generate_files_from_brief
from pathlib import Path
import base64
import os


def generate_app_from_brief(
    brief: str,
    attachments_dir: Path,
    repo_dir: Path,
    round_num: int = 1,
    previous_repo_dir: Path = None
):
    """
    Generate or update the app from brief.
    Saves all files into repo_dir.
    """

    import os

    # Convert attachments folder to list of dicts
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

    # Generate files from LLM
    files = generate_files_from_brief(
        brief,
        attachments,
        round_num=round_num,
        previous_repo_dir=previous_repo_dir
    )

    # Save files
    for file in files:
        path = repo_dir / file["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(file["content"])
