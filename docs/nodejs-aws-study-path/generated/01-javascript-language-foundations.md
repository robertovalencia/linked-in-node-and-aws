---
title: JavaScript language foundations for backend work
topic: JavaScript
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# JavaScript language foundations

Prerequisite: lesson 00 terminal checkpoint. JavaScript is the language; Node.js is a runtime that supplies server APIs. TypeScript adds compile-time checking and produces JavaScript. NestJS organizes that runtime into application components. Keep those four ideas separate.

## Values, bindings and control flow

A value has a runtime type. A binding gives a value a name. Use const when the binding should not be reassigned and let when it should. A const object can still be mutated. Primitives include string, number, boolean, undefined, null, bigint and symbol; arrays and functions are objects. null means an intentional empty value by convention; undefined often means missing. Use === for comparisons and explicitly convert request strings to numbers. The string "0" is truthy; the number 0 is falsy. An empty array is truthy.

Objects are shared through references. Spreading an object copies its own enumerable fields shallowly; nested arrays still reference the same data. This is why a React update must copy the particular nested structure being changed. map transforms each element, filter selects elements, find returns one element or undefined, and reduce accumulates. A Map is useful for keyed state; a Set removes duplicate scalar IDs. JSON is a wire representation, not a complete JavaScript object serializer: functions and undefined properties do not round-trip as ordinary fields.

## Runnable example: closure and copying

Save this as work/js-foundations.mjs in your practice copy and run node work/js-foundations.mjs.

~~~js
function counter() {
  let n = 0;
  return () => ++n;
}
const next = counter();
console.log(next(), next());
const provider = { name: 'Ava', skills: ['Node'] };
const copied = { ...provider };
copied.skills.push('SQL');
console.log(provider.skills.join(','));
console.log('0' === 0, Boolean('0'), Number('0'));
~~~

Expected output is 1 2, then Node,SQL, then false true 0. The returned function retains access to n after counter returns: that retained lexical environment is a closure. The spread copied the skills reference. Repair the example with skills: [...provider.skills] and show that the original array stays unchanged.

## Functions, classes and errors

Arrow functions capture this from the surrounding context; a method's this depends on how it is called. Destructuring a method and calling it standalone may lose its receiver. A class constructor stores instance state; prototype methods are shared. A JavaScript class does not imply Java's thread model. try/catch catches a synchronous throw and a rejected promise that is awaited in that try block; it does not magically catch a later unawaited callback.

Use optional chaining for possibly missing values and ?? when only null/undefined should trigger a default. || also replaces 0, false and empty strings, which can corrupt valid input. Destructuring extracts fields; rest collects the remaining fields; spread expands values. Template literals interpolate strings and are not SQL escaping.

## Read the project

In backend/src/catalog/catalog.service.ts follow providers.map, object destructuring of ownerEmail, the add closure that numbers SQL parameters, and filter construction. In frontend/src/hooks/useMarketplace.ts follow Set-based comparison deduplication and the lazy useState initializer. In backend/src/common/errors.ts find the unknown-error checks. Explain each expression in plain English before reading the framework decorators.

## Lab and debugging

Write a pure function summarize(providers) that returns the names of available providers under a numeric budget, sorted without modifying the input. Include a missing rate, a rate of 0, an empty list, and duplicate names. Assert that the original array is unchanged. Then deliberately replace ?? with || for a zero budget; explain the wrong output and repair it. Add a closure that counts successful searches; make two independent counters and prove they do not share counts.

Senior tradeoff: clever chains can hide invalid input and expensive work. Separate runtime validation from business transformation. Name intermediate values when that makes ownership or filtering rules easier to review. Know asymptotic cost: filtering n providers is O(n); sorting generally adds O(n log n); loading an entire catalog into Node does not replace database pagination.

## Interview answers



### What is a closure?

A function retaining access to lexical variables from its creation environment; it enables counters and event handlers, and can retain outdated React render values or unnecessary memory.



### Does const make an object immutable?

No. It prevents rebinding the name; nested data can still change. Copy deliberately or enforce immutability at the relevant boundary.

## Mastery check

- [ ] Predict every line of the runnable example before execution.
- [ ] Explain mutation, reference identity, coercion, closure and this.
- [ ] Implement and test summarize without mutating input.
- [ ] Find these patterns in real catalog and React source.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) — accessed 2026-10-22.
- [closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures) — accessed 2026-10-22.
- [Project source: backend/src/catalog/catalog.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/catalog/catalog.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/hooks/useMarketplace.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/hooks/useMarketplace.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/errors.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/errors.ts) — local baseline inspected 2026-10-22; private published source may lag.
