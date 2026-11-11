# Independent installed-output review · November 10, 2026

Reviewer: separate non-building critic spawned with `fork_turns=none`. Verdict: **accepted; no blocking finding**.

The reviewer independently reran17 focused tests after the CSS repair. All92 managed files match the committed-source plan at `841f0cf6484d6d6e4d7d752c2fcde9341a2f635f`. Final sanitized and actual HTTP output contains137 unique question targets,24 incident targets and all161 source targets; all companion local link/fragment targets resolve, and search stays scoped to NodeJs/AWS. Raw HTML remains disabled; hostile anchor/script input stays literal. The scoped CSS rule adds block display and88px clearance only to validated stable-card anchors.

Preservation was independently checked against306 baseline hashes:20 intentional existing-file changes,286 protected files unchanged. The final full-suite log records99 tests with98 passing and one optional skip; JavaScript15 pass. The original84 numbered-lesson action/reference assertions remain, with separate supplemental counts, table assertions and reference-fallback checks.

Largest gap and repair: explicit card anchors were escaped; the narrow parser restores real targets without enabling raw HTML. Browser inspection then exposed sticky-header obstruction; the scoped scroll clearance repairs the visible heading.

The builder reported visible index/question/source/search checks. The critic independently verified corresponding live HTTP output. Separate incident/lesson browser click-through remained unobserved after capture failure; runnable final-render tests verify those targets. This limitation is recorded rather than presented as complete browser coverage.
