import 'package:flutter/widgets.dart';

/// Example screen demonstrating the framework's idiomatic structure with
/// generic-domain content only. Replace it when copying the template out.
class HomeScreen extends StatelessWidget {
  final String appName;

  const HomeScreen({super.key, required this.appName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Text(
            'Hello, $appName!',
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w600),
          ),
        ),
      ),
    );
  }
}
