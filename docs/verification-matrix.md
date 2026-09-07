# ForgeBase Verification Matrix

This matrix is the public evidence index for ForgeBase starter status.
It is generated from each template's `forgebase.json` metadata by
`python scripts/update_verification_matrix.py`; edit metadata or this
generator instead of hand-editing template rows.

Evidence labels use the repository vocabulary:

- `PASS`: the named check ran and passed for the stated scope.
- `FAIL`: the named check ran and found a defect.
- `NOT_RUN`: the check did not run; no pass is implied.
- `BLOCKED`: the check could not complete because a required tool,
  credential, service, or permission was unavailable.

The root README availability table stays intentionally compact. Use this
matrix for evidence details and for the boundary between local checks,
container checks, CI-first checks, and remote GitHub Actions on a pushed
commit.

## Current Matrix

| Template | Language | Framework | Category | Runtime | Evidence | Command category | Local/toolchain note | Remote CI boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `c-vanilla` | c | vanilla | library | `C11` | PASS | validator + language unit/build checks where toolchain is available | Official gcc:14-bookworm container evidence. | Remote CI remains required on the exact pushed head. |
| `cpp-vanilla` | cpp | vanilla | library | `C++20` | PASS | validator + language unit/build checks where toolchain is available | Official gcc:14-bookworm container evidence. | Remote CI remains required on the exact pushed head. |
| `csharp-aspnetcore` | csharp | aspnetcore | backend | `>=8.0` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `csharp-vanilla` | csharp | vanilla | library | `>=8.0` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `dart-flutter` | dart | flutter | frontend | `Flutter stable / Dart >=3.3` | NOT_RUN | validator + lint/format/test/build where toolchain is available | CI-first mobile starter; local native/device gate is NOT_RUN here. | Remote CI remains required on the exact pushed head. |
| `dart-vanilla` | dart | vanilla | library | `>=3.3` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `go-fiber` | go | fiber | backend | `>=1.25` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `go-gin` | go | gin | backend | `>=1.25` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `go-net-http` | go | net-http | backend | `>=1.25` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `go-vanilla` | go | vanilla | library | `>=1.25` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `java-quarkus` | java | quarkus | backend | `21` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `java-spring-boot` | java | spring-boot | backend | `21` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `java-vanilla` | java | vanilla | library | `21` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `kotlin-ktor` | kotlin | ktor | backend | `JDK 21 / Ktor 3` | PASS | validator + unit/API tests + Docker where toolchain is available | Official gradle:8.14-jdk21 container evidence. | Remote CI remains required on the exact pushed head. |
| `kotlin-vanilla` | kotlin | vanilla | library | `JDK 21` | PASS | validator + language unit/build checks where toolchain is available | Official gradle:8.14-jdk21 container evidence. | Remote CI remains required on the exact pushed head. |
| `php-laravel` | php | laravel | backend | `>=8.4.1` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `php-vanilla` | php | vanilla | library | `>=8.3` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `python-django` | python | django | backend | `>=3.12` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `python-fastapi` | python | fastapi | backend | `>=3.12` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `python-flask` | python | flask | backend | `>=3.12` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `python-vanilla` | python | vanilla | library | `>=3.12` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `ruby-rails` | ruby | rails | backend | `Ruby >=3.3 / Rails 8.1` | NOT_RUN | validator + unit/API tests + Docker where toolchain is available | Source-reviewed locally where host Ruby/Rails tooling was unavailable. | Remote CI remains required on the exact pushed head. |
| `ruby-vanilla` | ruby | vanilla | library | `>=3.3` | NOT_RUN | validator + language unit/build checks where toolchain is available | Source-reviewed locally where host Ruby tooling was unavailable. | Remote CI remains required on the exact pushed head. |
| `rust-actix-web` | rust | actix-web | backend | `rust stable / actix-web 4` | NOT_RUN | validator + unit/API tests + Docker where toolchain is available | Source-reviewed locally where host Rust tooling was unavailable. | Remote CI remains required on the exact pushed head. |
| `rust-axum` | rust | axum | backend | `rust stable / axum 0.8` | NOT_RUN | validator + unit/API tests + Docker where toolchain is available | Source-reviewed locally where host Rust tooling was unavailable. | Remote CI remains required on the exact pushed head. |
| `rust-vanilla` | rust | vanilla | library | `stable` | NOT_RUN | validator + language unit/build checks where toolchain is available | Source-reviewed locally where host Rust tooling was unavailable. | Remote CI remains required on the exact pushed head. |
| `typescript-angular` | typescript | angular | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-express` | typescript | express | backend | `>=22` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-fastify` | typescript | fastify | backend | `>=22` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-nestjs` | typescript | nestjs | backend | `>=22` | PASS | validator + unit/API tests + Docker where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-nextjs` | typescript | nextjs | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-node` | typescript | node | library | `>=22` | PASS | validator + language unit/build checks where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-nuxt` | typescript | nuxt | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-react` | typescript | react | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-react-native` | typescript | react-native | frontend | `Expo SDK ~57 / React 19.2` | NOT_RUN | validator + lint/format/test/build where toolchain is available | CI-first mobile starter; native device gate is NOT_RUN here. | Remote CI remains required on the exact pushed head. |
| `typescript-svelte` | typescript | svelte | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-sveltekit` | typescript | sveltekit | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |
| `typescript-vue` | typescript | vue | frontend | `>=22` | PASS | validator + lint/format/test/build where toolchain is available | Local metadata/static gates and affected starter checks were recorded in the hardening pass. | Remote CI remains required on the exact pushed head. |

## Maintenance

- Regenerate after metadata or evidence wording changes:
  `python scripts/update_verification_matrix.py`.
- Check that the committed file matches generated output:
  `python scripts/update_verification_matrix.py --check`.
- A `NOT_RUN` row can move to `PASS` only after the named local,
  container, or remote CI gate has been observed for that exact scope.
