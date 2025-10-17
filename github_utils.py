"""
github_utils.py — Handles GitHub repo creation, update, and GitHub Pages deployment.
Used by app.py for both Round 1 and Round 2 operations.
"""

import requests
import subprocess
import shutil
import time
from pathlib import Path
from config import GITHUB_USERNAME, GITHUB_TOKEN


# ------------------------
# Utility: Shell runner
# ------------------------
def run(cmd, cwd=None, check=True):
    """Run a shell command and show output."""
    print(f"🧩 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result


# ------------------------
# Round 1: Create new repo
# ------------------------
def create_repo_round1(repo_name: str, local_path: Path):
    """
    Round 1 — Create a new GitHub repo, push local files, and enable Pages.
    Returns: (repo_name, latest_commit_sha, pages_url)
    """
    print(f"🚀 Round 1: Creating new GitHub repo `{repo_name}`...")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git"
    pages_url = f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"

    # --- Create GitHub repository ---
    payload = {"name": repo_name, "private": False, "auto_init": False}
    r = requests.post("https://api.github.com/user/repos", json=payload, headers=headers)

    if r.status_code not in (200, 201):
        if "already exists" not in r.text.lower():
            raise Exception(f"❌ GitHub repo creation failed: {r.status_code} {r.text}")
        else:
            print(f"ℹ️ Repo `{repo_name}` already exists, proceeding to push...")

    # --- Initialize Git locally ---
    run(["git", "init"], cwd=local_path)
    run(["git", "branch", "-M", "main"], cwd=local_path)
    run(["git", "config", "user.name", GITHUB_USERNAME], cwd=local_path)
    run(["git", "config", "user.email", "21f3001995@ds.study.iitm.ac.in"], cwd=local_path)
    run(["git", "add", "."], cwd=local_path)
    run(["git", "commit", "-m", "Initial commit"], cwd=local_path)
    run(["git", "remote", "add", "origin", remote_url], cwd=local_path)
    run(["git", "push", "-u", "origin", "main"], cwd=local_path)

    # --- Enable GitHub Pages ---
    pages_api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/pages"
    pages_payload = {"source": {"branch": "main", "path": "/"}}
    r_pages = requests.post(pages_api_url, headers=headers, json=pages_payload)

    if r_pages.status_code not in (201, 204):
        print(f"⚠️ Pages activation warning ({r_pages.status_code}): {r_pages.text}")
    else:
        print("🌍 GitHub Pages activated. Waiting for it to go live...")
        time.sleep(5)
        try:
            resp = requests.get(pages_url)
            if resp.status_code == 200:
                print(f"✅ GitHub Pages live: {pages_url}")
            else:
                print(f"⚠️ Pages URL returned status {resp.status_code}")
        except Exception as e:
            print(f"⚠️ Error checking Pages URL: {e}")

    # --- Get latest commit SHA ---
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=local_path, capture_output=True, text=True)
    commit_sha = result.stdout.strip() if result.returncode == 0 else "N/A"

    print(f"✅ Round 1 completed — Commit: {commit_sha}")
    return repo_name, commit_sha, pages_url


# ------------------------
# Round 2: Update repo
# ------------------------
def update_repo_round2(repo_name: str, local_path: Path):
    """
    Round 2 — Pull latest repo, apply updates, push only if changes exist, verify Pages.
    Returns: (repo_name, latest_commit_sha, pages_url)
    """
    print(f"🔁 Round 2: Updating existing repo `{repo_name}`...")
    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git"
    pages_url = f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"

    tmp_clone = local_path.parent / f"{repo_name}_clone"
    if tmp_clone.exists():
        shutil.rmtree(tmp_clone)

    run(["git", "clone", remote_url, str(tmp_clone)])

    # --- Copy updated files ---
    for item in local_path.iterdir():
        if item.name == ".git":
            continue
        dest = tmp_clone / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # --- Git config ---
    run(["git", "config", "user.name", GITHUB_USERNAME], cwd=tmp_clone)
    run(["git", "config", "user.email", "21f3001995@ds.study.iitm.ac.in"], cwd=tmp_clone)

    # --- Check for changes ---
    status = subprocess.run(["git", "status", "--porcelain"], cwd=tmp_clone, capture_output=True, text=True)
    if status.stdout.strip():
        run(["git", "add", "."], cwd=tmp_clone)
        run(["git", "commit", "-m", "Round 2 update"], cwd=tmp_clone)
        print("✅ Changes detected and committed.")
    else:
        print("ℹ️ No changes detected; skipping commit.")

    # --- Pull + push updates ---
    run(["git", "pull", "--rebase", "origin", "main"], cwd=tmp_clone, check=False)
    run(["git", "push", "origin", "main"], cwd=tmp_clone, check=False)

    # --- Verify GitHub Pages ---
    try:
        resp = requests.get(pages_url)
        if resp.status_code == 200:
            print(f"✅ GitHub Pages live: {pages_url}")
        else:
            print(f"⚠️ Pages URL returned status {resp.status_code}")
    except Exception as e:
        print(f"⚠️ Error checking Pages URL: {e}")

    # --- Get latest commit SHA ---
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_clone, capture_output=True, text=True)
    commit_sha = result.stdout.strip() if result.returncode == 0 else "N/A"

    print(f"✅ Round 2 completed — Commit: {commit_sha}")
    return repo_name, commit_sha, pages_url


# ------------------------
# Wrapper: Auto select round
# ------------------------
def create_or_update_repo(repo_name: str, local_path: Path, round_num: int):
    """
    Wrapper that chooses Round 1 or Round 2 automatically.
    Returns: (repo_name, latest_commit_sha, pages_url)
    """
    if round_num == 1:
        return create_repo_round1(repo_name, local_path)
    else:
        return update_repo_round2(repo_name, local_path)
