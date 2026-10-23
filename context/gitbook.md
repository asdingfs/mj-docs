# GitBook integration findings

Verified 23 October 2026 against official GitBook documentation. Keep live-account observations distinct from product documentation.

## Configuration and preservation

- `gitbook-docs.yaml` defines site structure and maps spaces to repository directories. `.gitbook.yaml` configures one space; `SUMMARY.md` defines its navigation.
- Preserve existing `key` values. Changing a key creates a replacement space and detaches the original; titles and paths can change without replacing it.
- `hidden: true` hides a space from site navigation. GitBook's documented schema does not support `draft` on sections or spaces; Draft is a UI setting and does not set account permissions.

Source: [Content configuration](https://gitbook.com/docs/docs-as-code/git-sync/content-configuration).

Local mapping: Guide (`space-1`, `product`) → `./guide`; Changelog (`space-2`, hidden) → `./changelog`; Help Center (`space-3`, hidden) → `./help`; Contracts (Private) (`space-4`, `api-reference`) → `./api-docs/api-reference`, under MyJourney - APIs (`section-2`, `api`). Preserve these keys and paths.

## Current API site and access

On 23 October 2026, commit `e50a4ec` synced successfully from `asdingfs/mj-docs` on `main`. The GitBook UI shows **SAMS Syncing API** at `sams-syncing-api` inside Contracts (`space-4`), under MyJourney - APIs (`section-2`). The site `site_Yi3HL` remains unpublished and MyJourney - APIs remains Draft. The Contracts space still contains the Petstore OpenAPI sample pages alongside the SAMS contract.

The Contracts Share panel showed inherited organisation access (1 of 1 members), the MyJourney Team administrator, and guest-link invites off. This is not an account-specific ACL. An unpublished site and Draft section keep the content out of public publication; repository and workspace access are separate. See [audit.md](audit.md) before claiming exclusive account access.

## Page placement, sync and review

To add a page, put its Markdown inside the target space's mapped `content.directory` and add it exactly once to that space's `SUMMARY.md`. The SAMS contract uses `api-docs/api-reference/`; its page link belongs in `api-docs/api-reference/SUMMARY.md`. Reuse the existing site section and space; do not make a new GitBook key for each page. Keep `context/` outside mapped directories and do not link it from published pages.

Git Sync uses a selected repository and branch. A push or merge to that branch can update GitBook immediately; initial sync can replace content, so verify the connection and mapping first. Treat it as a publication boundary. GitBook PR previews require a published site and GitHub app PR-read access; authenticated-access sites do not support them. A local render approximates Markdown but does not certify GitBook rendering.

Sources: [Enabling GitHub Sync](https://gitbook.com/docs/docs-as-code/git-sync/enabling-github-sync), [Monorepos](https://gitbook.com/docs/docs-as-code/git-sync/monorepos), [GitHub pull request preview](https://gitbook.com/docs/docs-as-code/git-sync/github-pull-request-preview), [Quickstart](https://gitbook.com/docs/getting-started/quickstart).
