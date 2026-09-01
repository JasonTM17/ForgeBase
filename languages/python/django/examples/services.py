"""Example service — framework-free, in-memory, unit-testable."""

from __future__ import annotations

from common.exceptions import NotFoundError
from examples.schemas import Example


class ExampleService:
    def __init__(self) -> None:
        self._items: dict[int, Example] = {}
        self._next_id = 1

    def create(self, name: str) -> Example:
        item = Example(id=self._next_id, name=name)
        self._items[item.id] = item
        self._next_id += 1
        return item

    def get(self, item_id: int) -> Example:
        item = self._items.get(item_id)
        if item is None:
            raise NotFoundError(f"Example {item_id} not found")
        return item

    def list(self) -> list[Example]:
        return list(self._items.values())


# One instance per process; wire a real store behind this interface.
service = ExampleService()
