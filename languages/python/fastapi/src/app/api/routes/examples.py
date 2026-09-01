"""Example resource routes demonstrating the full request flow."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.envelope import envelope
from app.schemas.example import ExampleCreate
from app.services.example_service import ExampleService, example_service

router = APIRouter(prefix="/api/v1/examples", tags=["examples"])


def get_example_service() -> ExampleService:
    # Dependency injection point: swap the instance in tests or with DI.
    return example_service


ServiceDep = Annotated[ExampleService, Depends(get_example_service)]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_example(payload: ExampleCreate, service: ServiceDep) -> dict:
    created = service.create(payload.name)
    return envelope(created.model_dump(), "created")


@router.get("")
async def list_examples(service: ServiceDep) -> dict:
    return envelope([item.model_dump() for item in service.list()])


@router.get("/{item_id}")
async def get_example(item_id: int, service: ServiceDep) -> dict:
    return envelope(service.get(item_id).model_dump())
