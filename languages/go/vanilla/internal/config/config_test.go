package config_test

import (
	"testing"

	"forgebase/go-vanilla/internal/config"
)

func TestLoadDefaults(t *testing.T) {
	t.Setenv("APP_ENV", "")
	t.Setenv("APP_NAME", "")

	cfg, err := config.Load()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if cfg.AppName != "forgebase-go" {
		t.Errorf("expected default app name, got %q", cfg.AppName)
	}
	if cfg.AppEnv != config.Development {
		t.Errorf("expected development env, got %q", cfg.AppEnv)
	}
}

func TestLoadInvalidEnvFailsFast(t *testing.T) {
	t.Setenv("APP_ENV", "staging")
	if _, err := config.Load(); err == nil {
		t.Fatal("expected error for invalid APP_ENV")
	}
}
