
import shutil
import tempfile
import time
from pathlib import Path
import git
import logging

from ..config import get_settings
from ..utils.secure import sanitize_error
from .output_writer import save_agent_outputs_to_repo

log = logging.getLogger(__name__)

def push_outputs_to_github(outputs_list, phase_index: int) -> bool:
    """
    Push structured agent outputs for the given phase to GitHub.
    Uses a temp clone for safety (stateless between runs).
    """
    s = get_settings()
    repo_url = s.github_repo
    token = s.github_token
    branch = s.github_branch

    if not repo_url or not token:
        log.error("GitHub repo or token not configured.")
        return False

    repo_url_with_token = repo_url.replace("https://", f"https://{token}@")

    tmpdir = tempfile.mkdtemp()
    tmp_path = Path(tmpdir)

    try:
        repo = git.Repo.clone_from(repo_url_with_token, tmp_path, branch=branch)

        phase_folder = tmp_path / f"phase_{phase_index+1}"
        phase_folder.mkdir(parents=True, exist_ok=True)

        save_agent_outputs_to_repo(outputs_list, phase_folder)

        repo.git.add(all=True)
        repo.index.commit(f"🤖 DevHero: Added outputs for phase {phase_index+1}")
        repo.remote(name="origin").push(branch)

        time.sleep(0.3)
        return True

    except Exception as e:
        log.exception("Failed to push to GitHub.")
        # Return False; caller can render sanitized toasts/errors
        return False

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
