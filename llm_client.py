from pathlib import Path
from typing import List, Dict, Optional
import base64
import os
import openai

# Make sure you set OPENAI_API_KEY in environment
# export OPENAI_API_KEY="sk-..."

def generate_files_from_brief(
    brief: str,
    attachments: List[Dict],
    round_num: int = 1,
    previous_repo_dir: Optional[Path] = None
) -> List[Dict]:
    """
    Generate project files from a brief using OpenAI API.
    Supports R1 creation and R2 updates.

    Parameters
    ----------
    brief : str
        The project instructions.
    attachments : list of dict
        Each dict: {"name": str, "url": str (data URI)}
    round_num : int
        1 = new project, 2 = update existing project
    previous_repo_dir : Path
        Path to previous repo (for round 2 updates)
    
    Returns
    -------
    files : list of dict
        Each dict: {"path": relative_path, "content": str}
    """

    context = ""

    if round_num == 2 and previous_repo_dir is not None:
        # Include current repo files in context for update
        for root, _, files in os.walk(previous_repo_dir):
            for f in files:
                path = Path(root) / f
                rel_path = path.relative_to(previous_repo_dir)
                with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                context += f"\nFile: {rel_path}\n{content}\n"

    # Include attachments info
    attachments_info = "\n".join([f"{a['name']}: {a['url'][:80]}..." for a in attachments])

    prompt = f"""
You are a code generator LLM.

Round: {round_num}
Brief:
{brief}

Attachments:
{attachments_info}

Existing files (if any):
{context}

Task: Generate the minimal set of files for this app. Return as a JSON array of objects:
[{{"path": "file_path", "content": "file_content"}}]
"""

    # Call OpenAI Chat Completions API (1.0.0+)
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate project files."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=2500,
    )

    text = response.choices[0].message.content

    import json
    try:
        files = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"LLM response could not be parsed as JSON:\n{text}")

    return files
