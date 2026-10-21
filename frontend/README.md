# Expertly frontend

React 19 and TypeScript UI, migrated from the reference marketplace while retaining its CSS, image credits, responsive layout, and user journeys. The backend API contract stays unchanged.

From this directory:

```sh
npm ci
npm run dev       # http://localhost:5183; backend ports 8181–8184
npm test          # rendered journeys, service failures, request race regressions
npm run lint
npm run format:check
npm run build
```

The root project's local setup starts PostgreSQL, runs migrations/seeds, and starts the NestJS services. No AWS credentials are required for frontend development. Vite proxies `/api/auth`, `/api/providers`, `/api/inquiries`, and `/api/notifications` to the corresponding local services. Set `VITE_PROXY_HOST` when dependencies live on a different host, or override each URL with `IDENTITY_PROXY_URL`, `CATALOG_PROXY_URL`, `INQUIRIES_PROXY_URL`, and `NOTIFICATIONS_PROXY_URL`. These are Vite server settings, not browser secrets. Root Docker Compose serves the production bundle through nginx on port 8180.

`src/routes/MarketplaceRoute.tsx` composes the screen and dialogs. `components/` groups small UI files by feature; every named component has its own file. `hooks/useMarketplace.ts` coordinates discovery, selection, and dialog state; it cancels superseded requests and prevents late responses from reopening closed profiles. `contexts/AuthContext.tsx` restores the token with server validation; `hooks/useAuth.ts` provides access. `services/marketplace.ts` owns typed API operations, and `services/http.ts` handles headers, server errors, and empty responses. `types/marketplace.ts` defines shared contracts; `utils/presentation.ts` holds display formatting and categories.

The CRUD path is UI event → hook or form state → typed service → HTTP API → NestJS → PostgreSQL → response → React state. The provider editor preserves experience and portfolio collections and submits the full profile. An inquiry uses one idempotency key across retries. Providers accept or decline pending inquiries in their workspace; notifications link into it. Authentication and comparison persistence use `expertly-node-aws-*` keys so this independent project never changes the original project's browser state.

Local demo accounts: `company@demo.local`, `individual@demo.local`, `ava@demo.local`, `leo@demo.local`; password `DemoPass123!`. These are deliberate local demonstration credentials. AWS dev setup must follow the root deployment guide's secret and seed configuration.

Tests use mocked HTTP responses to verify UI behavior deterministically; root acceptance tests verify the running backend and actual persistence. Passing frontend tests alone does not prove AWS deployment or visual parity. See the root documentation for architecture, environments, security, and interview walkthroughs.

An inquiry's pending idempotency key and canonical payload are saved together in this tab's `sessionStorage`. An uncertain response freezes the details, including after closing/reopening or refreshing the page. **Retry original inquiry** replays that exact attempt. **Resolve saved inquiry** replays the saved key and payload through the server's idempotency endpoint; only that authoritative response can clear the attempt. An older inquiry with identical content cannot establish delivery of the current attempt. A definite validation/authorization rejection on the first transmission unlocks correction as a new logical attempt. After an uncertain response, a rejected retry never clears the saved attempt: the original may already have committed before that later rejection. This temporary browser storage contains the inquiry text; signing out or closing the tab should be considered when using a shared device.

The production nginx config uses Docker's embedded resolver and shared upstream zones so service DNS is refreshed after container replacement. Verify a restart drill through the edge URL (not only direct service health) before declaring deployment healthy.
