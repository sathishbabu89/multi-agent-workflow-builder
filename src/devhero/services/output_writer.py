
import io
import re
import zipfile
import tempfile
from pathlib import Path
from typing import List, Dict, Any

from ..utils.parsing import (
    normalize_text, extract_filename_from_content, code_blocks_from_text, detect_file_type
)

def save_agent_outputs_and_zip(outputs: List[Dict[str, Any]], zip_name: str = "agent_outputs.zip") -> bytes:
    """
    Save outputs from multiple agents to temp files (detecting code blocks & file types),
    then return a ZIP as bytes.
    """
    code_ext_map = {
        "python": ".py", "py": ".py",
        "javascript": ".js", "js": ".js",
        "html": ".html",
        "css": ".css",
        "json": ".json",
        "txt": ".txt",
        "java": ".java",
        "ts": ".ts",
        "go": ".go",
        "cs": ".cs",
        "yaml": ".yaml",
        "yml": ".yml",
        "sql": ".sql",
        "": ".txt"
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        for idx, out in enumerate(outputs, start=1):
            agent_name = re.sub(r"\W+", "_", out.get("agent", f"agent_{idx}")).strip("_") or f"agent_{idx}"
            raw_text = normalize_text(out.get("output", ""))

            hinted_name = extract_filename_from_content(raw_text)
            blocks = code_blocks_from_text(raw_text)

            if blocks:
                for part_idx, (lang, code) in enumerate(blocks, start=1):
                    ext = code_ext_map.get((lang or "").lower(), ".txt")
                    filename = hinted_name or f"{agent_name}_part{part_idx}{ext}"
                    (tmp_path / filename).write_text(code.strip(), encoding="utf-8")
            else:
                ext = detect_file_type(raw_text, agent_name)
                filename = hinted_name or f"{agent_name}{ext}"
                (tmp_path / filename).write_text(raw_text, encoding="utf-8")

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in tmp_path.rglob("*"):
                if file.is_file():
                    zf.write(file, arcname=file.name)
        zip_buf.seek(0)
        return zip_buf.getvalue()

def save_agent_outputs_to_repo(outputs_list: List[Dict[str, Any]], base_path: Path) -> None:
    """
    Save agent outputs into a phase folder with best effort file types.
    """
    code_ext_map = {
        "python": ".py", "py": ".py",
        "javascript": ".js", "js": ".js",
        "html": ".html", "css": ".css",
        "json": ".json", "txt": ".txt",
        "java": ".java",
        "ts": ".ts",
        "go": ".go",
        "cs": ".cs",
        "yaml": ".yaml", "yml": ".yml",
        "sql": ".sql",
        "": ".txt"
    }

    for i, item in enumerate(outputs_list):
        agent_name = re.sub(r"\W+", "_", item.get("agent", f"agent_{i+1}")).strip("_") or f"agent_{i+1}"
        agent_folder = base_path / f"{i+1}_{agent_name}"
        agent_folder.mkdir(parents=True, exist_ok=True)

        raw = normalize_text(item.get("output", ""))
        hinted_name = extract_filename_from_content(raw)
        blocks = code_blocks_from_text(raw)

        if blocks:
            for block_idx, (lang, code) in enumerate(blocks, start=1):
                ext = code_ext_map.get((lang or "").lower(), ".txt")
                filename = hinted_name or f"{agent_name}_part{block_idx}{ext}"
                (agent_folder / filename).write_text(code.strip(), encoding="utf-8")
        else:
            ext = detect_file_type(raw, agent_name)
            filename = hinted_name or f"{agent_name}_output{ext}"
            (agent_folder / filename).write_text(raw, encoding="utf-8")
