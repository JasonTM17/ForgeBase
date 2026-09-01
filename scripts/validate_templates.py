#!/usr/bin/env python3
"""ForgeBase template validator.

Enforces docs/template-specification.md at the file/metadata level:

  All templates (MUST) ......... README.md, forgebase.json, .gitignore,
                                 entrypoint (non-empty template dir), >=1 test
  Backend (MUST) ............... Dockerfile, .dockerignore, .env.example
  Frontend SPA/SSR (MUST) ...... Dockerfile + env documentation (.env.example
                                 or a framework config file)
  Mobile (react-native, flutter)  Dockerfile exempt
  Metadata (ADR 0002) .......... exact schema, known fields only, semver,
                                 id == "<language>-<framework>", path match,
                                 id uniqueness repo-wide
  Self-containment (MUST) ...... static scan: no symlinks, no absolute/host
                                 paths, no references to repo tooling or other
                                 templates, no traversal out of the template
                                 root, no external-root workspace configs

Usage:
  python scripts/validate_templates.py [--root PATH] [--quiet]
  python scripts/validate_templates.py --selftest

Exit codes: 0 = all templates valid (or selftest passed), 1 = violations found.
Standard library only, so CI can run it anywhere.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

METADATA_FIELDS = {
    "id": str,
    "name": str,
    "language": str,
    "framework": str,
    "category": str,
    "tags": list,
    "version": str,
    "runtimeVersion": str,
    "description": str,
}
CATEGORIES = {"backend", "frontend", "library", "cli", "mobile"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

MOBILE_FRAMEWORKS = {"react-native", "flutter"}
# Frontend config files that satisfy "documented environment variables" when a
# framework has no .env convention (nuxt runtimeConfig, sveltekit $env, next).
FRONTEND_ENV_PROXIES = [
    "nuxt.config.ts", "nuxt.config.js", "next.config.ts", "next.config.mjs",
    "src/app.d.ts", "src/environments/environment.ts",
]
# Extensions scanned for boundary violations. Markdown is exempt: linking to
# repository documentation from a README is explicitly allowed by the spec.
TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".go", ".rs",
    ".java", ".kt", ".kts", ".cs", ".php", ".rb", ".dart", ".c", ".h", ".cpp",
    ".hpp", ".cc", ".json", ".toml", ".yaml", ".yml", ".xml", ".gradle",
    ".mod", ".sum", ".properties", ".html", ".css", ".scss", ".sh", ".cfg",
    ".ini", ".env", ".txt",
}
# Static proxies for "escapes its own directory" (template-specification §1).
BOUNDARY_PATTERNS = [
    (re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)"), "absolute host path"),
    (re.compile(r"\.\./\.\./\.\./"), "traversal beyond template root"),
    (re.compile(r"(?<![\w.])scripts/"), "reference to repo tooling scripts/"),
    (re.compile(r"(?<![\w.])\.github/"), "reference to repo CI .github/"),
    (re.compile(r"languages/[a-z][a-z0-9_-]*/"), "reference to another template"),
]
EXTERNAL_ROOT_WORKSPACES = {"go.work"}


class Violation:
    def __init__(self, template: str, message: str):
        self.template = template
        self.message = message

    def __str__(self) -> str:
        return f"[{self.template}] {self.message}"


def find_templates(root: Path) -> list[Path]:
    """Every languages/<language>/<framework>/ directory that contains files."""
    languages_dir = root / "languages"
    if not languages_dir.is_dir():
        return []
    found = []
    for language in sorted(p for p in languages_dir.iterdir() if p.is_dir()):
        for framework in sorted(p for p in language.iterdir() if p.is_dir()):
            if any(framework.iterdir()):
                found.append(framework)
    return found


def load_metadata(template: Path, violations: list[Violation]) -> dict | None:
    name = f"{template.parent.name}/{template.name}"
    meta_path = template / "forgebase.json"
    if not meta_path.is_file():
        violations.append(Violation(name, "missing forgebase.json"))
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        violations.append(Violation(name, f"unreadable forgebase.json: {exc}"))
        return None
    if not isinstance(meta, dict):
        violations.append(Violation(name, "forgebase.json must be a JSON object"))
        return None

    known = set(METADATA_FIELDS)
    for field in sorted(set(meta) - known):
        violations.append(Violation(name, f"unknown metadata field: {field}"))
    for field, expected in METADATA_FIELDS.items():
        if field not in meta:
            violations.append(Violation(name, f"missing metadata field: {field}"))
        elif not isinstance(meta[field], expected):
            violations.append(
                Violation(name, f"metadata field {field} has wrong type "
                                f"(expected {expected.__name__})")
            )
    if any(v.template == name and "field" in v.message for v in violations):
        return None

    expected_id = f"{meta['language']}-{meta['framework']}"
    if meta["id"] != expected_id:
        violations.append(
            Violation(name, f"id {meta['id']!r} must equal {expected_id!r}")
        )
    if not ID_RE.match(str(meta["id"])):
        violations.append(Violation(name, f"id {meta['id']!r} is not kebab-case"))
    if meta["language"] != template.parent.name or meta["framework"] != template.name:
        violations.append(
            Violation(name, "metadata language/framework do not match directory")
        )
    if meta["category"] not in CATEGORIES:
        violations.append(
            Violation(name, f"category {meta['category']!r} not in {sorted(CATEGORIES)}")
        )
    if not SEMVER_RE.match(str(meta["version"])):
        violations.append(
            Violation(name, f"version {meta['version']!r} is not semver")
        )
    return meta


def require_files(template: Path, meta: dict, violations: list[Violation]) -> None:
    name = f"{template.parent.name}/{template.name}"
    for required in ("README.md", ".gitignore"):
        if not (template / required).is_file():
            violations.append(Violation(name, f"missing required file: {required}"))

    category = meta["category"]
    if category == "backend":
        for required in ("Dockerfile", ".dockerignore", ".env.example"):
            if not (template / required).is_file():
                violations.append(Violation(name, f"backend template missing: {required}"))
    elif category == "frontend":
        if meta["framework"] not in MOBILE_FRAMEWORKS:
            if not (template / "Dockerfile").is_file():
                violations.append(Violation(name, "frontend template missing Dockerfile"))
            has_env_doc = (template / ".env.example").is_file() or any(
                (template / proxy).is_file() for proxy in FRONTEND_ENV_PROXIES
            )
            if not has_env_doc:
                violations.append(
                    Violation(name, "frontend template lacks env documentation "
                                    "(.env.example or framework config)")
                )


def check_self_containment(template: Path, violations: list[Violation]) -> None:
    name = f"{template.parent.name}/{template.name}"
    for path in sorted(template.rglob("*")):
        if path.is_symlink():
            violations.append(Violation(name, f"symlink inside template: {path.relative_to(template)}"))
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(template)
        if path.name in EXTERNAL_ROOT_WORKSPACES:
            violations.append(
                Violation(name, f"workspace config rooted outside template: {rel}")
            )
        if rel.suffix not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, label in BOUNDARY_PATTERNS:
            if pattern.search(content):
                violations.append(
                    Violation(name, f"{label} in {rel.as_posix()}")
                )


def has_test_file(template: Path) -> bool:
    markers = ("test", "spec", "Test")
    for path in template.rglob("*"):
        if path.is_file() and any(m in path.name for m in markers):
            return True
    return False


def validate(root: Path) -> tuple[list[Violation], list[str]]:
    violations: list[Violation] = []
    seen_ids: dict[str, str] = {}
    names: list[str] = []
    templates = find_templates(root)
    if not templates:
        return [Violation("repository", "no templates found under languages/")], names

    for template in templates:
        name = f"{template.parent.name}/{template.name}"
        names.append(name)
        meta = load_metadata(template, violations)
        if meta is None:
            continue
        template_id = str(meta["id"])
        if template_id in seen_ids:
            violations.append(
                Violation(name, f"duplicate id {template_id!r} (also {seen_ids[template_id]})")
            )
        seen_ids[template_id] = name
        require_files(template, meta, violations)
        if not has_test_file(template):
            violations.append(Violation(name, "no test file found (spec §1 MUST)"))
        check_self_containment(template, violations)
    return violations, names


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_template(base: Path, language: str, framework: str, meta: dict,
                  files: dict[str, str], binary_links: list[tuple[str, str]] | None = None) -> bool:
    """Create a fixture template; returns False if link fixtures were skipped
    (symlink creation needs privileges on some Windows setups)."""
    template = base / "languages" / language / framework
    write_file(template / "forgebase.json", json.dumps(meta, indent=2))
    write_file(template / "README.md", f"# {meta['name']}\n")
    write_file(template / ".gitignore", "ignored\n")
    for rel, content in files.items():
        write_file(template / rel, content)
    for link_target, link_name in binary_links or []:
        target = base / link_target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("x", encoding="utf-8")
        try:
            (template / link_name).symlink_to(target)
        except OSError:
            return False
    return True


def valid_meta(language: str, framework: str, category: str) -> dict:
    return {
        "id": f"{language}-{framework}",
        "name": f"{language.title()} {framework.title()} Starter",
        "language": language,
        "framework": framework,
        "category": category,
        "tags": [],
        "version": "1.0.0",
        "runtimeVersion": "stable",
        "description": "Fixture template for validator self-test.",
    }


def build_selftest_fixtures(base: Path) -> bool:
    """Build positive+negative fixture trees; returns whether symlink fixtures
    could be created (False on platforms without symlink privilege)."""
    make_template(base, "python", "good-backend", valid_meta("python", "good-backend", "backend"), {
        "Dockerfile": "FROM scratch\n",
        ".dockerignore": "node_modules\n",
        ".env.example": "APP_ENV=development\n",
        "app.py": "print('hi')\n",
        "test_app.py": "def test_ok():\n    assert True\n",
    })
    make_template(base, "python", "good-library", valid_meta("python", "good-library", "library"), {
        "starter.py": "def run():\n    return 1\n",
        "test_starter.py": "def test_run():\n    assert run() == 1\n",
    })
    make_template(base, "typescript", "good-frontend", valid_meta("typescript", "good-frontend", "frontend"), {
        "Dockerfile": "FROM node AS build\n",
        "next.config.mjs": "export default {}\n",
        "src/App.tsx": "export default function App() { return null }\n",
        "src/test/App.test.tsx": "it('renders', () => {})\n",
    })
    make_template(base, "typescript", "react-native", valid_meta("typescript", "react-native", "frontend"), {
        "App.tsx": "export default function App() { return null }\n",
        "__tests__/App.test.tsx": "it('renders', () => {})\n",
    })

    # Negative fixtures — each must be REJECTED for the stated reason.
    make_template(base, "python", "bad-missing-readme", valid_meta("python", "bad-missing-readme", "library"), {
        "starter.py": "x = 1\n",
        "test_starter.py": "def test_x():\n    assert x == 1\n",
    })
    (base / "languages/python/bad-missing-readme/README.md").unlink()

    bad_meta = valid_meta("python", "bad-unknown-field", "library")
    bad_meta["author"] = "nobody"  # unknown field must be rejected
    make_template(base, "python", "bad-unknown-field", bad_meta, {
        "starter.py": "x = 1\n", "test_starter.py": "def test_x():\n    assert x\n",
    })

    mismatched = valid_meta("python", "bad-id-mismatch", "library")
    mismatched["id"] = "python-other"  # id/path mismatch must be rejected
    make_template(base, "python", "bad-id-mismatch", mismatched, {
        "starter.py": "x = 1\n", "test_starter.py": "def test_x():\n    assert x\n",
    })

    make_template(base, "python", "bad-backend-missing-docker", valid_meta("python", "bad-backend-missing-docker", "backend"), {
        ".env.example": "APP_ENV=development\n",
        "app.py": "print('hi')\n",
        "test_app.py": "def test_ok():\n    assert True\n",
    })

    make_template(base, "python", "bad-boundary", valid_meta("python", "bad-boundary", "library"), {
        "starter.py": "import pathlib\nCONFIG = pathlib.Path('/Users/someone/secret.txt')\n",
        "helper.py": "# see scripts/validate_templates.py\nx = 1\n",
        "test_starter.py": "def test_x():\n    assert x\n",
    })
    symlink_supported = make_template(
        base, "python", "bad-symlink", valid_meta("python", "bad-symlink", "library"), {
            "starter.py": "x = 1\n", "test_starter.py": "def test_x():\n    assert x\n",
        }, binary_links=[("outside.txt", "linked.txt")])

    make_template(base, "go", "bad-no-tests", valid_meta("go", "bad-no-tests", "library"), {
        "main.go": "package main\nfunc main() {}\n",
    })
    return symlink_supported


def selftest() -> int:
    """Build positive+negative fixture trees and assert the validator's verdicts."""
    base = Path(tempfile.mkdtemp(prefix="forgebase-validator-selftest-"))
    try:
        symlink_supported = build_selftest_fixtures(base)
        violations, names = validate(base)
        by_template: dict[str, list[str]] = {}
        for v in violations:
            by_template.setdefault(v.template, []).append(v.message)

        must_pass = ["python/good-backend", "python/good-library",
                     "typescript/good-frontend", "typescript/react-native"]
        must_fail = {
            "python/bad-missing-readme": ["missing required file: README.md"],
            "python/bad-unknown-field": ["unknown metadata field: author"],
            "python/bad-id-mismatch": ["must equal"],
            "python/bad-backend-missing-docker": ["missing: Dockerfile"],
            "python/bad-boundary": ["absolute host path", "reference to repo tooling"],
            "go/bad-no-tests": ["no test file found"],
        }
        skipped: list[str] = []
        if symlink_supported:
            must_fail["python/bad-symlink"] = ["symlink inside template"]
        else:
            skipped.append("python/bad-symlink (symlink privilege unavailable)")
        failures: list[str] = []
        for name in must_pass:
            if name in by_template:
                failures.append(f"expected PASS, got violations: {name}: {by_template[name]}")
        for name, expected_snippets in must_fail.items():
            got = by_template.get(name)
            if not got:
                failures.append(f"expected FAIL, validator passed: {name}")
                continue
            for snippet in expected_snippets:
                if not any(snippet in message for message in got):
                    failures.append(f"{name}: missing expected violation {snippet!r}, got {got}")

        if failures:
            print("SELFTEST FAIL")
            for failure in failures:
                print(f"  - {failure}")
            return 1
        skipped_note = f", skipped: {', '.join(skipped)}" if skipped else ""
        print(f"SELFTEST PASS ({len(names)} fixtures, "
              f"{len(must_pass)} positive, {len(must_fail)} negative{skipped_note})")
        return 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ForgeBase templates")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: script's parent's parent)")
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    parser.add_argument("--selftest", action="store_true",
                        help="run built-in positive/negative fixture test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    violations, names = validate(args.root)
    if not args.quiet:
        print(f"Validating {len(names)} templates under {args.root / 'languages'}")
    for violation in violations:
        print(violation)
    if violations:
        print(f"FAIL: {len(violations)} violation(s) in {len(names)} templates")
        return 1
    if not args.quiet:
        print(f"PASS: {len(names)} templates valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
