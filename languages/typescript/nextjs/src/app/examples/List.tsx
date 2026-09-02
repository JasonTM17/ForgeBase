import type { ExampleItem } from "./service";

export default function ExamplesList({ items }: { items: ExampleItem[] }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          {item.id}: {item.name}
        </li>
      ))}
    </ul>
  );
}
