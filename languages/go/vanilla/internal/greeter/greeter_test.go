package greeter_test

import (
	"testing"

	"forgebase/go-vanilla/internal/greeter"
)

func TestGreet(t *testing.T) {
	svc := greeter.New()
	g, err := svc.Greet("World")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if g != "Hello, World!" {
		t.Errorf("unexpected greeting: %q", g)
	}
}

func TestGreetTrimsWhitespace(t *testing.T) {
	g, err := greeter.New().Greet("  World  ")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if g != "Hello, World!" {
		t.Errorf("unexpected greeting: %q", g)
	}
}

func TestGreetRejectsBlank(t *testing.T) {
	if _, err := greeter.New().Greet("   "); err == nil {
		t.Fatal("expected error for blank name")
	}
}
