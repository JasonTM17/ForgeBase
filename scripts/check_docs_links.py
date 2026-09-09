#!/usr/bin/env python3
"""Check that relative links in tracked Markdown files resolve.

This makes the release-gate item "tracked Markdown relative links resolve"
executable: it verifies every relative file link inside repository Markdown
and, for pure-ASCII anchors into local Markdown files, that a matching
heading exists (GitHub slug rules).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

INLINE_LINK = re.compile(r"\[[^\]\[]*\]\(\s*<?([^)>\s]+)>?\s*\)")
REFERENCE_LINK = re.compile(r"^[ \t]*\[[^\]\[]+\]:[ \t]+(\S+)[ \t]*$", re.MULTILINE)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def strip_code_fences(text: str) -> str:
    """Drop fenced code blocks so examples do not register as links."""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0] * 3
                continue
            kept.append(line)
        else:
            if match and match.group(1)[0] * 3 == fence:
                fence = None
    return "\n".join(kept)


def link_targets(text: str) -> list[str]:
    stripped = strip_code_fences(text)
    targets = INLINE_LINK.findall(stripped)
    targets += REFERENCE_LINK.findall(stripped)
    return targets


def github_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug, flags=re.UNICODE)
    return slug.replace(" ", "-")


def heading_slugs(text: str) -> set[str]:
    slugs: set[str] = set()
    for line in strip_code_fences(text).splitlines():
        heading = re.match(r"^ {0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
        if heading:
            base = github_slug(heading.group(1))
            slugs.add(base)
            # GitHub disambiguates duplicate headings with -1, -2, ...
            slugs.update(f"{base}-{i}" for i in range(1, 30))
    return slugs


def check_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path}: unreadable: {exc}"]
    problems: list[str] = []
    for target in link_targets(text):
        if target.startswith(("http://", "https://", "mailto:", "data:", "#")):
            continue
        file_part, _, fragment = target.partition("#")
        if not file_part:
            continue
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            problems.append(f"{path}: broken relative link -> {target}")
            continue
        if fragment and resolved.suffix == ".md" and fragment.isascii():
            try:
                slugs = heading_slugs(resolved.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                continue
            if fragment.lower() not in slugs:
                problems.append(f"{path}: missing anchor -> {target}")
    return problems


def tracked_markdown(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    names = [name for name in result.stdout.decode("utf-8").split("\0") if name]
    return [root / name for name in names]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check relative Markdown links")
    parser.add_argument("paths", nargs="*", type=Path, default=None,
                        help="explicit Markdown files or directories (default: tracked *.md)")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    args = parser.parse_args(argv)

    files: list[Path] = []
    if args.paths:
        for entry in args.paths:
            if entry.is_dir():
                files.extend(sorted(entry.rglob("*.md")))
            else:
                files.append(entry)
    else:
        files = tracked_markdown(args.root)

    problems: list[str] = []
    for file in files:
        problems.extend(check_file(file))

    for problem in problems:
        print(f"BROKEN {problem}", file=sys.stderr)
    if problems:
        print(f"{len(files)} Markdown file(s) checked, {len(problems)} problem(s)", file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"PASS {len(files)} Markdown file(s) checked, 0 broken links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
