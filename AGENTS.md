# Marketplace working agreement

Read README.md, CONTRACT.md, docs/specs/requirements.md and docs/architecture.md before changing behavior. Preserve four capability boundaries and service-owned databases. Never edit the original Java project. Generated plans and evidence must describe actual execution.

Use strict TypeScript and NestJS dependency injection. Keep React components in separate files; API calls belong in services, domain types in types, auth in contexts, reusable effects in hooks, page composition in routes. Never replace domain persistence with browser storage.

For each requirement, update its specification, traceability row and meaningful test. Keep changes reviewable. An independent critic must review security, contracts, failure paths and actual output; builders cannot approve their own work. Record the largest gap and the repair in docs/reviews.md. Compare visuals anonymously where possible and behavior through runnable tests. Never reduce checks to claim a win.

Run npm run check, npm test, npm run build and npm run acceptance as appropriate. Preserve failed evidence when it explains a repair. External GitHub/Jira/Sonar/AWS integrations need actual execution to be described as verified. Do not manufacture coverage or AI-generation percentages. Codex is the development agent; 95% is a target, not a measured result.

Local uses compose project linked-in-node-local and ports 8180–8184, 5183, 55432, 19092. AWS dev uses its own state, secrets and data. Local scripts must never invoke AWS. Keep .env and Terraform state/plans out of Git. Cloud provisioning requires approval of the concrete saved plan and current cost estimate; preparation is authorized. Do not send messages or invent external repository destinations.
