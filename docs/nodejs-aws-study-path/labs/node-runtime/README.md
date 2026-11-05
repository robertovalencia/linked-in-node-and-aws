# Credential-free Node runtime lab

From the repository root:

```sh
node docs/nodejs-aws-study-path/labs/node-runtime/run.mjs
```

From the extracted study pack's `NodeJs-AWS` directory:

```sh
node labs/node-runtime/run.mjs
```

Use the project's declared Node range (`>=22 <25`). No npm install, database, Docker or cloud credentials are needed. The script creates its own temporary directory and removes it in `finally`; it does not change application data.

Expected: JSON reporting ten passed assertion groups and the actual Node version. Failures exit nonzero. The groups prove synchronous EventEmitter listener/error behavior; CommonJS versus ECMAScript-module entry-point scheduling; closure/shallow-copy/byte-length observations; pipeline byte equality, error rejection and stream closure; producer pause/drain behavior; independent async context; successful and failed worker handling; literal child arguments and failed exit; supported-operation cancellation; and query/conversion edge cases.

The scheduler assertions apply to these entry-point contexts. They do not predict every timer or input/output callback order. This is an illustrative lab, not a marketplace streaming endpoint, worker service or production benchmark.

Related cards: [NR19](../../node-backend-runtime.md#nr19), [NR22](../../node-backend-runtime.md#nr22), [NR27–28](../../node-backend-runtime.md#nr27), [NR30–33](../../node-backend-runtime.md#nr30). Official references are linked on each card.
