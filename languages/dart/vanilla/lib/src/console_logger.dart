import 'dart:io';

import 'log_severity.dart';

/// Minimal leveled logger: ISO-8601 UTC timestamp, severity tag, and service
/// context on every line. Errors go to stderr so redirection keeps
/// diagnostics out of data pipelines. Replace with a structured logging
/// package when the copied-out project needs richer sinks.
class ConsoleLogger {
  final LogSeverity threshold;
  final String service;

  ConsoleLogger(this.threshold, this.service);

  void info(String message) => _write(LogSeverity.information, message);
  void warning(String message) => _write(LogSeverity.warning, message);
  void error(String message) => _write(LogSeverity.error, message);

  void _write(LogSeverity severity, String message) {
    if (severity.index > threshold.index) return;

    final line = '${DateTime.now().toUtc().toIso8601String()} '
        '[${severity.tag}] service=$service $message';
    if (severity.isError) {
      stderr.writeln(line);
    } else {
      stdout.writeln(line);
    }
  }
}
