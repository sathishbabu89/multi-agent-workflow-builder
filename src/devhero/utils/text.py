
import html

def normalize_text(s: str) -> str:
    """Unescape any HTML-escaped content from LLM output."""
    return html.unescape(s) if isinstance(s, str) else s

