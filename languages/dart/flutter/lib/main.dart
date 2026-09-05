import 'package:flutter/widgets.dart';

import 'src/app.dart';
import 'src/error_widget.dart';

void main() {
  // Fail fast on a missing configuration variable before building the UI.
  final appName = const String.fromEnvironment('APP_NAME');
  if (appName.isEmpty) {
    throw StateError(
      'Missing required environment variable: APP_NAME. '
      'Set it via --dart-define=APP_NAME=... at build/run time.',
    );
  }

  // App-level error boundary: a recoverable fallback instead of the red
  // error screen.
  ErrorWidget.builder =
      (FlutterErrorDetails details) => AppErrorWidget(details: details);

  runApp(App(appName: appName));
}
