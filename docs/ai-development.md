# Directing Codex and reviewing generated code

The role description mentions Claude Code. This portfolio practices the same specification, implementation and review responsibilities with the Codex app, as requested. Approximately 95% generated application code is a workflow target, not an audited measurement. A line count cannot reliably distinguish generated, adapted and human-directed work. This migration reuses reference assets/behavior; disclose that instead of implying every line was generated from scratch.

Open this repository in Codex. Repository instructions live in `AGENTS.md`; deeper requirements and acceptance live in `docs/specs`. Codex reads applicable repository instructions, while prompts define the current outcome. This follows [OpenAI's AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md), consulted October 21, 2026. Other spec/review filenames here are our project conventions.

For each change, first state the requirement, contract, threat/failure cases and evidence needed. Ask a builder to implement the smallest coherent slice. Give a separate critic fresh context with the requirements and actual output, without the builder's self-assessment. The critic names a blocking defect with a reproducible example. Repair, rerun relevant checks and record the result. Human architectural judgment remains necessary even when the agent writes most code.

Use [builder](prompts/builder.md) and [critic](prompts/critic.md) prompts. Update [traceability](traceability.md) and [review records](reviews.md) for each completed slice. Record prompts/agent roles and Git commits, not a fabricated generation percentage. Explain “I directed and validated AI-generated work” and demonstrate a specific bug caught by a critic.

The architect should review capability boundaries, API compatibility, deployment/security tradeoffs and migration strategy before broad implementation. The developer checks generated code for authorization bypasses, SQL injection, incorrect async behavior, exposed secrets, missing negative tests and unsupported claims. Automation provides repeatability; it does not decide whether a requirement is correct.
