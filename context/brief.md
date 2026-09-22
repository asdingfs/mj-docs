# Brief: MyJourney student documentation

**In one line:** A visual, GitBook-compatible documentation repository for MyJourney students so that they can find features, recognise controls, and complete tasks independently.
**Owner:** MyJourney documentation owner (user) · **Deliverable:** Markdown guide and maintenance context · **Due:** No fixed deadline · **Status:** Draft v2 for review · **Date:** 22 September 2026

## 1. Background: why this, why now

MyJourney already has a documentation repository with Guide, Help Center, and Changelog spaces. Much of the Guide is empty, while Help Center and Changelog include generic template content. The owner has verified the original chapter-creation walkthrough, including its crop flow, against current development. Students need useful instructions now, supported by a repeatable way to identify later changes.

## 2. Objective

Give every first-release task a discoverable guide with code-supported steps, clear outcomes, and a record of the sources that must be reviewed when implementation changes. The broader goal is student confidence: readers should spend their attention on presenting their experiences, rather than guessing how the interface works.

## 3. Audience

The primary reader is a student using MyJourney to build and share their experiences. They need to locate specific controls and understand what an action changes. Staff and faculty may later use the same guide to support students. This release does not assume administrative access or familiarity with the implementation.

## 4. Core message

Capture an experience in a Chapter, arrange relevant Chapters into a Story, and check what readers will see before sharing it.

## 5. Deliverable and scope

Produce task-oriented Markdown pages in the existing Guide structure, with existing annotated screenshots where the relevant controls remain consistent with the code. Prepare a rendered local preview and exact file diff outside the live repository for approval. Follow the documentation work with concise reusable context and an explicit source-to-page map.

**In scope:** Finding, creating, editing, organising, publishing, and sharing Stories and Chapters; source records; cover settings; common saving and visibility questions; auditing adjacent template content; researching GitBook integration.

**Out of scope:** Changes to `mj-be`, invented product policies, credential collection, unapproved live publication, and a complete rewrite of other student features in this first release.

## 6. Supporting content

Use `origin/feature/ui-improvement` as the development reference: read templates for control labels, JavaScript for interactions, and backend services for persistence and visibility. Do not substitute working-tree files for the named branch. Existing specifications provide supporting context but cannot establish that an undeployed feature is available. Explain separate Story and Chapter publication states, crop confirmation versus saving, and the distinction between a 3:4 Chapter card cover and the separate 16:9 Chapter banner or Story header cover.

Reuse suitable repository screenshots with useful alternative text and captions. Retain the owner-verified chapter-creation screenshots. Record other capture gaps; never manufacture product screenshots from code. A source map connects each drafted page to the files used to verify it.

## 7. Tone, style and references

Friendly: Speak as a helpful sidekick, with occasional short encouragement after practical instructions.

Clear: Use the interface's exact labels, short numbered steps, and explicit outcomes.

Professional: Explain publishing and data-loss consequences precisely, with no jokes obscuring them.

Visual: Place a relevant annotated screenshot beside the task it explains and describe the target control in text as well.

Retain the existing journey metaphor, but avoid inventing institutional promises or programme details.

## 8. Constraints and mandatories

Treat `mj-be` as read-only: inspect files without running application commands that could write there. Preserve current documentation paths, assets, and GitBook space identities. Keep root `context/` outside every published content directory and avoid public links to it. The user must preview and approve the proposed changes before they are applied. Committing, pushing, and publishing the approved result are permitted, subject to verified sync behaviour and the approved scope.

## 9. Timeline

There is no fixed deadline. Work proceeds through code audit, page drafting, context extraction, local checks, preview, and user review. Verify the actual GitBook connection before a remote change could affect published content. Request fresh captures only if the owner later chooses to supply them.

## 10. Success metrics

Review the first-release tasks against the draft pages. Check local navigation and asset references, retain existing URLs, and verify that published content does not reference private context. The maintenance checker should identify affected pages when mapped source files change. These checks establish review readiness; they do not substitute for deployed-interface or GitBook-native verification.

## 11. Assumptions and open questions

Assumed: Use English with British spelling, following the existing guide. Owner: documentation author, under the user's delegated writing choices.

Assumed: Use the checks in section 10 as initial acceptance criteria. Owner: documentation author; user reviews the result.

Open: Whether the deployed interface matches this code revision, and whether the live GitBook branch, space mapping, and permissions support native previews. Owner: user. Record screenshot gaps without treating them as verified captures.

## 12. Next step

The documentation author will draft the scoped pages directly from repository evidence, then derive maintenance instructions and source mappings from that work. Present the staged preview, exact diff, and unresolved verification items to the user for approval before applying changes.
