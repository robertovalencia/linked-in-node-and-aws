# Node.js concepts and tools by service

Study the runtime and library mechanics first. Use the marketplace code as the concrete example for each concept.

## Choose a service

| Service | Concepts and libraries | Guide |
|---|---|---|
| Identity | Callbacks, promisify, scrypt, salt, Buffer, JWT, Zod, Map | [Technical notes](06-identity-tools.md) |
| Catalog | Zod parse/coercion, closures, SQL parameters, JSONB, row locks | [Technical notes](07-catalog-tools.md) |
| Inquiries | Native fetch, abort timeout, SHA-256, UUIDs, advisory locks, outbox | [Technical notes](08-inquiries-tools.md) |
| Notifications | KafkaJS, groups/offsets, Buffer decoding, unique event IDs, timers | [Technical notes](09-notifications-tools.md) |

Shared foundations: [NestJS decorators, injection and lifecycle](../nodejs-aws-study-path/generated/05-nestjs-service-wiring.md), [pg pools and transactions](../nodejs-aws-study-path/generated/07-postgresql-and-transactions.md), and [the full study path](../nodejs-aws-study-path/README.md).

## Study one concept in five minutes

1. Read What and How; explain the mechanism in your own words.
2. Open Real code. The link highlights verified lines in a fixed commit.
3. Read the small excerpt and predict its result or failure.
4. Answer the recall question without notes.
5. Complete the practice check when ready.

Source excerpts are fragments, not standalone programs. Practice extensions are labeled and do not describe current application behavior.

## Application walkthroughs and local practice

- [Runtime and wiring](01-runtime-and-wiring.md)
- [Four-service workflow](02-four-services.md)
- [Browser, events and AWS](03-browser-events-and-aws.md)
- [Local debugging and practice scripts](04-debugging-and-practice.md)
- [Vocabulary glossary](05-glossary.md)

The practical walkthroughs complement the technical notes. Learner labs remain instructions until you run and record them yourself.
