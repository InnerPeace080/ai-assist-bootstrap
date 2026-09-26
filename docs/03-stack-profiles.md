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

