# ForgeBase Maintainer Guide

Languages: English | [Tiếng Việt](maintainer-guide.vi.md)

This guide turns the public AgentKit workflow into day-to-day repository
operations. It is for maintainers handling dependency updates, branch hygiene,
release evidence, and repository settings.

## Operating Principles

- Keep template changes small, idiomatic, and independently reviewable.
- Prefer one dependency-update group per ecosystem, matching
  `.github/dependabot.yml`.
- Record `PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` exactly as observed.
- Keep private local runtime files out of public commits:
  `.agentkit/`, `.agents/`, `.codex/`, `AGENTS.md`, and `plans/`.
- Treat a local pass, a pushed branch, GitHub Actions, and a release tag as
  separate evidence boundaries.

## Dependabot Triage

1. Fetch and inspect every open dependency branch before merging.
2. Read the changed manifests, lockfiles, and workflow files for that group.
3. Check upstream CI failures before assuming the update is bad; stale failures
   can come from earlier repository bugs.
4. Merge grouped updates only when the branch head is known and the affected
   gates have a verification path.
5. If a grouped update exposes a real incompatibility, fix the smallest
   dependency or template boundary that restores the supported runtime.

Useful commands:

```bash
git fetch --all --prune --tags
gh pr list --state open --json number,title,headRefName,headRefOid,baseRefName,mergeStateStatus,statusCheckRollup
git merge-base --is-ancestor origin/<branch> HEAD
```

## Branch Hygiene

Before deleting a remote branch, prove its head is already contained in the
intended base:

```bash
git merge-base --is-ancestor origin/<branch> origin/main
git rev-list --count origin/main..origin/<branch>
```

Only delete branches that return `ahead=0` and have no unmerged work. If the
proof is unavailable, keep the branch and report `NOT_RUN` or `BLOCKED`
instead of guessing.

## Main Branch Protection

`main` should be protected before a release is called complete. Recommended
settings:

- require pull requests for changes to `main`;
- require status checks only when they report reliably for the protected
  branch. With path-filtered workflows, do not require a check that can be
  skipped for unrelated PRs unless a ruleset, merge queue, or fan-in check
  keeps the required status stable;
- disallow force pushes and branch deletion;
- require conversation resolution before merge;
- keep administrator bypass explicit and rare.

When changing repository settings, record the date, the exact setting changed,
and whether the change was verified through GitHub UI or API.

## Release Evidence

Use this release sequence:

1. Verify the intended public diff and staged paths.
2. Run repository gates:
   `python scripts/validate_templates.py --quiet`,
   `python scripts/validate_templates.py --selftest`,
   `python scripts/update_verification_matrix.py --check`, Markdown link
   checks, workflow YAML parsing, secret scan, and `git diff --check`.
3. Run affected ecosystem gates from the template README or workflow.
4. Push the exact commit.
5. Verify GitHub Actions for that exact commit.
6. Tag only after the commit, checks, documentation, and release notes agree.

Do not say "release-ready" when exact-head CI, tag, provenance, or another
required external gate has not been observed.

## Documentation Updates

Update docs when a change affects setup, supported runtime versions, commands,
CI behavior, verification evidence, repository policy, or maintainer workflow.
Do not duplicate long template README content into root docs; link to the
source of truth instead.

For bilingual updates, keep English and Vietnamese docs aligned in meaning even
when the wording is not a literal translation.
