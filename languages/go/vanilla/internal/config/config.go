// Package config provides fail-fast, environment-driven configuration.
//
// Misconfiguration must stop the process at boot with a message naming the
// offending variable — never undefined runtime behavior later.
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
}

func Load() (AppConfig, error) {
	appName := strings.TrimSpace(os.Getenv("APP_NAME"))
	if appName == "" {
		appName = "forgebase-go"
	}

	env := strings.TrimSpace(os.Getenv("APP_ENV"))
	if env == "" {
		env = "development"
	}
	appEnv := AppEnv(env)
	switch appEnv {
	case Development, Testing, Production:
		return AppConfig{AppName: appName, AppEnv: appEnv}, nil
	default:
		return AppConfig{}, fmt.Errorf("APP_ENV must be one of development, testing, production, got %q", env)
	}
}
