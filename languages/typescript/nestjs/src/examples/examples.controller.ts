import {
  Body,
  Controller,
  Get,
  NotFoundException,
  Param,
  ParseIntPipe,
  Post,
} from "@nestjs/common";
import { z } from "zod";

import { ExamplesService } from "./examples.service.js";

const createSchema = z.object({
  name: z.string().trim().min(1).max(100),
});

@Controller("api/v1/examples")
export class ExamplesController {
  constructor(private readonly examplesService: ExamplesService) {}

  @Post()
  create(@Body() body: unknown) {
    const parsed = createSchema.safeParse(body);
    if (!parsed.success) {
      throw parsed.error; // flows to the global exception filter
    }
    const created = this.examplesService.create(parsed.data.name);
    return { data: created, message: "created" };
  }

  @Get()
  list() {
    return { data: this.examplesService.list(), message: "ok" };
  }

  @Get(":id")
  get(@Param("id", ParseIntPipe) id: number) {
    const item = this.examplesService.get(id);
    if (!item) {
      throw new NotFoundException(`Example ${id} not found`);
    }
    return { data: item, message: "ok" };
  }
}
