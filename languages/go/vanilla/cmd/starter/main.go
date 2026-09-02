// Command entry point: `go run ./cmd/starter <name>` or build with `go build`.
//
// Config problems are fatal and must not print a stack trace to users.
package main

import (
	"fmt"
	"log/slog"
	"os"
	"strings"

	"forgebase/go-vanilla/internal/config"
	"forgebase/go-vanilla/internal/greeter"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintf(os.Stderr, "configuration error: %s\n", err)
		os.Exit(1)
	}

	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	logger.Info("application started", "app", cfg.AppName, "env", cfg.AppEnv)

	if len(os.Args) < 2 || strings.TrimSpace(os.Args[1]) == "" {
		fmt.Fprintln(os.Stderr, "usage: starter <name>")
		os.Exit(1)
	}

	greeting, err := greeter.New().Greet(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %s\n", err)
		os.Exit(1)
	}
	fmt.Println(greeting)
}
