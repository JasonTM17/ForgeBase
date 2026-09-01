# Security Policy

ForgeBase is a collection of starter templates, so its security posture has
two layers: the repository itself, and the templates it ships.

## Supported versions

Only the latest commit on `main` is supported. Template `version`s in
`forgebase.json` are informational; security fixes are made on `main` and
consumers copy templates from there.

## Reporting a vulnerability

- Do **not** open a public issue for a security vulnerability.
- Use GitHub's private vulnerability reporting for this repository
  (Security → Report a vulnerability), or contact the maintainers privately.
- Include: affected template(s) (`<language>-<framework>`), a description,
  reproduction steps, and any known mitigations.

You can expect an initial response within a reasonable time frame; please
allow time for a fix before any public disclosure.

## What we secure in the repository

- **No secrets.** Templates never contain credentials, API keys, JWT secrets,
  or database passwords. `.env.example` files carry empty or obviously-safe
  placeholder values only.
- **Validation gate.** `scripts/validate_templates.py` and the
  `repository-check.yml` CI workflow reject templates violating the
  specification's security requirements.
- **Least privilege in CI.** Workflows declare minimal `permissions` and are
  scoped to their language's paths.

## What the templates guarantee

Every backend template, per
[docs/template-specification.md](docs/template-specification.md):

- environment-variable configuration validated (fail-fast) at startup;
- centralized error handling that never exposes stack traces, database
  errors, internal paths, or implementation details in production responses;
- structured/leveled logging (never leaking secrets into logs);
- input validation at the boundary;
- Docker images that are multi-stage, lightweight, and non-root;
- no debug mode enabled by default in production configuration;
- no unsafe defaults (permissive CORS, disabled protections) — secure
  defaults are the template's starting point.

Known limitations are documented in each template's README under
"Production notes" — read it before going to production.

## Scope

This policy covers this repository and its templates. It does not cover the
projects you create from templates — running a template is the start of *your*
application, and its production security is your responsibility: rotate the
placeholder configuration, add authentication, TLS, rate limiting, and the
operational controls your deployment needs.
