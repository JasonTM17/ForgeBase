# Using a ForgeBase Starter

Languages: English | [Tiếng Việt](using-a-starter.vi.md)

This guide walks a developer through copying one ForgeBase starter into a new
project. It keeps the repository-level steps in one place; after the copy, the
selected template's own README becomes the source of truth.

## 1. Choose the template

List the available template ids from the repository root:

```bash
python scripts/forgebase.py list
```

Inspect one template before copying it:

```bash
python scripts/forgebase.py show python-fastapi
```

Use the root [README](../README.md) for the human catalog and the
[verification matrix](verification-matrix.md) for evidence notes. Choose by
runtime, framework convention, and category first; do not pick a template only
because it has the newest dependency set.

## 2. Copy it out

Copy into an empty destination directory:

```bash
python scripts/forgebase.py create python-fastapi ../my-api
cd ../my-api
```

The CLI refuses to write into a non-empty destination. That is intentional: a
template copy-out must not overwrite an existing project or mix generated
files with source.

Manual copying is also valid when you want to inspect every file first. Copy
only the selected `languages/<language>/<framework>/` directory — not the
repository tooling, the CI folder, local configs, or unrelated templates.

## 3. Rename the starter

After copying, make the project yours:

- Update the README title and project description.
- Rename packages, modules, namespaces, and Docker image names where the
  ecosystem expects it.
- Replace placeholder package names such as `com.example.starter`.
- Review `.env.example` and create a local `.env` only inside the new project.
- Initialize a new Git remote for the copied project if needed.

Never commit real secrets. Keep `.env`, credentials, local certificates,
device signing files, build outputs, and package caches ignored.

## 4. Verify the copied project

Run the commands from the selected template's README. The exact commands vary
by ecosystem, but the expected categories are:

- dependency install;
- lint and format checks;
- tests;
- build;
- Docker build, for backend, SSR, or SPA templates that include a Dockerfile.

ForgeBase repository CI does not follow the copied project automatically. Once
copied out, the new project owns its own CI, deployment, secrets, and release
evidence.

## 5. Know what is deliberately absent

Phase-1 starters are production-oriented bases, not finished applications.
They do not include real credentials, domain-specific business logic,
authentication policy, database schema, paid-provider wiring, hosted
infrastructure, or a global package installation for the ForgeBase CLI.

Database/ORM variants, Playwright suites, packaged template releases, and
additional production variants are tracked in the [roadmap](roadmap.md).

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| Unknown template id | Run `python scripts/forgebase.py list` and copy the exact id from the first column. |
| Destination is not empty | Choose a new directory, or empty the target yourself after backing up anything important. |
| Missing local toolchain | Use the Docker or CI route documented by the template. Report local checks as `NOT_RUN` rather than as a pass. |
| Mobile native build not observed | React Native and Flutter starters can pass source-level checks without proving a real device build; keep that distinction in project docs and release notes. |

## Related documents

- Root [README](../README.md) — catalog and quick start.
- [Verification matrix](verification-matrix.md) — per-starter evidence.
- [Template specification](template-specification.md) — what every starter contains.
