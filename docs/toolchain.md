# Development toolchain and release gates

The repository implements the workflow locally and supplies GitHub/AWS configuration. A configured file is not a verified external integration. See the current evidence in [testing](testing.md) and the [progress page](progress.html). Jira, GitHub branch protection, hosted SonarQube connectivity, and AWS permissions require the owner's accounts. The reference project's successful runs and findings are historical comparison material, never proof for this Node implementation.

## Daily development

Use Node 22 and lock-file installs. `npm run setup` creates independent local secrets; `npm run up` starts the integrated environment; `npm run dev` enables the documented hot reload workflow. Run `npm run check`, `npm test`, `npm run build`, and `npm run acceptance` before asking for review. The root delegates source checks to backend/frontend; Jest verifies Node behavior and Vitest/Testing Library verifies UI behavior. Full HTTP/DB/Kafka acceptance verifies the integrated product. Type checking is not a replacement for those runtime tests.

VS Code recommendations are in `.vscode/extensions.json`: ESLint, Prettier, Terraform, Docker, Codex, and SonarLint (now branded SonarQube for IDE). `.vscode/settings.json` enables format-on-save and explicit ESLint fixes. Install only trusted extensions, open the independent project directory, and check the workspace's `AGENTS.md` before directing Codex. Do not put credentials into VS Code settings, prompts, screenshots, or commit messages.

ESLint catches code mistakes and React hook usage. Prettier makes mechanical formatting consistent. Strict TypeScript checks contracts within each package. Review real permission/ownership behavior at API boundaries; a correct type does not authorize a caller. Dependabot updates the root, backend/frontend npm, GitHub Actions, Terraform, and Docker ecosystems weekly. Review generated dependency PRs, audit production dependency reports, run acceptance, and inspect image scan results before merging. Version tags constrain infrastructure images but should be resolved to reviewed digests for a stricter production supply chain.

## Jira and traceability

Import the requirement/acceptance backlog linked from [AI development](ai-development.md) into your Jira project using Jira's CSV import. Replace local requirement IDs with actual Jira keys in the traceability record; retain the local IDs so tests remain stable. Use the issue key in a branch, commit, pull request, and release record. A requirement should link to its specification, acceptance test, source change, test/coverage evidence, architecture review, deployment manifest, and smoke result. Mark an unconfigured Jira connection honestly rather than fabricating issue URLs.

The normal cycle is: approve a small specification and its acceptance criteria; ask Codex to implement it within `AGENTS.md`; review the diff and security implications; have a separate critic execute checks; resolve the largest remaining gap; record evidence; open a pull request; promote only the reviewed commit. Generation percentage is a workflow target, not a measured quality metric or assurance that generated code is correct.

## GitHub Actions

| Workflow | Trigger | Enforced behavior |
|---|---|---|
| Verify | Pull request, main push, manual | Locked installs, source checks, Jest/Vitest coverage, builds, production npm audit, complete Compose acceptance and Playwright desktop/mobile journeys, Terraform format/validate/mock security assertions |
| SonarQube quality gate | Main push or manual | Generates LCOV, scans actual source, waits for server gate; missing server/token fails |
| Deploy AWS dev | Manual, main only | Repeats source/runtime/Sonar checks, protected environment approval, OIDC, digest image publication, High/Critical image rejection, SSM deploy, readiness/business acceptance, previous-image rollback |

The workflows have no AWS infrastructure apply path. Fork pull requests receive no deploy credentials. Only the deploy job requests the protected `dev` environment and OIDC role. Restrict branch/environment access in GitHub itself; YAML does not configure those server-side policies. Action majors are maintained by Dependabot; for a production organization, enforce approved immutable action commit SHAs and review updates under its supply-chain policy.

Source CI and a passing local integration test do not establish a cloud deployment. Record real run links and artifacts once executed. Deployment image scans include unfixed vulnerabilities and fail on High/Critical. Do not lower thresholds, add broad exclusions, or suppress security findings merely to pass the gate. Retain reports and resolve a finding or obtain a narrowly reviewed applicability decision first.

## SonarLint / SonarQube

`sonar-project.properties` declares the actual backend/frontend source and test roots and consumes `backend/coverage/lcov.info` and `frontend/coverage/lcov.info`. Tests are excluded from source indexing, not from execution. Generated code, build artifacts, and dependencies must not inflate source metrics.

The optional local SonarQube server is defined in `compose.quality.yaml` at `127.0.0.1:9191`. Run the backend and frontend coverage commands, start `sonar-db` and `sonarqube` with both Compose files, then run `node scripts/sonar-local.mjs`. The script creates a unique local admin password in ignored `work/sonar-admin-password`, uses a short-lived scanner token, revokes it, and saves the actual gate and issue responses. The 21 October 2026 local scan passed an evaluated gate with 89.3% new-code coverage, 0% new duplication and 0 new violations. Use `docker compose -f compose.yaml -f compose.quality.yaml down` to stop the quality services while retaining their volumes.

For GitHub, create a project with key `linked-in-node-and-aws` on an owner-managed SonarQube Server, configure a meaningful new-code definition and quality gate, and issue a project-scoped analysis token. For hosted GitHub runners the server must be reachable over trusted HTTPS with its authentication required. A laptop's `localhost:9191` is not reachable from a hosted runner; choose a secured reachable server or a dedicated trusted runner with private network connectivity. Never open an unauthenticated public SonarQube server to make a workflow pass.

Set repository variable `SONAR_HOST_URL` and repository secret `SONAR_TOKEN`. Protect the token from PR code and logs. The scan action waits on the real server gate (`sonar.qualitygate.wait=true`); a successful scanner upload alone is insufficient. Initially create a new-code baseline, review security hotspots, and inspect whether the gate includes coverage/duplication conditions and small-change exceptions. Report actual new/overall coverage separately. Do not claim a gate passed before running the server.

In VS Code, bind SonarQube for IDE to the same project using the extension's secure connection UI. This binding needs the account URL/token and is deliberately not committed. IDE diagnostics shorten feedback; only server analysis supplies the release gate. If enterprise gate rules exceed the current test coverage, improve tests and code rather than weakening rules.

## Releases, failures, and maintenance

Use [AWS dev](aws-dev.md) for exact account setup, reviewed Terraform plans, secret initialization, deployment variables, SSM access, rollback, and cleanup. Image manifests contain source SHA and both digests; release evidence belongs beside the requirement/Jira record. Keep migrations backward compatible so rolling images back is safe. Rehearse restoration before claiming a recoverable service.

For a red source check, fix the reported behavior or formatting and rerun the affected gate. For red acceptance, inspect the failing check plus relevant service logs and database invariants. For a red dependency/image gate, retain the finding and patch the affected dependency/base image. For a failed cloud health check, preserve the SSM output and inspect `/var/log/cloud-init-output.log` and Docker logs before retrying. Runbooks are part of the deliverable; untested recovery remains a documented limitation.
