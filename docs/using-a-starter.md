# Using A ForgeBase Starter

Languages: English | [Tiếng Việt](using-a-starter.vi.md)

This guide is for developers who want to copy one ForgeBase starter into a new
project. It keeps the repository-level steps in one place; after the copy, the
selected template's own README becomes the source of truth.

## 1. Choose The Template

List the available template ids from the repository root:

```bash
python scripts/forgebase.py list
```

Inspect one template before copying it:

```bash
python scripts/forgebase.py show python-fastapi
```

Use the root [README](../README.md) for the human catalog and
[verification matrix](verification-matrix.md) for evidence notes. Choose by
runtime, framework convention, and category first; avoid choosing a template
only because it is the newest dependency set.

## 2. Copy It Out

Copy into an empty destination directory:

```bash
python scripts/forgebase.py create python-fastapi ../my-api
cd ../my-api
```

The CLI refuses to write into a non-empty destination. That is intentional:
template copy-out should not overwrite an existing project or mix generated
files with source.

Manual copying is also valid when a user wants to inspect every file first.
Copy only the selected `languages/<language>/<framework>/` directory, not the
repository tooling, CI folder, private AgentKit files, or unrelated templates.

## 3. Rename The Starter

After copying, make the project yours:

- update the README title and project description;
- rename packages, modules, namespaces, and Docker image names where the
  ecosystem expects it;
- replace placeholder package names such as `com.example.starter`;
- review `.env.example` and create a local `.env` only in the new project;
- initialize a new Git remote for the copied project if needed.

Do not commit real secrets. Keep `.env`, credentials, local certificates,
device signing files, build outputs, and package caches ignored.

## 4. Verify The Copied Project

Run the commands from the selected template README. The exact commands vary by
ecosystem, but the expected categories are:

- dependency install;
- lint and format checks;
- tests;
- build;
- Docker build for backend, SSR, or SPA templates that include a Dockerfile.

ForgeBase repository CI does not follow the copied project automatically. Once
copied out, the new project owns its own CI, deployment, secrets, and release
evidence.

## 5. Know What Is Deliberately Absent

Phase-1 starters are production-oriented bases, not finished applications. They
do not include real credentials, domain-specific business logic, authentication
policy, database schema, paid-provider wiring, hosted infrastructure, or a
global package installation for the ForgeBase CLI.

Database/ORM variants, Playwright suites, packaged template releases, and
additional production variants are tracked in the [roadmap](roadmap.md).

## Troubleshooting

- **Unknown template id**: run `python scripts/forgebase.py list` and copy the
  exact id from the first column.
- **Destination is not empty**: choose a new directory or empty it yourself
  after backing up anything important.
- **Missing local toolchain**: use the Docker or CI route documented by the
  template. Report local checks as `NOT_RUN` rather than pass.
- **Mobile native build not observed**: React Native and Flutter starters can
  run source-level checks without proving a real device build; keep that
  distinction in project docs and release notes.
