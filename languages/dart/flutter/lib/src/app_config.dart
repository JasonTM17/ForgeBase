/// Fail-fast, typed application configuration.
///
/// Flutter has no runtime environment: values arrive as compile-time
/// `--dart-define` constants, so validation happens once at startup before
/// any widget is built.
class AppConfig {
  final String appName;

  const AppConfig({required this.appName});

  /// Reads APP_NAME from compile-time defines when no explicit value is
  /// given, and throws [AppConfigError] when it is missing or empty.
  factory AppConfig.fromDefines([String? appName]) {
    final name = appName ?? const String.fromEnvironment('APP_NAME');
    if (name.isEmpty) {
      throw AppConfigError(
        'Missing required environment variable: APP_NAME. '
        'Set it via --dart-define=APP_NAME=... at build/run time.',
      );
    }
    return AppConfig(appName: name);
  }
}

/// Raised only for configuration problems, so hosts can catch it and show
/// a clean message instead of a stack trace.
class AppConfigError implements Exception {
  final String message;
  AppConfigError(this.message);

  @override
  String toString() => message;
}
