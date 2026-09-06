package config_test

import (
	"context"
	"log/slog"
	"testing"

	"forgebase/go-net-http/internal/config"
)

func TestLoadDefaults(t *testing.T) {
	t.Setenv("APP_ENV", "")
	t.Setenv("APP_NAME", "")
	t.Setenv("APP_ADDR", "")

	cfg, err := config.Load()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if cfg.AppName != "go-net-http" {
		t.Errorf("expected default app name, got %q", cfg.AppName)
	}
	if cfg.AppEnv != config.Development {
		t.Errorf("expected development env, got %q", cfg.AppEnv)
	}
	if cfg.Addr != ":8000" {
		t.Errorf("expected default addr, got %q", cfg.Addr)
	}
}

func TestLoadInvalidEnvFailsFast(t *testing.T) {
	t.Setenv("APP_ENV", "staging")
	if _, err := config.Load(); err == nil {
		t.Fatal("expected error for invalid APP_ENV")
	}
}

func TestLoggerHonorsAppEnv(t *testing.T) {
	dev := config.Logger(config.AppConfig{AppEnv: config.Development})
	if !dev.Enabled(context.Background(), slog.LevelDebug) {
		t.Error("expected debug logging enabled outside production")
	}
	prod := config.Logger(config.AppConfig{AppEnv: config.Production})
	if prod.Enabled(context.Background(), slog.LevelDebug) {
		t.Error("expected production logger to stay at info")
	}
}
