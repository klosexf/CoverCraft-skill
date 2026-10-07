#!/usr/bin/env python3
"""Optional OpenAI Images API client for hosts without a maintained image CLI."""

import argparse
import base64
from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


def generate(prompt_file, out_dir, images=None, model=None, size=None, quality=None, dry_run=False, client=None):
    from PIL import Image

    model = (model or os.environ.get("OPENAI_IMAGE_MODEL", "")).strip()
    if not model or not (model.startswith("gpt-image-") or model == "chatgpt-image-latest"):
        raise ValueError("Choose a GPT Image model with --model or OPENAI_IMAGE_MODEL")
    size = size or os.environ.get("OPENAI_IMAGE_SIZE") or None
    quality = quality or os.environ.get("OPENAI_IMAGE_QUALITY") or None
    if size and size != "auto" and not re.fullmatch(r"[1-9][0-9]*x[1-9][0-9]*", size):
        raise ValueError("Size must be auto or WIDTHxHEIGHT; verify the selected model's supported sizes")
    if quality and quality not in {"auto", "low", "medium", "high", "xhigh", "max"}:
        raise ValueError("Unsupported quality value; verify options for the selected model")
    prompt_path = Path(prompt_file).expanduser().resolve()
    prompt = prompt_path.read_text(encoding="utf-8")
    if not prompt.strip():
        raise ValueError("Prompt file is empty")
    out_dir = Path(out_dir).expanduser().resolve()
    if out_dir.exists():
        raise ValueError("Refusing to overwrite existing output directory: " + str(out_dir))
    sources = [Path(p).expanduser().resolve() for p in (images or [])]
    if len(sources) > 16:
        raise ValueError("This API helper accepts at most 16 input images")
    for source in sources:
        if not source.is_file():
            raise ValueError("Input image not found: " + str(source))
        if source.stat().st_size >= 50_000_000:
            raise ValueError("Input image must be smaller than 50 MB")
        with Image.open(source) as opened:
            if opened.format not in {"PNG", "JPEG", "WEBP"} or getattr(opened, "n_frames", 1) != 1:
                raise ValueError("Expected a still PNG, JPEG or WebP input: " + str(source))
            opened.verify()
    params = {"model": model, "prompt": prompt, "n": 1, "output_format": "png"}
    if size:
        params["size"] = size
    if quality:
        params["quality"] = quality
    metadata = {"execution_channel": "openai_api", "provider": "openai", "requested_model": model,
                "model_id": None, "operation": "edit" if sources else "generate",
                "input_images": [str(p) for p in sources], "requested_size": size,
                "requested_quality": quality, "api_key_configured": bool(os.environ.get("OPENAI_API_KEY"))}
    if dry_run:
        return {**metadata, "status": "dry_run", "api_called": False}

    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Set OPENAI_API_KEY in your local environment before using the API")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ValueError("Install the dependencies in requirements-openai.txt before using the API") from exc
        client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1", max_retries=0, timeout=300.0)

    out_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".cover-openai-", dir=out_dir.parent))
    try:
        try:
            with ExitStack() as stack:
                if sources:
                    handles = [stack.enter_context(p.open("rb")) for p in sources]
                    result = client.images.edit(image=handles, **params)
                else:
                    result = client.images.generate(**params)
        except Exception as exc:
            status = getattr(exc, "status_code", None)
            raise RuntimeError("OpenAI request failed ({}, HTTP {}). No model switch or automatic retry was made.".format(
                type(exc).__name__, status if isinstance(status, int) else "unknown"
            )) from None
        rows = getattr(result, "data", None)
        if not rows or not getattr(rows[0], "b64_json", None):
            raise ValueError("OpenAI returned no base64 image; no image was saved")
        decoded = base64.b64decode(rows[0].b64_json, validate=True)
        with Image.open(io.BytesIO(decoded)) as opened:
            if opened.format != "PNG":
                raise ValueError("Expected a PNG response")
            native_size = list(opened.size)
            opened.verify()
        metadata.update({"status": "generated", "api_called": True,
                         "model_id": getattr(result, "model", None), "native_size": native_size,
                         "file": "cover.png", "fallback_reason": None})
        (staging / "cover.png").write_bytes(decoded)
        (staging / "prompt.txt").write_text(prompt, encoding="utf-8")
        (staging / "generation.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if out_dir.exists():
            raise ValueError("Output directory appeared while generating; refusing to overwrite it")
        staging.rename(out_dir)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, help="New directory for image and metadata")
    parser.add_argument("--image", action="append", help="Local reference or edit target; repeat in prompt order")
    parser.add_argument("--model", help="Explicit GPT Image model, or set OPENAI_IMAGE_MODEL")
    parser.add_argument("--size", help="Selected model's supported size, or set OPENAI_IMAGE_SIZE")
    parser.add_argument("--quality", help="Selected model's supported quality, or set OPENAI_IMAGE_QUALITY")
    parser.add_argument("--dry-run", action="store_true", help="Validate local inputs; never contact the API")
    args = parser.parse_args()
    try:
        result = generate(args.prompt_file, args.out_dir, args.image, args.model, args.size, args.quality, args.dry_run)
    except (ValueError, OSError, RuntimeError, ImportError) as exc:
        print("Image API: " + str(exc), file=sys.stderr)
        return 1
    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Saved: " + str(args.out_dir.resolve() / "cover.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
