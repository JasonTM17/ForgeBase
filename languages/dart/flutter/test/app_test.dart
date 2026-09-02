import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:starter/src/app.dart';
import 'package:starter/src/home_screen.dart';

void main() {
  testWidgets('HomeScreen renders the app name', (tester) async {
    await tester.pumpWidget(
      const MediaQuery(
        data: MediaQueryData(),
        child: Directionality(
          textDirection: TextDirection.ltr,
          child: HomeScreen(appName: 'ForgeBase'),
        ),
      ),
    );

    expect(find.text('Hello, ForgeBase!'), findsOneWidget);
  });

  testWidgets('App renders the home screen with the given name', (tester) async {
    await tester.pumpWidget(const _TestApp(appName: 'ForgeBase'));

    expect(find.text('Hello, ForgeBase!'), findsOneWidget);
  });
}

/// Minimal host that supplies the directionality MediaQuery the widgets
/// need without booting the full framework.
class _TestApp extends StatelessWidget {
  final String appName;

  const _TestApp({required this.appName});

  @override
  Widget build(BuildContext context) {
    return MediaQuery(
      data: const MediaQueryData(),
      child: Directionality(
        textDirection: TextDirection.ltr,
        child: App(appName: appName),
      ),
    );
  }
}
