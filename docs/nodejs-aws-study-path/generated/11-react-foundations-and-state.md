---
title: React components, state ownership and forms
topic: React
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# React describes a view of state

Prerequisites: 01–02; backend gates help connect the UI. A component is a function that receives props and returns a description of the interface. JSX is syntax for that description. A render should be pure: do not send an inquiry or mutate browser storage while calculating JSX. Event handlers perform user actions; effects synchronize with external systems.

## Explained state example

~~~tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => {
    setCount(c => c + 1);
    setCount(c => c + 1);
  }}>{count}</button>;
}
~~~

Import useState from react. Place this scratch component in a practice copy and render it temporarily. One click increments by two because each updater receives the queued previous value. Replacing both lines with setCount(count + 1) produces one increment for that event, because both capture the same render snapshot. A setter requests another render; it does not rewrite the old closure's count binding.

## Read the application's layers

frontend/src/main.tsx mounts the React root and auth provider. routes/MarketplaceRoute.tsx composes the screen; there is no React Router dependency. hooks/useMarketplace.ts owns discovery filters, selected provider, comparison IDs, dialogs and API-backed lists. components/discovery renders cards/search. components/inquiries/InquiryForm.tsx uses controlled form state and the useInquiryAttempt transport protocol. contexts/AuthContext.tsx shares identity; hooks/useAuth.ts accesses it. services own HTTP calls, types describe contracts and utils/presentation.ts handles formatting.

Props flow down; event callbacks request state changes up. Keep a single owner for shared state rather than synchronizing two independent copies with effects. Derived values such as a comparison count usually come from existing state. The large marketplace hook is understandable as the current implementation, but splitting responsibilities or using a reducer could become useful as transitions grow. That is a design proposal, not a claim the repository already uses Redux or useReducer.

Lists need stable domain keys so React preserves the intended component identity. Index keys can attach form state to the wrong item after sorting. Controlled fields use value and onChange; numeric input text must be parsed and validated intentionally, with empty input treated separately from zero. Avoid mutating arrays in state; use filter, map or a copied array.

## Executable lab

Run npm --prefix frontend test -- src/routes/MarketplaceRoute.test.tsx from the repository root. Then start the local UI, filter providers, open/close details, choose up to three comparisons and reload. Observe that comparison preference survives but catalog data is fetched again. The cap is implemented in toggleCompare and storage sanitization; it is not a business persistence rule.

Add a practice-only “available count” derived from the current providers array. Test no providers, one available provider and a filter change. Do not add an effect that stores the count as separate state. Use React DevTools to identify the state owner and explain why its children update. Restore exploratory changes after recording your result.

## Debugging and senior tradeoffs

An infinite render loop often comes from calling a setter unconditionally during render or an effect that changes its own unstable dependency. A stale event handler can read an older snapshot. Changing keys can reset local form state. Context is a sharing mechanism, not a security boundary and not a promise of zero rerenders. Profile before adding memoization; useCallback alone does not make a feature fast.

Interview:

### State versus props?

Props are inputs from a parent; state is a component's remembered data across renders.

### Why no domain data in localStorage?

The API/database is authoritative; cached or pending transport state needs explicit policy and cannot replace it. Here a pending inquiry payload does enter sessionStorage for recovery.

- [ ] Demonstrate snapshot versus functional state updates.
- [ ] Trace one form field and one click to their owner.
- [ ] Render a derived count without duplicate state.
- [ ] Explain actual storage behavior, route composition and list keys.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [React state as a snapshot](https://react.dev/learn/state-as-a-snapshot) — accessed 2026-10-22.
- [choosing state structure](https://react.dev/learn/choosing-the-state-structure) — accessed 2026-10-22.
- [Project source: frontend/src/main.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/main.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/routes/MarketplaceRoute.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/routes/MarketplaceRoute.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/hooks/useMarketplace.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/hooks/useMarketplace.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/components/inquiries/InquiryForm.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/components/inquiries/InquiryForm.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/types/marketplace.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/types/marketplace.ts) — local baseline inspected 2026-10-22; private published source may lag.
