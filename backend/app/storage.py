from pathlib import Path
import json
from typing import List, Dict

DATA_DIR = Path("/app/data")
UPLOAD_DIR = DATA_DIR / "uploads"
DOCS_FILE = DATA_DIR / "documents.json"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
if not DOCS_FILE.exists():
    DOCS_FILE.write_text("[]")


def load_documents() -> List[Dict]:
    with DOCS_FILE.open() as f:
        return json.load(f)


def save_documents(docs: List[Dict]) -> None:
    with DOCS_FILE.open("w") as f:
        json.dump(docs, f, indent=2)
