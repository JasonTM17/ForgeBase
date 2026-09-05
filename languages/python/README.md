# Python

Production-oriented Python starters. Each folder is a fully self-contained
project — copy it out of ForgeBase and start building.

| Starter  | Category | Description                                        |
| -------- | -------- | -------------------------------------------------- |
| [vanilla](vanilla/) | library | Stdlib-only library/CLI base: env config, JSON logging, pytest + ruff, uv |
| [fastapi](fastapi/) | backend | FastAPI REST API base: validated config, structured logging, centralized errors, health endpoints, Docker |
| [flask](flask/) | backend | Flask application-factory API base: validated config, structured logging, centralized errors, health endpoints, Docker |
| [django](django/) | backend | API-only Django base: environment-driven settings, JSON logging, error middleware, health endpoints, Docker |

Verification: these templates use the `uv` lockfile and are checked with
`ruff` plus their documented test runner; API starters additionally use
`docker build` when Docker is available.
