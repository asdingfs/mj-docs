# GitBook integration findings

Verified against current official GitBook documentation on 22 September 2026. Research only; neither repository nor the GitBook account was changed.

## Configuration and preservation

- `gitbook-docs.yaml` defines site structure and maps spaces to repository directories. `.gitbook.yaml` remains supported and configures an individual space; it is not an obsolete alternative to the site file. `SUMMARY.md` defines a space’s navigation.
- Space identity depends on `key`. Changing an existing key creates a replacement space with a different ID and detaches the original. Restoring the old key does not restore that original space identity. Keep existing keys permanently.
- `hidden` hides a space from site navigation; it does not establish a private publishing boundary.

Source: [Content configuration](https://gitbook.com/docs/docs-as-code/git-sync/content-configuration).

Local observation: `mj-docs/gitbook-docs.yaml` maps Guide (`space-1`, URL path `product`, default) to `./guide`; Changelog (`space-2`, hidden) to `./changelog`; and Help Center (`space-3`, path `help`) to `./help`. Preserve these keys and initial mappings.

## Keeping context unpublished

Each mapped space syncs only its assigned directory; sibling directories are unavailable through that space’s `root` setting. Keep assets inside their respective mapped directories. If moving a directory later, update files and mapping in the same commit while retaining the key.

Source: [Monorepos](https://gitbook.com/docs/docs-as-code/git-sync/monorepos).

Application to this repository (inference): keep `context/` at the repository root, beside `guide/`, `help/`, and `changelog/`, with no mapping and no links from published pages or summaries. This keeps it outside those published content roots, provided the live account uses the shown mapping. Merely hiding context in navigation would not suffice. Repository visibility remains separate: unpublished context is readable wherever repository access permits. Do not store secrets there.

## Review and preview

GitBook generates a preview status URL for a GitHub PR targeting a synced branch when its GitHub app has the required PR read permissions. Preview readers need a GitBook account. The docs site must be published; authenticated-access sites do not support Git Sync PR previews. Fork previews are disabled by default.

Source: [GitHub pull request preview](https://gitbook.com/docs/docs-as-code/git-sync/github-pull-request-preview).

GitBook change requests support split or inline content diffs. Merging applies changes to live docs immediately; subsequent corrections require another change request.

Source: [Change requests](https://gitbook.com/docs/collaborate/change-requests).

GitBook’s quickstart also documents desktop/mobile previews and says merging a repository PR updates the GitBook content and the live site when published.

Source: [Quickstart](https://gitbook.com/docs/getting-started/quickstart).

## Sync and publication implications

Git Sync connects a selected repository and branch, then synchronizes commits back to GitBook. Initial GitHub-to-GitBook sync can replace existing content, including replacing a section with empty repository content. Inspect the current connection before attempting any setup or reconfiguration. The setup article mentions `docs.yaml`, while the dedicated configuration and monorepo articles consistently specify `gitbook-docs.yaml`; preserve the existing file and use the dedicated configuration reference.

Source: [Enabling GitHub Sync](https://gitbook.com/docs/docs-as-code/git-sync/enabling-github-sync).

Recommended review workflow: prepare a separate candidate and exact diff; review rendered pages; apply approved changes to a dedicated branch; use a same-repository PR for GitBook’s native preview; obtain approval of the final diff and preview before merging into the synced branch. Treat a direct push to that branch as a possible publication action, not a harmless backup.

Not verified from local files: GitBook account/site URL, current connected branch, actual live content mapping, publication/audience settings, GitHub app permissions, branch protections, merge rules, or preview availability. A local render is useful for content review but cannot certify GitBook-specific rendering or live integration behavior.
