---
name: nextjs-frontend-expert
description: Build production-grade frontend pages and components using Next.js 16+ App Router. Focus on layout, styling, performance, and scalability.
---

# Next.js 16+ Frontend Expert Skill

## Instructions

1. **Architecture (App Router)**
   - Use `/app` directory only
   - Route segments with `layout.tsx`, `page.tsx`, and `loading.tsx`
   - Server Components by default
   - Client Components only when required (`"use client"`)

2. **Pages & Routing**
   - File-based routing with nested layouts
   - Dynamic routes (`[slug]`, `[id]`)
   - Route groups for organization
   - Parallel and intercepting routes when needed

3. **Components**
   - Reusable, composable UI components
   - Clear separation:
     - `ui/` → atomic UI (Button, Card, Input)
     - `sections/` → page sections
     - `layouts/` → structural components
   - Minimal client-side state
   - Props-driven customization

4. **Layouts**
   - Shared layouts using `layout.tsx`
   - Persistent navigation and footer
   - Grid/Flex-based responsive systems
   - Slot-based composition

5. **Styling**
   - Tailwind CSS (preferred)
   - Design tokens via Tailwind config
   - Utility-first, no inline styles
   - Dark mode support
   - Consistent spacing & typography scale

6. **Data & Performance**
   - Server-side data fetching
   - Streaming with `Suspense`
   - Caching & revalidation
   - Avoid unnecessary client hydration

7. **UX & Accessibility**
   - Keyboard navigation support
   - Proper ARIA attributes
   - Focus states and contrast compliance
   - Skeleton loaders instead of spinners

## Best Practices
- Default to Server Components
- Keep Client Components small and isolated
- Avoid prop drilling — prefer composition
- No unnecessary libraries
- Follow atomic design principles
- Optimize for Core Web Vitals
- Production-ready folder structure

## Example Structure
```txt
app/
 ├─ layout.tsx
 ├─ page.tsx
 ├─ loading.tsx
 ├─ (dashboard)/
 │   ├─ layout.tsx
 │   └─ page.tsx
components/
 ├─ ui/
 │   ├─ button.tsx
 │   └─ card.tsx
 ├─ sections/
 │   └─ hero-section.tsx
lib/
 └─ utils.ts
