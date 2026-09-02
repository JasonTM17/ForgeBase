import { Component, ErrorHandler, Injectable, NgZone, inject, signal } from "@angular/core";

import { ExamplesComponent } from "./examples.component";

// App-level error handler — component crashes are captured and surfaced
// without blanking the whole app.
@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  #errorMessage = signal<string | null>(null);
  readonly errorMessage = this.#errorMessage.asReadonly();

  constructor(private zone: NgZone) {}

  handleError(error: unknown): void {
    const message = error instanceof Error ? error.message : String(error);
    this.zone.run(() => this.#errorMessage.set(message));
    console.error("[GlobalErrorHandler]", error);
  }
}

@Component({
  selector: "app-root",
  standalone: true,
  imports: [ExamplesComponent],
  providers: [{ provide: ErrorHandler, useClass: GlobalErrorHandler }],
  template: `
    @if (handler.errorMessage(); as msg) {
      <div role="alert">
        <h1>Something went wrong</h1>
        <pre>{{ msg }}</pre>
      </div>
    } @else {
      <main>
        <h1>ForgeBase Angular Starter</h1>
        <app-examples />
      </main>
    }
  `,
})
export class AppComponent {
  handler = inject(ErrorHandler) as GlobalErrorHandler;
}
