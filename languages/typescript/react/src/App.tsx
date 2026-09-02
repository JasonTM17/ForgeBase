import { useState } from "react";

import { exampleService, type ExampleItem } from "./services/exampleService.js";
import { ErrorBoundary } from "./ErrorBoundary.js";

function ExampleList(): React.JSX.Element {
  const [items, setItems] = useState<ExampleItem[]>(exampleService.list());

  function add(): void {
    const name = window.prompt("Name?");
    if (name && name.trim()) {
      exampleService.create(name);
      setItems(exampleService.list());
    }
  }

  return (
    <section>
      <h2>Examples</h2>
      <button type="button" onClick={add}>
        Add
      </button>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.id}: {item.name}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function App(): React.JSX.Element {
  return (
    <ErrorBoundary>
      <main>
        <h1>ForgeBase React Starter</h1>
        <ExampleList />
      </main>
    </ErrorBoundary>
  );
}
