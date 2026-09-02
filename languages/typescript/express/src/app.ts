/**
 * Application factory — the single place the Express app is assembled.
 * Kept separate from server.ts so tests can build isolated instances.
 */

import cors from "cors";
import express, { type Express } from "express";
import helmet from "helmet";

import { type AppConfig } from "./config.js";
import { errorHandler } from "./middleware/errorHandler.js";
import { examplesRouter } from "./routes/examples.js";
import { healthRouter } from "./routes/health.js";
import { type Logger } from "./logger.js";

export function buildApp(config: AppConfig, logger: Logger): Express {
  const app = express();

  // Secure defaults first; CORS only with an explicit allow-list.
  app.use(helmet());
  if (config.corsOrigins.length > 0) {
    app.use(
      cors({
        origin: config.corsOrigins,
        methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
      }),
    );
  }
  app.use(express.json({ limit: "1mb" }));

  app.use(healthRouter);
  app.use(examplesRouter);

  // 404 fall-through in the error envelope.
  app.use((_req, res) => {
    res.status(404).json({ error: { code: "NOT_FOUND", message: "Route not found" } });
  });

  app.use(errorHandler(logger));
  return app;
}
