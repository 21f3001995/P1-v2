import os
import json
import time
from openai import OpenAI
from typing import List, Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_files_from_brief(
    brief: str,
    attachments: List[Dict] = None,
    previous_repo_dir: str = None,
    max_retries: int = 3
) -> List[Dict]:
    """
    Generates project files from a brief using OpenAI.
    attachments: [{"name": "...", "url": "..."}]
    previous_repo_dir: If set, include current repo files for R2 modifications.
    Returns a list of {"path": "...", "content": "..."} dicts.
    """
    attachments = attachments or []
    prompt = f"""
You are a software engineer LLM. Generate a project as requested:

Brief:
{brief}

Attachments:
{json.dumps(attachments)}

"""
    if previous_repo_dir:
        prompt += f"\nExisting repo files: {previous_repo_dir}\nModify them as needed.\n"

    prompt += "\nReturn ONLY JSON array of files: [{'path': 'file', 'content': '...'}, ...]"

    delay = 1
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2500
            )

            text = response.choices[0].message.content.strip()

            # Parse JSON safely
            files = json.loads(text)
            # Ensure it's a list of dicts with required keys
            for f in files:
                assert "path" in f and "content" in f
            return files

        except (json.JSONDecodeError, AssertionError) as e:
            # Try to clean LLM output
            try:
                text_clean = text[text.find("["):text.rfind("]")+1]
                files = json.loads(text_clean)
                return files
            except Exception:
                pass

            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise ValueError(f"LLM response could not be parsed as JSON:\n{text}") from e

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e
