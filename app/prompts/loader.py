from functools import cache
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


@cache
def load_prompt(name: str) -> str:
    file_path = PROMPTS_DIR / f"{name}.txt"

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt introuvable : {name}")

    return file_path.read_text(encoding="utf-8")
