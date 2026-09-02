import { defineEventHandler } from "h3";
import { exampleService } from "../service.js";

export default defineEventHandler(() => {
  return { data: exampleService.list(), message: "ok" };
});
