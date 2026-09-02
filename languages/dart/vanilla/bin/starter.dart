import 'dart:io';

import 'package:starter/src/config.dart';
import 'package:starter/src/console_logger.dart';
import 'package:starter/src/greeter.dart';

// Fail-fast demo: a missing or invalid configuration variable exits with a
// clean message and a non-zero code instead of a stack trace.
void main() {
  final config = EnvConfig.fromEnvironment();
  final logger = ConsoleLogger(config.logLevel, config.serviceName);

  logger.info('service starting');
  stdout.writeln(Greeter().greet('ForgeBase'));
  logger.info('service finished');
}
