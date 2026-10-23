# SAMS Syncing API

**Status:** Draft v0.1 for MyJourney owner review, followed by IT/SAMS approval.
**Date:** 23 October 2026. **Provider:** SAMS. **Consumer:** MyJourney.

This is a proposed contract, not a description of an available endpoint. Requirements reported by the MyJourney owner are distinguished below from proposed interface details that need IT/SAMS agreement. All examples are synthetic.

## Purpose and agreed scope

Synchronise authoritative SAMS student attributes into MyJourney so management can filter analytics by pillar, cohort, graduation information and student status, and identify groups needing more engagement.

- Include current and former students, including graduated, withdrawn, terminated and leave-of-absence statuses. Store their attributes; apply exclusions in reporting rather than silently dropping them during ingestion.
- Return newly created students and every student whose agreed attributes changed, including changes originating in related SAMS tables.
- Return the latest complete student record, rather than a sequence of change events. MyJourney does not require historical values or effective-date tracking.
- SAMS owns academic attributes. MyJourney overwrites those agreed attributes with the supplied values. Student lifecycle changes are represented by status updates; the owner's stated expectation is that SAMS does not delete students.
- For a student without a MyJourney account, create a minimal user with `username = student_id`. Okta supplies identity details when the student later signs in.
- The initial population is approximately 7,000 students across 14 years, according to the owner. Bootstrap uses a manual Excel export; ongoing pulls run twice daily at approximately 07:00 and 19:00. Singapore time and weekend operation remain to be confirmed.
- A failed sync emails the MyJourney operators for manual investigation and resolution.

**Out of scope:** implementation code, AWS provisioning, student history, bidirectional writes, synchronising Okta-owned identity fields, account deletion, reporting UI changes and automatic removal of access based on academic status.

## Proposed endpoint

```http
GET {SAMS_BASE_URL}/students/sync?last_update={checkpoint}
Accept: application/json
```

The route, parameter names and JSON field names are proposals. SAMS will confirm the environment URLs, deployed route, authentication, response encryption requirements, access permissions and network restrictions. Use HTTPS and server-to-server credentials; no credential or real student record belongs in this document. Reuse the existing integration profile only after IT confirms it applies to this endpoint.

| Parameter | Type | Requirement |
| --- | --- | --- |
| `last_update` | UTC timestamp | Required. The exact checkpoint from the successful bootstrap or previous successful sync; URL-encode it. It is not MyJourney's local run time. |

**Proposed time format:** RFC 3339 UTC with `Z`, retaining the source's agreed fractional-second precision without rounding. SAMS must confirm that this precision can distinguish the required checkpoints. Missing, malformed, unsupported or future checkpoints must be rejected rather than silently converted to a full sync.

## Selection and checkpoint guarantees

For input checkpoint **L**, SAMS chooses a completed source cutoff **U** and returns `next_last_update = U`.

1. The response covers source changes in **(L, U]**. A creation counts as a change. A change to any agreed attribute, including a related-table change or a cleared value, must make that student eligible.
2. Return each eligible student once, containing the latest agreed attribute values as of U. Multiple changes to one student may be collapsed into that one record.
3. U must represent a consistent, complete view of committed source data. No change may become visible later with a change timestamp at or before U and consequently fall out of subsequent requests.
4. The next request uses U as its lower checkpoint. Changes at U have already been included; changes after U are returned by a later request.
5. The response must be complete. Do not truncate a successful response or return a success-shaped partial result. A successful empty response still supplies a valid U.

These are required correctness guarantees for the proposed timestamp design, not verified SAMS capabilities. A wall-clock timestamp alone does not establish them. If SAMS cannot provide them, the teams must revise the contract to use a source-issued change cursor or another demonstrated no-gap mechanism before approval.

Start with one response containing all changed students. SAMS must confirm that the largest supported catch-up response fits its payload and timeout limits. Add pagination only if necessary; any paginated revision must retain one consistent cutoff across all pages and advance the checkpoint only after all pages succeed.

## Proposed student schema

Every listed key is required in each full record. A nullable field must be present with either its value or explicit `null`; omission is not the same as clearing a value.

| Field | Proposed type | Meaning and review requirement |
| --- | --- | --- |
| `student_id` | Nonempty string | Stable unique matching key, used unchanged as MyJourney's username. Preserve leading zeroes. SAMS/Okta must confirm matching, normalisation and whether IDs can ever change or be reused. |
| `pillar_code` | String or null | Authoritative pillar code. SAMS supplies the code definitions and meaning of null. |
| `cohort` | String or null | Authoritative cohort value. Intake/admission year is a candidate meaning, not yet agreed. |
| `student_status_code` | Nonempty string | Authoritative status code. SAMS supplies the complete vocabulary and definitions, including distinctions between suspension, leave and absence. No guessed enum is binding. |
| `graduation_date` | `YYYY-MM-DD` or null | Proposed graduation field. Expected versus actual graduation, whether both are needed, and null meaning must be resolved before finalising the schema. |
| `source_updated_at` | UTC timestamp | Latest source change time for any agreed attribute, including creation and related-table changes. Must be compatible with the selection guarantee and no later than U. |

**Proposed null policy:** explicit null clears the corresponding stored SAMS-owned attribute. Missing required keys, invalid values or duplicate student IDs fail the batch. The owner and SAMS must approve null semantics and distinguish unknown values from inapplicable values where needed.

## Proposed responses

Success uses HTTP `200`, including when nothing changed. JSON is shown as the logical payload; any required encrypted transport envelope needs separate confirmation.

```json
{
  "next_last_update": "2026-10-23T11:00:00.000000Z",
  "students": [
    {
      "student_id": "EXAMPLE-STUDENT-001",
      "pillar_code": "EXAMPLE_PILLAR",
      "cohort": "EXAMPLE_COHORT",
      "student_status_code": "EXAMPLE_STATUS",
      "graduation_date": null,
      "source_updated_at": "2026-10-23T10:30:00.000000Z"
    }
  ]
}
```

The `EXAMPLE_*` values illustrate shape only; they are not real identifiers or agreed code values. An empty result contains `"students": []` with a valid `next_last_update`.

| HTTP status | Proposed meaning | MyJourney action |
| --- | --- | --- |
| `400` | Invalid checkpoint or request | Keep checkpoint; notify operators. |
| `401` / `403` | Authentication or authorisation failure | Keep checkpoint; notify operators. |
| `410` | Checkpoint is outside SAMS's supported recovery range, if a retention limit exists | Stop; arrange an approved bootstrap/recovery. Do not silently skip ahead. |
| `429` | Rate limited | Bounded retry; honour `Retry-After` if supplied. |
| `5xx` / timeout | Source or transport failure | Bounded retry; notify operators if the run fails. |

Error payload proposal: `{"code":"INVALID_CHECKPOINT","message":"The checkpoint is invalid."}`. Messages must not expose credentials or student payloads. SAMS confirms actual error codes, retry limits and any checkpoint retention limit; `410` is unnecessary if checkpoints do not expire.

## Initial Excel bootstrap

1. SAMS supplies all in-scope students with the same field meanings as the API, plus a documented source cutoff L. A file-generation timestamp is usable only if SAMS guarantees that it represents a complete, consistent data snapshot for the incremental handover.
2. Treat student IDs and cohort/code values as text. Preserve leading zeroes and validate required columns, unique IDs, dates, statuses and nulls before import.
3. MyJourney imports the records and saves L as the sync checkpoint only when the import succeeds. A failed import must not establish a successful checkpoint.
4. The first API pull uses L. SAMS demonstrates that changes during export generation and transfer remain covered. Use the same academic-field mapping and validation for Excel and API ingestion.

The file's generation time, a student's `source_updated_at`, MyJourney's processing time and the global successful checkpoint are distinct concepts. Store and label them accordingly.

## MyJourney processing and ownership

Proposed minimal implementation plan, for later approval:

1. Allow one active sync. Read its saved checkpoint, fetch the complete response and validate the payload before writing.
2. In one database transaction, create missing users by student ID, update only agreed SAMS-owned attributes, and save the new checkpoint. Serialise application and reject a stale run if another run has advanced the checkpoint.
3. Provisioning must not record a login, grant staff/superuser permissions, create student content or bypass normal authentication. Preserve Okta-owned names/email and MyJourney-owned preferences/content.
4. On failure, roll back the database batch and keep the previous checkpoint. Email operators with safe run context, checkpoint and failure category. Do not include student payloads or credentials. Recipients remain to be configured.

Applying the same records again must not create duplicate users or alter unrelated fields. A valid empty response advances the checkpoint. Reuse the existing SAMS/HTTP client where compatible; place orchestration and transaction rules in one sync module, with persistence following the repository's existing structure. EventBridge and Step Functions invoke that module later; no new integration framework or parallel processing is proposed.

Reporting must separately adopt the authoritative SAMS fields. The inspected reference reports currently require a recorded login and nonblank names, so precreated students would be excluded by that filter. The eligible-student denominator and default status exclusions remain product decisions; provisioning does not itself change those reports. Latest-state reporting will regroup older activity using a student's current attributes.

## Acceptance scenarios for team review

| Scenario | Required result |
| --- | --- |
| New SAMS student after L | Returned once; a missing MyJourney user is provisioned by exact student ID. |
| Pillar, cohort, status, graduation or related-table change | Student returned with latest complete attributes, even if the main SAMS student table did not change. |
| Several changes to one student | One latest record as of U; no historical event processing required. |
| Explicit null | Clears only the agreed nullable attribute under the approved null policy. |
| No changes | Empty array; valid U is saved after validation. |
| Change exactly at U or during export/request | Included in the appropriate completed window; no gap between windows. |
| Request failure, malformed response or database failure | No checkpoint advance; failed batch rolls back; failed run emails operators. |
| Retry or overlapping invocation | No duplicate users, lost changes or checkpoint regression. |
| First Okta login after precreation | Existing user is reused and identity fields populated; no duplicate account. |
| Graduation, withdrawal or leave | Stored status updates; content remains; agreed report filters determine inclusion. |

## Decisions required before implementation

| Decision | Owner |
| --- | --- |
| Cohort meaning; graduation fields; complete codes; null semantics; stable ID matching | MyJourney owner and SAMS |
| Eligible population, adoption denominator and default report exclusions | MyJourney owner |
| Cutoff completeness, timestamp precision, joined-table change detection and bootstrap handover | SAMS API team |
| Route, URLs, authentication/encryption, limits, errors and recovery retention | IT and SAMS API team |
| Singapore schedule, weekend operation, email recipients and operational response expectations | MyJourney owner/operations |
| First-draft deadline and review date | MyJourney owner |

**Approval sequence:** MyJourney owner reviews this draft; IT/SAMS reviews and approves the final contract; implementation and operational sync begin afterwards. No approval or deployment is implied by this document.
