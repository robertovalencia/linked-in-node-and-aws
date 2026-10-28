---
title: "Caching and DynamoDB access-pattern design"
topic: "Caching and DynamoDB access-pattern design"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 58 · Caching and DynamoDB access-pattern design

**Prerequisites:** 57; key-value lookup, transactions, and application ownership.

[Previous: 57](57-rds-postgresql-backups-and-failover.md) · [Next: 59](59-msk-kafka-security-and-operations.md) · [Study path](../README.md)

**Implementation boundary:** ElastiCache and DynamoDB are absent from the current architecture. PostgreSQL remains the actual source of truth. These examples explore separate design choices rather than replace existing persistence.

A cache stores data to reduce repeated work or latency under an explicit freshness policy. A cache miss means the requested entry is unavailable, not that the underlying business record does not exist. DynamoDB is a managed key-value and document database whose primary key consists of a partition key and optionally a sort key. A secondary index offers another key-based access path. Cache design and DynamoDB modeling both begin with concrete read/write patterns, but one is not automatically a substitute for the other.

## 1. Classify authoritative and derived data

Identify which system decides the durable truth for each entity. In a cache-aside design, the application reads a cache, loads a miss from the authoritative store, and populates the cache. A cache entry’s disappearance should not silently destroy the underlying business fact. Define whether the chosen cache configuration is disposable or intentionally durable; newer service modes may change durability options. Do not make blanket claims about every ElastiCache configuration from an old cache-only mental model.

## 2. Define cache keys, freshness, and failure behavior

A key should include all relevant tenant and representation context. Time to live limits how long an entry should remain usable, while invalidation addresses changes before expiry. Avoid negative caching that hides newly created records for too long. Concurrent misses can create a cache stampede, where many callers overload the backing database; bounded refresh coordination, jitter, and safe stale responses may help. If the cache fails, ensure fallback load does not overwhelm the authoritative system.

## 3. Model DynamoDB from required queries

Write access patterns before choosing keys: get one notification by identity, list one user’s recent notifications, or enforce one event receipt. A partition key selects a logical item collection; the sort key orders or distinguishes related items. A Query uses a specific partition-key condition, while Scan reads across a broader table/index scope. Replacing every missing index with Scan is rarely a sound high-traffic design. Secondary indexes add write/storage work and have their own consistency and key-distribution considerations.

## 4. Distribute activity and enforce safe writes

A high-cardinality key can still be hot if one value receives most traffic. Model request distribution and large tenants, not just the number of distinct values. Conditional writes can enforce a creation precondition; transactions support coordinated changes within their documented boundaries. Use durable event identity for idempotency instead of assuming no duplicate message arrives. Time-to-live deletion is asynchronous cleanup and should not be used as an exact authorization-expiry clock; applications must check validity where correctness requires it.

## 5. Compare consistency and migration implications

DynamoDB consistency depends on the selected read path and feature; verify table, index, and multi-Region behavior in current documentation. A cache adds its own staleness policy regardless of database consistency. A move from relational data to DynamoDB can require denormalization, new indexes, and migration/backfill logic. Keep the project’s database ownership intact and justify any change with an actual access pattern. This lesson offers no throughput sizing, pricing estimate, or claim of a completed data migration.

## Source or illustrative example

**New illustrative key design:** `PK=USER#u123`, `SK=NOTIFICATION#2026-10-27T12:00:00Z#event-7` supports a user-scoped ordered collection. The exact timestamp and identity strategy must handle collisions and pagination. This is a modeling sketch, not an existing DynamoDB table. A PostgreSQL query and a cache key should not be called a DynamoDB implementation merely because they contain similar strings.

## Safe exercise

Run a local key-distribution demonstration:

```sh
python3 - <<'PY'
from collections import Counter
keys = ['TENANT#large'] * 90 + [f'TENANT#{i}' for i in range(10)]
print(Counter(keys).most_common(1))
print('distinct:', len(set(keys)))
PY
```

Expected outcome: one logical key receives 90 operations despite 11 distinct keys. These are synthetic counts, not workload measurements. Design three access patterns and map each to a key/index query. Then describe a cache invalidation timeline where an inquiry changes while an earlier representation remains cached.

## Failure diagnosis

A low hit rate can mean unsuitable TTLs, unstable keys, small working-set coverage, or unnecessary variation. Correct cache hits with wrong data suggest a missing tenant/input dimension or invalidation error. DynamoDB throttling concentrated on one pattern can indicate a hot key even when aggregate capacity seems adequate. Missing list results may reflect index consistency, pagination, or sort-key boundaries. Separate these hypotheses before increasing capacity or adding a second cache.

## Recall and answers

### Does a cache miss prove a record does not exist?

No. Query the authoritative store according to the chosen cache strategy.

### Does many distinct partition keys guarantee balanced traffic?

No. Activity can still concentrate on one hot key.

## Mastery check

Present an authority/cache diagram, freshness policy, three DynamoDB access patterns, and a hot-key counterexample. Explain conditional-write idempotency and the limits of TTL. State that the current application still uses PostgreSQL and that these service choices require separate implementation evidence.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [DynamoDB partition key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [ElastiCache caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html)
- [DynamoDB developer guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [DynamoDB TTL behavior](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
