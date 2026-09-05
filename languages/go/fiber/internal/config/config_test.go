package config

import "testing"

func TestLoadParsesExplicitCorsOrigins(t *testing.T) {
	t.Setenv("APP_NAME", "demo")
	t.Setenv("APP_ENV", "testing")
	t.Setenv("APP_ADDR", ":9000")
	t.Setenv("CORS_ORIGINS", " https://example.test, ,http://localhost:3000 ")

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}

	want := []string{"https://example.test", "http://localhost:3000"}
	if len(cfg.CorsOrigins) != len(want) {
		t.Fatalf("CorsOrigins = %#v, want %#v", cfg.CorsOrigins, want)
	}
	for i := range want {
		if cfg.CorsOrigins[i] != want[i] {
			t.Errorf("CorsOrigins[%d] = %q, want %q", i, cfg.CorsOrigins[i], want[i])
		}
	}
}
