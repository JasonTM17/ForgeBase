import { NestFactory } from "@nestjs/core";
import { Logger } from "@nestjs/common";

import { AppModule } from "./app.module.js";
import { ErrorEnvelopeFilter } from "./filters/error.filter.js";
import { loadConfig } from "./config.js";

/**
 * Bootstraps the NestJS application with graceful shutdown.
 */
async function bootstrap(): Promise<void> {
  const config = loadConfig();
  const app = await NestFactory.create(AppModule, { bufferLogs: false });

  app.useLogger(new Logger(config.appName));
  app.useGlobalFilters(new ErrorEnvelopeFilter());

  if (config.corsOrigins.length > 0) {
    app.enableCors({ origin: config.corsOrigins });
  }

  await app.listen(config.appPort);
}

void bootstrap();
