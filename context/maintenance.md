# Maintenance and approval rules

## Every task

1. Read the context index and check repository status. Keep `mj-be` read-only, including generated files and Git metadata. Use read-only file inspection; do not run its application commands.
2. Run `python3 scripts/check_docs.py --code-root ../mj-be`. It reads the named branch in the source map, not the working tree. Confirm branch freshness with read-only `git ls-remote origin refs/heads/feature/ui-improvement` and compare its SHA to the local remote-tracking ref. Do not fetch or switch branches inside `mj-be`; if the object is unavailable, use an isolated reference copy. Source changes are review signals, not proof of changed behaviour.
3. Draft outside this checkout. Preserve unrelated edits, existing page paths, asset paths, navigation, and GitBook space identities. Include any proposed deletion or structural change explicitly in review.
4. Read source files with `git show origin/feature/ui-improvement:<path>` or extract that revision outside the repository. A dirty working tree can contain an older implementation even when HEAD is current. Verify exact labels in templates and interactions in JavaScript; verify visibility and persistence in backend services. Record conflicts with screenshots or specifications. Code inspection does not establish deployed behaviour.
5. Update affected documentation, source dependencies, screenshot register, and unresolved audit items together. Update fingerprints only after reading the changed sources and reviewing the corresponding prose. Never clear a drift report by blindly refreshing hashes.
6. Run the checker against the candidate. Show a rendered content preview, exact diff, and remaining gaps. Apply only what the owner explicitly approves. If the candidate changes after review, show the new diff.
7. Before applying, check that the original files still match the review baseline; reconcile newer edits instead of overwriting them. Before remote publication, verify the connected branch and content mapping. A synced-branch push or merge may publish immediately.

## Keep context lean

Maintain these files during every task, before handoff. Edit existing facts in place; remove superseded decisions and closed audit items. Give each rule one home and link to it elsewhere. Store source paths and concise findings rather than copied code, tool logs, or conversation transcripts. Keep portable task procedures here; do not copy every installed skill or machine-specific tool configuration.

Keep the index under 250 words and individual playbooks under 600 words. Split only when a distinct task needs its own guidance. Treat these as review limits, not reasons to omit essential constraints. Keep the brief and research notes out of the default reading path. Revisit GitBook research before changing integration settings.

For every unresolved item, record its owner and what evidence closes it. At handoff, report changed pages, checks, context changes, and open items. Git history supplies the historical record; context describes the current working state.
