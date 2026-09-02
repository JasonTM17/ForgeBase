import 'dart:io';

import 'log_severity.dart';

/// Fail-fast configuration: missing required required variables or values
/// that fail validation abort startup before any real work happens, so
/// misconfiguration is never discovered in production traffic.
class EnvConfig {
  final String serviceName;
  final LogSeverity logLevel;

  const EnvConfig({required this.serviceName, required this.logLevel});

  factory EnvConfig.fromEnvironment([Map<String, String>? environment]) {
    environment ??= Platform.environment;
    final serviceName = _required(environment, 'SERVICE_NAME');
    final levelName = _optional(environment, 'APP_LOG_LEVEL', 'information');
    final parsed = LogSeverity.parse(levelName);
    if (parsed == null) {
      throw EnvConfigError(
        "APP_LOG_LEVEL '$levelName' is invalid. Valid values: "
        '${LogSeverity.values.map((l) => l.name).join(', ')}.',
      );
    }
    return EnvConfig(serviceName: serviceName, logLevel: parsed);
  }

  static String _required(Map<String, String> environment, String name) {
    final value = environment[name];
    if (value == null || value.trim().isEmpty) {
      throw EnvConfigError(
        'required environment variable $name is missing or empty',
      );
    }
    return value;
  }

  static String _optional(
    Map<String, String> environment,
    String name,
    String fallback,
  ) {
    final value = environment[name];
    return (value == null || value.trim().isEmpty) ? fallback : value;
  }
}

/// Raised only for configuration problems, so hosts can catch it and exit
/// with a clean message instead of a stack trace.
class EnvConfigError implements Exception {
  final String message;
  EnvConfigError(this.message);

  @override
  String toString() => message;
}
