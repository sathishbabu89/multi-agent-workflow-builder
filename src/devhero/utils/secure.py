
import os

def sanitize_error(msg: str) -> str:
    """
    Mask tokens in error messages before showing to UI.
    """
    token = os.getenv("GITHUB_TOKEN")
    if token:
        msg = msg.replace(token, "****")
    repo_url = os.getenv("GITHUB_REPO", "")
    if repo_url and token:
        msg = msg.replace(repo_url.replace("https://", f"https://{token}@"), repo_url)
    return msg
