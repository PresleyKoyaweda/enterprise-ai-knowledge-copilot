from pathlib import Path
from functools import lru_cache

PROMPTS_DIR = Path(__file__).parent


@lru_cache(maxsize=None)
def load_prompt(name: str) -> str:
    file_path = PROMPTS_DIR / f"{name}.txt"

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt introuvable : {name}")

    return file_path.read_text(encoding="utf-8")