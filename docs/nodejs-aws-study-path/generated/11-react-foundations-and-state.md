---
title: "React tools: state, props, refs and controlled inputs"
topic: "React tools: state, props, refs and controlled inputs"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# React tools: state, props, refs and controlled inputs

Prerequisites: JavaScript functions and TypeScript. These are browser-side concepts, not backend Node APIs.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Component functions and render snapshots

**What:** A React component calculates UI from its current props and state. Each render has its own snapshot of those values.

**How:** useState remembers a value across renders. A setter schedules another render; it does not rewrite variables captured by an older callback.

**Real code:** [frontend/src/hooks/useMarketplace.ts · lines 7–10](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L7-L10).

```ts
const [providers, setProviders] = useState<Provider[]>([]);
const [total, setTotal] = useState(0);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");
```

**Watch for:** Calling a state setter during every render can cause a render loop.

### When does a state setter change the displayed value?

On a subsequent render, rather than by mutating the old render’s local variable.

## Props and callback contracts

**What:** Props are inputs supplied by a parent. Callback props let a child request a parent-owned action.

**How:** InquiryForm receives provider, auth, onClose and onSent. Their TypeScript shapes describe the interface, while actual authorization still belongs to the backend.

**Real code:** [frontend/src/components/inquiries/InquiryForm.tsx · lines 7–16](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/inquiries/InquiryForm.tsx#L7-L16).

```tsx
export function InquiryForm({
  provider,
  auth,
  onClose,
  onSent,
}: {
  provider: Provider;
  auth: Auth;
  onClose: () => void;
  onSent: () => void;
```

**Watch for:** Passing auth as a prop does not make browser data trustworthy to a server.

### Who owns the close action?

The parent supplies its behavior through onClose; the child calls it at the appropriate interaction.

## Controlled inputs and explicit conversion

**What:** A controlled input displays state through value and updates state through onChange.

**How:** The budget field stores text while editing, then Number converts it for submission. Empty text and numeric zero need deliberate handling rather than accidental truthiness.

**Real code:** [frontend/src/components/inquiries/InquiryForm.tsx · lines 42–44](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/inquiries/InquiryForm.tsx#L42-L44).

```tsx
  budget: Number(budget),
  clientType,
});
```

**Watch for:** Browser input limits improve feedback; callers can bypass them, so Zod must validate again.

### Why keep numeric input as text while editing?

An empty field or incomplete edit is not necessarily a valid final number.

## Immutable updates and identity

**What:** React state updates should supply the changed value rather than mutate an existing state array.

**How:** The comparison toggle removes an ID with filter or adds one with spread. Stable domain IDs also provide better list identity than changing array positions.

**Real code:** [frontend/src/hooks/useMarketplace.ts · lines 152–154](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L152-L154).

```ts
if (compare.includes(id)) setCompare(compare.filter((x) => x !== id));
else if (compare.length < 3) setCompare([...compare, id]);
else setToast("You can compare up to three professionals at a time.");
```

**Watch for:** Object spread is shallow; copy the nested structure you actually change.

### Why not compare.push(id) followed by the same array?

It mutates existing state and preserves its reference, which can defeat expected update behavior.

## Refs versus state

**What:** A ref retains a mutable value without scheduling a render. State is appropriate when a changed value should update the UI.

**How:** The inquiry hook uses inFlight to suppress overlapping submissions and busy to display progress. Neither browser mechanism replaces durable server idempotency.

**Real code:** [frontend/src/hooks/useInquiryAttempt.ts · lines 41–44](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useInquiryAttempt.ts#L41-L44).

```ts
const mounted = useRef(true);
const inFlight = useRef(false);
useEffect(() => {
  mounted.current = true;
```

**Watch for:** A ref is local to that mounted hook instance, not shared coordination between replicas.

### Why use both inFlight and busy?

The ref guards immediate re-entry; state drives visible loading behavior.

## Context and custom hooks

**What:** Context shares values with descendants. A custom hook packages reusable stateful behavior using React hooks.

**How:** AuthProvider supplies auth state, and useMarketplace/useInquiryAttempt organize separate concerns. Context is not a security boundary or a guarantee of zero rerenders.

**Real code:** [frontend/src/contexts/AuthContext.tsx · lines 48–50](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/contexts/AuthContext.tsx#L48-L50).

```tsx
<AuthContext.Provider value={{ auth, setAuth, restoring }}>
  {children}
</AuthContext.Provider>
```

**Watch for:** Keep hooks at valid top-level call positions; do not call them conditionally inside event handlers.

### Why does the app not require Redux for this?

Its existing state ownership, context and custom hooks implement the current behavior without that dependency.

## Practice and mastery

In a scratch component, queue `setCount(c => c + 1)` twice in one click handler. Expected increment: 2. Replace both with `setCount(count + 1)`; expected increment for that event: 1.

- Explain the queued updater values rather than memorizing the result.
- Add a practice-only available-provider count derived from the current array. Do not store a second count that must be synchronized with an effect.
- Run `npm --prefix frontend test -- src/routes/MarketplaceRoute.test.tsx` and explain which user-visible behavior its assertions protect.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [React state snapshots](https://react.dev/learn/state-as-a-snapshot)
- [React state structure](https://react.dev/learn/choosing-the-state-structure)
- [Project example: Component functions and render snapshots](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L7-L10)
- [Project example: Props and callback contracts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/inquiries/InquiryForm.tsx#L7-L16)
- [Project example: Controlled inputs and explicit conversion](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/inquiries/InquiryForm.tsx#L42-L44)
- [Project example: Immutable updates and identity](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L152-L154)
- [Project example: Refs versus state](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useInquiryAttempt.ts#L41-L44)
- [Project example: Context and custom hooks](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/contexts/AuthContext.tsx#L48-L50)
