---
title: NestJS bootstrap and the four-process dependency graph
topic: NestJS
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# How Nest wires this application

Prerequisites: 01–04. Dependency injection means a class declares what it needs and the framework supplies registered instances. It lets a controller ask for a service and a service ask for Database without manually constructing a new connection pool for every request.

## Read bootstrap in execution order

Open backend/src/main.ts. First reflect-metadata is loaded. bootstrap validates configuration, gets SERVICE and chooses entries from controller/provider lookup tables. A locally declared @Module registers HealthController, exactly one capability controller, Database, AuthGuard, WorkerHealth, and the providers required by that capability. NestFactory builds the application graph. Middleware, global error mapping and shutdown hooks are installed before listen.

The source package imports all four capabilities, but each running process registers only its selected capability. This is a module class assembled at bootstrap; it is not four listeners inside one Node process and is not an example of a DynamicModule.register API. Four containers can use one image because SERVICE and DB_URL vary per container.

| SERVICE | Controller | Capability providers | Extra runtime work |
|---|---|---|---|
| identity | IdentityController | IdentityService | Optional accounts seed and dummy password hash |
| catalog | CatalogController | CatalogService | Optional provider seed |
| inquiries | InquiriesController | InquiriesService, OutboxPublisher | Poll persisted outbox and publish |
| notifications | NotificationsController | NotificationsService, InquiryConsumer | Subscribe and persist notifications |

Database is an injectable provider whose onModuleInit applies the selected service's migrations. Identity/Catalog seed in onApplicationBootstrap when SEED_DEMO=true. Workers start in that bootstrap phase but their run loops continue asynchronously. WorkerHealth distinguishes an HTTP listener being alive from a worker being ready. Nest awaits relevant initialization hooks, but you should not infer exact ordering between unrelated providers beyond documented lifecycle guarantees and actual dependencies.

## Trace a request

For GET /api/inquiries, the controller-level AuthGuard extracts and verifies a bearer token, writes actor to the request, then the controller passes that actor into InquiriesService.list. The service restricts SQL by actor.email; Database delegates to pg.Pool; the returned rows are mapped into the API view. A thrown error travels to the global ErrorFilter. Authorization remains in business services for operations such as create/respond, so the framework decorator alone is not the business policy.

## Runnable lab

First inspect npm scripts and docs/local-setup.md. In a configured local practice environment run npm run up from the repository root, then:

~~~bash
curl -i http://127.0.0.1:8181/health/live
curl -i http://127.0.0.1:8182/health/ready
curl -i http://127.0.0.1:8183/api/inquiries
~~~

Expect live 200, ready 200 when its dependencies initialize, and unauthenticated inquiries 401. Direct local backend ports are for the lab; edge management routing differs. Record actual readiness rather than assuming startup means healthy. Run npm run down when finished. No cloud scripts are involved.

In a practice branch remove Database from the providers array, run the backend build and start a configured service. Explain why typechecking can succeed while Nest reports unresolved dependencies at runtime. Restore it immediately. Draw constructor arrows: NotificationsController → NotificationsService → Database, plus InquiryConsumer → NotificationsService and WorkerHealth.

## Senior tradeoffs

Shared infrastructure code reduces duplication while distinct processes retain deployment and data ownership. It also couples all capabilities to the shared image/build version. A modular monolith might lower operational cost for a small team. Request-scoped providers have different lifecycle/cost implications; these providers are ordinary singleton instances per application context. Creating globals or service locators to hide missing registrations makes testing and ownership harder.

Interview:

### Where are the four applications?

In four independent processes selecting SERVICE.

### Who constructs Database?

Nest resolves the registered injectable and passes it through constructors.

### Does the controller enforce all ownership?

No; inspect each service's explicit actor/owner checks.

- [ ] Draw all four provider graphs and name their ports.
- [ ] Explain migration versus seeding versus worker startup.
- [ ] Demonstrate a dependency-resolution failure and repair.
- [ ] Trace one authenticated request through guard, controller, service and SQL.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Nest providers](https://docs.nestjs.com/providers) — accessed 2026-10-22.
- [lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events) — accessed 2026-10-22.
- [Project source: backend/src/main.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/main.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/database.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/database.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/health.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/health.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/inquiries/inquiries.controller.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiries.controller.ts) — local baseline inspected 2026-10-22; private published source may lag.
