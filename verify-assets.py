"""Check the committed reader assets without requiring the release PDF."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent / "docs"
issue = json.loads((root / "issue.json").read_text())
assert isinstance(issue["pages"], int) and issue["pages"] > 0
for number in range(1, issue["pages"] + 1):
    image = root / "pages" / f"{number:03}.webp"
    data = image.read_bytes()
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP", image
    text = json.loads((root / "pages" / f"{number:03}.json").read_text())
    assert isinstance(text["text"], str), number
for chapter in issue["chapters"]:
    assert 1 <= chapter["page"] <= issue["pages"], chapter
for name in ("index.html", "reader.js", "cover.webp", ".nojekyll"):
    assert (root / name).is_file(), name
print(f"Validated {issue['pages']} page images and text files, chapters, and entry assets")
