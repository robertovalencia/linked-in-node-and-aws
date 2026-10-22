---
title: "TypeScript: erased types, narrowing, generics and ESM"
topic: "TypeScript: erased types, narrowing, generics and ESM"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# TypeScript: erased types, narrowing, generics and ESM

Prerequisite: lesson 01. Keep compile-time checking separate from runtime behavior.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## unknown versus any

**What:** `unknown` requires checks before you use a value. `any` disables useful checking at that boundary.

**How:** Catalog accepts unknown input and calls a Zod schema. An assertion such as `as Provider` would only tell the compiler to trust the programmer.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 48–50](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L48-L50).

```ts
async update(email: string, input: unknown): Promise<Provider> {
  const updated = providerSchema.parse(input);
  return this.db.transaction(async (client) => {
```

**Watch for:** A successful build does not prove JSON received from another process matches a type.

### What changes when TypeScript compiles unknown?

The type is erased; runtime validation remains ordinary executable JavaScript.

## Literal unions and as const

**What:** A union lists permitted type alternatives. `as const` preserves literal values instead of widening them to general strings.

**How:** The SERVICES tuple supplies the ServiceName union through indexed access. The runtime includes check is still needed because environment variables are untrusted text.

**Real code:** [backend/src/common/config.ts · lines 1–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/config.ts#L1-L7).

```ts
export const SERVICES = ['identity', 'catalog', 'inquiries', 'notifications'] as const;
export type ServiceName = (typeof SERVICES)[number];
export function serviceName(): ServiceName {
  const value = process.env.SERVICE;
  if (!SERVICES.includes(value as ServiceName))
    throw new Error('SERVICE must be identity, catalog, inquiries, or notifications');
  return value as ServiceName;
```

**Watch for:** A type assertion in serviceName does not itself validate process.env.

### Why keep includes when ServiceName already exists?

The environment value arrives at runtime and can be any string.

## Generic functions describe relationships

**What:** A generic parameter carries a type relationship through a function. It does not automatically supply a decoder.

**How:** api<T> promises a T to TypeScript callers, then returns parsed JSON. A runtime response schema would be a deliberate extension to this helper.

**Real code:** [frontend/src/services/http.ts · lines 11–15](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/services/http.ts#L11-L15).

```ts
export async function api<T>(
  path: string,
  auth: Auth | null = null,
  options: RequestInit = {},
): Promise<T> {
```

**Watch for:** A generic result can still contain incorrect runtime fields.

### Does api<Provider> reject an unexpected server payload?

No. The current helper parses JSON and relies on the expected contract.

## Types, interfaces and runtime tokens

**What:** Object types and interfaces describe structure and disappear during compilation. Classes can also exist as runtime constructor values.

**How:** Nest uses the Database class as a runtime dependency token. A plain interface would need an explicit token and matching provider registration.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 13–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L13-L13).

```ts
constructor(private readonly db: Database) {}
```

**Watch for:** private and readonly are compile-time restrictions, not database permissions.

### Why can a class type help Nest where an interface cannot?

The class has a runtime value that emitted metadata can reference.

## ES modules and emitted file paths

**What:** An ES module uses import/export. Node decides module interpretation using file extensions and package configuration.

**How:** The backend uses NodeNext and local .js import suffixes because emitted files run as JavaScript. Vite handles frontend module bundling separately.

**Real code:** [backend/src/common/database.ts · lines 6–6](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L6-L6).

```ts
import { serviceName, required } from './config.js';
```

**Watch for:** Do not paste CommonJS require into an ES module without understanding the different loading model.

### Why import config.js from a TypeScript file?

The runtime output file is JavaScript; the compiler resolves the corresponding TypeScript source.

## Decorator metadata is a compiler/runtime agreement

**What:** The backend enables strict checking and the legacy decorator metadata options used by this Nest setup.

**How:** The compiler emits information Nest uses for constructor injection. Changing decorator modes is not just a formatting change; it can change dependency resolution.

**Real code:** [backend/tsconfig.json · lines 10–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/tsconfig.json#L10-L13).

```json
"emitDecoratorMetadata": true,
"experimentalDecorators": true,
"skipLibCheck": true,
"resolveJsonModule": true,
```

**Watch for:** Declaration packages such as @types/pg add type information, not runtime validation or executable pg code.

### Why inspect tsconfig when Nest injection fails?

The emitted runtime metadata depends on compiler configuration as well as provider registration.

## Practice and mastery

In a temporary backend source file, define:

```ts
type Result = { ok: true; id: string } | { ok: false; reason: string };
function describe(result: Result): string {
  return result.ok ? result.id : result.reason;
}
```

Run `npm --prefix backend run typecheck`. Access `result.reason` before narrowing and observe the compiler error; then repair it and remove the scratch file.

- Explain `unknown`, `as`, `z.infer` and a runtime class token separately.
- Inspect emitted imports after a build. Do not change the project’s module settings merely to copy a tutorial.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [TypeScript modules](https://www.typescriptlang.org/docs/handbook/2/modules.html)
- [Project example: unknown versus any](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L48-L50)
- [Project example: Literal unions and as const](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/config.ts#L1-L7)
- [Project example: Generic functions describe relationships](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/services/http.ts#L11-L15)
- [Project example: Types, interfaces and runtime tokens](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L13-L13)
- [Project example: ES modules and emitted file paths](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L6-L6)
- [Project example: Decorator metadata is a compiler/runtime agreement](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/tsconfig.json#L10-L13)
