# Dart Starters

Self-contained Dart basecode templates. Copy a starter folder out of this
repository and it runs as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency Dart package: fail-fast env config, leveled logging, example service, `dart test` suite |
| [`flutter`](./flutter/) | mobile | Flutter app layout (CI-first verification) |

## Verification strategy

- `vanilla` is verified in the official `dart:3.9` container
  (`dart test`). No Dart SDK is assumed on the host.
- `flutter` is deliberately CI-first: the Flutter SDK is large and the
  template documents its verification commands honestly; see the starter
  README.

## Copying a starter out

```bash
cp -r languages/dart/vanilla /path/to/my-project
cd /path/to/my-project
# rename the package in pubspec.yaml
dart test
```
