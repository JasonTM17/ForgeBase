# Support

ForgeBase is an open-source starter catalog. This page routes questions and
reports to the right public or private channel.

## Security Vulnerabilities

Do not open a public issue for a suspected vulnerability. Follow
[SECURITY.md](SECURITY.md) and use GitHub's private vulnerability reporting for
this repository.

## Starter Bugs

Open a starter bug report when a template does not install, run, test, build,
or copy out as documented. Include:

- the template id, such as `python-fastapi`;
- whether you ran commands in the repository or in a copied-out project;
- the exact command, result, runtime version, and relevant error output;
- whether the result is `FAIL`, `NOT_RUN`, or `BLOCKED`.

## Documentation Issues

Open a documentation issue when a command, link, explanation, status label, or
evidence boundary is stale or confusing. Point to the owning source of truth
when possible: template README, `forgebase.json`, validator behavior, workflow,
or public docs page.

## Template Requests

Use a template request for new languages, frameworks, or variants. Requests
should explain the common generic use case and the verification route. A
template enters ForgeBase only when it can stay self-contained, idiomatic to
its ecosystem, and honestly verified.

## Usage Questions

Start with [Using a ForgeBase Starter](docs/using-a-starter.md), then the
selected template's own README. Once a template is copied out, the new project
owns its own dependencies, CI, secrets, deployment, and release evidence.

## Support Boundary

Only the latest `main` branch is supported for repository fixes. Template
versions in `forgebase.json` describe the template itself; security and
maintenance fixes land on `main`.
