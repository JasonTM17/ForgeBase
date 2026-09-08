#!/usr/bin/env python3
"""Generate the public ForgeBase starter verification matrix."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from forgebase import Template, discover_templates  # noqa: E402

OUTPUT = REPO_ROOT / "docs" / "verification-matrix.md"

LOCAL_TOOLCHAIN_NOTES = {
    "c-vanilla": "Official gcc:14-bookworm container evidence.",
    "cpp-vanilla": "Official gcc:14-bookworm container evidence.",
    "dart-flutter": "CI-first mobile starter; local native/device gate is NOT_RUN here.",
    "kotlin-ktor": "Official gradle:8.14-jdk21 container evidence.",
    "kotlin-vanilla": "Official gradle:8.14-jdk21 container evidence.",
    "ruby-rails": "Official ruby:3.3 container evidence with Rails test and Docker build.",
    "ruby-vanilla": "Source-reviewed locally where host Ruby tooling was unavailable.",
    "rust-actix-web": "Source-reviewed locally where host Rust tooling was unavailable.",
    "rust-axum": "Source-reviewed locally where host Rust tooling was unavailable.",
    "rust-vanilla": "Source-reviewed locally where host Rust tooling was unavailable.",
    "typescript-react-native": "CI-first mobile starter; native device gate is NOT_RUN here.",
}


def evidence_label(template: Template) -> str:
    if template.id in {
        "ruby-vanilla",
        "rust-actix-web",
        "rust-axum",
        "rust-vanilla",
        "dart-flutter",
        "typescript-react-native",
    }:
        return "NOT_RUN"
    return "PASS"


def local_gate_note(template: Template) -> str:
    return LOCAL_TOOLCHAIN_NOTES.get(
        template.id,
        "Local metadata/static gates and affected starter checks were recorded in the hardening pass.",
    )


def command_category(template: Template) -> str:
    if template.category == "backend":
        return "validator + unit/API tests + Docker where toolchain is available"
    if template.category == "frontend":
        return "validator + lint/format/test/build where toolchain is available"
    return "validator + language unit/build checks where toolchain is available"


def row(template: Template) -> str:
    return (
        f"| `{template.id}` | {template.language} | {template.framework} | "
        f"{template.category} | `{template.runtime_version}` | "
        f"{evidence_label(template)} | {command_category(template)} | "
        f"{local_gate_note(template)} | Verify GitHub Actions on the exact pushed head before release; skipped path-filtered workflows are not evidence for untouched templates. |"
    )


def render(templates: list[Template]) -> str:
    lines = [
        "# ForgeBase Verification Matrix",
        "",
        "This matrix is the public evidence index for ForgeBase starter status.",
        "It is generated from each template's `forgebase.json` metadata by",
        "`python scripts/update_verification_matrix.py`; edit metadata or this",
        "generator instead of hand-editing template rows.",
        "",
        "Evidence labels use the repository vocabulary:",
        "",
        "- `PASS`: the named check ran and passed for the stated scope.",
        "- `FAIL`: the named check ran and found a defect.",
        "- `NOT_RUN`: the check did not run; no pass is implied.",
        "- `BLOCKED`: the check could not complete because a required tool,",
        "  credential, service, or permission was unavailable.",
        "",
        "The root README availability table stays intentionally compact. Use this",
        "matrix for template-level evidence details and for the boundary between",
        "local checks, container checks, CI-first checks, and remote GitHub",
        "Actions on a pushed commit. This matrix is not a release ledger; record",
        "exact commit hashes, run ids, and tags in PRs or release notes.",
        "",
        "## Current Matrix",
        "",
        "| Template | Language | Framework | Category | Runtime | Local evidence | Command category | Local/toolchain note | Remote CI boundary |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(row(template) for template in templates)
    lines.extend(
        [
            "",
            "## Maintenance",
            "",
            "- Regenerate after metadata or evidence wording changes:",
            "  `python scripts/update_verification_matrix.py`.",
            "- Check that the committed file matches generated output:",
            "  `python scripts/update_verification_matrix.py --check`.",
            "- A local `NOT_RUN` row can move to `PASS` only after the named",
            "  local or container gate has been observed for that exact scope.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate docs/verification-matrix.md")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--check", action="store_true", help="fail if output is stale")
    args = parser.parse_args(argv)

    output = args.root / "docs" / "verification-matrix.md"
    content = render(discover_templates(args.root))
    if args.check:
        try:
            existing = output.read_bytes().decode("utf-8")
        except FileNotFoundError:
            print(f"missing generated file: {output}", file=sys.stderr)
            return 1
        if existing != content:
            print(f"stale generated file: {output}", file=sys.stderr)
            return 1
        print(f"PASS: {output.relative_to(args.root)} is up to date")
        return 0
    output.write_bytes(content.encode("utf-8"))
    print(f"wrote {output.relative_to(args.root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
