# 03. Stack Profiles

This document details the stack-specific configurations, invariants, scoped rules, and curated skills for each supported application architecture.

---

## 1. Next.js Profile (`profile: nextjs`)

### Overview
* **Target Stack**: Next.js 15+ (App Router), React 19, TypeScript, Tailwind CSS, shadcn/ui, Zod.
* **Package Manager**: `pnpm` (default), `npm`, or `bun`.
* **Testing**: Vitest + React Testing Library + Playwright E2E.

### Key AI Invariants & Rules
1. **Server-First Boundary**:
   - Default all components to React Server Components (RSC).
   - Only add `'use client'` at leaf nodes requiring interactivity, browser APIs, or state hooks (`useState`, `useEffect`).
   - Never import server-only modules (database, secret API keys) into client components.
2. **Data Mutations**:
   - Use **Server Actions** (`'use server'`) located in dedicated `actions/` files.
   - Always validate action inputs with Zod schemas before database queries.
   - Return structured results `{ success: boolean, data?: T, error?: string }` instead of raw exceptions.
3. **Route Handlers**:
   - Limit `route.ts` handlers to webhooks or external API consumers. Internal UI interactions should use Server Actions.
4. **Styling & Components**:
   - Use Tailwind utility classes with `cn()` (`clsx` + `tailwind-merge`).
   - Follow shadcn/ui accessibility standards (Radix UI primitives, ARIA attributes).

### Curated Skills
* `nextjs-app-router`: Dynamic segments, parallel routes, intercepting routes, caching rules (`revalidatePath`, `revalidateTag`).
* `tailwind-shadcn`: Accessible component composition, theming, dark mode.
* `nextjs-performance`: Next Image optimization, bundle analysis, font loading.

---

## 2. NestJS Profile (`profile: nestjs`)

### Overview
* **Target Stack**: NestJS 10+, TypeScript, Express or Fastify, Prisma or TypeORM, Class-Validator or Zod.
* **Testing**: Jest unit tests + Supertest E2E tests.

### Key AI Invariants & Rules
1. **Module Architecture**:
   - Enforce the NestJS modular pattern: every domain entity lives in its own module (`user.module.ts`, `auth.module.ts`).
   - Controllers handle HTTP routing and request/response mapping ONLY.
   - Services contain business logic and database orchestration.
   - Repositories or ORM services handle data persistence.
2. **DTO & Validation**:
   - Every input payload must have an explicit DTO class.
   - Use `ValidationPipe` with `{ whitelist: true, forbidNonWhitelisted: true }`.
   - Never accept untyped `any` or raw `req.body` in controller handlers.
3. **Error Handling**:
   - Use standard NestJS HTTP exceptions (`NotFoundException`, `BadRequestException`, `ForbiddenException`).
   - Never expose internal database stack traces to clients.
4. **Configuration & Secrets**:
   - Access environment variables exclusively through `@nestjs/config` `ConfigService` with typed schemas.

### Curated Skills
* `nestjs-module-architect`: Scaffolds controller, service, DTOs, and test specs following architectural standards.
* `db-prisma-migration`: Safe schema migration, indexing, foreign keys, transaction handling.
* `api-testing`: Supertest integration tests with mocked database or test containers.

---

## 3. React Native & Expo Profile (`profile: react-native`)

### Overview
* **Target Stack**: Expo SDK 52+, Expo Router, TypeScript, NativeWind v4 or Tamagui.
* **Testing**: Jest with `@testing-library/react-native` + Maestro for mobile E2E.

### Key AI Invariants & Rules
1. **File-Based Routing**:
   - Follow Expo Router conventions in `app/` (`(tabs)`, `(auth)`, `[id].tsx`).
   - Use typed navigation routes with `router.push('/...')`.
2. **Platform Specificity**:
   - Handle Android vs iOS differences cleanly using `Platform.OS` or platform extensions (`.android.tsx`, `.ios.tsx`).
   - Always wrap screens in `SafeAreaProvider` and `useSafeAreaInsets()`.
3. **Mobile Performance**:
   - Never use raw `<ScrollView>` for long lists; use `<FlatList>` or `FlashList` with `keyExtractor` and `getItemType`.
   - Memoize expensive render functions and callbacks (`useMemo`, `useCallback`).
   - Avoid blocking the main JS thread; offload animations to `react-native-reanimated`.
4. **Permissions & Native Modules**:
   - Use Expo config plugins (`app.json` / `app.config.ts`) for native permissions instead of manual Xcode/Gradle hacking.

### Curated Skills
* `expo-router`: Navigation hierarchies, tabs, deep linking, modal presentations.
* `mobile-perf-tuning`: List rendering optimization, memory leak prevention, layout thrashing prevention.

---

## 4. Monorepo Profile (`profile: monorepo`)

### Overview
* **Target Stack**: Turborepo + `pnpm` workspaces.
* **Layout**:
  ```
  apps/
    ├── web/              # Next.js App
    ├── api/              # NestJS Backend
    └── mobile/           # Expo App (optional)
  packages/
    ├── ui/               # Shared React/Tailwind component library
    ├── shared-types/     # Common DTOs, interfaces, and schemas (Zod)
    ├── config-eslint/    # Shared linting configs
    └── config-typescript/# Base tsconfig files
  ```

### Key AI Invariants & Rules
1. **Package Boundaries**:
   - Apps must import from `@repo/ui` or `@repo/shared-types` via package exports.
   - Sibling apps (`apps/web` and `apps/api`) MUST NEVER import code directly from each other's directory trees.
2. **Shared Types as Contracts**:
   - DTOs and API contracts live in `packages/shared-types`.
   - Modifying a contract requires updating both the API controller and the Web/Mobile consumer.
3. **Turborepo Caching**:
   - All `turbo.json` tasks must declare explicit inputs and outputs to preserve remote cache integrity.
4. **Hierarchical AI Rules**:
   - **Root Level (`/AGENTS.md`)**: Defines monorepo-wide rules, package manager commands (`pnpm -w`, `pnpm --filter`), and architecture layout.
   - **App Level (`apps/web/.cursor/rules/`, etc.)**: Overlays stack-specific frontend/backend rules without cluttering the root context.

---

## 5. React.js SPA Profile (`profile: reactjs`)

### Overview
* **Target Stack**: React 19 / 18, Vite, TypeScript (Strict), Tailwind CSS, TanStack Query (React Query) v5, Zustand.
* **Testing & Verification**:
  - Fast typecheck: `pnpm exec tsc --noEmit`
  - Test suite: `pnpm run test` (Vitest + Testing Library)
  - Production build: `pnpm run build`

### Key AI Invariants & Rules
1. **Feature-First Architecture**:
   - Organize code by domain feature (`src/features/[feature-name]/components/`, `api/`, `hooks/`) rather than flat technical folders.
   - Colocate tests (`*.test.tsx`) next to the components they test.
2. **Strict State Separation**:
   - **Server State**: Managed exclusively through **TanStack Query v5**. Wrap queries and mutations in custom hooks (`useUsersQuery()`).
   - **Query Key Factories**: Always use typed key factory objects to prevent cache invalidation drift:
     ```typescript
     export const userKeys = {
       all: ['users'] as const,
       lists: () => [...userKeys.all, 'list'] as const,
       detail: (id: string) => [...userKeys.all, 'detail', id] as const,
     };
     ```
   - **Client State**: Lightweight UI state only via **Zustand** (modals, theme, active drawers).
   - **Negative Constraint**: **NEVER** copy server state into Zustand or `useState`.
3. **Negative Constraints on Hooks**:
   - **NEVER** use `useEffect` for data fetching (use TanStack Query).
   - **NEVER** use `useEffect` to derive or sync state (compute during render or `useMemo`).
   - Avoid barrel `index.ts` files that cause circular bundle dependencies.
4. **Forms & Validation**:
   - `react-hook-form` with `zod` schema resolvers.

### Curated Skills
* `vite-react-spa`: Feature-first architecture, `React.lazy`/`Suspense` boundaries, Vite environment variables (`import.meta.env`).
* `tanstack-query-v5`: Key factories, optimistic updates, infinite queries, retry strategies.
* `tailwind-component-design`: UI primitives, class-variance-authority (`cva`), accessible ARIA states.

---

## 6. Golang Profile (`profile: golang`)

### Overview
* **Target Stack**: Go 1.23+, Standard Library, Chi / Echo / Gin, `sqlc` or `gorm`, `golangci-lint`.
* **Testing & Verification**:
  - Race-checked tests: `go test -race -v ./...`
  - Linter: `golangci-lint run ./...`
  - Vet: `go vet ./...`

### Key AI Invariants & Rules
1. **Explicit Error Handling & Wrapping**:
   - Check errors immediately: `if err != nil { return fmt.Errorf("context: %w", err) }`.
   - Wrap with `%w` so callers can use `errors.Is` and `errors.As`.
   - Never silence errors with `_`. Never panic in production handlers.
2. **Project Layout Standards**:
   - `cmd/server/main.go`: Application initialization, configuration, dependency injection, and OS signal trap for graceful shutdown.
   - `internal/`: Private business logic, services, and repositories (compiler-enforced privacy).
   - `pkg/`: Only for code explicitly intended for external public consumption (default to `internal/`).
3. **Structured Concurrency**:
   - First argument of any network, DB, or async function must be `ctx context.Context`.
   - Goroutines must have defined lifecycles (via `errgroup.Group` or channel termination signals) to prevent goroutine leaks.
4. **Testing Standards**:
   - Write **table-driven tests** (`tests := []struct{ name string; ... }`).
   - Use `_test` black-box packages for external integration tests.

### Curated Skills
* `go-idiomatic-architecture`: Domain-driven layout in `internal/`, constructor pattern (`NewService(...)`).
* `go-concurrency-patterns`: Worker pools, channel synchronization, context cancellation, graceful shutdown.
* `sqlc-database`: Type-safe Go code generation from raw SQL queries, transactions, and migration management.

---

## 7. Python Profile (`profile: python`)

### Overview
* **Target Stack**: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (Async), `uv`, `ruff`.
* **Testing & Verification**:
  - Run development server: `uv run fastapi dev app/main.py`
  - Linter & Formatter: `uv run ruff check . --fix && uv run ruff format .`
  - Type checking: `uv run mypy src/`
  - Test runner: `uv run pytest -v` (or single file: `uv run pytest tests/test_user.py`)

### Key AI Invariants & Rules
1. **Environment Hygiene**:
   - **Always** use `uv` (`uv run`, `uv sync`). Never execute bare `pip` or unmanaged `python` commands.
2. **Pydantic v2 & Clean Types**:
   - Use native Python 3.10+ union types (`int | None`, `list[str]`).
   - All controller endpoints must have explicit Pydantic v2 input and response models (`response_model=UserResponse`).
   - No `Any` types; use generics (`TypeVar`) or `TypedDict`.
3. **Layered Architecture**:
   - Follow strict separation: `Router` → `Service` → `Repository`.
   - **Negative Constraint**: Never make direct database queries inside router files.
4. **Async & SQLAlchemy 2.0 Standards**:
   - Use SQLAlchemy 2.0 async syntax (`await session.execute(select(...))`).
   - Never call blocking synchronous I/O inside `async def` endpoints. Offload to `asyncio.to_thread()`.

### Curated Skills
* `fastapi-pydantic-v2`: Router composition, Pydantic v2 validators, dependency injection with `Depends()`.
* `sqlalchemy2-alembic`: Async sessions, typed `Mapped[]` models, Alembic migrations.
* `pytest-asyncio`: Async fixtures, database rollback isolation per test, test client configuration.

---

## 8. Rust Profile (`profile: rust`)

### Overview
* **Target Stack**: Rust 1.83+ (2021 Edition), Cargo, Axum 0.8+, Tokio 1.48+, `sqlx` 0.8+, `thiserror` + `anyhow`.
* **Testing & Verification**:
  - Fast type check: `cargo check`
  - Strict linter: `cargo clippy --all-targets -- -D warnings`
  - Test suite: `cargo test --workspace`
  - Formatting: `cargo fmt --check`

### Key AI Invariants & Rules
1. **Idiomatic Error Handling**:
   - Custom module/domain errors must use `thiserror` enums.
   - Axum route handlers must return `Result<T, AppError>` where `AppError` implements `IntoResponse`.
   - Use `anyhow::Result` for application binaries and scripts.
   - **Negative Constraint**: **NEVER** use `.unwrap()` or `.expect()` in production handler paths; propagate errors via `?`.
2. **Borrowing & Memory Safety**:
   - Avoid unnecessary allocations and `.clone()`. Prefer passing references (`&str`, `&[T]`).
   - Disallow `unsafe` blocks.
3. **Tokio Async Safety**:
   - Never hold standard library `std::sync::Mutex` across `.await` points; use `tokio::sync::Mutex` or message passing via channels.
   - Ensure async handler futures satisfy `Send + 'static`.
4. **Module Organization**:
   - Group by domain/feature rather than technical layer. Keep structs and their `impl` blocks in the same file.

### Curated Skills
* `rust-axum-web`: State extractors, Tower middleware, error response mapping via `IntoResponse`.
* `rust-error-handling`: Designing domain error enums with `thiserror`, mapping third-party errors, tracing spans.
* `sqlx-compile-time`: Compile-time verified SQL queries, connection pooling, migration management.

---

## 9. Erlang Profile (`profile: erlang`)

### Overview
* **Target Stack**: Erlang/OTP 26+, `rebar3`, Cowboy for HTTP, EUnit & Common Test (`ct`).
* **Testing & Verification**:
  - Unit tests: `rebar3 eunit`
  - Integration / Node tests: `rebar3 ct`
  - Static type analysis: `rebar3 dialyzer`
  - Code style audit: `rebar3 as test elvis rock`

### Key AI Invariants & Rules
1. **Supervision Trees & "Let It Crash"**:
   - All long-running processes must be placed under an OTP supervisor (`one_for_one`, `one_for_all`, `rest_for_one`).
   - Do not catch every error defensively. Allow unexpected worker failures to crash cleanly; let the supervisor restart from known valid state.
2. **GenServer Separation**:
   - Strictly separate public client API (`call/2`, `cast/2`) from internal server callbacks (`handle_call/3`, `handle_cast/2`, `handle_info/2`).
   - Always return canonical OTP response tuples (`{reply, Reply, State}`, `{noreply, State}`).
3. **Pattern Matching & Guards**:
   - Use pattern matching in function heads and guards (`when is_integer(X)`) instead of deep nested `case` or `if` statements.
4. **Type Specifications**:
   - Provide `-spec` declarations for all exported functions.
   - Maintain `-type` definitions for record and state types to ensure clean Dialyzer runs.

### Curated Skills
* `erlang-otp-design`: Supervision hierarchies, application specifications (`.app.src`), release packaging.
* `erlang-genserver`: State transitions, message queues, timeout handling, and worker termination.
* `erlang-testing`: Writing EUnit suites, Common Test specs, and mocking with `meck`.

---

## 10. Shell Script Profile (`profile: shell`)

### Overview
* **Target Stack**: Bash 5+ / POSIX Shell, `shellcheck`, `shfmt`, `bats-core` (Bash Automated Testing System).
* **Testing & Verification**:
  - Static Analysis: `shellcheck bin/* lib/* test/*.bats`
  - Code Formatting: `shfmt -d -i 2 -ci .` (or apply: `shfmt -w -i 2 -ci .`)
  - Automated Unit/Integration Tests: `bats test/`

### Project Layout Standard
```
.
├── bin/                 # Executable scripts/entrypoints (chmod +x, #!/usr/bin/env bash)
├── lib/                 # Reusable sourced modules/functions (no side effects on source)
├── test/                # Test suite
│   ├── test_helper/     # bats-support, bats-assert
│   └── *.bats           # BATS test files
├── .shellcheckrc        # ShellCheck rules configuration
├── Makefile             # make test, make lint, make fmt
└── README.md
```

### Key AI Invariants & Rules
1. **Strict Mode by Default**:
   - Every executable script must begin with `#!/usr/bin/env bash` followed immediately by:
     ```bash
     set -euo pipefail
     IFS=$'\n\t'
     ```
   - `-e`: Exit immediately on command failure.
   - `-u`: Treat unset variables as errors (prevents catastrophic bugs like `rm -rf "$UNSET_VAR/*"`).
   - `-o pipefail`: Return pipeline exit code from the rightmost command to exit with non-zero.
2. **Quoting & Expansion Safety**:
   - **Always** double-quote variable expansions (`"$var"`, `"${array[@]}"`) to prevent word splitting and globbing.
   - Use `$(...)` for command substitution; **never** use legacy backticks (`` `...` ``).
3. **Deterministic Script Location**:
   - Always resolve the script's directory portably before sourcing libraries:
     ```bash
     SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
     # shellcheck source=lib/utils.sh
     source "${SCRIPT_DIR}/../lib/utils.sh"
     ```
4. **Defensive Coding & Traps**:
   - Check tool existence before executing: `command -v jq >/dev/null 2>&1 || { echo "Error: jq required" >&2; exit 1; }`.
   - Use `trap cleanup EXIT INT TERM` for temporary files, locks, or child processes.
   - **Negative Constraint**: **NEVER** use `eval` or execute unsanitized string input as code.

### Curated Skills
* `shell-script-architecture`: Modular `bin/` + `lib/` layout, robust CLI argument parsing (`getopts`), usage/help generation (`--help`), and exit trap lifecycles.
* `shellcheck-remediation`: Analyzing and fixing common ShellCheck warnings (SC2086 unquoted variables, SC2155 masked return values, SC2046 unquoted command substitutions).
* `bats-testing`: Writing hermetic unit tests with `bats-core`, asserting exit status (`[ "$status" -eq 0 ]`), output assertions with `bats-assert`, and mocking external commands.




