package errors

import (
	"log/slog"

	"github.com/gofiber/fiber/v3"
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

// Write maps an error to the error envelope and writes the Fiber response.
// Unexpected (non-client) errors are logged server-side with their cause —
// the response body stays generic so internals never leak.
func Write(c fiber.Ctx, log *slog.Logger, err error) error {
	var status int
	var body ErrorEnvelope

	switch e := err.(type) {
	case ClientError:
		status = statusForCode(e.ClientCode())
		body.Error.Code = e.ClientCode()
		body.Error.Message = e.Error()
	default:
		status = fiber.StatusInternalServerError
		body.Error.Code = "INTERNAL_ERROR"
		body.Error.Message = "An unexpected error occurred"
		if log != nil {
			log.Error("unhandled error", "err", err, "path", c.Path())
		}
	}

	return c.Status(status).JSON(body)
}

func statusForCode(code string) int {
	if code == "RESOURCE_NOT_FOUND" {
		return fiber.StatusNotFound
	}
	return fiber.StatusBadRequest
}
