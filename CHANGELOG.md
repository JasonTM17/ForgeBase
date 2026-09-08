# Changelog

All notable ForgeBase repository changes are recorded here. This file is a
human release history, not verification proof. Exact commits, GitHub Actions
runs, tags, and published artifacts remain separate evidence.

## Unreleased

### Added

- Bilingual repository documentation hub pages for users, evaluators,
  contributors, and maintainers.
- Bilingual starter copy-out guidance covering template selection, renaming,
  verification, support boundaries, and troubleshooting.
- Maintainer guidance for Dependabot triage, branch hygiene, branch
  protection, and release evidence.
- GitHub PR and issue templates for evidence-driven contribution intake.
- CODEOWNERS and issue-template contact routing for review ownership and
  private security reports.

### Changed

- Consolidated Dependabot updates across affected ecosystems after focused
  compatibility fixes.
- Clarified verification matrix wording so local evidence, path-filtered CI,
  release tags, and current `main` evidence remain separate claims.
- Updated the Ruby Rails matrix row after observed `ruby:3.3` container Rails
  tests and Docker build.

## v0.1.0 - 2026-09-06

### Added

- Phase 1 starter catalog: 38 starters across 12 languages.
- Per-language GitHub Actions workflows and repository-level validation.
- `scripts/forgebase.py` for repo-local template listing, inspection, and
  copy-out.
- Generated verification matrix from template metadata.
- Public architecture, template specification, roadmap, contribution,
  security, and conduct documentation.
