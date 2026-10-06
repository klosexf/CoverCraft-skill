#!/usr/bin/env python3
"""Export existing generated covers. No generation, cropping, or composition."""

import argparse
import html
import json
import re
import sys
from pathlib import Path


def parse_size(value):
    match = re.fullmatch(r"([1-9][0-9]*)x([1-9][0-9]*)", value)
    if not match:
        raise argparse.ArgumentTypeError("Size must be WIDTHxHEIGHT, e.g. 1920x1080")
    size = tuple(int(part) for part in match.groups())
    if max(size) > 8192 or size[0] * size[1] > 32_000_000:
        raise argparse.ArgumentTypeError("Export size exceeds the 32MP / 8192px limit")
    return size


def export(images, out_dir, size=None):
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise ValueError("Exporter requires Pillow; generation does not depend on it") from exc

    resampling = getattr(Image, "Resampling", Image).LANCZOS
    out_dir = Path(out_dir).expanduser().resolve()
    prepared = []
    reserved = [out_dir / "index.html", out_dir / "export-manifest.json"]
    # Validate every input before writing anything, including ratio and collisions.
    for index, raw in enumerate(images, 1):
        source = Path(raw).expanduser().resolve()
        if not source.is_file():
            raise ValueError("Image not found: " + str(source))
        with Image.open(source) as opened:
            if getattr(opened, "n_frames", 1) != 1:
                raise ValueError("Expected a single still image: " + str(source))
            image = ImageOps.exif_transpose(opened)
            native = image.size
            if size and native[0] * size[1] != native[1] * size[0]:
                raise ValueError(
                    "Aspect ratio mismatch: {} is {}x{}, target {}x{}; "
                    "recompose with the selected image tool before export".format(
                        source.name, *native, *size
                    )
                )
            has_alpha = "A" in image.getbands() or "transparency" in image.info
            image = image.convert("RGBA" if has_alpha else "RGB")
            if size and image.size != size:
                image = image.resize(size, resampling)
            stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", source.stem).strip("-")[:60] or "cover"
            base = "{:02d}-{}".format(index, stem)
            names = {"png": base + ".png", "jpeg": base + ".jpg", "thumbnail": base + "-thumb.png"}
            reserved.extend(out_dir / name for name in names.values())
            prepared.append((source, image, native, names))
    for path in reserved:
        if path.exists() or path.is_symlink():
            raise ValueError("Refusing to overwrite existing output: " + str(path))

    out_dir.mkdir(parents=True, exist_ok=True)
    records, cards = [], []
    for source, image, native, names in prepared:
        image.save(out_dir / names["png"], "PNG")
        if image.mode == "RGBA":
            jpeg = Image.new("RGB", image.size, "white")
            jpeg.paste(image, mask=image.getchannel("A"))
        else:
            jpeg = image
        jpeg.save(out_dir / names["jpeg"], "JPEG", quality=95, subsampling=0)
        thumb_width = min(320, image.width)
        thumb_height = max(1, round(image.height * thumb_width / image.width))
        image.resize((thumb_width, thumb_height), resampling).save(out_dir / names["thumbnail"], "PNG")
        record = {"source": str(source), "native_size": list(native), "export_size": list(image.size),
                  "files": names, "jpeg_alpha_background": "white" if image.mode == "RGBA" else None}
        records.append(record)
        label = html.escape(source.name)
        cards.append(
            '<article><a href="{png}"><img src="{thumb}" alt="{label}"></a>'
            '<p>{label} · {width} × {height}</p><a href="{png}">PNG</a> · '
            '<a href="{jpeg}">JPEG</a></article>'.format(
                label=label, width=image.width, height=image.height,
                png=names["png"], thumb=names["thumbnail"], jpeg=names["jpeg"]
            )
        )
    page = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>封面对比</title><style>body{margin:32px;background:#f4f4f4;'
            'color:#222;font:16px system-ui,sans-serif}main{display:flex;flex-wrap:wrap;'
            'gap:24px;align-items:flex-start}article{padding:16px;background:white;'
            'border-radius:12px;width:320px}img{width:100%;height:auto;display:block}'
            'p{overflow-wrap:anywhere}a{color:#2459a9}</style><body><h1>封面对比</h1>'
            '<p>点击缩略图查看完整封面。</p><main>' + ''.join(cards) + '</main></body></html>')
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    (out_dir / "export-manifest.json").write_text(
        json.dumps({"images": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", action="append", required=True, help="Existing image; repeat for multiple files")
    parser.add_argument("--out-dir", type=Path, required=True, help="Directory for exports")
    parser.add_argument("--size", type=parse_size, help="Optional exact size; must match every input's ratio")
    args = parser.parse_args()
    try:
        result = export(args.image, args.out_dir, args.size)
    except (ValueError, OSError) as exc:
        print("Export failed: " + str(exc), file=sys.stderr)
        return 1
    print("Exported {} image(s) to {}".format(len(result), args.out_dir.resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
