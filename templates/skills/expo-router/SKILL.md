---
name: expo-router
description: File-based navigation patterns, typed routing, modal stacks, and deep link configuration in Expo React Native.
author: "Expo Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/expo/expo/tree/main/packages/expo-router"
  upstream_file: "README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Strict typed routes integration"
    - "Folder group separation for auth, tabs, modals"
---

# Expo Router Runbook

## When to Use
Use this skill when implementing or modifying screens, navigation stacks, tabs, modals, deep linking, and route parameters in Expo React Native applications.

---

## 1. Directory Layout & Route Groups

Use parenthesis `(group)` to group navigation features without creating additional path segments in URLs:

```text
app/
├── _layout.tsx           # Global Providers & Root Stack Navigator
├── (auth)/               # Auth flow (login, signup, onboarding)
│   ├── _layout.tsx       # Auth stack options
│   ├── login.tsx
│   └── register.tsx
├── (tabs)/               # Main bottom-tab application
│   ├── _layout.tsx       # Tabs navigator definition
│   ├── index.tsx         # Home tab
│   └── settings.tsx      # Settings tab
├── (modals)/             # Sliding modals
│   └── filter.tsx
└── [id].tsx              # Dynamic detail route
```

---

## 2. Root Navigator (`app/_layout.tsx`)

Always wrap the application with necessary context providers and define the root stack:

```typescript
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <StatusBar style="auto" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        <Stack.Screen
          name="(modals)/filter"
          options={{ presentation: 'modal', headerShown: true, title: 'Filters' }}
        />
      </Stack>
    </SafeAreaProvider>
  );
}
```

---

## 3. Strongly Typed Routing & Search Params

- **Type-safe Navigation**: Use `<Link href="/(tabs)/settings" />` or `router.push('/(tabs)/settings')`.
- **Dynamic Search Params**: Always parse and type search parameters explicitly:
  ```typescript
  import { useLocalSearchParams } from 'expo-router';

  type ProductParams = {
    id: string;
    referrer?: string;
  };

  export default function ProductDetailScreen() {
    const { id, referrer } = useLocalSearchParams<ProductParams>();
    // ...
  }
  ```

---

## 4. Best Practices & Rules
- **Keep Screen Files Thin**: Delegate business logic, API calls, and custom hooks to `hooks/` and reusable UI to `components/`.
- **Static Header Configuration**: Configure headers in `_layout.tsx` via `<Stack.Screen options={{ title: '...' }} />` instead of runtime updates inside page components.
- **Back Button Safety**: Handle hardware back button behavior cleanly across nested navigators using `router.back()` or `router.canGoBack()`.

