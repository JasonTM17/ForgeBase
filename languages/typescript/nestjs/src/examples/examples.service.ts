import { Injectable } from "@nestjs/common";

import { NotFoundError } from "../errors.js";

export interface Example {
  id: number;
  name: string;
}

/**
 * Example service — framework-free, in-memory, unit-testable.
 */
@Injectable()
export class ExamplesService {
  private readonly items = new Map<number, Example>();
  private nextId = 1;

  create(name: string): Example {
    const trimmed = name.trim();
    if (!trimmed) {
      throw new Error("name must not be empty");
    }
    const item: Example = { id: this.nextId, name: trimmed };
    this.items.set(item.id, item);
    this.nextId += 1;
    return item;
  }

  get(id: number): Example {
    const found = this.items.get(id);
    if (!found) {
      throw new NotFoundError(`Example ${id} not found`);
    }
    return found;
  }

  list(): Example[] {
    return [...this.items.values()];
  }

  // Test helper: reset the in-memory store between tests.
  reset(): void {
    this.items.clear();
    this.nextId = 1;
  }
}
