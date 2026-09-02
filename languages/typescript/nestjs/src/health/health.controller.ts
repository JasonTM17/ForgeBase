import { Controller, Get } from "@nestjs/common";

@Controller("health")
export class HealthController {
  @Get()
  check() {
    return { status: "ok" };
  }

  @Get("live")
  liveness() {
    // The process is running; no dependency checks here by definition.
    return { status: "ok" };
  }

  @Get("ready")
  readiness() {
    // Add dependency probes (database, cache) here as the project grows.
    return { status: "ok" };
  }
}
