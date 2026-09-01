/**
 * Leveled JSON logging on stderr.
 *
 * Zero dependencies: one JSON object per line, level-filtered, ready for any
 * log aggregator. stdout stays reserved for program output.
 */

import type { LogLevel } from "./config.js";

const LEVEL_WEIGHT: Record<LogLevel, number> = { debug: 10, info: 20, warn: 30, error: 40 };

export class Logger {
  #threshold: number;

  constructor(level: LogLevel = "info") {
    this.#threshold = LEVEL_WEIGHT[level];
  }

  #write(level: LogLevel, message: string, meta?: Record<string, unknown>): void {
    if (LEVEL_WEIGHT[level] < this.#threshold) return;
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...(meta ? { meta } : {}),
    };
    process.stderr.write(`${JSON.stringify(entry)}\n`);
  }

  debug(message: string, meta?: Record<string, unknown>): void {
    this.#write("debug", message, meta);
  }

  info(message: string, meta?: Record<string, unknown>): void {
    this.#write("info", message, meta);
  }

  warn(message: string, meta?: Record<string, unknown>): void {
    this.#write("warn", message, meta);
  }

  error(message: string, meta?: Record<string, unknown>): void {
    this.#write("error", message, meta);
  }
}
