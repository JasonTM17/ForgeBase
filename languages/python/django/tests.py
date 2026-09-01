"""Django system tests: health, example flow, error envelopes, settings.

Run with ``python manage.py test`` — SimpleTestCase keeps these free of any
database requirement, matching the API-only starter design.
"""

import json

from django.core.exceptions import ImproperlyConfigured
from django.test import Client, SimpleTestCase, override_settings

from common.exceptions import NotFoundError
from examples.schemas import ExampleCreate
from examples.services import ExampleService


@override_settings(ALLOWED_HOSTS=["testserver"])
class HealthTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_health_returns_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_liveness_and_readiness_return_ok(self):
        self.assertEqual(self.client.get("/health/live").json(), {"status": "ok"})
        self.assertEqual(self.client.get("/health/ready").json(), {"status": "ok"})


@override_settings(ALLOWED_HOSTS=["testserver"])
class ExampleFlowTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        # Patch the reference the views actually resolve (views module global).
        import examples.views as views

        self._original = views.service
        views.service = ExampleService()
        self.addCleanup(setattr, views, "service", self._original)

    def test_create_returns_envelope(self):
        response = self.client.post(
            "/api/v1/examples",
            data=json.dumps({"name": "first"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"data": {"id": 1, "name": "first"}, "message": "created"}
        )

    def test_list_and_get_flow(self):
        self.client.post(
            "/api/v1/examples", data=json.dumps({"name": "a"}), content_type="application/json"
        )
        self.client.post(
            "/api/v1/examples", data=json.dumps({"name": "b"}), content_type="application/json"
        )
        names = [item["name"] for item in self.client.get("/api/v1/examples").json()["data"]]
        self.assertEqual(names, ["a", "b"])
        self.assertEqual(self.client.get("/api/v1/examples/2").json()["data"]["name"], "b")

    def test_blank_name_is_rejected_with_validation_error(self):
        response = self.client.post(
            "/api/v1/examples", data=json.dumps({"name": ""}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "VALIDATION_ERROR")

    def test_unknown_resource_returns_error_envelope(self):
        response = self.client.get("/api/v1/examples/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "RESOURCE_NOT_FOUND")

    def test_unknown_route_returns_error_envelope(self):
        response = self.client.get("/api/v1/does-not-exist")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "NOT_FOUND")


class SettingsTests(SimpleTestCase):
    def test_invalid_app_env_fails_at_import(self):
        import importlib
        import os
        from unittest.mock import patch

        import config.settings as settings

        with (
            patch.dict(os.environ, {"FORGE_APP_ENV": "staging"}),
            self.assertRaises(ImproperlyConfigured),
        ):
            importlib.reload(settings)
        # Restore the settings module loaded with the real environment.
        importlib.reload(settings)

    def test_service_rejects_unknown_item(self):
        with self.assertRaises(NotFoundError):
            ExampleService().get(1)

    def test_schema_rejects_blank_name(self):
        with self.assertRaises(ValueError):
            ExampleCreate(name="")
