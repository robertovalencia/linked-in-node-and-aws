# Node.js services: a beginner's guided tour

You do not need to know NestJS to begin. You need to be able to open a terminal, read a JavaScript function, and recognize a JSON object. If `async`, a class, or an import is unfamiliar, keep the [glossary](05-glossary.md) open beside the code. This guide explains the application that is actually in this repository. It does not claim that preparing AWS files means deploying AWS, or that reading a guide establishes senior experience.

Imagine a company asks Ava to build a customer portal. The browser collects the message. Identity establishes who the sender is. Catalog knows which profile belongs to Ava. Inquiries records the request and its intention to announce it. Notifications eventually creates Ava's inbox item. Each service is a separate running Node.js program with a separate database. They cooperate through HTTP and Kafka, rather than reaching into each other's tables.

## Read in this order

| Guide | What you should be able to do afterward |
|---|---|
| [1. Runtime, configuration, and wiring](01-runtime-and-wiring.md) | Explain how one source package becomes four processes, when migrations run, and what Nest injects |
| [2. Walk through all four services](02-four-services.md) | Follow each endpoint from controller through validation, permissions, SQL, and response |
| [3. Browser, events, and AWS](03-browser-events-and-aws.md) | Trace a click through React, the proxy, a database transaction, Kafka, and a recipient inbox; explain the prepared AWS environment |
| [4. Debugging and practice](04-debugging-and-practice.md) | Run bounded local experiments, recover from failures, and explain your evidence in an interview |
| [5. Read the language](05-glossary.md) | Translate the JavaScript, TypeScript, Node, Nest, SQL, and React vocabulary used here into plain language |

Read [the API contract](../../CONTRACT.md) when you need exact public shapes, and [the architecture reference](../architecture.md) for the concise overview. The guides expand those references; the source remains the executable truth. See [the Java-to-NestJS comparison](../interview-topics/java-to-nestjs.md) if you already know Spring.

## Your first 45 minutes

1. Draw five boxes: browser and four services. Add a separate database below each service. Put Kafka between Inquiries and Notifications.
2. Read `bootstrap` in [main.ts](../../backend/src/main.ts). Find `controllers[service]` and `providers[service]`. Say aloud which entries are selected when `SERVICE=inquiries`.
3. Open [InquiriesController.create](../../backend/src/inquiries/inquiries.controller.ts) and then [InquiriesService.create](../../backend/src/inquiries/inquiries.service.ts). Write down the difference between the `actor`, the idempotency key, and the body.
4. Find the two `INSERT` statements inside the same transaction. One saves a request; one saves a promise to publish an event later.
5. Read [OutboxPublisher.publishBatch](../../backend/src/common/messaging.ts), then [NotificationsService.consume](../../backend/src/notifications/notifications.service.ts). Identify the duplicate-delivery window and the database constraint that makes a replay harmless.

Do not try to memorize decorators first. Follow one business action, and learn each language feature when it appears in that action.

## Scope and evidence

This documentation was built by reading the repository's source, SQL migrations, Compose files, frontend wiring, deployment scripts, and existing specifications. Commands in the practice guide are instructions for your local laboratory; their presence does not mean they were run during documentation authoring. [Results](../results.md) and dated [evidence](../evidence/README.md) describe separately recorded execution. Record your own environment and observed results when doing the exercises.

**Implemented** means code/configuration exists in this checkout. **Prepared AWS** means infrastructure or release code exists and still needs its own execution evidence. **Extension** means an exercise or proposed hardening that is not current behavior. This distinction matters when describing the portfolio to an interviewer.

## Completion checkpoint

You are ready to leave this guide when you can trace an inquiry without guessing, explain a 401 versus a 403 versus a 409, show why a network retry must reuse its original key, and recover from a local broker outage without deleting data. Senior readiness additionally requires the broader study path's design, performance, security, operating, and tradeoff work.
