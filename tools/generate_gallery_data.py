from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ALBUMS_DIR = ROOT / "assets" / "albums"
ALBUMS_OPTIMIZED_DIR = ROOT / "assets" / "albums-optimized"
OUTPUT_PATH = ROOT / "assets" / "gallery-data.json"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DATE_PATTERN = re.compile(r"^(?P<date>\d{8}|\d{4}-\d{2}-\d{2})[_-](?P<title>.+)$")


@dataclass
class GalleryItem:
    filename: str
    title: str
    src: str
    date: str | None
    sort_date: datetime | None


def normalize_title(raw_title: str) -> str:
    title = raw_title.replace("_", " ").replace("-", " ")
    title = re.sub(r"\s+", " ", title).strip()
    return title or "Untitled"


def parse_item(path: Path) -> GalleryItem:
    stem = path.stem
    match = DATE_PATTERN.match(stem)
    sort_date = None
    display_date = None

    if match:
      date_token = match.group("date")
      title_token = match.group("title")
      date_format = "%Y%m%d" if len(date_token) == 8 else "%Y-%m-%d"
      try:
          parsed = datetime.strptime(date_token, date_format)
          sort_date = parsed
          display_date = parsed.strftime("%Y.%m.%d")
      except ValueError:
          title_token = stem
    else:
      title_token = stem

    optimized_name = f"{path.stem}.webp"
    output_name = optimized_name if (ALBUMS_OPTIMIZED_DIR / optimized_name).exists() else path.name
    output_folder = "albums-optimized" if output_name == optimized_name else "albums"
    encoded_name = quote(output_name)
    return GalleryItem(
        filename=path.name,
        title=normalize_title(title_token),
        src=f"assets/{output_folder}/{encoded_name}",
        date=display_date,
        sort_date=sort_date,
    )


def sort_key(item: GalleryItem) -> tuple[int, float, str]:
    if item.sort_date is not None:
        return (0, -item.sort_date.timestamp(), item.filename.lower())
    return (1, 0.0, item.filename.lower())


def main() -> None:
    ALBUMS_DIR.mkdir(parents=True, exist_ok=True)
    items = [
        parse_item(path)
        for path in sorted(ALBUMS_DIR.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    items.sort(key=sort_key)

    payload = [
        {
            "filename": item.filename,
            "title": item.title,
            "src": item.src,
            "date": item.date,
        }
        for item in items
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
