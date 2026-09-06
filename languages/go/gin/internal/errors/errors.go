package errors

import (
	"log/slog"
	"net/http"

	"github.com/gin-gonic/gin"
)

// ClientError marks an error as a 4xx client error with a stable code.
type ClientError interface {
	error
	ClientCode() string
}

// ErrorEnvelope is the consistent error contract.
type ErrorEnvelope struct {
	Error struct {
		Code    string `json:"code"`
		Message string `json:"message"`
	} `json:"error"`
}

// Write maps an error to the error envelope and aborts the Gin context.
// Expected client errors keep their stable code; unexpected errors return a
// generic 500 and are logged server-side with their cause — the response body
// never leaks internals.
func Write(c *gin.Context, log *slog.Logger, err error) {
	var status int
	var body ErrorEnvelope

	switch e := err.(type) {
	case ClientError:
		status = statusForCode(e.ClientCode())
		body.Error.Code = e.ClientCode()
		body.Error.Message = e.Error()
	default:
		status = http.StatusInternalServerError
		body.Error.Code = "INTERNAL_ERROR"
		body.Error.Message = "An unexpected error occurred"
		if log != nil {
			log.Error("unhandled error", "err", err, "path", c.Request.URL.Path)
		}
	}

	c.AbortWithStatusJSON(status, body)
}

func statusForCode(code string) int {
	if code == "RESOURCE_NOT_FOUND" {
		return http.StatusNotFound
	}
	return http.StatusBadRequest
}
