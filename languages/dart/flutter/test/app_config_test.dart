import 'package:flutter_test/flutter_test.dart';

import 'package:starter/src/app_config.dart';

void main() {
  test('rejects an empty app name', () {
    expect(() => AppConfig.fromDefines(''), throwsA(isA<AppConfigError>()));
  });

  test('accepts an explicitly provided app name', () {
    final config = AppConfig.fromDefines('demo');

    expect(config.appName, 'demo');
  });
}
