#!/usr/bin/env python3
"""Preview existing covers in a simulated feed; never alter source images."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile


def create_preview(images, out_dir, video_title="", labels=None):
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError("Preview requires Pillow to validate image files") from exc

    images = list(images)
    labels = list(labels or [])
    if not images:
        raise ValueError("Provide at least one image")
    if labels and len(labels) != len(images):
        raise ValueError("Provide exactly one label per image, or omit all labels")
    if not isinstance(video_title, str):
        raise ValueError("Video title must be text")
    out_dir = Path(out_dir).expanduser().resolve()
    if out_dir.exists():
        raise ValueError("Refusing to overwrite existing preview directory: " + str(out_dir))

    template = Path(__file__).resolve().parents[1] / "assets/feed-preview.html"
    page = template.read_text(encoding="utf-8")
    marker = "__COVER_STUDIO_DATA__"
    if page.count(marker) != 1:
        raise ValueError("Preview template must contain one data placeholder")

    records = []
    formats = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp", "GIF": ".gif"}
    for index, raw in enumerate(images, 1):
        source = Path(raw).expanduser().resolve()
        if not source.is_file():
            raise ValueError("Image not found: " + str(source))
        with Image.open(source) as opened:
            if opened.format not in formats or getattr(opened, "n_frames", 1) != 1:
                raise ValueError("Expected a still PNG, JPEG, WebP or GIF: " + str(source))
            extension = formats[opened.format]
            opened.verify()
        with Image.open(source) as opened:
            width, height = opened.size
            if opened.getexif().get(274) in (5, 6, 7, 8):
                width, height = height, width
        label = labels[index - 1] if labels else "方案 " + (chr(64 + index) if index <= 26 else str(index))
        if not isinstance(label, str):
            raise ValueError("Labels must be text")
        records.append({"source": str(source), "file": "preview-assets/cover-{:02d}{}".format(index, extension),
                        "label": label, "size": [width, height],
                        "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})

    data = {"videoTitle": video_title, "images": [
        {"file": row["file"], "label": row["label"], "size": row["size"]} for row in records
    ]}
    # Prevent titles such as </script> from ending the embedded JSON element.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    page = page.replace(marker, payload)

    out_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".cover-feed-", dir=out_dir.parent))
    try:
        (staging / "preview-assets").mkdir()
        for row in records:
            copied = staging / row["file"]
            shutil.copy2(row["source"], copied)
            if hashlib.sha256(copied.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError("Source changed during preview preparation: " + row["source"])
        (staging / "feed-preview.html").write_text(page, encoding="utf-8")
        (staging / "preview-manifest.json").write_text(json.dumps({
            "schema_version": 1, "video_title": video_title,
            "preview_kind": "generic_simulation", "images_unchanged": True,
            "images": records
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if out_dir.exists():
            raise ValueError("Preview directory appeared during preparation: " + str(out_dir))
        staging.rename(out_dir)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", action="append", required=True, help="Existing cover; repeat for candidates")
    parser.add_argument("--label", action="append", help="One label per image, in the same order")
    parser.add_argument("--video-title", default="", help="Video title displayed below covers, separate from image text")
    parser.add_argument("--out-dir", type=Path, required=True, help="New directory for the page and unchanged image copies")
    args = parser.parse_args()
    try:
        records = create_preview(args.image, args.out_dir, args.video_title, args.label)
    except (ValueError, OSError) as exc:
        print("Preview failed: " + str(exc), file=sys.stderr)
        return 1
    print("Prepared {} cover(s): {}".format(len(records), args.out_dir.resolve() / "feed-preview.html"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
