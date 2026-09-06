package api

import (
	"log/slog"
	"strconv"

	"github.com/gofiber/fiber/v3"

	"forgebase/go-fiber/internal/errors"
	"forgebase/go-fiber/internal/examples"
)

func Register(app *fiber.App, service *examples.Service, log *slog.Logger) {
	app.Get("/health", func(c fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok"})
	})
	app.Get("/health/live", func(c fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok"})
	})
	app.Get("/health/ready", func(c fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok"})
	})

	g := app.Group("/api/v1/examples")
	g.Get("", func(c fiber.Ctx) error {
		return c.JSON(fiber.Map{"data": service.List(), "message": "ok"})
	})
	g.Post("", func(c fiber.Ctx) error {
		var req struct {
			Name string `json:"name"`
		}
		if err := c.Bind().Body(&req); err != nil {
			return errors.Write(c, log, &clientError{msg: err.Error()})
		}
		created, err := service.Create(req.Name)
		if err != nil {
			return errors.Write(c, log, err)
		}
		return c.Status(fiber.StatusCreated).JSON(fiber.Map{"data": created, "message": "created"})
	})
	g.Get("/:id", func(c fiber.Ctx) error {
		id, err := strconv.Atoi(c.Params("id"))
		if err != nil {
			return errors.Write(c, log, &clientError{msg: "id must be an integer"})
		}
		item, err := service.Get(id)
		if err != nil {
			return errors.Write(c, log, err)
		}
		return c.JSON(fiber.Map{"data": item, "message": "ok"})
	})
}

type clientError struct {
	msg string
}

func (e *clientError) Error() string      { return e.msg }
func (e *clientError) ClientCode() string { return "VALIDATION_ERROR" }
