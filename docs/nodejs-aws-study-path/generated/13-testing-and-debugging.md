---
title: Tests, debugging and quality evidence
topic: Testing
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Prove behavior at the right boundary

Prerequisites: 01–12. A test is useful when it detects a meaningful broken promise. Formatting checks, typechecking, unit tests, real SQL/concurrency tests and browser tests answer different questions. A green unit test cannot prove a broker delivered a message, and a screenshot cannot prove an inquiry survived a restart.

## The project's test layers

backend/test uses Jest with ts-jest's ESM preset, experimental VM modules and a .js-to-source mapper. Fakes isolate services and cover validation, roles, mapping and error paths. frontend uses Vitest, jsdom, React Testing Library, user-event, jest-dom assertions and V8 coverage. Root scripts/acceptance.mjs performs real HTTP checks against a running local application. scripts/browser-smoke.mjs uses Playwright against the browser. scripts/failure-drill.mjs exercises a controlled local outage.

Read a test before running it. Identify arrange, act, assert, the boundary being faked, and a plausible implementation bug it would catch. Avoid tests that merely assert that a mock was called with the same literal already copied from the implementation. Authorization, duplicate retries, outbox recovery, form uncertainty and focus restoration deserve behavioral assertions.

## Executable validation ladder

From the repository root with dependencies installed using the separate backend/frontend lockfiles:

~~~bash
npm run check
npm test
npm run build
~~~

Expected outcome: zero exit status for each command, with actual test counts and any warnings recorded. check runs lint/format/typechecking; it is not application execution. Build creates compiled artifacts. Then start the isolated local application using npm run up and run npm run acceptance. Install the declared browser runtime as needed with npx playwright install chromium before npm run test:browser. These integration steps need Docker and a running edge on port 8180. Preserve failures when they explain a repair; do not claim a run occurred from reading results.md.

## Red-to-green debugging exercise

In a practice copy add a deterministic test for replaying an inquiry with a changed body under the same client/key. It should expect ConflictException/409 and no second insert. Temporarily remove the fingerprint mismatch branch to prove the test fails, then restore the behavior and show it passes. Separately simulate delayed old/new provider responses in a frontend hook test; assert newest query wins. Do not use real-time sleeps when controlled promise resolution can make the case deterministic.

When a test fails, classify it: assertion failure, invalid test fixture, ESM transform/configuration, port collision, missing dependencies or real application behavior. Read the complete stack and first relevant application frame. Set a breakpoint in source using the repository's VS Code configuration or loopback inspector; inspect actor, transaction client and parsed input. Never log tokens or full runtime secrets to diagnose a 401.

## Coverage and tooling interpretation

Coverage shows which instrumented statements/branches were exercised, not whether assertions are correct. main.ts is excluded from backend collected coverage, so do not imply it was fully tested by that percentage. ESLint detects selected code patterns; Prettier enforces formatting; tsc checks static types; npm audit/Dependabot report dependency risks; Sonar analyzes configured code and quality rules. Each has false positives, scope limits and policy choices. Backend ESLint and frontend ESLint major versions differ by package; do not homogenize versions without compatibility work.

## Senior interview answers



### What do you mock?

Isolate pure business decisions and external failure branches, then use real integration tests for SQL locks, transactions, Kafka offsets and proxy routing.

### How do you validate AI code?

Review the invariant, write meaningful negative/failure tests, inspect the diff, execute relevant checks and keep evidence tied to the requirement. Test-generated-by-AI is not independently verified merely because it agrees with generated code.

- [ ] Name the promise each selected test proves and what it cannot prove.
- [ ] Demonstrate a real regression test failing then passing.
- [ ] Trace a failure through browser/network/backend/SQL boundaries.
- [ ] Record commands, output, actual coverage scope and unresolved limits.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Jest ESM](https://jestjs.io/docs/ecmascript-modules) — accessed 2026-10-22.
- [Vitest](https://vitest.dev/guide/) — accessed 2026-10-22.
- [Testing Library guiding principles](https://testing-library.com/docs/guiding-principles/) — accessed 2026-10-22.
- [Playwright](https://playwright.dev/docs/intro) — accessed 2026-10-22.
- [Project source: backend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/test/workflows.spec.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/test/workflows.spec.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/hooks/useMarketplace.test.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/hooks/useMarketplace.test.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/acceptance.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/acceptance.mjs) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/browser-smoke.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/browser-smoke.mjs) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/testing.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/testing.md) — local baseline inspected 2026-10-22; private published source may lag.
