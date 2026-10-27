# Marketplace API and event contract

This document defines the local application boundaries and the API behavior that the frontend and services rely on. The schemas below define the public migration contract; the executable reference is `scripts/acceptance.mjs`.

**Stack:** Node.js 22, NestJS, strict TypeScript, React/Vite, PostgreSQL and Kafka. Local and AWS dev have independent configuration, secrets and data.

## Service boundaries and routing

| Service       |   Port | Frontend route       | Responsibility                                        |
| ------------- | -----: | -------------------- | ----------------------------------------------------- |
| Identity      | `8181` | `/api/auth`          | Accounts, login, and current user                     |
| Catalog       | `8182` | `/api/providers`     | Public provider discovery and provider-owned profiles |
| Inquiries     | `8183` | `/api/inquiries`     | Client requests and provider decisions                |
| Notifications | `8184` | `/api/notifications` | Provider inbox and read state                         |

The production frontend serves through nginx on port `8180`; local Vite development uses port `5183`. Both proxy the listed API routes to the corresponding service. Each Nest service exposes `/health/live`, `/health/serve` (database-dependent serving health) and `/health/ready` (database plus messaging readiness where applicable); the frontend `/health` checks nginx. Management routes are not forwarded by nginx.

Each service owns a PostgreSQL database and a distinct database user on one local PostgreSQL server. Kafka carries the inquiry-created event to notifications. Services do not share domain tables.

## Authentication and demo identities

| Method | Path              | Result                                                                 |
| ------ | ----------------- | ---------------------------------------------------------------------- |
| `POST` | `/api/auth/login` | Accepts `{email, password}`; returns `{token, id, email, name, role}`. |
| `GET`  | `/api/auth/me`    | Returns the authenticated principal.                                   |

JWTs use HS256 and a shared `JWT_SECRET` of at least 32 bytes. The issuer and audience are both `marketplace`; the subject is the account email. The role claim is `PROVIDER` or `CLIENT`, enforced by verified actor role and domain ownership checks.

All demo accounts use password `DemoPass123!`:

| Email                   | Role       | Use                        |
| ----------------------- | ---------- | -------------------------- |
| `ava@demo.local`        | `PROVIDER` | Ava Martinez's profile     |
| `leo@demo.local`        | `PROVIDER` | Leo Chen's profile         |
| `company@demo.local`    | `CLIENT`   | Company inquiry journey    |
| `individual@demo.local` | `CLIENT`   | Individual inquiry journey |

Account IDs are stable email addresses. Provider IDs are stable slugs such as `ava-martinez` and `leo-chen`.

## Provider catalog

| Method | Path                  | Access and behavior                                          |
| ------ | --------------------- | ------------------------------------------------------------ |
| `GET`  | `/api/providers`      | Public search; returns `{items: Provider[], total: number}`. |
| `GET`  | `/api/providers/{id}` | Public provider profile.                                     |
| `GET`  | `/api/providers/me`   | `PROVIDER` only; returns the caller's profile.               |
| `PUT`  | `/api/providers/me`   | `PROVIDER` only; updates the caller's profile.               |

Search accepts `q`, `category`, `skill`, `maxRate`, `available`, `sort`, `page`, and `size`. The documented example uses `page=0&size=12`. Sort values are `recommended`, `rate-asc`, and `rating`. The `/me` route must be matched before the dynamic `/{id}` route.

```ts
type Provider = {
  id: string;
  name: string;
  headline: string;
  location: string;
  category: string;
  about: string;
  avatarUrl: string;
  coverColor: string;
  skills: string[];
  tools: string[];
  services: string[];
  experience: {
    title: string;
    company: string;
    period: string;
    description: string;
  }[];
  portfolio: { title: string; description: string; url: string }[];
  hourlyRate: number;
  currency: "USD";
  available: boolean;
  rating: number;
  reviewCount: number;
  completedProjects: number;
  responseTime: string;
};
```

The edit request accepts the same editable profile fields. The service takes ownership from the JWT and rejects an ID that belongs to another provider. Public profiles never expose the owner's email. The seeded catalog contains at least six detailed providers across Software Development, IT Consulting, Design, and Marketing.

## Inquiries and notifications

| Method  | Path                           | Access and behavior                                                             |
| ------- | ------------------------------ | ------------------------------------------------------------------------------- |
| `POST`  | `/api/inquiries`               | `CLIENT` only. Requires an `Idempotency-Key` header and the request body below. |
| `GET`   | `/api/inquiries`               | Authenticated participants see only their inquiries.                            |
| `PATCH` | `/api/inquiries/{id}/status`   | Target provider only; body selects `ACCEPTED` or `DECLINED`.                    |
| `GET`   | `/api/notifications`           | Authenticated recipient sees their inbox.                                       |
| `PATCH` | `/api/notifications/{id}/read` | Recipient only; marks that notification read.                                   |

```ts
type CreateInquiry = {
  providerId: string;
  subject: string;
  message: string;
  budget: number;
  clientType: "COMPANY" | "INDIVIDUAL";
};

type Inquiry = {
  id: string;
  providerId: string;
  providerName: string;
  clientName: string;
  subject: string;
  message: string;
  budget: number;
  clientType: "COMPANY" | "INDIVIDUAL";
  status: "PENDING" | "ACCEPTED" | "DECLINED";
  createdAt: string;
};

type Notification = {
  id: string;
  inquiryId: string;
  message: string;
  createdAt: string;
  read: boolean;
};
```

Before creating an inquiry, the inquiries service verifies the provider through catalog's internal HTTP route:

```text
GET /internal/providers/{id}
X-Internal-Key: <local internal key>
→ {id, ownerEmail, name}
```

The internal route is protected by `X-Internal-Key` and is not exposed through the frontend proxy. The recipient's email remains private service data.

Creating an inquiry saves the inquiry and an outbox record together. The outbox publisher sends `inquiry.created.v1` to Kafka; the event includes UUID `eventId` and `inquiryId` values plus the recipient provider email. Notifications consumes the event and uses unique event identity to avoid duplicate inbox records. `GET /api/notifications` returns notification objects with `id`, `inquiryId`, `message`, `createdAt`, and `read`.

## Errors and frontend data rules

Errors use JSON `{status, detail}`:

| Status | Meaning                                          |
| -----: | ------------------------------------------------ |
|  `400` | Invalid request or validation failure            |
|  `401` | Missing or invalid authentication                |
|  `403` | Wrong role or resource ownership                 |
|  `404` | Resource not found                               |
|  `409` | Conflict, including incompatible repeat requests |

The frontend shows success only after an API response. It may keep a token and comparison preference in `localStorage`; provider, inquiry, and notification data must come from APIs.

## Local configuration and acceptance

The local environment supplies `JWT_SECRET`, `INTERNAL_API_KEY`, `DB_URL` (service-specific URI), `KAFKA_BROKERS`, and `CATALOG_URL`. Each service receives its own database credentials. These are demo runtime values, not real user credentials.

Acceptance requires strict types, ESLint/Prettier, Jest/Vitest behavior tests, reproducible builds and all 48 real HTTP checks with zero failures. See [testing](docs/testing.md) and [results](docs/results.md). AWS execution is separately reported; prepared configuration is not a deployed environment.

## Selected ECS runtime adaptation

Public API/event payloads and all 48 acceptance checks remain unchanged. ECS uses field-based database settings with verified PostgreSQL TLS and a separate owned role/database per capability; local DB_URL remains supported. Kafka clients authenticate with separate SCRAM-SHA-512 identities over verified TLS. TLS-downgrading database URL settings are rejected. ECS health checks use `/health/serve` so a broker outage does not evict durable inquiry HTTP serving; `/health/ready` retains strict messaging diagnostics. Seed accounts require explicit demo activation. See [runtime/security/recovery boundaries](docs/aws-ecs-dev.md). These definitions and local checks do not establish cloud execution.
