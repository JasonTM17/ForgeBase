import ExamplesList from "./List";
import { exampleService } from "./service";

export default function ExamplesPage() {
  const items = exampleService.list();
  return (
    <main>
      <h1>Examples</h1>
      <ExamplesList items={items} />
      {items.length === 0 && (
        <p>No examples yet. (This is an SSR starter — wire a form to your API.)</p>
      )}
    </main>
  );
}
