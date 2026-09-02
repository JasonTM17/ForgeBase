# Kotlin Starters

Self-contained Kotlin basecode templates. Copy a starter folder out of this
repository and it builds as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Gradle KTS library/CLI base: fail-fast env config, leveled logging, example service, kotlin.test suite |
| [`ktor`](./ktor/) | backend | Ktor 3 + Netty API: health trio, envelope errors, example resource, non-root Docker |

## Verification strategy

- Both starters are verified in the official `gradle:8.14-jdk21` container
  (`gradle test`). No Kotlin/Gradle toolchain is assumed on the host.
- `ktor` additionally verifies a Docker build of its multi-stage, non-root
  image.

## Copying a starter out

```bash
cp -r languages/kotlin/ktor /path/to/my-api
cd /path/to/my-api
# rename the project in settings.gradle.kts and the starter package
./gradlew build
```
