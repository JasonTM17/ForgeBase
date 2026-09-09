# Contributing to ForgeBase

Thank you for contributing. ForgeBase's value is consistency: every template
feels hand-crafted for its ecosystem yet obeys the same baseline contract. This
guide explains how to change the repository so that contract holds; the full
process lives in [docs/development-workflow.md](docs/development-workflow.md)
([Tiếng Việt](docs/development-workflow.vi.md)).

## Ways to contribute

- **Add a template** — follow
  [docs/adding-a-language.md](docs/adding-a-language.md) or
  [docs/adding-a-framework.md](docs/adding-a-framework.md).
- **Improve an existing template** — bug fixes, better production defaults,
  clearer documentation.
- **Improve repository tooling or CI** — anything under `scripts/` or
  `.github/`.
- **Fix or extend documentation** — small doc fixes are genuinely welcome; for
  documentation-only changes, `python scripts/check_docs_links.py` and a clean
  diff are enough.

## Ground rules

1. **Read the spec first.**
   [docs/template-specification.md](docs/template-specification.md) defines
   what every template MUST/SHOULD/OPTIONAL provide; the validator
   (`python scripts/validate_templates.py`) enforces the file-level rules.
2. **Stay idiomatic.** Follow the ecosystem's own conventions, never a
   one-size-fits-all architecture.
3. **Stay generic.** Templates demonstrate architecture — a health endpoint
   and at most one generic example resource. No product domains.
4. **Keep dependencies minimal.** Every dependency must be justified in the
   template's README. Standard library first.
5. **No secrets, no generated artifacts.** Inspect `git diff --staged` before
   committing.
6. **No placeholder code.** Unimplemented features belong in the roadmap as
   `Planned`, not as fake implementations.
7. **Verify honestly.** Claim only what you actually ran; use the evidence
   labels `PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` with their exact meanings.

## Development process

1. Branch from `main` using `feature/*`, `fix/*`, `docs/*`, `refactor/*`, or
   `chore/*`.
2. Make focused, atomic changes following
   [docs/conventions.md](docs/conventions.md) (Conventional Commits, one
   logical change per commit).
3. Verify the affected template(s): install dependencies; run lint and format
   checks; run tests; run build; run `docker build` if the template has a
   Dockerfile; and run `python scripts/validate_templates.py` for template
   changes.
4. Update the template's README, `.env.example` (or equivalent), and
   `forgebase.json` — including its `version` — together with the code.
5. Open a pull request. The PR template asks for the same scope, verification,
   and evidence-boundary information maintainers use during review.

## Verification discipline

- State exactly what changed and which template(s), workflow(s), or docs are
  affected.
- Use `PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` honestly; a local pass does not
  prove CI, device behavior, or a published release.
- Do not claim release readiness from local checks alone.
- Keep local workspace files, editor configurations, and caches out of
  commits, and stage explicit public paths only.

Maintainer-specific operations — Dependabot triage, branch hygiene, branch
protection, and release evidence — live in
[docs/maintainer-guide.md](docs/maintainer-guide.md)
([Tiếng Việt](docs/maintainer-guide.vi.md)).

## Commit messages

Conventional Commits with a template, language, or repo scope:
`feat(fastapi): ...`, `fix(react): ...`, `docs(repo): ...`. One logical change
per commit; every commit on `main` must build and pass its focused checks.

## Review

Maintainers review for:

- spec compliance (validator plus human review);
- idiomatic structure for the ecosystem;
- security defaults (no secrets, no leaking error handlers, non-root images);
- documentation accuracy (the documented commands actually work);
- CI correctness (path filters, caching, honest gates).

Reviewer findings do not automatically expand scope; they become immediate
work only when they expose an in-scope defect or block acceptance.

## Getting help

Report bugs, request templates, or raise documentation issues through the
repository [issue templates](https://github.com/JasonTM17/ForgeBase/issues/new/choose);
routing is described in [SUPPORT.md](SUPPORT.md). Suspected vulnerabilities
follow [SECURITY.md](SECURITY.md) — never open a public issue for those.
Participants are expected to uphold the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
