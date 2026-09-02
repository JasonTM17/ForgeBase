# Dart Flutter Starter

A Flutter app layout with typed fail-fast environment configuration, an
app-level error widget, one example screen, and `flutter_test` widget
tests. Per the repository's Phase-1 scope, Flutter's native verification
is **CI-first**: this directory is an idiomatic, self-contained Flutter
project you copy out; the Flutter SDK and a device/emulator are not run
locally here.

## Features

- Fail-fast `String.fromEnvironment('APP_NAME')` that throws before the UI
  builds if the required variable is missing (set via
  `--dart-define=APP_NAME=...`)
- App-level `ErrorWidget.builder` wired to a recoverable fallback widget
  (the idiomatic Flutter error boundary)
- Example screen with generic-domain content only
- `flutter_test` widget tests for the screen and the root `App`

## Requirements

- Flutter stable + Dart >= 3.3
- A device or emulator for runtime checks (managed by CI in Phase 1)

## Project structure

```text
flutter/
├── lib/
│   ├── main.dart                 # bootstrap: config, error widget, runApp
│   └── src/
│       ├── app.dart              # root widget
│       ├── home_screen.dart      # example screen
│       └── error_widget.dart     # app-level error boundary
├── test/app_test.dart            # flutter_test widget tests
└── pubspec.yaml
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/dart/flutter /path/to/my-app
cd /path/to/my-app
# rename the package in pubspec.yaml
flutter pub get
flutter run --dart-define=APP_NAME=my-app
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `APP_NAME` | yes | — | app identity shown on the home screen |

Set it at build/run time via `--dart-define=APP_NAME=...`; a missing value
throws a `StateError` before the UI builds.

## Running

```bash
flutter run --dart-define=APP_NAME=my-app
```

## Testing

```bash
flutter test
```

The repository does not run `flutter test` locally because the Flutter SDK
and a device/emulator are not part of the local verification matrix. The
`test/app_test.dart` file is written against `flutter_test` and is expected
to pass in CI with the Flutter SDK installed.

## Linting / formatting

```bash
flutter analyze
dart format --output=none --set-exit-if-changed .
```

## Docker

Not applicable for mobile starters in Phase 1. Containerized Flutter
builds are a roadmap item.

## Production notes

- The example screen and `App` widget use generic content only; replace
  them with your product when copying out.
- `ErrorWidget.builder` is process-global; if the copied-out project uses
  other packages that set it, coordinate which wins.
- All runtime configuration should flow through `--dart-define` (the
  Flutter convention for compile-time env vars); do not commit secrets.

## Common issues

- **"Missing required environment variable: APP_NAME"** — you ran without
  `--dart-define=APP_NAME=...`; add it.
- **Tests fail on a missing `flutter` SDK** — that is expected locally;
  this starter's verification is CI-first.
