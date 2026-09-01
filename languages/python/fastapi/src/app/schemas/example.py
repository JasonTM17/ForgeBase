"""Schemas for the example resource."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ExampleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["first example"])


class Example(BaseModel):
    id: int
    name: str
