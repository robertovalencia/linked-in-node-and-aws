# Testing and quality evidence

Run from the project root after installing both package lock files:

```bash
npm --prefix backend ci
npm --prefix frontend ci
npm run check
npm test
npm run build
bash scripts/local.sh up
npm run acceptance
npm run test:browser
```

The copied acceptance suite remains a behavioral reference rather than inherited evidence. A passing report needs **48 PASS, 0 FAIL**; conditional branches must not silently shrink the check count. It makes real HTTP calls through the edge to PostgreSQL and Kafka. See `docs/evidence/local-acceptance.json` after execution. Test runs create additional inquiries but restore edited seed profiles.

Jest isolates backend domain/security behavior. Vitest and React Testing Library exercise frontend behavior. Strict TypeScript catches incompatible shapes during compilation; ESLint and Prettier enforce readable code. None substitutes for an ownership test or a durable transaction. Review coverage for meaningful assertions and uncovered failure branches, not only the percentage.

Run `node scripts/failure-drill.mjs` for negative API, database restart, broker outage and deduplication behavior once the full local stack is healthy. It is explicitly local and uses the new Compose namespace. Preserve evidence of failures and repairs in [reviews](reviews.md). A dependency outage should not require resetting domain data.

The browser command uses Playwright Chromium; install it with `npx playwright install chromium` if the browser binary is missing. Its desktop and mobile journeys exercise compare, profile, sign-in and a persisted inquiry. The GitHub verification workflow runs this browser smoke after the 48 API checks and uploads the screenshots as artifacts.

Local SonarQube was started with `docker compose -f compose.yaml -f compose.quality.yaml up -d --wait sonar-db sonarqube`, then scanned with `node scripts/sonar-local.mjs` after generating Jest/Vitest LCOV. The local server actually evaluated the quality gate; see [results](results.md). A local pass is not a GitHub Actions or cloud SonarQube run. See [toolchain](toolchain.md) for account prerequisites.
