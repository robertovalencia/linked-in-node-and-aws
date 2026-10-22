---
title: "NestJS tools: decorators, injection and lifecycle"
topic: "NestJS tools: decorators, injection and lifecycle"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# NestJS tools: decorators, injection and lifecycle

Prerequisites: JavaScript classes, TypeScript types, promises. Used by all four services.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Decorators attach metadata

**What:** A decorator is a function applied to a class or member. Nest reads its metadata to discover routes and providers.

**How:** `@Controller`, `@Get` and `@Injectable` describe different roles. `reflect-metadata` supports metadata storage; TypeScript emits constructor type metadata for dependency resolution.

**Real code:** [backend/src/main.ts · lines 1–3](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L1-L3).

```ts
import 'reflect-metadata';
import { Module, Type } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
```

**Watch for:** Importing a class does not register it as a provider.

### Does @Injectable create a database connection?

No. It marks a class for Nest; its constructor or initialization code creates resources.

## The dependency-injection container

**What:** Dependency injection supplies a class with the objects it needs. The container is Nest’s registry of those objects.

**How:** The module lists provider classes. Nest resolves constructor parameters and normally reuses one provider instance per application context; this is not one instance shared between separate Node processes.

**Real code:** [backend/src/main.ts · lines 36–40](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L36-L40).

```ts
@Module({
  controllers: [HealthController, controllers[service]],
  providers: [Database, AuthGuard, WorkerHealth, ...providers[service]],
})
class ApplicationModule {}
```

**Watch for:** An interface is erased at runtime; injecting an interface requires an explicit runtime token.

### What happens when Database is missing from providers?

TypeScript may compile, but Nest cannot resolve the constructor dependency at startup.

## Constructor parameter properties

**What:** `constructor(private readonly db: Database)` declares a parameter and stores it as a field.

**How:** `private` restricts TypeScript access. `readonly` prevents rebinding the field. Neither makes the pool or database contents immutable.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 13–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L13-L13).

```ts
constructor(private readonly db: Database) {}
```

**Watch for:** A readonly field can still reference a mutable object.

### Who supplies db?

Nest resolves the registered Database provider and passes that object to the constructor.

## Lifecycle hooks and awaited setup

**What:** A lifecycle hook is a method Nest calls at a defined initialization or shutdown stage.

**How:** `onModuleInit` applies migrations. Identity’s `onApplicationBootstrap` awaits its dummy hash and optional seed. A returned promise delays that lifecycle stage until it settles.

**Real code:** [backend/src/identity/identity.service.ts · lines 11–14](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L11-L14).

```ts
async onApplicationBootstrap(): Promise<void> {
  this.dummyHash = await hashPassword('dummy-password-never-used');
  if (process.env.SEED_DEMO !== 'true') return;
  const providers: { ownerEmail: string; name: string }[] = JSON.parse(
```

**Watch for:** Do not assume unrelated providers initialize in their array order.

### Why is the dummy hash ready before login requests?

The bootstrap hook awaits hash creation before application initialization finishes.

## Middleware: Helmet and the JSON parser

**What:** Middleware runs around the HTTP request before a controller handles it.

**How:** Helmet sets security-related response headers. Express `json` converts JSON bytes into a JavaScript value and limits body size to 128kb; it does not validate business fields.

**Real code:** [backend/src/main.ts · lines 45–47](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L45-L47).

```ts
app.use(helmet());
app.use(json({ limit: '128kb' }));
app.useGlobalFilters(new ErrorFilter());
```

**Watch for:** Header hardening, JSON parsing and Zod validation solve separate problems.

### Does Helmet validate an inquiry budget?

No. inquirySchema performs that runtime validation.

## Guards and exception filters

**What:** A guard decides whether execution may reach a route. A filter turns thrown errors into HTTP responses.

**How:** AuthGuard verifies a token and attaches an actor. ErrorFilter maps known errors, maps Zod errors to 400, and masks unexpected 500 details.

**Real code:** [backend/src/common/errors.ts · lines 16–22](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/errors.ts#L16-L22).

```ts
const status =
  error instanceof ZodError
    ? 400
    : error instanceof HttpException
      ? error.getStatus()
      : (parserStatus ?? 500);
let detail =
```

**Watch for:** Passing a guard does not establish ownership of a particular row.

### Why handle error as unknown?

Thrown values need runtime checks before reading properties or selecting an error response.

## RxJS: installed versus used

**What:** RxJS provides Observables: lazy streams that can emit several values and support unsubscription.

**How:** It is installed for the Nest ecosystem here. Application services use promises and KafkaJS callbacks; they do not implement custom Observable pipelines.

**Real code:** [backend/package.json · lines 32–32](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L32-L32).

```json
"rxjs": "^7.8.2",
```

**Watch for:** A package in package.json is not evidence of an application-level reactive design.

### Promise or Observable for this code?

Describe the actual Promise-returning service methods first; Observable operators would be an extension.

## Practice and mastery

- Explain one decorator, one injected constructor and one lifecycle hook without describing the marketplace workflow.
- In a practice copy, remove `Database` from module providers. Build, observe the runtime injection error, then restore it.
- Read `ErrorFilter`: predict the status for a Zod error and an unexpected Error. Expected: 400 and masked 500.
- Name one singleton limitation: state in one process is not shared with another replica.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Nest providers](https://docs.nestjs.com/providers)
- [Nest lifecycle](https://docs.nestjs.com/fundamentals/lifecycle-events)
- [Project example: Decorators attach metadata](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L1-L3)
- [Project example: The dependency-injection container](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L36-L40)
- [Project example: Constructor parameter properties](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L13-L13)
- [Project example: Lifecycle hooks and awaited setup](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L11-L14)
- [Project example: Middleware: Helmet and the JSON parser](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L45-L47)
- [Project example: Guards and exception filters](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/errors.ts#L16-L22)
- [Project example: RxJS: installed versus used](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L32-L32)
