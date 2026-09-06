package api

import (
	"log/slog"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"

	"forgebase/go-gin/internal/errors"
	"forgebase/go-gin/internal/examples"
)

// Register wires the health probes and the example resource onto the engine.
// CORS is applied by main from the validated config, not here.
func Register(r *gin.Engine, service *examples.Service, log *slog.Logger) {
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})
	r.GET("/health/live", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})
	r.GET("/health/ready", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	g := r.Group("/api/v1/examples")
	{
		g.GET("", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{"data": service.List(), "message": "ok"})
		})
		g.POST("", func(c *gin.Context) {
			var req struct {
				Name string `json:"name" binding:"required"`
			}
			if err := c.ShouldBindJSON(&req); err != nil {
				errors.Write(c, log, &clientBindingError{err.Error()})
				return
			}
			created, err := service.Create(req.Name)
			if err != nil {
				errors.Write(c, log, err)
				return
			}
			c.JSON(http.StatusCreated, gin.H{"data": created, "message": "created"})
		})
		g.GET("/:id", func(c *gin.Context) {
			id, err := strconv.Atoi(c.Param("id"))
			if err != nil {
				errors.Write(c, log, &clientBindingError{"id must be an integer"})
				return
			}
			item, err := service.Get(id)
			if err != nil {
				errors.Write(c, log, err)
				return
			}
			c.JSON(http.StatusOK, gin.H{"data": item, "message": "ok"})
		})
	}
}

// clientBindingError reports request-binding failures with a stable code.
type clientBindingError struct {
	msg string
}

func (e *clientBindingError) Error() string      { return e.msg }
func (e *clientBindingError) ClientCode() string { return "VALIDATION_ERROR" }

var _ errors.ClientError = (*clientBindingError)(nil)
