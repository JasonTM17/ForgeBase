import { describe, expect, it, vi } from "vitest";

import { Logger } from "../src/logger.js";

describe("Logger", () => {
  it("emits parseable JSON with level and message", () => {
    const write = vi.spyOn(process.stderr, "write").mockImplementation(() => true);
    new Logger("debug").info("hello", { key: "value" });
    const line = write.mock.calls[0]?.[0]?.toString() ?? "";
    const entry = JSON.parse(line) as { level: string; message: string; meta: object };
    expect(entry.level).toBe("info");
    expect(entry.message).toBe("hello");
    expect(entry.meta).toEqual({ key: "value" });
    write.mockRestore();
  });

  it("filters records below the threshold", () => {
    const write = vi.spyOn(process.stderr, "write").mockImplementation(() => true);
    const logger = new Logger("warn");
    logger.debug("quiet");
    logger.info("still quiet");
    expect(write).not.toHaveBeenCalled();
    logger.warn("loud");
    expect(write).toHaveBeenCalledTimes(1);
    write.mockRestore();
  });
});
