---
title: Strict TypeScript, runtime boundaries and modules
topic: TypeScript
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Strict TypeScript and modules

Prerequisite: 01. TypeScript asks what shapes are allowed before execution. The HTTP caller, database and Kafka broker can still send arbitrary runtime values. Therefore a compiler-successful application can reject or mishandle actual data. Treat external values as unknown until checked.

## Explained example

~~~ts
type Status = 'PENDING' | 'ACCEPTED' | 'DECLINED';
type Outcome = { ok: true; status: Status } | { ok: false; reason: string };
function describe(result: Outcome): string {
  return result.ok ? result.status : result.reason;
}
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}
~~~

A union restricts alternatives; the ok discriminator lets the compiler narrow to the corresponding shape. unknown requires checks before use. any disables that protection. A type assertion such as value as Provider tells the compiler to trust you; it performs no validation. Generic api<T> in the frontend describes an expected result, but cannot prove the server returned T. A useful production extension is runtime decoding at that API boundary.

## Type tools you actually encounter

Interfaces and object type aliases describe structure, not nominal class identity. Optional fields may be absent; a field with a union containing undefined may be present but empty. Omit<Auth, 'token'> removes a property in the type model. ReturnType<typeof useMarketplace> derives the hook's returned shape. as const narrows the SERVICES array into literal names, and (typeof SERVICES)[number] produces their union. Record<string, Type[]> models the provider lookup table. Type-only imports disappear from emitted JavaScript.

backend/tsconfig.json is strict and emits decorator metadata. Legacy TypeScript decorators and reflect-metadata let Nest associate controller/service classes with runtime dependency information. This is not identical to every newer JavaScript decorator proposal. Preserve the repository compiler settings; changing decorator mode can break dependency injection even when a tutorial's syntax looks similar.

## ESM and package boundaries

Both package.json files declare type: module. Backend source imports local modules using .js suffixes because emitted files run as JavaScript. The compiler and Jest mapper account for the .ts source during development. The frontend uses Vite's bundling pipeline and extensionless imports. Do not copy a CommonJS require example into an ESM file and assume it has the same behavior. npm scripts run with their package folder as the working directory, which matters for migrations and seed paths based on process.cwd().

## Source reading

Read backend/src/common/config.ts, backend/src/main.ts, backend/tsconfig.json and backend/package.json. Then compare backend/src/inquiries/inquiry.schema.ts with frontend/src/types/marketplace.ts. Identify compile-time contracts, Zod runtime schemas, and fields whose names change when mapping SQL rows. The project uses direct Zod parsing, not Nest's class-validator ValidationPipe.

## Executable lab

In a practice branch add a scratch .ts file inside backend/src. Define the Outcome union above, intentionally access result.reason without narrowing, and run npm --prefix backend run typecheck from the repository root. Expect a compiler error about the property not existing on the success alternative. Repair it with narrowing and rerun. Remove the scratch file afterward. Then run this from backend: node --input-type=module -e 'console.log(JSON.parse("{\"budget\":\"many\"}").budget)'. It prints many despite your intended numeric budget; discuss how inquirySchema closes that gap.

Debugging: “Cannot find module” after compilation often concerns output paths or .js imports, not missing business data. “Nest cannot resolve dependencies” concerns module registration, reflection metadata or injection tokens. Inspect emitted dist/main.js and configuration before reinstalling packages.

Senior tradeoff: duplication between SQL, Zod and UI types can drift. Schema inference or generated clients may reduce duplication, but still require versioning, compatibility tests and ownership. Code generation is an extension, not an existing feature here.

## Interview answers and mastery



### Why use unknown?

It forces evidence before accessing external data, while any suppresses checking.

### Does TypeScript validate JSON?

No; runtime checks such as Zod are necessary.

- [ ] Demonstrate a useful compiler failure and its repair.
- [ ] Explain .js suffixes in .ts backend source.
- [ ] Distinguish runtime decorators, erased types and runtime schemas.
- [ ] Identify where api<T> gives an assumption rather than validation.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) — accessed 2026-10-22.
- [modules](https://www.typescriptlang.org/docs/handbook/2/modules.html) — accessed 2026-10-22.
- [Project source: backend/tsconfig.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/tsconfig.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/config.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/config.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/main.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/main.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/inquiries/inquiry.schema.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiry.schema.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/types/marketplace.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/types/marketplace.ts) — local baseline inspected 2026-10-22; private published source may lag.
