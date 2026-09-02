/**
 * Example resource routes demonstrating the full request flow.
 * Routes validate input and translate HTTP; business rules live in services.
 */

import { Router, type NextFunction, type Request, type Response } from "express";
import { z } from "zod";

import { exampleService } from "../services/exampleService.js";

export const examplesRouter = Router();

const createSchema = z.object({
  name: z.string().trim().min(1).max(100),
});

examplesRouter.post("/api/v1/examples", (req: Request, res: Response, next: NextFunction) => {
  const parsed = createSchema.safeParse(req.body);
  if (!parsed.success) {
    // Validation errors flow through the central error handler.
    return next(parsed.error);
  }
  const created = exampleService.create(parsed.data.name);
  res.status(201).json({ data: created, message: "created" });
});

examplesRouter.get("/api/v1/examples", (_req: Request, res: Response) => {
  res.json({ data: exampleService.list(), message: "ok" });
});

examplesRouter.get("/api/v1/examples/:id", (req: Request, res: Response, next: NextFunction) => {
  const id = Number(req.params["id"]);
  if (!Number.isInteger(id)) {
    return next(
      Object.assign(new Error("id must be an integer"), { status: 400, code: "INVALID_ID" }),
    );
  }
  res.json({ data: exampleService.get(id), message: "ok" });
});
