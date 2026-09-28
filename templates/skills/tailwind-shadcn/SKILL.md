---
name: tailwind-shadcn
description: Standardized procedure for building accessible, composable UI components with Tailwind CSS and Radix/shadcn primitives.
author: "shadcn community, customized by innerpeace080"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/shadcn-ui/ui"
  source_type: "community-curated"
  lineage: "forked-and-customized"
  last_upstream_sync: "2026-09-26T23:30:00Z"
---

# Tailwind CSS & shadcn/ui Component Runbook

## When to Use
Activate this skill when creating, styling, or refactoring UI components in web projects using Tailwind and Radix/shadcn primitives.

---

## 1. Class Merging Utility (`cn`)
Always wrap class names using the canonical `cn()` helper (`clsx` + `tailwind-merge`):

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## 2. Component Variant Structure (`cva`)
Use `class-variance-authority` for robust component state and variant mapping:

```typescript
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);
```

---

## 3. Accessibility Standards
- All interactive controls must support full keyboard navigation (`Tab`, `Enter`, `Space`, `Escape`).
- Ensure accessible contrast ratios (minimum 4.5:1 for normal text).
- Use Radix UI primitives (`@radix-ui/react-*`) for complex accessible dialogs, dropdowns, and popovers.

