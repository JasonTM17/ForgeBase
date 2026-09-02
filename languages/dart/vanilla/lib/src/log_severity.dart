/// Severity levels for the built-in console logger, ordered from most to
/// least severe. The declaration order is the severity order.
enum LogSeverity {
  critical,
  error,
  warning,
  information,
  debug,
  trace;

  /// Case-insensitive name parsing; null when unknown.
  static LogSeverity? parse(String value) {
    final lowered = value.trim().toLowerCase();
    for (final level in LogSeverity.values) {
      if (level.name == lowered) return level;
    }
    return null;
  }

  /// Short uppercase tag used in log lines, e.g. "INF".
  String get tag => name.substring(0, 3).toUpperCase();

  /// Errors and worse belong on stderr.
  bool get isError => index <= LogSeverity.error.index;
}
