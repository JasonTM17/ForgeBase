import { appName } from "./env";
import { exampleService } from "./examples/service";
import ExamplesList from "./examples/List";

export const metadata = { title: appName, description: "ForgeBase Next.js Starter" };

export default function HomePage() {
  const items = exampleService.list();
  return (
    <main>
      <h1>{appName}</h1>
      <ExamplesList items={items} />
    </main>
  );
}
