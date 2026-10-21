# React structure and data flow

The reference placed its application in one large entry file. This version extracts components into their own files and gives each layer a clear purpose. Open `frontend/src` and follow the actual imports rather than treating directory names as proof of separation.

| Directory | Responsibility | Avoid |
|---|---|---|
| `components` | Reusable rendering, forms, dialogs and layout | Direct ownership of unrelated page queries |
| `routes` | Compose the current page and coordinate journeys | Duplicating API request plumbing |
| `services` | Typed HTTP requests and response/error handling | Rendering UI or storing fake domain data |
| `types` | Shared API/domain contracts | Assuming compile-time types validate server JSON |
| `contexts` | Shared authentication state and actions | Global state for every small form value |
| `hooks` | Reusable queries, effects and state lifecycles | Effects that allow old results to overwrite a new query |

A search starts in controlled filter state, triggers a query effect, calls the API through a service and renders pending/results/empty/failure states. Abort superseded requests and ignore stale results. Profile editing sends the owned profile to the API and confirms success from the actual response. Inquiry submission uses one idempotency key per logical attempt so transport retries do not create duplicates.

Comparison is a UI preference over real catalog records. It may be stored locally; profiles and inquiry outcomes may not. Authentication context restores a token by verifying `/api/auth/me`; a browser role guard only affects navigation. The backend still checks every protected action.

Component tests should exercise behavior: an error is visible after a failed request, a stale query cannot replace current results, dialogs can close/focus correctly and the provider edit flow uses the right API. Full user journeys through nginx are a separate integration/browser layer. Responsive CSS alone does not prove mobile usability; inspect at 390px and navigate by keyboard.
