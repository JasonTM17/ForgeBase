import { appName } from "./env";

export default function NotFound() {
  return (
    <main>
      <h1>404 — Not Found</h1>
      <p>The page you requested does not exist on {appName}.</p>
    </main>
  );
}
