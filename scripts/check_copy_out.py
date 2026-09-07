#!/usr/bin/env python3
"""Verify ForgeBase templates remain self-contained after copying out."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from forgebase import Template, copy_template, template_index  # noqa: E402
from validate_templates import validate  # noqa: E402


def synthetic_target(temp_root: Path, template: Template) -> Path:
    return temp_root / "languages" / template.language / template.framework


def check_template(template: Template, temp_root: Path, root: Path) -> list[str]:
    target = synthetic_target(temp_root, template)
    copy_template(template, target, root)
    violations, _names = validate(temp_root)
    return [str(violation) for violation in violations]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check copied-out ForgeBase templates")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--template", dest="template_id", help="template id to check")
    group.add_argument("--all", action="store_true", help="check every template")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--keep", action="store_true", help="keep the temporary copy")
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    args = parser.parse_args(argv)

    index = template_index(args.root)
    if args.template_id:
        if args.template_id not in index:
            print(f"unknown template id: {args.template_id}", file=sys.stderr)
            return 2
        selected = [index[args.template_id]]
    else:
        selected = list(index.values())

    temp_root = Path(tempfile.mkdtemp(prefix="forgebase-copy-out-"))
    failures: list[str] = []
    try:
        for template in selected:
            candidate_root = temp_root / template.id
            errors = check_template(template, candidate_root, args.root)
            if errors:
                failures.extend(errors)
            elif not args.quiet:
                print(f"PASS {template.id}")
        if failures:
            for failure in failures:
                print(failure)
            print(f"FAIL: {len(failures)} violation(s) across {len(selected)} template(s)")
            return 1
        if not args.quiet:
            print(f"PASS: copied and validated {len(selected)} template(s)")
        return 0
    finally:
        if args.keep:
            print(f"kept copy-out root: {temp_root}")
        else:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
