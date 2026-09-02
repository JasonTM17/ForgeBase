import { Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";

import { ExamplesModule } from "./examples/examples.module.js";
import { HealthModule } from "./health/health.module.js";

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), HealthModule, ExamplesModule],
})
export class AppModule {}
