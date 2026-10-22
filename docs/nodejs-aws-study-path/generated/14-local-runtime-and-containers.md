---
title: "Runtime tools: npm, tsc, Docker and process supervision"
topic: "Runtime tools: npm, tsc, Docker and process supervision"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Runtime tools: npm, tsc, Docker and process supervision

Prerequisites: lessons 02–05. Keep dependency installation, compilation and execution separate.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## npm scripts and separate package scopes

**What:** package.json defines commands and dependencies; a lockfile records a resolved dependency graph.

**How:** Root, backend and frontend each have their own manifests and lockfiles. npm --prefix selects a package directory; this repository is not configured as npm workspaces.

**Real code:** [package.json · lines 10–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/package.json#L10-L13).

```json
"check": "npm --prefix backend run check && npm --prefix frontend run check",
"test": "npm --prefix backend test && npm --prefix frontend test",
"build": "npm --prefix backend run build && npm --prefix frontend run build",
"acceptance": "node scripts/acceptance.mjs http://localhost:8180 docs/evidence/local-acceptance.json",
```

**Watch for:** A root npm ci does not automatically install every nested package.

### Why install backend and frontend separately?

They are separate package scopes with separate locks and tools.

## tsc emits; node executes

**What:** tsc compiles TypeScript to JavaScript. Node runs the emitted JavaScript entry point.

**How:** The backend image compiles during its build stage and keeps runtime dependencies afterward. Migration files must still be copied because startup reads them at runtime.

**Real code:** [backend/Dockerfile · lines 7–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/Dockerfile#L7-L13).

```text
RUN npm run build && npm prune --omit=dev
FROM node:22.22.0-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/dist ./dist
COPY --chown=node:node migrations ./migrations
```

**Watch for:** A successful TypeScript build does not prove startup config or database reachability.

### Why copy migrations into the final image?

The Database initialization hook needs the SQL files when the container starts.

## Docker image versus container

**What:** An image is a packaged filesystem and command. A container is a running instance of that image with its own process environment.

**How:** The four backend services share one image but set different SERVICE/DB_URL values. They do not share a JavaScript heap.

**Real code:** [compose.yaml · lines 2–9](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/compose.yaml#L2-L9).

```yaml
x-node: &node
  image: linked-in-node/backend:local
  build: ./backend
  init: true
  restart: unless-stopped
  mem_limit: 256m
  cpus: 1
  security_opt: [no-new-privileges:true]
```

**Watch for:** A non-root image user reduces privileges; it does not replace secret management or network policy.

### Why can one image run four capabilities?

The startup selection is driven by each container’s environment.

## Container DNS and published ports

**What:** Containers discover each other by Compose service names. Published ports provide a different access path from the host.

**How:** The host database port is 55432 while PostgreSQL listens on 5432 inside its network. localhost inside a backend container identifies that container, not PostgreSQL.

**Real code:** [compose.yaml · lines 31–34](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/compose.yaml#L31-L34).

```yaml
ports: ['127.0.0.1:55432:5432']
environment:
  POSTGRES_USER: marketplace_admin
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Run npm run setup}
```

**Watch for:** Kafka also returns advertised addresses; a reachable bootstrap address alone is not sufficient.

### Why does postgres:5432 work in a container but not as a normal host URL?

postgres is a Compose-network name, not necessarily a hostname known by the laptop.

## Child-process supervision and inspectors

**What:** A development supervisor starts compiler and runtime processes and forwards their output and termination.

**How:** The launcher uses Node’s executable path, watch mode and an optional loopback inspector. Each capability needs its own output/inspector configuration.

**Real code:** [backend/scripts/dev.mjs · lines 6–11](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/scripts/dev.mjs#L6-L11).

```js
const outDir = `dist-dev/${service}`;
const compiler = 'node_modules/typescript/bin/tsc';
const build = spawn(process.execPath, [compiler, '--outDir', outDir], { stdio: 'inherit' });
const built = await new Promise((resolve) => build.on('exit', resolve));
if (built !== 0) process.exit(Number(built ?? 1));
const children = [
```

**Watch for:** Do not run host APIs and container APIs on the same ports at the same time.

### What is the inspector for?

Attaching a debugger to runtime execution; it is not the HTTP application port.

## Practice and mastery

From the repository root:

```bash
node --version
npm --prefix backend ci
npm --prefix frontend ci
npm run check
npm run build
```

Use the declared Node range and locks as the compatibility baseline. For the full local stack use `npm run setup` then `npm run up`; setup preserves an existing local environment file.

- Draw host ports versus container ports without reading secrets.
- Explain image, process memory, container filesystem and persistent Docker volume separately.
- Stop the local stack with `npm run down`; ordinary stopping preserves volumes.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci)
- [Docker build stages](https://docs.docker.com/build/building/multi-stage/)
- [Project example: npm scripts and separate package scopes](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/package.json#L10-L13)
- [Project example: tsc emits; node executes](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/Dockerfile#L7-L13)
- [Project example: Docker image versus container](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/compose.yaml#L2-L9)
- [Project example: Container DNS and published ports](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/compose.yaml#L31-L34)
- [Project example: Child-process supervision and inspectors](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/scripts/dev.mjs#L6-L11)
