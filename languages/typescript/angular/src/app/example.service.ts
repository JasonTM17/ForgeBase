import { Injectable } from "@angular/core";

export interface ExampleItem {
  id: number;
  name: string;
}

@Injectable({ providedIn: "root" })
export class ExampleService {
  #items = new Map<number, ExampleItem>();
  #nextId = 1;

  create(name: string): ExampleItem {
    const trimmed = name.trim();
    if (!trimmed) {
      throw new Error("name must not be empty");
    }
    const item: ExampleItem = { id: this.#nextId++, name: trimmed };
    this.#items.set(item.id, item);
    return item;
  }

  list(): ExampleItem[] {
    return [...this.#items.values()];
  }
}
