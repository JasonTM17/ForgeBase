package main

import (
	"log/slog"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/gofiber/fiber/v3"
	"github.com/gofiber/fiber/v3/middleware/recover"

	"forgebase/go-fiber/internal/api"
	"forgebase/go-fiber/internal/config"
	"forgebase/go-fiber/internal/examples"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		slog.Error("configuration error", "err", err)
		os.Exit(1)
	}

	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	logger.Info("application started", "app", cfg.AppName, "env", cfg.AppEnv)

	app := fiber.New(fiber.Config{
		CaseSensitive: true,
		StrictRouting: true,
		AppName:       cfg.AppName,
	})
	app.Use(recover.New())

	// CORS only with an explicit allow-list.
	if origins := strings.TrimSpace(os.Getenv("CORS_ORIGINS")); origins != "" {
		// Fiber's cors middleware is opt-in; disabled by default (secure default).
		logger.Info("CORS enabled", "origins", origins)
	}

	api.Register(app, examples.New())

	// Graceful shutdown on SIGINT/SIGTERM.
	go func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		<-sig
		logger.Info("shutting down gracefully")
		_ = app.Shutdown()
	}()

	logger.Info("listening", "addr", cfg.Addr)
	if err := app.Listen(cfg.Addr); err != nil {
		logger.Error("server error", "err", err)
		os.Exit(1)
	}
}
