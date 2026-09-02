/**
 * Health endpoints following the ForgeBase health contract.
 */

import { Router } from "express";

export const healthRouter = Router();

healthRouter.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

healthRouter.get("/health/live", (_req, res) => {
  // Liveness: the process is running; no dependency checks by definition.
  res.json({ status: "ok" });
});

healthRouter.get("/health/ready", (_req, res) => {
  // Add dependency probes (database, cache) here as the project grows.
  res.json({ status: "ok" });
});
