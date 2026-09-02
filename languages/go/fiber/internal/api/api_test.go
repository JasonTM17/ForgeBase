package api_test

import (
	"encoding/json"
	"io"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gofiber/fiber/v3"

	"forgebase/go-fiber/internal/api"
	"forgebase/go-fiber/internal/examples"
)

func setup() *fiber.App {
	app := fiber.New()
	api.Register(app, examples.New())
	return app
}

func doReq(app *fiber.App, method, path, body string) (int, []byte) {
	req := httptest.NewRequest(method, path, strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, err := app.Test(req)
	if err != nil {
		panic(err)
	}
	data, _ := io.ReadAll(resp.Body)
	return resp.StatusCode, data
}

func TestHealth(t *testing.T) {
	app := setup()
	code, body := doReq(app, fiber.MethodGet, "/health", "")
	if code != fiber.StatusOK {
		t.Fatalf("expected 200, got %d", code)
	}
	var b map[string]string
	_ = json.Unmarshal(body, &b)
	if b["status"] != "ok" {
		t.Errorf("unexpected: %s", string(body))
	}
}

func TestLivenessAndReadiness(t *testing.T) {
	app := setup()
	for _, p := range []string{"/health/live", "/health/ready"} {
		code, _ := doReq(app, fiber.MethodGet, p, "")
		if code != fiber.StatusOK {
			t.Fatalf("%s: expected 200, got %d", p, code)
		}
	}
}

func TestCreateEnvelope(t *testing.T) {
	app := setup()
	code, body := doReq(app, fiber.MethodPost, "/api/v1/examples", `{"name":"first"}`)
	if code != fiber.StatusCreated {
		t.Fatalf("expected 201, got %d: %s", code, string(body))
	}
	var b map[string]any
	_ = json.Unmarshal(body, &b)
	data, _ := b["data"].(map[string]any)
	if data["name"] != "first" {
		t.Errorf("unexpected: %s", string(body))
	}
}

func TestCreateBlankRejected(t *testing.T) {
	app := setup()
	code, body := doReq(app, fiber.MethodPost, "/api/v1/examples", `{"name":""}`)
	if code != fiber.StatusBadRequest {
		t.Fatalf("expected 400, got %d: %s", code, string(body))
	}
	var b map[string]any
	_ = json.Unmarshal(body, &b)
	errObj, _ := b["error"].(map[string]any)
	if errObj["code"] != "VALIDATION_ERROR" {
		t.Errorf("unexpected: %s", string(body))
	}
}

func TestUnknownResource404(t *testing.T) {
	app := setup()
	code, body := doReq(app, fiber.MethodGet, "/api/v1/examples/999", "")
	if code != fiber.StatusNotFound {
		t.Fatalf("expected 404, got %d: %s", code, string(body))
	}
	var b map[string]any
	_ = json.Unmarshal(body, &b)
	errObj, _ := b["error"].(map[string]any)
	if errObj["code"] != "RESOURCE_NOT_FOUND" {
		t.Errorf("unexpected: %s", string(body))
	}
}
