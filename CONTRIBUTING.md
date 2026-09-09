# Contributing to ForgeBase

Thank you for considering a contribution. ForgeBase's value is consistency:
every template feels hand-crafted for its ecosystem but obeys the same
baseline contract. Read this guide before opening a pull request.

## Ways to contribute

- Add a new template (`docs/adding-a-language.md`,
  `docs/adding-a-framework.md`).
- Improve an existing template (bug fixes, better production defaults,
  clearer docs).
- Improve repository tooling (`scripts/`) or CI.
- Fix documentation.

## Ground rules

1. **Read the spec first.** [docs/template-specification.md](docs/template-specification.md)
   defines what every template MUST/SHOULD/OPTIONAL provide. The validator
   (`python scripts/validate_templates.py`) enforces the file-level rules.
2. **Stay idiomatic.** Follow the ecosystem's conventions, not a
   one-size-fits-all architecture.
3. **Stay generic.** Templates demonstrate architecture (health endpoint,
   at most one generic example resource). No product domains.
4. **Minimal dependencies.** Every dependency must be justified in the
   template's README. Standard library first.
5. **No secrets, no generated artifacts.** Check `git diff --staged` before
   committing.
6. **No placeholder code.** Unimplemented features belong in the roadmap as
   `Planned`, not as fake implementations.
7. **Honest verification only.** Claim in README/PR exactly what you ran.

## Development workflow

1. Fork / branch using `feature/*`, `fix/*`, `docs/*`, `chore/*`, or
   `refactor/*`.
2. Make focused changes; follow [docs/conventions.md](docs/conventions.md)
   for commits (Conventional Commits, atomic).
3. Verify the affected template(s):
   - install dependencies;
   - run lint + format check;
   - run tests;
   - run build;
   - run `docker build` if the template has a Dockerfile;
   - run `python scripts/validate_templates.py` for template changes.
4. Update the template's README, `.env.example`/equivalent, and
   `forgebase.json` (bump its `version`) together with the code.
5. Open a pull request describing what you changed and what you ran.
   The repository PR template asks for the same scope, verification, and
   evidence-boundary information maintainers use during review.

## Development & verification discipline

ForgeBase maintainers follow the structured
[development workflow](docs/development-workflow.md)
([Tiếng Việt](docs/development-workflow.vi.md)) for non-trivial template, CI, and
release work. Contributors and pull requests should follow the same evidence discipline:

- say exactly what changed and which template(s), workflow(s), or docs are
  affected;
- use `PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` honestly;
- do not claim release readiness from local checks alone;
- keep local workspace files, editor configs, and caches out of commits;
- stage explicit public paths only.

Maintainer-specific operations for Dependabot triage, branch hygiene, branch
protection, and release evidence live in
[docs/maintainer-guide.md](docs/maintainer-guide.md)
([Tiếng Việt](docs/maintainer-guide.vi.md)).

## Commit messages

Conventional Commits (`feat(fastapi): ...`, `fix(react): ...`,
`docs(repo): ...`). One logical change per commit; `main` must always build.

## Review checklist (what maintainers look at)

- spec compliance (validator + human review);
- idiomatic structure for the ecosystem;
- security defaults (no secrets, no leaking error handlers, non-root images);
- documentation accuracy (commands actually work);
- CI correctness (path filters, caching, honest gates).

Use the repository issue templates when reporting a starter bug, requesting a
new template, or proposing a documentation update.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
