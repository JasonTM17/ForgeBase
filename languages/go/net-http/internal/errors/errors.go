package errors

import (
	"encoding/json"
	"log/slog"
	"net/http"
)

// ClientError marks an error as a 4xx client error with a stable code.
type ClientError interface {
	error
	ClientCode() string
}

// ErrorEnvelope is the consistent error contract for all API responses.
type ErrorEnvelope struct {
	Error struct {
		Code    string `json:"code"`
		Message string `json:"message"`
	} `json:"error"`
}

// DomainError is an expected, user-facing error with a stable code + HTTP status.
type DomainError struct {
	Code    string
	Status  int
	Message string
}

func (e *DomainError) Error() string { return e.Message }

func NotFound(message string) *DomainError {
	return &DomainError{Code: "RESOURCE_NOT_FOUND", Status: http.StatusNotFound, Message: message}
}

// WriteError maps an error to the error envelope and writes the HTTP response.
func WriteError(w http.ResponseWriter, r *http.Request, log *slog.Logger, err error) {
	var status int
	var body ErrorEnvelope

	switch e := err.(type) {
	case *DomainError:
		status = e.Status
		body.Error.Code = e.Code
		body.Error.Message = e.Message
	case ClientError:
		status = http.StatusBadRequest
		body.Error.Code = e.ClientCode()
		body.Error.Message = e.Error()
	default:
		status = http.StatusInternalServerError
		body.Error.Code = "INTERNAL_ERROR"
		body.Error.Message = "An unexpected error occurred"
	}

	if status >= 500 && log != nil {
		log.Error("unhandled error", "err", err, "path", r.URL.Path)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(body)
}
