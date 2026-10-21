# From Spring Boot to NestJS

The business rule survives the language change: only the target provider can respond to an inquiry. The framework expresses routing and dependency injection, but the service must enforce that rule itself.

| Java reference | Node implementation concept | What to explain |
|---|---|---|
| Spring application per capability | Nest bootstrap selects capability module | Four runtime processes, one shared source/build package |
| Controller + service | Decorated Nest controller + injectable service | Controller parses HTTP; service protects business invariants |
| Spring Security filter chain | JWT guard and service ownership checks | Signature/issuer/audience/expiry and role are distinct checks |
| Bean validation | Explicit DTO/input validation | TypeScript types disappear at runtime; untrusted JSON still needs checking |
| JPA repository | Parameterized `pg` SQL repository/service | SQL is explicit; parameters prevent value interpolation injection |
| `@Transactional` | Checked-out PostgreSQL client with BEGIN/COMMIT/ROLLBACK | All transaction statements must use the same connection |
| Liquibase | Versioned SQL migrations with checksums | Migration files are immutable after execution; no startup schema reset |
| BCrypt | Node password hashing with per-password salt | The hash format changes; do not copy reference password hashes |
| Kafka template/listener | KafkaJS producer/consumer | Acknowledgments and consumer commits have failure windows |
| JUnit/Mockito | Jest and dependency fakes + real integration tests | Unit isolation does not prove SQL locks or broker delivery |

Node handles network I/O asynchronously on an event loop. `await` suspends a handler while other work proceeds; it does not serialize concurrent incoming requests. Protect duplicate requests in PostgreSQL, not with a process-local map. Avoid expensive synchronous hashing in request handlers. Database pool limits and broker connection cleanup remain important under load.

Read `backend/src` alongside [the contract](../../CONTRACT.md). Rehearse: “I preserved business capability boundaries and observable API behavior while replacing framework-specific code. I verified the port with the original acceptance suite and extra failure tests. I would choose architecture based on product constraints rather than assume microservices are always better.”
