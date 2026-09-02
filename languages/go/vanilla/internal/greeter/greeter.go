// Package greeter is a deliberately trivial example service demonstrating the
// testable service-layer pattern.
package greeter

import (
	"fmt"
	"strings"
)

type Service struct{}

func New() *Service { return &Service{} }

func (s *Service) Greet(name string) (string, error) {
	trimmed := strings.TrimSpace(name)
	if trimmed == "" {
		return "", fmt.Errorf("name must not be empty")
	}
	return "Hello, " + trimmed + "!", nil
}
