package api_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"

	"forgebase/go-gin/internal/api"
	"forgebase/go-gin/internal/examples"
)

func setupServer() (*httptest.ResponseRecorder, *gin.Engine) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	api.Register(r, examples.New(), nil)
	return httptest.NewRecorder(), r
}

func doRequest(r *gin.Engine, method, path, body string) *httptest.ResponseRecorder {
	rec := httptest.NewRecorder()
	req := httptest.NewRequest(method, path, strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	r.ServeHTTP(rec, req)
	return rec
}

func TestHealth(t *testing.T) {
	_, r := setupServer()
	rec := doRequest(r, http.MethodGet, "/health", "")
	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	var body map[string]string
	_ = json.Unmarshal(rec.Body.Bytes(), &body)
	if body["status"] != "ok" {
		t.Errorf("unexpected body: %s", rec.Body.String())
	}
}

func TestLivenessAndReadiness(t *testing.T) {
	_, r := setupServer()
	for _, path := range []string{"/health/live", "/health/ready"} {
		rec := doRequest(r, http.MethodGet, path, "")
		if rec.Code != http.StatusOK {
			t.Fatalf("%s: expected 200, got %d", path, rec.Code)
		}
	}
}

func TestCreateEnvelope(t *testing.T) {
	_, r := setupServer()
	rec := doRequest(r, http.MethodPost, "/api/v1/examples", `{"name":"first"}`)
	if rec.Code != http.StatusCreated {
		t.Fatalf("expected 201, got %d: %s", rec.Code, rec.Body.String())
	}
	var body map[string]any
	_ = json.Unmarshal(rec.Body.Bytes(), &body)
	data, _ := body["data"].(map[string]any)
	if data["name"] != "first" {
		t.Errorf("unexpected body: %s", rec.Body.String())
	}
}

func TestCreateBlankRejected(t *testing.T) {
	_, r := setupServer()
	rec := doRequest(r, http.MethodPost, "/api/v1/examples", `{"name":""}`)
	if rec.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d: %s", rec.Code, rec.Body.String())
	}
	var body map[string]any
	_ = json.Unmarshal(rec.Body.Bytes(), &body)
	errObj, _ := body["error"].(map[string]any)
	if errObj["code"] != "VALIDATION_ERROR" {
		t.Errorf("unexpected error code: %v", errObj["code"])
	}
}

func TestUnknownResource404(t *testing.T) {
	_, r := setupServer()
	rec := doRequest(r, http.MethodGet, "/api/v1/examples/999", "")
	if rec.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d: %s", rec.Code, rec.Body.String())
	}
	var body map[string]any
	_ = json.Unmarshal(rec.Body.Bytes(), &body)
	errObj, _ := body["error"].(map[string]any)
	if errObj["code"] != "RESOURCE_NOT_FOUND" {
		t.Errorf("unexpected error code: %v", errObj["code"])
	}
}
