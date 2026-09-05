# Java Vanilla Starter

Production-oriented **Java 21 library/CLI base**: Maven, fail-fast environment
configuration, small service layer, clean console diagnostics, CLI entry point,
and JUnit 5 tests.

## Features

- Java 21 Maven project with a plain `main` entry point
- Fail-fast `APP_ENV` validation with safe defaults
- Generic `Greeter` service with input validation
- JUnit 5 test suite covering config and service behavior
- No framework runtime dependency; copy the folder out and it stays independent

## Requirements

- Java 21+
- Maven 3.9+

## Project structure

```text
vanilla/
├── src/main/java/com/forgebase/vanilla/
│   ├── AppConfig.java
│   ├── Greeter.java
│   └── Main.java
├── src/test/java/com/forgebase/vanilla/
├── pom.xml
├── .gitignore
└── forgebase.json
```

## Getting started

Copy this folder out and rename the Maven coordinates:

```bash
cp -r languages/java/vanilla /path/to/my-java-app
cd /path/to/my-java-app
mvn test
mvn exec:java -Dexec.args="ForgeBase"
```

## Configuration

| Variable   | Required | Default          | Meaning |
| ---------- | -------- | ---------------- | ------- |
| `APP_NAME` | no       | `forgebase-java` | Application/service name |
| `APP_ENV`  | no       | `development`    | One of `development`, `testing`, `production` |

Invalid `APP_ENV` values throw during config loading.

## Running

```bash
mvn exec:java -Dexec.args="ForgeBase"
mvn package
java -cp target/classes com.forgebase.vanilla.Main ForgeBase
```

## Testing

```bash
mvn test
```

## Linting / formatting

No formatter plugin is pinned in this minimal base. Keep Java formatting
consistent with the existing source and add Spotless or Checkstyle when your
copied-out project needs an enforced style gate.

## Docker

Not shipped for this library/CLI starter. Add a Dockerfile in the copied-out
project when you decide the runtime packaging shape.

## Production notes

- Keep configuration behind `AppConfig` so invalid runtime settings fail before
  business logic runs.
- Replace the sample `Greeter` service with your own domain service while
  keeping the same test structure.
- Do not commit generated `target/` output; it is intentionally gitignored.

## Common issues

- **`usage: Main <name>`** — pass a non-empty argument to the CLI entry point.
- **`APP_ENV must be one of...`** — fix the environment variable or unset it to
  use the safe development default.
