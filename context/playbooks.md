# Task playbooks

## Clarify scope

Adapted from the user-invoked `brain-dump-to-brief` skill: establish audience, outcome, scope, constraints, approvals, and timing before a broad new initiative. Confirm uncertainties rather than inventing product facts. A small page correction does not require another full interview. The project brief records the current direction; reopen it only when that direction changes.

## Verify and write a feature guide

Start with the reader's task and templates from the user-designated branch. Resolve its commit and read Git objects; do not assume the checked-out files match that branch. The original Create a Chapter walkthrough and its cropping screenshots are owner-verified references. Follow the UI handlers into backend services for consequential actions. Prefer implemented behaviour over proposals; flag conflicts rather than editing the application. Map the page to the files that substantiate it. Treat filenames and code terminology as research aids, not student-facing language.

Write an outcome, prerequisites, short numbered steps with exact UI labels, an expected result, and a relevant next link. State public visibility, shared changes, and destructive consequences at the action. Use encouragement sparingly. Do not invent support contacts, student programmes, verification policies, or release dates.

## Use screenshots

Inspect existing images before reuse. Match the relevant controls against code and note capture limitations in the register. Retain useful original annotations. Give every image alternative text naming the control and a caption explaining the task. Never fabricate a product screenshot from code or use a generated interface as evidence.

For new captures supplied later, use a demo state, confirm the matching version, and annotate only controls needed for the task. Keep original and annotated assets traceable. Prefer numbered callouts with matching instructions; do not rely solely on colour. Check mobile readability. An outdated screenshot must not carry current instructions without an explicit discrepancy.

## Research GitBook integration

Adapted from the Research skill: use official documentation, trace claims to primary sources, and retain a concise cited note. Use independent background research when available and useful. Keep live-account observations separate from documentation claims. Preserve the current space keys and paths. Verify the actual synced branch before any remote action.

## Check and review

Run `scripts/check_docs.py` against the candidate with the explicit code-root path. Review affected pages and their images in the local content preview. The preview approximates Markdown content, not GitBook's renderer. Use GitBook's native PR preview when the existing connection supports it. Present remaining limitations alongside the exact diff.

No scheduled monitor is configured. The checker is an on-demand review aid; it cannot detect every semantic change or announce updates by itself.
