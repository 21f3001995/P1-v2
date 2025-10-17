from llm_client import generate_files_from_brief
from pathlib import Path
import base64
import os

def generate_app_from_brief(
    brief: str,
    attachments_dir: Path,
    repo_dir: Path,
    round_num: int = 1
):
    """
    Handles R1/R2 project generation:
    - Converts attachments to base64 URLs
    - Calls LLM client to generate files
    - Writes files to repo_dir
    """

    # Convert attachments to base64 URLs
    attachments = []
    if attachments_dir.exists():
        for f in os.listdir(attachments_dir):
            path = attachments_dir / f
            if path.is_file():
                with open(path, "rb") as fp:
                    b64 = base64.b64encode(fp.read()).decode()
                mime = "application/octet-stream"
                if f.endswith(".csv"):
                    mime = "text/csv"
                elif f.endswith(".json"):
                    mime = "application/json"
                attachments.append({"name": f, "url": f"data:{mime};base64,{b64}"})

    # Determine previous repo for R2
    previous_repo_dir = repo_dir if round_num > 1 else None

    # Generate files from LLM
    files = generate_files_from_brief(
        brief,
        attachments=attachments,
        previous_repo_dir=previous_repo_dir
    )

    # Write files to repo_dir
    for file in files:
        file_path = repo_dir / file["path"]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as fp:
            fp.write(file["content"])
