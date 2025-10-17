"""
llm_generator.py
----------------
Handles project generation and professional README creation using LLM.
"""

from llm_client import generate_files_from_brief
from pathlib import Path
import base64
import os
from config import DEBUG_MODE
import json

def generate_app_from_brief(
    brief: str,
    attachments_dir: Path,
    repo_dir: Path,
    round_num: int = 1
):
    """
    Generates or updates project files from a brief:
    - Converts attachments to base64 URLs
    - Calls LLM client to generate code files
    - Writes files to repo_dir
    """

    # Convert attachments to base64 URLs
    attachments = []
    if attachments_dir.exists():
        for f in attachments_dir.iterdir():
            if f.is_file():
                with open(f, "rb") as fp:
                    b64 = base64.b64encode(fp.read()).decode()
                mime = "application/octet-stream"
                if f.suffix == ".csv":
                    mime = "text/csv"
                elif f.suffix == ".json":
                    mime = "application/json"
                elif f.suffix == ".md":
                    mime = "text/markdown"
                attachments.append({"name": f.name, "url": f"data:{mime};base64,{b64}"})

    # Previous repo for Round 2
    previous_repo_dir = repo_dir if round_num > 1 else None

    # Generate project files via LLM
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

    if DEBUG_MODE:
        print(f"📝 Generated {len(files)} file(s) from LLM for round {round_num}")


def generate_readme_for_repo(
    brief: str,
    attachments_dir: Path,
    round_num: int = 1,
    existing_readme: str = "",
    checks: list = None
) -> str:
    """
    Generates a professional README for the repo using LLM:
    - Preserves existing R1 content for R2
    - Lists attachments and evaluation checks
    - Returns the README content as a string
    """

    checks = checks or []

    # List attachment filenames
    attachment_files = ""
    if attachments_dir.exists():
        attachment_files = "\n".join([f"- {f.name}" for f in attachments_dir.iterdir() if f.is_file()])

    prompt = f"""
You are an expert software engineer. Generate a professional README.md for a GitHub repository.

Instructions:
- Include project title, brief, deployment info, license.
- Document attachments and evaluation checks.
- Preserve existing content if updating (round_num > 1).
- Return markdown only.

Round: {round_num}
Brief: {brief}
Attachments:
{attachment_files}
Evaluation checks:
{json.dumps(checks)}

Existing README content:
{existing_readme if round_num > 1 else ""}
"""

    # Call LLM to generate README
    from llm_client import client  # OpenAI client
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500
    )

    readme_text = response.choices[0].message.content.strip()

    if DEBUG_MODE:
        print("📝 LLM README output:")
        print(readme_text[:1000] + ("..." if len(readme_text) > 1000 else ""))

    return readme_text
