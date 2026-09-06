package config

import (
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"strings"
	"time"
)

type AppEnv string

const (
	Development AppEnv = "development"
	Testing     AppEnv = "testing"
	Production  AppEnv = "production"
)

type AppConfig struct {
	AppName string
	AppEnv  AppEnv
	Addr    string
}

func Load() (AppConfig, error) {
	appName := strings.TrimSpace(os.Getenv("APP_NAME"))
	if appName == "" {
		appName = "go-net-http"
	}
	env := strings.TrimSpace(os.Getenv("APP_ENV"))
	if env == "" {
		env = "development"
	}
	appEnv := AppEnv(env)
	switch appEnv {
	case Development, Testing, Production:
		// ok
	default:
		return AppConfig{}, fmt.Errorf("APP_ENV must be one of development, testing, production, got %q", env)
	}
	addr := strings.TrimSpace(os.Getenv("APP_ADDR"))
	if addr == "" {
		addr = ":8000"
	}
	return AppConfig{AppName: appName, AppEnv: appEnv, Addr: addr}, nil
}

// NewServer builds an *http.Server with graceful shutdown on SIGINT/SIGTERM.
func NewServer(addr string, handler http.Handler) *http.Server {
	return &http.Server{
		Addr:              addr,
		Handler:           handler,
		ReadHeaderTimeout: 5 * time.Second,
		IdleTimeout:       60 * time.Second,
	}
}

// Logger returns a structured JSON logger at the configured level:
// development and testing log debug detail, production stays at info.
func Logger(cfg AppConfig) *slog.Logger {
	level := slog.LevelInfo
	if cfg.AppEnv != Production {
		level = slog.LevelDebug
	}
	return slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: level}))
}
