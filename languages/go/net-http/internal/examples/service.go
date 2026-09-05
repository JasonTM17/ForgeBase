package examples

import (
	"fmt"
	"strings"
	"sync"
)

// Example is the generic example resource.
type Example struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// Service is a framework-free, in-memory, thread-safe example service.
type Service struct {
	mu     sync.Mutex
	items  map[int]Example
	nextID int
}

func New() *Service {
	return &Service{items: make(map[int]Example), nextID: 1}
}

func (s *Service) Create(name string) (Example, error) {
	if strings.TrimSpace(name) == "" {
		return Example{}, validationError{msg: "name must not be empty"}
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	item := Example{ID: s.nextID, Name: strings.TrimSpace(name)}
	s.items[item.ID] = item
	s.nextID++
	return item, nil
}

func (s *Service) Get(id int) (Example, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	item, ok := s.items[id]
	if !ok {
		return Example{}, fmt.Errorf("Example %d not found", id)
	}
	return item, nil
}

func (s *Service) List() []Example {
	s.mu.Lock()
	defer s.mu.Unlock()
	out := make([]Example, 0, len(s.items))
	for _, item := range s.items {
		out = append(out, item)
	}
	return out
}

// validationError satisfies errors.ClientError for 400 responses.
type validationError struct {
	msg string
}

func (e validationError) Error() string      { return e.msg }
func (e validationError) ClientCode() string { return "VALIDATION_ERROR" }
