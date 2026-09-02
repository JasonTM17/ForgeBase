package config

import (
	"fmt"
	"os"
	"strings"
)

type AppEnv string

const (
	Development AppEnv = "development"
	Testing    AppEnv = "testing"
	Production AppEnv = "production"
)

type AppConfig struct {
	AppName string
	AppEnv  AppEnv
	Addr    string
}

func Load() (AppConfig, error) {
	appName := strings.TrimSpace(os.Getenv("APP_NAME"))
	if appName == "" {
		appName = "go-fiber"
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
	return AppConfig{AppName: appName, AppEnv: appEnv, Addr: addr}, nil
}
