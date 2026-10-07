#!/usr/bin/env python3
"""Install this skill once; optional replacement preserves a separate backup."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile


def install(source, root, replace=False):
    source, root = Path(source).resolve(), Path(root).expanduser().resolve()
    destination = root / "video-cover-craft"
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source is missing SKILL.md")
    if source == destination:
        raise ValueError("This source is already installed at the requested location")
    if source in root.parents or source == root:
        raise ValueError("Destination cannot be inside the source skill")
    if destination.is_symlink():
        raise ValueError("Destination is a symlink; choose a different skill root")
    if destination.exists() and not replace:
        raise ValueError("Skill already exists; use --replace to retain a backup and install the new version")
    preferences = destination / "user-preferences.json"
    if destination.exists() and (preferences.exists() or preferences.is_symlink()):
        if preferences.is_symlink() or not preferences.is_file():
            raise ValueError("Existing preferences must be a regular file; resolve it before replacement")
    root.mkdir(parents=True, exist_ok=True)
    backup = None
    # Copy before moving an existing installation so a copy failure leaves it intact.
    staging = Path(tempfile.mkdtemp(prefix=".video-cover-craft-install-", dir=root))
    try:
        ready = staging / "video-cover-craft"
        shutil.copytree(source, ready, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        # Account choices belong to the user, not the release being installed.
        if preferences.is_file():
            staged_preferences = ready / "user-preferences.json"
            if staged_preferences.is_symlink():
                raise ValueError("Source preferences must be a regular file")
            shutil.copy2(preferences, staged_preferences)
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            # Keep backups outside the discovery root to avoid duplicate skills.
            backup_dir = root.parent / "skill-backups" / "video-cover-craft"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup = backup_dir / stamp
            destination.rename(backup)
        try:
            ready.rename(destination)
        except OSError:
            if backup is not None and not destination.exists():
                backup.rename(destination)
            raise
    finally:
        shutil.rmtree(staging)
    return destination, backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["codex"], default="codex")
    parser.add_argument("--destination", type=Path, help="Skill root, e.g. ~/.agents/skills")
    parser.add_argument("--replace", action="store_true", help="Preserve existing skill as a backup before replacement")
    args = parser.parse_args()
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    root = args.destination if args.destination is not None else codex_root / "skills"
    try:
        destination, backup = install(Path(__file__).resolve().parents[1], root, args.replace)
    except (ValueError, OSError) as exc:
        print("Install failed: " + str(exc), file=sys.stderr)
        return 1
    print("Installed: " + str(destination))
    if backup:
        print("Previous version preserved: " + str(backup))
    print("Reload the session to discover the updated skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
