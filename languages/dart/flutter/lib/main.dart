import 'package:flutter/widgets.dart';

import 'src/app.dart';
import 'src/app_config.dart';
import 'src/error_widget.dart';

void main() {
  // Fail fast on a missing configuration variable before building the UI.
  final config = AppConfig.fromDefines();

  // App-level error boundary: a recoverable fallback instead of the red
  // error screen.
  ErrorWidget.builder =
      (FlutterErrorDetails details) => AppErrorWidget(details: details);

  runApp(App(appName: config.appName));
}
