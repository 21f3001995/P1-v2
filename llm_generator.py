from llm_client import generate_files_from_brief
from pathlib import Path

def generate_app_from_brief(brief: str, attachments_dir: Path, repo_dir: Path):
    """
    Generates all files for the project using LLM and saves them to repo_dir
    """
    # Convert attachments folder into JSON objects with base64 URLs
    import os, base64
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
    files = generate_files_from_brief(brief, attachments)

    # Save files to repo_dir
    for file in files:
        path = repo_dir / file["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(file["content"])
