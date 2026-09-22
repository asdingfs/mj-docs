# Audit and unresolved items

Development reference: `origin/feature/ui-improvement`, commit `737a3e5daa5553a62319ccebcc1af0a99656dca4`, verified against the remote branch tip on 22 September 2026. Original docs: `91faef4f341525c02ff2704d597293dc85ae6443`.

The working tree in `mj-be` differs from this branch. Read branch objects explicitly. The owner confirmed that the original Create a Chapter page and its cropping flow represent current development; the earlier draft's title-only flow was incorrect. Neither source checkout nor Git metadata was changed by this documentation task.

## Findings reflected in the draft

- Chapter creation supports an optional 3:4 cropped card cover. The original annotated screenshot sequence is retained with clearer steps and alternative text.
- Edit Chapter changes the title and card cover; Edit Draft opens the content editor.
- The Chapter banner is separate and uses a 16:9 crop in Canvas Settings → Chapter Banner. Without a dedicated card cover, the banner can supply the card fallback.
- Story creation/editing supports a 16:9 cropped header cover. Chapter and Story card/header covers are staged until Create/Save; accepting a Chapter banner crop starts the upload immediately.
- Draft content blocks are versioned; Chapter title, cover, banner, and canvas settings remain shared. Avoid promising that all edits remain private until publication.
- Story and Chapter publishing are independent. A public Story lists published Chapters only; copying a link does not publish.

## Open items

| Item | Owner | Evidence needed to close |
| --- | --- | --- |
| Other deployed behaviours | Product owner | Confirmation where the branch and deployed UI differ; original Chapter creation is already confirmed |
| Remaining screenshot gaps | Documentation owner | Matching Story creation/editing, Edit Chapter, and Chapter Banner captures |
| Chapter shared-details behaviour vs broad UI privacy message | Product owner | Confirm intended behaviour; documentation currently describes the branch implementation |
| Guide About stubs: dream journey, Champions, verification flow | Product owner | Approved programme/process facts; paths retained |
| Help Center generic content | Documentation owner | Separate approved rewrite; templates are not verified MyJourney guidance |
| Changelog template entries | Product owner | Actual release facts; hidden navigation is not private |
| Live GitBook connection | Repository owner | Verify mapping, branch, native preview, and publication settings before remote integration |

The first review updates the 16 scoped Guide pages. Remove closed items instead of appending progress logs.
