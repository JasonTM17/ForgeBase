package config

import (
	"fmt"
	"os"
	"strings"
)

type AppEnv string

const (
	Development AppEnv = "development"
	Testing     AppEnv = "testing"
	Production  AppEnv = "production"
)

type AppConfig struct {
	AppName     string
	AppEnv      AppEnv
	Addr        string
	CorsOrigins []string
}

func Load() (AppConfig, error) {
	appName := strings.TrimSpace(os.Getenv("APP_NAME"))
	if appName == "" {
		appName = "go-gin"
	}
	env := strings.TrimSpace(os.Getenv("APP_ENV"))
	if env == "" {
		env = "development"
	}
	appEnv := AppEnv(env)
	switch appEnv {
	case Development, Testing, Production:
	default:
		return AppConfig{}, fmt.Errorf("APP_ENV must be one of development, testing, production, got %q", env)
	}
	addr := strings.TrimSpace(os.Getenv("APP_ADDR"))
	if addr == "" {
		addr = ":8000"
	}
	return AppConfig{
		AppName:     appName,
		AppEnv:      appEnv,
		Addr:        addr,
		CorsOrigins: parseOrigins(os.Getenv("CORS_ORIGINS")),
	}, nil
}

// parseOrigins splits a comma-separated allow-list, dropping empty entries.
func parseOrigins(raw string) []string {
	var origins []string
	for _, origin := range strings.Split(raw, ",") {
		if trimmed := strings.TrimSpace(origin); trimmed != "" {
			origins = append(origins, trimmed)
		}
	}
	return origins
}
