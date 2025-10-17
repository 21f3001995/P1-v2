from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env if present
load_dotenv()

# ---------------------------------------------------------------------
# Core Credentials
# ---------------------------------------------------------------------
STUDENT_SECRET = os.getenv("STUDENT_SECRET")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")

# ---------------------------------------------------------------------
# Local Directories
# ---------------------------------------------------------------------
BASE_REPO_DIR = Path(os.getenv("BASE_REPO_DIR", "./repos"))
BASE_REPO_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------
# Debug Mode
# ---------------------------------------------------------------------
# Enables verbose internal logging (LLM responses, payloads, etc.)
# You can set RENDER_DEBUG_MODE=false in Render environment variables to disable.
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
