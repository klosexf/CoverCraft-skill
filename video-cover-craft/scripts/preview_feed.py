#!/usr/bin/env python3
"""Preview existing covers in a simulated feed; never alter source images."""

import argparse
import hashlib
import re
import json
from pathlib import Path
import shutil
import sys
import tempfile


def create_preview(images, out_dir, video_title="", labels=None, feedback=None, current_image=None, previous_image=None):
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

    feedback_data = None
    if feedback is not None:
        feedback_path = Path(feedback).expanduser().resolve()
        if feedback_path.stat().st_size > 5 * 1024 * 1024:
            raise ValueError("Feedback exceeds 5 MB")
        try:
            feedback_data = json.loads(feedback_path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc:
            raise ValueError("Invalid feedback JSON") from exc
        if (not isinstance(feedback_data, dict)
                or feedback_data.get("schema_version") != 1
                or feedback_data.get("kind") != "covercraft-feedback"
                or not isinstance(feedback_data.get("images"), list)
                or len(feedback_data["images"]) > 100):
            raise ValueError("Expected a covercraft-feedback v1 file")
        seen = set()
        for entry in feedback_data["images"]:
            if not isinstance(entry, dict):
                raise ValueError("Invalid feedback image")
            digest = entry.get("image_sha256", "")
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest) or digest in seen:
                raise ValueError("Invalid or duplicate feedback image hash")
            seen.add(digest)
            if not isinstance(entry.get("notes"), list) or len(entry["notes"]) > 500:
                raise ValueError("Invalid feedback notes")

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

    def requested_image_hash(raw, option):
        if raw is None:
            return None
        source = str(Path(raw).expanduser().resolve())
        match = next((row for row in records if row["source"] == source), None)
        if match is None:
            raise ValueError(option + " must refer to one of the --image inputs")
        return match["sha256"]

    current_hash = requested_image_hash(current_image, "--current-image")
    previous_hash = requested_image_hash(previous_image, "--previous-image")
    if previous_hash and not current_hash:
        raise ValueError("--previous-image requires --current-image")
    if current_hash and previous_hash == current_hash:
        raise ValueError("Current and previous versions must be different images")
    if current_hash and not previous_hash:
        previous_hash = next((row["sha256"] for row in records if row["sha256"] != current_hash), None)

    data = {"schemaVersion": 3, "previewMode": "revision" if current_hash else "candidates",
            "currentImageSha256": current_hash, "previousImageSha256": previous_hash,
            "videoTitle": video_title, "images": [
        {"file": row["file"], "label": row["label"], "size": row["size"], "sha256": row["sha256"]} for row in records
    ], "feedback": feedback_data}
    # Prevent titles such as </script> from ending the embedded JSON element.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    page = page.replace(marker, payload)

    out_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".cover-feed-", dir=out_dir.parent))
    try:
        (staging / "preview-assets").mkdir()
        for asset_name in ("feed-review.css", "feed-review.js"):
            shutil.copy2(template.parent / asset_name, staging / "preview-assets" / asset_name)
        for row in records:
            copied = staging / row["file"]
            shutil.copy2(row["source"], copied)
            if hashlib.sha256(copied.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError("Source changed during preview preparation: " + row["source"])
        (staging / "feed-preview.html").write_text(page, encoding="utf-8")
        (staging / "preview-manifest.json").write_text(json.dumps({
            "schema_version": 3, "video_title": video_title,
            "preview_mode": data["previewMode"], "current_image_sha256": current_hash, "previous_image_sha256": previous_hash,
            "preview_kind": "generic_simulation", "images_unchanged": True,
            "features": ["feed", "visual_diagnostics", "region_annotations", "feedback_export", "version_compare"],
            "feedback_included": feedback_data is not None, "images": records
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
    parser.add_argument("--feedback", type=Path, help="Optional cover-feedback.json from an earlier review; matches exact image hashes")
    parser.add_argument("--current-image", type=Path, help="Explicit current revision, also supplied with --image; opens annotation on this version")
    parser.add_argument("--previous-image", type=Path, help="Previous revision for comparison, also supplied with --image; requires --current-image")
    args = parser.parse_args()
    try:
        records = create_preview(args.image, args.out_dir, args.video_title, args.label, args.feedback, args.current_image, args.previous_image)
    except (ValueError, OSError) as exc:
        print("Preview failed: " + str(exc), file=sys.stderr)
        return 1
    print("Prepared {} cover(s): {}".format(len(records), args.out_dir.resolve() / "feed-preview.html"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
