---
title: "Testing tools: Jest, Vitest, mocks, types and browsers"
topic: "Testing tools: Jest, Vitest, mocks, types and browsers"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Testing tools: Jest, Vitest, mocks, types and browsers

Prerequisites: a service method and an effect you can explain. Choose the test tool from the evidence needed.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Jest spies isolate a service rule

**What:** A spy records calls; a mock supplies controlled behavior instead of a real dependency.

**How:** The backend tests inject a fake Database and inspect SQL-call intent. This is useful for ownership and retry branches, but cannot establish real PostgreSQL locking.

**Real code:** [backend/test/workflows.spec.ts · lines 43–51](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/test/workflows.spec.ts#L43-L51).

```ts
function database(rows: unknown[] = []) {
  const query = jest.fn<(...args: any[]) => Promise<any>>().mockResolvedValue({ rows });
  const db = {
    query,
    transaction: jest.fn(async (fn: (tx: { query: typeof query }) => Promise<unknown>) =>
      fn({ query }),
    ),
  };
  return { query, db: db as unknown as Database };
```

**Watch for:** A mock that repeats the implementation’s assumptions can pass while integration is broken.

### What does the duplicate test prove?

That this service path returns the previous result without issuing another insert against its fake database.

## Vitest and controllable promises

**What:** Vitest runs frontend tests; Testing Library drives components or hooks from their public behavior.

**How:** The hook test saves a promise resolver, changes the search, then resolves the older response last. The schedule is deterministic rather than dependent on network luck.

**Real code:** [frontend/src/hooks/useMarketplace.test.tsx · lines 13–20](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.test.tsx#L13-L20).

```tsx
let resolveFirst!: (value: Response) => void;
vi.stubGlobal(
  "fetch",
  vi
    .fn()
    .mockImplementationOnce(
      () =>
        new Promise<Response>((resolve) => {
```

**Watch for:** jsdom simulates DOM APIs; it does not reproduce every real browser layout or network behavior.

### Why avoid timing sleeps for the race test?

Explicit promise control reproduces the failing schedule reliably.

## TypeScript transformation and ESM

**What:** A test runner must execute JavaScript even when test sources are TypeScript.

**How:** ts-jest transforms backend tests; the ESM preset and .js-to-source mapper match the backend module convention. @types packages help compilation without changing runtime assertions.

**Real code:** [backend/package.json · lines 51–58](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L51-L58).

```json
"preset": "ts-jest/presets/default-esm",
"testEnvironment": "node",
"testMatch": [
  "<rootDir>/test/**/*.spec.ts"
],
"collectCoverageFrom": [
  "src/**/*.ts",
  "!src/main.ts"
```

**Watch for:** Changing test transforms can hide module-configuration problems rather than fix production loading.

### Why do tests need a mapper for .js suffixes?

Source imports name runtime output paths while the runner executes TypeScript source.

## Lint, format, typecheck and behavior

**What:** ESLint detects configured code issues; Prettier formats text; TypeScript checks types; tests assert behavior.

**How:** The project’s check script combines three different kinds of evidence. Passing it does not prove a database invariant or a user journey.

**Real code:** [backend/package.json · lines 18–23](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L18-L23).

```json
  "check": "npm run typecheck && npm run lint && npm run format:check",
  "lint": "eslint src test scripts eslint.config.js",
  "format": "prettier --write src test scripts eslint.config.js package.json tsconfig.json .prettierrc.json",
  "format:check": "prettier --check src test scripts eslint.config.js package.json tsconfig.json .prettierrc.json"
},
"dependencies": {
```

**Watch for:** Coverage measures executed code under the collected scope; it is not a direct correctness percentage.

### Can well-formatted code still be insecure?

Yes. Formatting and lint success do not establish authorization or safe failure behavior.

## Playwright exercises a real browser

**What:** Playwright drives a browser page, finds controls and waits for observable UI conditions.

**How:** The smoke script visits the running application and sends an inquiry. Its evidence differs from a component mock: the UI, proxy and real services participate.

**Real code:** [scripts/browser-smoke.mjs · lines 12–15](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/scripts/browser-smoke.mjs#L12-L15).

```js
await page.goto(base);await page.locator('.provider-card').first().waitFor();
assert.ok(await page.locator('.provider-card').count()>=6);
assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
await page.screenshot({path:`docs/evidence/browser/${name}-discovery.png`,fullPage:true});
```

**Watch for:** A passing happy path does not cover every retry or crash schedule.

### What should a locator wait for?

A meaningful visible or network condition, rather than an arbitrary fixed delay.

## Practice and mastery

- Run one backend file and one frontend file. Explain the inputs, dependency doubles and assertions before reading PASS.
- Break a real ownership or stale-response rule in a practice copy. Confirm a meaningful existing test fails, then restore the rule.
- Describe which extra real-database test is needed to prove advisory locking.
- Use the local breakpoint launcher for diagnosis; do not treat every failure as a reason to reinstall packages.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Jest mocks](https://jestjs.io/docs/mock-functions)
- [Vitest mocks](https://vitest.dev/guide/mocking.html)
- [Testing Library principles](https://testing-library.com/docs/guiding-principles/)
- [Project example: Jest spies isolate a service rule](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/test/workflows.spec.ts#L43-L51)
- [Project example: Vitest and controllable promises](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.test.tsx#L13-L20)
- [Project example: TypeScript transformation and ESM](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L51-L58)
- [Project example: Lint, format, typecheck and behavior](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L18-L23)
- [Project example: Playwright exercises a real browser](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/scripts/browser-smoke.mjs#L12-L15)
