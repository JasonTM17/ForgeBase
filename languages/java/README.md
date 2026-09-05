# Java

Production-oriented Java starters. Each folder is a fully self-contained project.

| Starter | Category | Description |
| ------- | -------- | ----------- |
| [vanilla](vanilla/) | library/cli | Maven + Java 21 library/CLI base: JUnit 5, fail-fast env config, clean console diagnostics |
| [spring-boot](spring-boot/) | backend | Spring Boot 3 REST base: actuator liveness/readiness, RFC 9457 Problem Details, non-root Docker image |
| [quarkus](quarkus/) | backend | Quarkus 3 REST base: MicroProfile health, centralized REST error mapping, fast-jar Docker runtime |

Verification: all starters pass `mvn test`; the spring-boot and quarkus
container builds are verified locally (vanilla is a library/CLI starter and
ships no Dockerfile — CI runs the same gates via `.github/workflows/java.yml`).
