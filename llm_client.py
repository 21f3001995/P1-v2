import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_files_from_brief(brief: str, attachments: list):
    """
    Uses OpenAI to generate project files from a given brief + attachments.
    Returns structured JSON with list of files (path + content).
    """
    system_prompt = (
        "You are a professional developer. Generate project files "
        "based on the given project brief and attachments. "
        "Respond ONLY in valid JSON following this schema:\n\n"
        "{ 'files': [ {'path': 'main.py', 'content': '...'} ] }"
    )

    prompt = f"""
PROJECT BRIEF:
{brief}

ATTACHMENTS:
{json.dumps(attachments, indent=2)}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    message = response.choices[0].message.content
    try:
        data = json.loads(message)
        return data.get("files", [])
    except json.JSONDecodeError:
        raise ValueError(f"❌ Invalid JSON output from LLM:\n{message}")
