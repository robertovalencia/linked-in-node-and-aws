---
title: Local setup, npm, containers and process lifecycle
topic: Local engineering
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Reproducibility begins on your machine

Prerequisites: 04–05, 13. The root package orchestrates commands, but this is not an npm workspaces project. Root, backend and frontend have separate package/lockfile scopes. npm ci installs a lockfile-consistent dependency graph; npm install can update the graph. Installing a package in the wrong folder will not repair a missing backend module.

## What actually runs locally

compose.yaml starts a built React/nginx edge, four Nest process containers, one PostgreSQL server with four owned databases/logins, and one Kafka KRaft node. The isolated Compose project is linked-in-node-local. The local ports include edge 8180, services 8181–8184, Vite 5183, PostgreSQL 55432 and Kafka 19092. No Kubernetes, managed RDS or managed MSK exists in this local topology.

The backend Dockerfile compiles TypeScript in a build stage, installs/prunes dependencies for runtime, copies needed migrations/seeds and runs as node rather than root. One image is reused with distinct SERVICE/DB_URL values. Containers have separate processes and network namespaces; localhost inside a container means that container, not the host or the database service. Compose service DNS names solve container-to-container addressing.

Development mode differs from the built edge. backend/scripts/dev.mjs compiles, runs tsc --watch and node --watch with separate dist-dev folders and debugger ports per capability. The root development script spawns those and Vite, forwards output and coordinates termination. It does not use nodemon, ts-node or tsx. Vite proxies same-origin API paths to backend ports; browser components call /api/... rather than private container DNS names.

## Setup and runnable lab

Read docs/local-setup.md and scripts/setup-local.sh before running setup. In a practice environment from the repository root run npm run setup then npm run up, and open http://localhost:8180. Use synthetic demo identities from README only. Verify login, provider discovery, inquiry creation and provider inbox. Record the exact application URL; Vite and nginx are different entry points.

For hot reload follow the documented switch: npm run down, bash scripts/local.sh deps, npm --prefix backend ci, npm --prefix frontend ci, then npm run dev. Open http://localhost:5183. Do not run both sets of host-facing services if their ports conflict. Finish using the corresponding documented stop command or Ctrl-C for the foreground development supervisor.

Use docker compose -p linked-in-node-local ps to inspect health and process roles; inspect scripts/local.sh if an env-file flag is needed in your setup. Never print the expanded Compose configuration when it would expose runtime secrets. Stop/start the lab through the supplied wrapper rather than deleting volumes. A stop is reversible; removing volumes destroys local data and is not required to learn service wiring.

## Debugging checkpoints

Connection refused: is the correct process listening and does its health pass? Authentication failure: do the service DB credentials match its owned database? Missing migrations: was the backend working directory preserved? Browser 502: is the proxy target healthy? ESM import failure: did the build complete and does emitted JavaScript use resolvable imports? Check logs at the failing boundary instead of reinstalling every dependency.

## Senior tradeoffs

Docker images improve repeatability but do not freeze every external service or eliminate platform differences. A volume survives a container replacement, so an old applied migration checksum remains significant. Readiness gates startup sequencing but dependencies can fail afterward. Dependency lockfiles and multi-stage builds need routine vulnerability review; a successful npm ci is not a security certification. Do not embed secret .env files in images or commit Terraform state.



### One image means one service?

No; runtime identity/configuration selects one capability per process.

### Why does localhost fail in Docker?

It refers to the caller container; use the intended service DNS or published host port for the correct context.

- [ ] Start one documented local mode and name every process.
- [ ] Explain dependency installation scopes and emitted-JS startup.
- [ ] Diagnose one connection/port/config failure without destructive cleanup.
- [ ] Distinguish container restart, image rebuild and volume persistence.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci) — accessed 2026-10-22.
- [Docker Compose networking](https://docs.docker.com/compose/how-tos/networking/) — accessed 2026-10-22.
- [multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — accessed 2026-10-22.
- [Project source: package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: compose.yaml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/compose.yaml) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/Dockerfile](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/Dockerfile) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/nginx.conf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/nginx.conf) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/vite.config.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/vite.config.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/scripts/dev.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/scripts/dev.mjs) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/dev.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/dev.mjs) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/local-setup.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/local-setup.md) — local baseline inspected 2026-10-22; private published source may lag.
