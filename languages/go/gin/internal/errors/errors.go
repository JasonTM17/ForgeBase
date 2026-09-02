package errors

import (
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
func Write(c *gin.Context, err error) {
	var status int
	var body ErrorEnvelope

	switch e := err.(type) {
	case ClientError:
		status = http.StatusBadRequest
		body.Error.Code = e.ClientCode()
		body.Error.Message = e.Error()
	default:
		status = http.StatusInternalServerError
		body.Error.Code = "INTERNAL_ERROR"
		body.Error.Message = "An unexpected error occurred"
	}

	c.AbortWithStatusJSON(status, body)
}
