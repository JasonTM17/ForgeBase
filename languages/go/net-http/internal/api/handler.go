package api

import (
	"encoding/json"
	"log/slog"
	"net/http"
	"strconv"
	"strings"

	"forgebase/go-net-http/internal/errors"
	"forgebase/go-net-http/internal/examples"
)

// Handler wires routes to the example service with the error envelope.
type Handler struct {
	service *examples.Service
	log     *slog.Logger
}

func NewHandler() *Handler {
	return &Handler{service: examples.New(), log: slog.Default()}
}

func (h *Handler) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", h.health)
	mux.HandleFunc("/health/live", func(w http.ResponseWriter, _ *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})
	mux.HandleFunc("/health/ready", func(w http.ResponseWriter, _ *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})
	mux.HandleFunc("/api/v1/examples", h.examplesCollection)
	mux.HandleFunc("/api/v1/examples/", h.exampleItem)
	return mux
}

func (h *Handler) health(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (h *Handler) writeError(w http.ResponseWriter, r *http.Request, err error) {
	errors.WriteError(w, r, h.log, err)
}

func (h *Handler) examplesCollection(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		writeJSON(w, http.StatusOK, map[string]any{"data": h.service.List(), "message": "ok"})
	case http.MethodPost:
		var req struct {
			Name string `json:"name"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			h.writeError(w, r, err)
			return
		}
		created, err := h.service.Create(req.Name)
		if err != nil {
			h.writeError(w, r, err)
			return
		}
		writeJSON(w, http.StatusCreated, map[string]any{"data": created, "message": "created"})
	default:
		h.writeError(w, r, &errors.DomainError{Code: "METHOD_NOT_ALLOWED", Status: http.StatusMethodNotAllowed, Message: "Method not allowed"})
	}
}

func (h *Handler) exampleItem(w http.ResponseWriter, r *http.Request) {
	idStr := strings.TrimPrefix(r.URL.Path, "/api/v1/examples/")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, r, &errors.DomainError{Code: "INVALID_ID", Status: http.StatusBadRequest, Message: "id must be an integer"})
		return
	}
	item, err := h.service.Get(id)
	if err != nil {
		h.writeError(w, r, errors.NotFound(err.Error()))
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"data": item, "message": "ok"})
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(body)
}
