from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

STUDENT_SECRET = os.getenv("STUDENT_SECRET")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_REPO_DIR = Path(os.getenv("BASE_REPO_DIR", "./repos"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")

# Ensure repo directory exists
BASE_REPO_DIR.mkdir(exist_ok=True)