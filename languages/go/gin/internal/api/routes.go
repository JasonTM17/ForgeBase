package api

import (
	"net/http"
	"strconv"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"

	"forgebase/go-gin/internal/errors"
	"forgebase/go-gin/internal/examples"
)

func Register(r *gin.Engine, service *examples.Service) {
	r.Use(gin.Recovery())

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
				errors.Write(c, &clientBindingError{err.Error()})
				return
			}
			created, err := service.Create(req.Name)
			if err != nil {
				mapAndWrite(c, err)
				return
			}
			c.JSON(http.StatusCreated, gin.H{"data": created, "message": "created"})
		})
		g.GET("/:id", func(c *gin.Context) {
			id, err := strconv.Atoi(c.Param("id"))
			if err != nil {
				errors.Write(c, &clientBindingError{"id must be an integer"})
				return
			}
			item, err := service.Get(id)
			if err != nil {
				mapAndWrite(c, err)
				return
			}
			c.JSON(http.StatusOK, gin.H{"data": item, "message": "ok"})
		})
	}
}

// mapAndWrite translates service errors to the envelope with proper status.
func mapAndWrite(c *gin.Context, err error) {
	var status int
	var body errors.ErrorEnvelope
	switch e := err.(type) {
	case errors.ClientError:
		code := e.ClientCode()
		status = statusForCode(code)
		body.Error.Code = code
		body.Error.Message = e.Error()
	default:
		status = http.StatusInternalServerError
		body.Error.Code = "INTERNAL_ERROR"
		body.Error.Message = "An unexpected error occurred"
	}
	c.AbortWithStatusJSON(status, body)
}

func statusForCode(code string) int {
	if code == "RESOURCE_NOT_FOUND" {
		return http.StatusNotFound
	}
	return http.StatusBadRequest
}

type clientBindingError struct {
	msg string
}

func (e *clientBindingError) Error() string      { return e.msg }
func (e *clientBindingError) ClientCode() string { return "VALIDATION_ERROR" }

// ApplyCors registers CORS with an explicit allow-list (empty = disabled).
func ApplyCors(r *gin.Engine, origins []string) {
	if len(origins) == 0 {
		return
	}
	r.Use(cors.New(cors.Config{
		AllowOrigins: origins,
		AllowMethods: []string{"GET", "POST", "PUT", "PATCH", "DELETE"},
		AllowHeaders: []string{"Authorization", "Content-Type"},
	}))
}

// Ensure errors.ClientError is used (CompileClientCarrier).
var _ errors.ClientError = (*clientBindingError)(nil)
