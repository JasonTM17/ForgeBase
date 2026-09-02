import { bootstrapApplication } from "@angular/platform-browser";

import { AppComponent } from "./app/app.component";

// Fail-fast at boot: missing env must fail the build/start.
import { required } from "./app/config";
export const appName = required("VITE_APP_NAME", "forgebase-angular");

bootstrapApplication(AppComponent).catch((err: unknown) => console.error(err));
