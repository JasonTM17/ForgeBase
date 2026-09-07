#!/usr/bin/env python3
"""Repo-local ForgeBase template CLI.

The first version is intentionally standard-library only: it reads
``forgebase.json`` metadata, lists available templates, and copies one template
to a caller-provided directory without dependency or generated artifacts.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_templates import is_ignored_artifact_path  # noqa: E402

FALLBACK_IGNORED_DIRS = {
    ".angular",
    ".bundle",
    ".cache",
    ".dart_tool",
    ".expo",
    ".gem",
    ".gradle",
    ".idea",
    ".mypy_cache",
    ".next",
    ".nuxt",
    ".output",
    ".phpunit.cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svelte-kit",
    ".turbo",
    ".venv",
    ".vs",
    ".vscode",
    "__pycache__",
    "android",
    "artifacts",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "ios",
    "node_modules",
    "obj",
    "staticfiles",
    "target",
    "tmp",
    "venv",
    "vendor",
    "web-build",
}
FALLBACK_IGNORED_PATTERNS = (
    "*.a",
    "*.aab",
    "*.apk",
    "*.class",
    "*.dart.js",
    "*.exe",
    "*.gem",
    "*.iml",
    "*.jks",
    "*.key",
    "*.keystore",
    "*.log",
    "*.mobileprovision",
    "*.o",
    "*.orig.*",
    "*.out",
    "*.p12",
    "*.p8",
    "*.pem",
    "*.pfx",
    "*.pyc",
    "*.pyo",
    "*.sqlite",
    "*.sqlite3",
    "*.sqlite3-*",
    "*.sqlite-*",
    "*.swp",
    "*.swo",
    "*.test",
    "*.tsbuildinfo",
    "*.user",
    ".env",
    ".env.*",
)


@dataclass(frozen=True)
class Template:
    """Machine-readable ForgeBase template entry."""

    id: str
    name: str
    language: str
    framework: str
    category: str
    tags: list[str]
    version: str
    runtime_version: str
    description: str
    path: Path

    @classmethod
    def from_metadata(cls, path: Path, metadata: dict[str, object]) -> "Template":
        return cls(
            id=str(metadata["id"]),
            name=str(metadata["name"]),
            language=str(metadata["language"]),
            framework=str(metadata["framework"]),
            category=str(metadata["category"]),
            tags=[str(tag) for tag in metadata["tags"]],
            version=str(metadata["version"]),
            runtime_version=str(metadata["runtimeVersion"]),
            description=str(metadata["description"]),
            path=path,
        )

    @property
    def rel_path(self) -> Path:
        return Path("languages") / self.language / self.framework


def discover_templates(root: Path = REPO_ROOT) -> list[Template]:
    """Discover templates from forgebase.json metadata."""
    templates: list[Template] = []
    for metadata_path in sorted((root / "languages").glob("*/*/forgebase.json")):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        templates.append(Template.from_metadata(metadata_path.parent, metadata))
    return templates


def template_index(root: Path = REPO_ROOT) -> dict[str, Template]:
    """Return templates keyed by id, rejecting duplicate ids."""
    index: dict[str, Template] = {}
    for template in discover_templates(root):
        if template.id in index:
            raise ValueError(f"duplicate template id: {template.id}")
        index[template.id] = template
    return index


def git_copyable_files(template: Template, root: Path = REPO_ROOT) -> list[Path] | None:
    """Return Git-known source files for a template, or None outside Git."""
    if not (root / ".git").exists():
        return None
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                template.rel_path.as_posix(),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    files: list[Path] = []
    for raw in proc.stdout.split(b"\0"):
        if raw:
            path = root / raw.decode("utf-8")
            if path.is_file():
                files.append(path)
    return sorted(files)


def fallback_copyable_files(template: Template) -> list[Path]:
    """Best-effort copy list for source archives that do not contain .git."""
    files: list[Path] = []
    for path in sorted(template.path.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(template.path)
        if any(part in FALLBACK_IGNORED_DIRS for part in rel.parts):
            continue
        if is_ignored_artifact_path(rel):
            continue
        if rel.name in {".gitignore", ".keep", ".env.example"}:
            files.append(path)
            continue
        if any(rel.match(pattern) for pattern in FALLBACK_IGNORED_PATTERNS):
            continue
        files.append(path)
    return files


def iter_copyable_files(template: Template, root: Path = REPO_ROOT) -> Iterable[Path]:
    """Yield files that belong in a copied-out template."""
    all_files = git_copyable_files(template, root)
    if all_files is None:
        all_files = fallback_copyable_files(template)
    for path in all_files:
        rel = path.relative_to(template.path)
        if is_ignored_artifact_path(rel):
            continue
        yield path


def copy_template(template: Template, target_dir: Path, root: Path = REPO_ROOT) -> None:
    """Copy a template to target_dir, rejecting non-empty destinations."""
    target_dir = target_dir.expanduser().resolve()
    if target_dir.exists() and any(target_dir.iterdir()):
        raise FileExistsError(f"target directory is not empty: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)
    for src in iter_copyable_files(template, root):
        rel = src.relative_to(template.path)
        dst = target_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def cmd_list(args: argparse.Namespace) -> int:
    templates = discover_templates(args.root)
    if args.json:
        payload = [
            {
                "id": template.id,
                "name": template.name,
                "language": template.language,
                "framework": template.framework,
                "category": template.category,
                "runtimeVersion": template.runtime_version,
                "version": template.version,
                "path": template.rel_path.as_posix(),
            }
            for template in templates
        ]
        print(json.dumps(payload, indent=2))
        return 0

    for template in templates:
        print(
            f"{template.id}\t{template.category}\t"
            f"{template.runtime_version}\t{template.rel_path.as_posix()}"
        )
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    index = template_index(args.root)
    template = index.get(args.template_id)
    if template is None:
        print(f"unknown template id: {args.template_id}", file=sys.stderr)
        return 2
    payload = {
        "id": template.id,
        "name": template.name,
        "language": template.language,
        "framework": template.framework,
        "category": template.category,
        "tags": template.tags,
        "version": template.version,
        "runtimeVersion": template.runtime_version,
        "description": template.description,
        "path": template.rel_path.as_posix(),
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    index = template_index(args.root)
    template = index.get(args.template_id)
    if template is None:
        print(f"unknown template id: {args.template_id}", file=sys.stderr)
        return 2
    try:
        copy_template(template, args.target_dir, args.root)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    print(f"created {template.id} at {args.target_dir.expanduser().resolve()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ForgeBase repo-local template CLI")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list available templates")
    list_parser.add_argument("--json", action="store_true", help="emit JSON")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="show one template")
    show_parser.add_argument("template_id")
    show_parser.set_defaults(func=cmd_show)

    create_parser = subparsers.add_parser("create", help="copy a template")
    create_parser.add_argument("template_id")
    create_parser.add_argument("target_dir", type=Path)
    create_parser.set_defaults(func=cmd_create)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
