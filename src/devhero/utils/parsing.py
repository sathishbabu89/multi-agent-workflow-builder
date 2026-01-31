
import json
import re
from pathlib import Path
from typing import List, Dict, Any

from .text import normalize_text

def parse_json_response(raw_text: str):
    """
    Extract JSON from LLM output (handles fenced blocks and minor formatting noise).
    Returns Python list[dict] or a fallback message as list.
    """
    if not raw_text:
        return []

    text = raw_text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    try:
        import ast
        return ast.literal_eval(text)
    except Exception:
        return [{"agent": "Manager", "task": "Could not parse JSON", "tools": [], "plan": text}]

def enforce_plan_structure(plan):
    """
    Normalize plan to a list of dicts with keys: agent, task, tools, plan.
    """
    if not isinstance(plan, list):
        plan = [plan]

    normalized = []
    for item in plan:
        if not isinstance(item, dict):
            item = {"agent": "Manager", "task": "Invalid item", "tools": [], "plan": str(item)}

        agent = item.get("agent") or item.get("agent_role") or item.get("role") or "—"
        task = item.get("task") or item.get("task_description") or "—"
        tools = item.get("tools") or item.get("tools_frameworks") or []
        plan_notes = item.get("plan") or item.get("implementation_plan") or "—"

        if isinstance(tools, str):
            tools = [tools]

        normalized.append({
            "agent": agent,
            "task": task,
            "tools": tools,
            "plan": plan_notes,
        })
    return normalized

def detect_file_type(content: str, agent_name: str) -> str:
    """
    Heuristic file type detection to write non-fenced outputs as best-guess code files.
    """
    text = (normalize_text(content) or "").lower()
    agent = (agent_name or "").lower()

    if "import react" in text or "<div" in text or "</div>" in text:
        return ".jsx"
    if "angular" in agent or " from '@angular/" in text:
        return ".ts"
    if "public static void main" in text and "class " in text:
        return ".java"
    if text.strip().startswith("package main") or "func main()" in text:
        return ".go"
    if "using system" in text:
        return ".cs"
    if text.strip().startswith("apiversion:") or text.strip().startswith("kind:"):
        return ".yaml"
    if "create table" in text or "insert into" in text:
        return ".sql"
    if text.strip().startswith("{") and text.strip().endswith("}"):
        return ".json"
    if "def " in text or re.search(r"\bimport\s+\w+", text):
        return ".py"
    if agent.startswith("test"):
        return ".java"
    return ".txt"

def extract_filename_from_content(content: str):
    """
    Extract a file name from a hint in the content, e.g.:
    // File: UserController.java
    # File: app.py
    <!-- File: index.html -->
    /* File: service.go */
    """
    c = normalize_text(content) or ""
    file_pattern = re.compile(r"(?:\/\/|#|<!--|\/\*)\s*File:\s*([\w.\-\\/]+)", re.IGNORECASE)
    match = file_pattern.search(c)
    if match:
        filename = Path(match.group(1)).name.strip()
        return filename
    return None

def code_blocks_from_text(output_text: str):
    """
    Return list of (lang, code) extracted from fenced code blocks.
    Accepts ```lang <code> ``` and ``` <code> ```.
    """
    text = normalize_text(output_text)
    return re.findall(r"```(\w+)?\s*(.*?)```", text, re.DOTALL)
