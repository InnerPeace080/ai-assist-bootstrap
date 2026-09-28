---
name: go-idiomatic-architecture
description: Standard Go layout (cmd/, internal/), constructor patterns, %w error wrapping, context.Context, and race testing.
author: "Go Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/golang-standards/project-layout"
  upstream_file: "README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Strict internal/ boundary enforcement"
    - "Explicit %w wrapping convention"
    - "context.Context first parameter invariant"
---

# Go Idiomatic Architecture Runbook

## When to Use
Use this skill when designing package structures, wiring dependencies, creating constructors, or managing concurrency and errors in Go 1.23+ applications.

---

## 1. Directory Structure

```text
├── cmd/
│   └── api/
│       └── main.go       # Dependency wiring, configuration parsing, graceful shutdown
├── internal/             # Compiler-enforced private packages (cannot be imported outside)
│   ├── domain/           # Core models and business interfaces
│   ├── service/          # Business logic implementations
│   └── repository/       # Database access / external client adapters
├── go.mod
└── go.sum
```

---

## 2. Constructor Pattern & Dependency Injection

- Always accept interfaces or parsed primitives, never unparsed strings or raw environments.
- Return `(*Struct, error)` when initialization can fail; do not return partial structs.

```go
package service

import (
	"context"
	"errors"
	"fmt"
)

type UserRepository interface {
	FindByID(ctx context.Context, id string) (*domain.User, error)
}

type UserService struct {
	repo UserRepository
}

func NewUserService(repo UserRepository) (*UserService, error) {
	if repo == nil {
		return nil, errors.New("user repository cannot be nil")
	}
	return &UserService{repo: repo}, nil
}
```

---

## 3. Idiomatic Error Handling

- **Error Wrapping**: Wrap errors with context using `%w` so callers can inspect with `errors.Is` or `errors.As`:
  ```go
  user, err := s.repo.FindByID(ctx, id)
  if err != nil {
      return nil, fmt.Errorf("retrieving user with id %s: %w", id, err)
  }
  ```
- **Sentinel Errors**: Define domain errors as package-level exported variables:
  ```go
  var ErrUserNotFound = errors.New("user not found")
  ```

---

## 4. Concurrency & Context Rules

- **`context.Context` First**: Any function performing network, file I/O, or database queries must accept `ctx context.Context` as its first parameter.
- **Graceful Shutdown**: Always listen for OS signals and pass cancellable contexts to HTTP servers and background workers:
  ```go
  ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
  defer stop()
  ```
- **Verification**: Always run tests with race detection enabled:
  ```bash
  go test -race ./...
  ```

