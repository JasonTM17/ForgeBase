/**
 * CLI entry point: node dist/cli.js <name>
 */

import { loadConfig, ConfigError } from "./config.js";
import { Logger } from "./logger.js";
import { ExampleService } from "./example.js";

const name = process.argv[2];

if (!name) {
  process.stderr.write("usage: starter <name>\n");
  process.exit(1);
}

try {
  const config = loadConfig();
  const logger = new Logger(config.logLevel);
  logger.info("application started", { appName: config.appName, appEnv: config.appEnv });
  const greeter = new ExampleService();
  process.stdout.write(`Hello, ${name.trim()}!\n`);
} catch (error) {
  // Config problems are fatal and must not print a stack trace to users.
  process.stderr.write(
    `configuration error: ${error instanceof ConfigError ? error.message : "unexpected failure"}\n`,
  );
  process.exit(1);
}
