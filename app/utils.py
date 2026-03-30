from bs4 import BeautifulSoup

def clean_html(text: str) -> str:
    if not text:
        return ""
    return BeautifulSoup(text, "html.parser").get_text()

def shorten_text(text: str, max_length: int = 500) -> str:
    if len(text) <= max_length:
        return text

    truncated = text[:max_length]

    # try to truncate after the last sentence
    last_dot = truncated.rfind(".")
    if last_dot != -1:
        return truncated[:last_dot + 1]

    return truncated.rstrip() + "..."