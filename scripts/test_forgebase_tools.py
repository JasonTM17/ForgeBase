#!/usr/bin/env python3
"""Focused tests for ForgeBase repository tooling."""

from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_copy_out
import check_docs_links
import forgebase
import update_verification_matrix


def run_cli(func, argv: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return int(func(argv))


class ForgeBaseToolTests(unittest.TestCase):
    def test_discovers_all_templates(self) -> None:
        templates = forgebase.discover_templates()
        self.assertEqual(38, len(templates))
        self.assertIn("python-fastapi", {template.id for template in templates})

    def test_create_rejects_unknown_template(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            rc = run_cli(forgebase.main, ["create", "missing-template", str(Path(temp) / "out")])
        self.assertEqual(2, rc)

    def test_create_rejects_non_empty_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "out"
            target.mkdir()
            (target / "already.txt").write_text("x", encoding="utf-8")
            rc = run_cli(forgebase.main, ["create", "python-fastapi", str(target)])
        self.assertEqual(3, rc)

    def test_create_copies_a_clean_template(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "fastapi"
            rc = run_cli(forgebase.main, ["create", "python-fastapi", str(target)])
            self.assertEqual(0, rc)
            self.assertTrue((target / "forgebase.json").is_file())
            self.assertTrue((target / "README.md").is_file())
            self.assertTrue((target / ".env.example").is_file())
            self.assertFalse((target / "node_modules").exists())

    def test_create_preserves_tracked_bin_sources_and_excludes_runtime_artifacts(self) -> None:
        source_artifact = forgebase.REPO_ROOT / "languages/ruby/rails/storage/test.sqlite3"
        if not source_artifact.exists():
            self.skipTest("local Rails runtime artifact is absent")
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "rails"
            rc = run_cli(forgebase.main, ["create", "ruby-rails", str(target)])
            self.assertEqual(0, rc)
            self.assertTrue((target / "bin/rails").is_file())
            self.assertFalse((target / "storage/test.sqlite3").exists())

    def test_create_preserves_dart_bin_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dart"
            rc = run_cli(forgebase.main, ["create", "dart-vanilla", str(target)])
            self.assertEqual(0, rc)
            self.assertTrue((target / "bin/starter.dart").is_file())

    def test_fallback_copy_works_without_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            index = forgebase.template_index()
            temp_root = Path(temp)
            dart_target = temp_root / "dart"
            rails_target = temp_root / "rails"
            laravel_target = temp_root / "laravel"
            forgebase.copy_template(index["dart-vanilla"], dart_target, root=temp_root)
            forgebase.copy_template(index["ruby-rails"], rails_target, root=temp_root)
            forgebase.copy_template(index["php-laravel"], laravel_target, root=temp_root)
            self.assertTrue((dart_target / "bin/starter.dart").is_file())
            self.assertTrue((rails_target / "bin/rails").is_file())
            self.assertFalse((rails_target / "storage/test.sqlite3").exists())
            self.assertTrue((laravel_target / "bootstrap/cache/.gitignore").is_file())
            self.assertFalse((laravel_target / "vendor/autoload.php").exists())
            self.assertFalse(any(path.parts[0] == "vendor" for path in laravel_target.rglob("*")))

    def test_copy_out_unknown_template_is_not_run_as_pass(self) -> None:
        rc = run_cli(check_copy_out.main, ["--template", "missing-template", "--quiet"])
        self.assertEqual(2, rc)

    def test_verification_matrix_has_one_row_per_template(self) -> None:
        templates = forgebase.discover_templates()
        content = update_verification_matrix.render(templates)
        rows = [line for line in content.splitlines() if line.startswith("| `")]
        self.assertEqual(len(templates), len(rows))
        self.assertIn("`python-fastapi`", content)
        self.assertIn("NOT_RUN", content)

    def test_cli_list_json_is_machine_readable(self) -> None:
        proc = subprocess.run(
            ["python", "scripts/forgebase.py", "list", "--json"],
            cwd=forgebase.REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn('"id": "python-fastapi"', proc.stdout)


class DocsLinkCheckTests(unittest.TestCase):
    def test_relative_links_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "guide.md").write_text("# Guide\n\n## Some Heading\n\nbody\n", encoding="utf-8")
            (root / "index.md").write_text(
                "[ok](guide.md) [anchor](guide.md#some-heading) [ext](https://example.com)\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_docs_links.check_file(root / "index.md"))

    def test_missing_file_and_anchor_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "guide.md").write_text("# Guide\n\n## Some Heading\n", encoding="utf-8")
            (root / "index.md").write_text(
                "[gone](missing.md) [anchor](guide.md#nope)\n", encoding="utf-8"
            )
            problems = check_docs_links.check_file(root / "index.md")
            self.assertEqual(2, len(problems))
            self.assertTrue(any("missing relative" in p or "broken" in p for p in problems))
            self.assertTrue(any("anchor" in p for p in problems))

    def test_links_inside_code_fences_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.md").write_text(
                "text\n\n```md\n[placeholder](docs/nonexistent.md)\n```\n", encoding="utf-8"
            )
            self.assertEqual([], check_docs_links.check_file(root / "index.md"))

    def test_repository_markdown_passes(self) -> None:
        rc = run_cli(check_docs_links.main, ["--quiet"])
        self.assertEqual(0, rc)


if __name__ == "__main__":
    unittest.main()
