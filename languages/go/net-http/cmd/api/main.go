package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"forgebase/go-net-http/internal/api"
	"forgebase/go-net-http/internal/config"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		slog.Error("configuration error", "err", err)
		os.Exit(1)
	}
	log := config.Logger(cfg)
	log.Info("application started", "app", cfg.AppName, "env", cfg.AppEnv)

	server := config.NewServer(cfg.Addr, api.NewHandler().Routes())

	// Graceful shutdown on SIGINT/SIGTERM.
	go func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		<-sig
		log.Info("shutting down gracefully")
		if err := server.Shutdown(context.Background()); err != nil {
			log.Error("shutdown error", "err", err)
		}
	}()

	log.Info("listening", "addr", cfg.Addr)
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Error("server error", "err", err)
		os.Exit(1)
	}
}
