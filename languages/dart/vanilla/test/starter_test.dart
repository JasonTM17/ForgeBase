import 'package:starter/src/config.dart';
import 'package:starter/src/greeter.dart';
import 'package:starter/src/log_severity.dart';
import 'package:test/test.dart';

void main() {
  group('EnvConfig', () {
    test('throws when required variable is missing', () {
      expect(
        () => EnvConfig.fromEnvironment({}),
        throwsA(isA<EnvConfigError>()),
      );
    });

    test('throws when required variable is blank', () {
      expect(
        () => EnvConfig.fromEnvironment({'SERVICE_NAME': '  '}),
        throwsA(isA<EnvConfigError>()),
      );
    });

    test('defaults log level to information', () {
      final config = EnvConfig.fromEnvironment({'SERVICE_NAME': 'demo'});
      expect(config.logLevel, LogSeverity.information);
    });

    test('throws on unknown log level', () {
      expect(
        () => EnvConfig.fromEnvironment(
          {'SERVICE_NAME': 'demo', 'APP_LOG_LEVEL': 'loud'},
        ),
        throwsA(isA<EnvConfigError>()),
      );
    });

    test('parses log level case insensitively', () {
      final config = EnvConfig.fromEnvironment(
        {'SERVICE_NAME': 'demo', 'APP_LOG_LEVEL': 'Warning'},
      );
      expect(config.logLevel, LogSeverity.warning);
    });
  });

  group('LogSeverity', () {
    test('orders by severity not alphabetically', () {
      expect(LogSeverity.error.index, lessThan(LogSeverity.information.index));
      expect(LogSeverity.critical.index, lessThan(LogSeverity.debug.index));
    });

    test('parse returns null for unknown names', () {
      expect(LogSeverity.parse('loud'), isNull);
      expect(LogSeverity.parse(''), isNull);
    });
  });

  group('Greeter', () {
    test('greets by name', () {
      expect(Greeter().greet('ForgeBase'), 'Hello, ForgeBase!');
    });

    test('rejects empty names', () {
      expect(() => Greeter().greet('   '), throwsArgumentError);
    });
  });
}
