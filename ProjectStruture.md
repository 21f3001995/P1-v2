# Project Directories Struture

<pre> 
P1-v1/                        # Root project folder
├─ app.py                     # FastAPI main server
├─ config.py                  # Environment variables + config
├─ requirements.txt           # Python dependencies
├─ .env                       # Local secrets (STUDENT_SECRET, GITHUB_TOKEN, etc.)
├─ github_utils.py            # GitHub repo create/update functions
├─ attachment_utils.py        # Save attachments from requests
├─ llm_client.py              # OpenAI API client (structured outputs)
├─ llm_generator.py           # Generates multi-file project from brief + attachments
├─ utils.py                   # Optional helpers (JSON extraction, validation)
├─ repos/                     # Base directory for temporary repos (from BASE_REPO_DIR)
├─ tests/                     # Optional, unit tests for your API
│  ├─ test_api.py
└─ README.md                  # Project documentation
</pre>

---------

| File                  | Responsibility                                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `app.py`              | FastAPI server. Accepts JSON requests, verifies secret, saves attachments, calls `llm_generator`, pushes repo, notifies evaluation API. Handles round 1 & 2. |
| `config.py`           | Loads `.env`, contains `STUDENT_SECRET`, `GITHUB_USERNAME`, `GITHUB_TOKEN`, `BASE_REPO_DIR`, etc.                                                            |
| `requirements.txt`    | List of Python dependencies (`fastapi`, `uvicorn`, `openai`, `requests`, etc.)                                                                               |
| `.env`                | Local secrets. Never commit real secrets.                                                                                                                    |
| `github_utils.py`     | Functions to create/update GitHub repo, enable Pages, return commit SHA and Pages URL.                                                                       |
| `attachment_utils.py` | Save attachments from `data:` URIs to disk for LLM or repo generation.                                                                                       |
| `llm_client.py`       | Wrapper around OpenAI API, sets API key, handles structured outputs, response validation.                                                                    |
| `llm_generator.py`    | Generates project files (HTML, JS, CSS) based on `brief` + attachments using `llm_client`.                                                                   |
| `utils.py`            | Optional: helper functions for JSON validation, parsing, logging.                                                                                            |
| `repos/`              | Local temporary repo folders. Each task/round gets a folder like `taskid_nonce_app`.                                                                         |
| `README.md`           | Explains project setup, usage, examples, and course-specific info.                                                                                           |
| `tests/`              | Optional unit tests for your API endpoints (useful for debugging and grading).                                                                               |
