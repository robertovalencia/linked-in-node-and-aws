---
title: "Catalog tools: Zod, coercion, closures and JSONB"
topic: "Catalog tools: Zod, coercion, closures and JSONB"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Catalog tools: Zod, coercion, closures and JSONB

Prerequisites: lessons 01–05. Focus: the tools used by Catalog, with patterns reused by the other services.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Zod parse: a runtime boundary

**What:** A schema is executable validation. `parse` returns a validated value or throws a ZodError.

**How:** The controller accepts `unknown`. Catalog parses that value before reading its fields. TypeScript types alone cannot reject malformed network input.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 70–73](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L70-L73).

```ts
const query = searchSchema.parse(input);
// Parameterized JSONB predicates keep filtering/pagination in PostgreSQL as the catalog grows.
const values: unknown[] = [];
const where: string[] = [];
```

**Watch for:** `value as Provider` only changes compiler assumptions; it does not validate data.

### Why parse if TypeScript already knows the type?

HTTP input has no trustworthy TypeScript type at runtime.

## Coercion, transforms and defaults

**What:** Query parameters arrive as text. Coercion converts selected values before bounds are checked.

**How:** `z.coerce.number()` converts numeric text. Availability instead accepts only the strings true/false and transforms them explicitly. A default supplies a value when input is undefined.

**Real code:** [backend/src/catalog/provider.schema.ts · lines 54–59](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L54-L59).

```ts
maxRate: z.coerce.number().int().min(0).max(1e6).optional(),
available: z
  .enum(['true', 'false'])
  .transform((v) => v === 'true')
  .optional(),
sort: z.enum(['recommended', 'rate-asc', 'rating']).default('recommended'),
```

**Watch for:** `Boolean("false")` is true; coercing arbitrary query text to Boolean is a trap.

### What happens to available=false?

The enum accepts it and the transform produces the boolean false.

## Strict objects and inferred types

**What:** A strict Zod object rejects unknown keys. `z.infer` derives the parsed TypeScript shape from a schema.

**How:** The schema is a runtime value; the inferred Provider type is erased. Nested objects need their own strictness rules; top-level strictness does not automatically configure every child.

**Real code:** [backend/src/catalog/provider.schema.ts · lines 48–50](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L48-L50).

```ts
export type Provider = z.infer<typeof providerSchema>;
export const searchSchema = z
  .object({
```

**Watch for:** Validation does not establish that the caller owns the validated profile.

### Does .strict() mean every field is required?

No. Required, optional and defaulted fields are defined by their individual schemas.

## Closures build positional SQL parameters

**What:** A closure retains access to variables from the scope where the function was created.

**How:** The local `add` function captures values, appends one item, and returns its positional placeholder. The resulting SQL and parameter array are sent separately to pg.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 74–77](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L74-L77).

```ts
const add = (value: unknown) => {
  values.push(value);
  return `$${values.length}`;
};
```

**Watch for:** Placeholders represent data values, not arbitrary SQL identifiers or ORDER BY expressions.

### Why does add return $1, then $2?

Each push increases the captured array length, which supplies the next parameter position.

## JSONB operators and explicit casts

**What:** PostgreSQL JSONB stores structured JSON. `->` returns JSON; `->>` extracts text.

**How:** Catalog extracts hourlyRate as text, casts it to numeric, then compares it with a parameter. Casting matters: textual sorting would put 100 before 20.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 89–92](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L89-L92).

```ts
if (query.maxRate !== undefined)
  where.push(`(document->>'hourlyRate')::numeric<=${add(query.maxRate)}`);
if (query.available !== undefined)
  where.push(`(document->>'available')::boolean=${add(query.available)}`);
```

**Watch for:** Database JSON extraction and JavaScript property access are different operations.

### Why check undefined instead of truthiness?

A numeric zero is a valid supplied filter and must not disappear.

## Escaping LIKE patterns versus SQL parameters

**What:** A parameter prevents a value from becoming SQL syntax. It does not remove special meaning inside a LIKE pattern.

**How:** Catalog escapes backslash, percent and underscore before adding wildcard characters around the query. Sort expressions come from fixed code branches rather than browser SQL.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 79–82](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L79-L82).

```ts
const escaped = query.q.trim().replace(/[\\%_]/g, '\\$&');
where.push(
  `(concat_ws(' ', document->>'name',document->>'headline',document->>'about',document->>'skills',document->>'tools',document->>'services',document->>'location')) ILIKE ${add(`%${escaped}%`)}`,
);
```

**Watch for:** Do not call a parameterized query a named prepared statement unless a statement name is actually configured.

### Why escape percent even with $1?

It changes wildcard matching, not SQL statement structure.

## Row locks and server-owned fields

**What:** `FOR UPDATE` locks selected rows until the transaction ends. Another conflicting writer must wait.

**How:** Catalog locks the owner’s row, checks the submitted ID, and preserves stored rating fields. Object spread order matters: later server values override earlier input fields.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 59–64](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L59-L64).

```ts
const document = {
  ...updated,
  rating: row.document.rating,
  reviewCount: row.document.reviewCount,
  completedProjects: row.document.completedProjects,
};
```

**Watch for:** A row lock serializes writers; it does not by itself detect a user editing a stale representation.

### Why put rating after ...updated?

The stored rating replaces any submitted rating with the same key.

## Practice and mastery

With the local stack running, execute:

```bash
curl -i 'http://127.0.0.1:8180/api/providers?available=false&size=2'
curl -i 'http://127.0.0.1:8180/api/providers?available=yes'
```

Expected: 200 and at most two items; then 400. Predict the parsed values before running.

- Write a tiny closure that collects values and returns `$1`, `$2`. Assert the array and placeholders match.
- Explain why a sort field needs an allowlist even though filter values use placeholders.
- In a practice extension, add `minRate` to the Zod query schema, SQL predicate and React control. See lesson 12.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Zod API](https://zod.dev/api)
- [node-postgres queries](https://node-postgres.com/features/queries)
- [Project example: Zod parse: a runtime boundary](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L70-L73)
- [Project example: Coercion, transforms and defaults](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L54-L59)
- [Project example: Strict objects and inferred types](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L48-L50)
- [Project example: Closures build positional SQL parameters](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L74-L77)
- [Project example: JSONB operators and explicit casts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L89-L92)
- [Project example: Escaping LIKE patterns versus SQL parameters](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L79-L82)
- [Project example: Row locks and server-owned fields](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L59-L64)
