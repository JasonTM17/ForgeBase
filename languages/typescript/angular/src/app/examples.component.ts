import { Component, inject, signal } from "@angular/core";

import { ExampleService, type ExampleItem } from "./example.service";

@Component({
  selector: "app-examples",
  standalone: true,
  template: `
    <section>
      <h2>Examples</h2>
      <button type="button" (click)="add()">Add</button>
      <ul>
        @for (item of items(); track item.id) {
          <li>{{ item.id }}: {{ item.name }}</li>
        }
      </ul>
    </section>
  `,
})
export class ExamplesComponent {
  private service = inject(ExampleService);
  items = signal<ExampleItem[]>(this.service.list());

  add(): void {
    const name = window.prompt("Name?");
    if (name && name.trim()) {
      this.service.create(name);
      this.items.set(this.service.list());
    }
  }
}
