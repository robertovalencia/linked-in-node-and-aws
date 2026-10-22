---
title: "JavaScript: values, closures, objects and collections"
topic: "JavaScript: values, closures, objects and collections"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# JavaScript: values, closures, objects and collections

Start here after the roadmap. No Node.js knowledge is assumed.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Bindings, values and mutation

**What:** `const` prevents reassignment of a variable. It does not freeze an object or array stored in that variable.

**How:** A variable can refer to an object shared with other code. Mutating that object is visible through its other references; creating a new object has a different identity.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 72–75](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L72-L75).

```ts
const values: unknown[] = [];
const where: string[] = [];
const add = (value: unknown) => {
  values.push(value);
```

**Watch for:** const and immutable do not mean the same thing.

### Can values.push work when values is const?

Yes. The array changes; the variable is not rebound to another array.

## Lexical scope and closures

**What:** A closure is a function retaining access to variables in its surrounding scope.

**How:** Catalog’s add function remembers the values array from the current search call. A different search call creates a different array and closure.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 74–77](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L74-L77).

```ts
const add = (value: unknown) => {
  values.push(value);
  return `$${values.length}`;
};
```

**Watch for:** A closure can retain old values or large objects longer than intended.

### Do two requests share the local values array?

No. Each call creates its own local array; module or instance fields would have a different lifetime.

## Destructuring and object spread

**What:** Destructuring extracts properties. Rest collects the remaining ones; object spread copies enumerable properties into a new object.

**How:** Catalog separates ownerEmail from public profile data. Its update also spreads user input before overriding protected fields with stored values.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 21–23](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L21-L23).

```ts
const { ownerEmail, ...document } = entry;
providerSchema.parse(document);
await client.query(
```

**Watch for:** These copies are shallow. Nested arrays or objects can still share references.

### Why can a shallow copy still change the original?

Both objects may refer to the same nested array or object.

## Truthiness, optional chaining and nullish defaults

**What:** `?.` stops an access when its receiver is null or undefined. `??` replaces only null/undefined; `||` also replaces false, zero and empty text.

**How:** Identity uses a missing account’s fallback hash. Catalog checks maxRate against undefined so a supplied zero does not vanish through a truthiness check.

**Real code:** [backend/src/identity/identity.service.ts · lines 52–53](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L52-L53).

```ts
const valid = await verifyPassword(password, account?.password_hash ?? this.dummyHash);
if (!account || !valid) throw new UnauthorizedException('Invalid email or password');
```

**Watch for:** The string "false" is truthy. Convert external values with an explicit rule.

### When does zero survive a default?

It survives a ?? default; an || default would replace it.

## Arrays, callbacks, Set and Map

**What:** `map` produces transformed elements; `filter` selects elements. A Set deduplicates values; a Map associates keys with values.

**How:** The React hook filters saved IDs, deduplicates them with Set and caps the result. Identity uses Map for per-IP attempt counters.

**Real code:** [frontend/src/hooks/useMarketplace.ts · lines 29–34](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L29-L34).

```ts
        ...new Set(
          saved.filter((id): id is string => typeof id === "string"),
        ),
      ].slice(0, 3)
    : [];
} catch {
```

**Watch for:** Set compares object references, not deep object content.

### Why does Set remove duplicate IDs reliably?

IDs are scalar strings, so equal string values compare as the same Set value.

## Errors and runtime narrowing

**What:** JavaScript can throw values that are not Error objects. A catch variable therefore cannot safely be assumed to have a message or stack.

**How:** The error filter uses instanceof and shape checks before deciding how to report a failure. A rejected awaited promise enters catch just like a synchronous throw.

**Real code:** [backend/src/common/errors.ts · lines 17–23](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/errors.ts#L17-L23).

```ts
  error instanceof ZodError
    ? 400
    : error instanceof HttpException
      ? error.getStatus()
      : (parserStatus ?? 500);
let detail =
  status === 500
```

**Watch for:** A try block does not catch an unrelated later callback unless the failure reaches its awaited promise chain.

### Why use instanceof instead of assuming error.message?

The thrown value may be a string, null or another non-Error value.

## Practice and mastery

Create `work/` in a practice copy. Save this as `work/values.mjs` and run `node work/values.mjs`:

```js
function counter() {
  let value = 0;
  return () => ++value;
}
const next = counter();
console.log(next(), next());
const original = { skills: ['Node'] };
const copy = { ...original };
copy.skills.push('SQL');
console.log(original.skills.join(','));
console.log('0' === 0, Boolean('0'), Number('0'));
```

Expected: `1 2`, then `Node,SQL`, then `false true 0`.

- Copy the nested skills array too; prove the original no longer changes.
- Explain one closure, one mutation and one conversion in the real Catalog code.
- Write a filter/map transformation without mutating its input.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [MDN JavaScript guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [MDN closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)
- [Project example: Bindings, values and mutation](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L72-L75)
- [Project example: Lexical scope and closures](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L74-L77)
- [Project example: Destructuring and object spread](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L21-L23)
- [Project example: Truthiness, optional chaining and nullish defaults](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L52-L53)
- [Project example: Arrays, callbacks, Set and Map](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L29-L34)
- [Project example: Errors and runtime narrowing](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/errors.ts#L17-L23)
