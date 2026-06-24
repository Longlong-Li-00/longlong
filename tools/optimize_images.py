from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ALBUMS_DIR = ROOT / "assets" / "albums"
ALBUMS_OPTIMIZED_DIR = ROOT / "assets" / "albums-optimized"
PROJECT_DIR = ROOT / "assets" / "Project"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def save_webp(source: Path, target: Path, max_edge: int, quality: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        width, height = image.size
        scale = min(1.0, max_edge / max(width, height))
        if scale < 1.0:
            image = image.resize((round(width * scale), round(height * scale)), Image.LANCZOS)
        image.save(target, "WEBP", quality=quality, method=6)


def optimize_directory(source_dir: Path, target_dir: Path, max_edge: int, quality: int) -> int:
    count = 0
    if not source_dir.exists():
        return count
    for source in source_dir.iterdir():
        if not source.is_file() or source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        target = target_dir / f"{source.stem}.webp"
        save_webp(source, target, max_edge=max_edge, quality=quality)
        count += 1
    return count


def main() -> None:
    album_count = optimize_directory(ALBUMS_DIR, ALBUMS_OPTIMIZED_DIR, max_edge=1200, quality=82)
    project_count = optimize_directory(PROJECT_DIR, PROJECT_DIR, max_edge=1100, quality=88)
    print(f"Optimized {album_count} gallery images and {project_count} project images.")


if __name__ == "__main__":
    main()
