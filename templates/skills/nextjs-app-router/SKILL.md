---
name: nextjs-app-router
description: Deep runbook for Next.js 15+ App Router, Server Actions, RSC boundaries, and revalidation.
author: "PatrickJS <patrick@cursor.directory>, customized by innerpeace080"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/PatrickJS/awesome-cursorrules"
  upstream_file: "rules/nextjs.mdc"
  source_type: "community-curated"
  lineage: "forked-and-customized"
  last_upstream_sync: "2026-09-26T23:30:00Z"
  customizations:
    - "Enforced Zod schema validation on all Server Actions"
    - "React 19 Server/Client component boundary rules"
---

# Next.js App Router Runbook

## When to Use
Use this skill when designing, building, or refactoring routes, layouts, server actions, or data fetching in Next.js 15+ applications.

---

## 1. Server Component vs Client Component Rules
- **Server Components (Default)**: Use for data fetching, backend security, accessing database/tokens directly.
- **Client Components (`'use client'`)**: Push to leaf nodes. Only use when:
  - Using event listeners (`onClick`, `onChange`).
  - Using React state hooks (`useState`, `useReducer`, `useEffect`).
  - Using browser APIs (`window`, `localStorage`).

---

## 2. Server Actions Architecture
Place mutations in dedicated action files (e.g. `app/actions/user.ts`):

```typescript
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

export type ActionState = {
  success: boolean;
  message?: string;
  errors?: Record<string, string[]>;
};

export async function createUser(prevState: ActionState, formData: FormData): Promise<ActionState> {
  const validated = CreateUserSchema.safeParse({
    email: formData.get('email'),
    name: formData.get('name'),
  });

  if (!validated.success) {
    return {
      success: false,
      errors: validated.error.flatten().fieldErrors,
    };
  }

  // Execute database operation
  // await db.user.create({ data: validated.data });

  revalidatePath('/users');
  return { success: true, message: 'User created successfully.' };
}
```

---

## 3. Best Practices & Anti-Patterns
- **DO**: Use `loading.tsx` and `error.tsx` for granular route segment fallbacks.
- **DO**: Use `revalidatePath` or `revalidateTag` after data mutations.
- **DON'T**: Fetch data in client components with `useEffect` (causes waterfalls).
- **DON'T**: Pass sensitive secrets as props to Client Components.

