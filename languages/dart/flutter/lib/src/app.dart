import 'package:flutter/widgets.dart';

import 'home_screen.dart';

/// Root widget: installs the app-level error widget and renders the home
/// screen. The error widget is wired in `main.dart` via
/// `ErrorWidget.builder`.
class App extends StatelessWidget {
  final String appName;

  const App({super.key, required this.appName});

  @override
  Widget build(BuildContext context) {
    return HomeScreen(appName: appName);
  }
}
