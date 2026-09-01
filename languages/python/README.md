# Python

Production-oriented Python starters. Each folder is a fully self-contained
project — copy it out of ForgeBase and start building.

| Starter  | Category | Description                                        |
| -------- | -------- | -------------------------------------------------- |
| [vanilla](vanilla/) | library | Stdlib-only library/CLI base: env config, JSON logging, pytest + ruff, uv |
| [fastapi](fastapi/) | backend | FastAPI REST API base: validated config, structured logging, centralized errors, health endpoints, Docker |

Verification: these templates are verified with the locally-installed Python
toolchain (uv, ruff, pytest) and — for the API starters — `docker build`.
