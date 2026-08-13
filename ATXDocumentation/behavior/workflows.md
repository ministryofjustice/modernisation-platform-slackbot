> ⚠️ **Early Access**: Behavior documentation is in early access. Please review critically.

# Workflows

## Workflow 1: PR Check Status Query (API — `GET /check-pr`)

**Entry Point**: `routes/check_pr.go:InitGetCheckPR`

```
1. Receive GET request with ?id=<comma-separated PR IDs>
2. Split IDs by comma
3. For each PR ID:
   a. Call GitHub API: ListCheckRunsForRef("refs/pull/{id}/head")
   b. If GitHub API error → return error response
   c. Evaluate check statuses via CheckPRStatus()
   d. If all checks pass (empty result) → skip this PR
   e. Get branch name via GetBranch()
   f. Append PR check results to response
4. Return aggregated PR check statuses as JSON
```

## Workflow 2: PR Message Handling (Slackbot — `handle_pull_request_message`)

**Entry Point**: `slackbot/app.py:handle_pull_request_message`

```
1. Receive Slack message matching repository PR URL pattern
2. Extract PR ID(s) from message text
3. Call API: GET /check-pr?id=<ids>
4. Attempt immediate reaction:
   a. If no invalid checks → add ✨ emoji → DONE
   b. If any configured check failed → add ❌ emoji + post summary → DONE
5. Attempt pending-recent reaction:
   a. If configured checks pending with RetryInNanoSec > 0:
      - Add 🔄 emoji
      - Post summary
      - Schedule retry timer
      - DONE
6. Check for queued-too-long:
   a. If configured checks queued > 10 min:
      - Add ⏳ emoji
      - Post blocking message
      - DONE
7. If configured checks still pending (not queued):
   - Add ⏳ emoji
   - Post "still running" message
```

## Workflow 3: Retry Timer (Slackbot — `retry_later`)

**Entry Point**: `slackbot/app.py:retry_later`

```
1. Wait for calculated delay (RetryInNanoSec / 1e9 * 1000 + 10 ms)
2. Re-query API: GET /check-pr?id=<ids>
3. Attempt reaction:
   a. If success or fail → remove 🔄 emoji → DONE
4. If still pending after retry:
   - Remove 🔄 emoji
   - Post "still pending" message
   - Add ⏳ + ⚠️ emojis
```

## Workflow 4: Retrigger Checks (API — `GET /retrigger-checks/:branch`)

**Entry Point**: `routes/retrigger_checks.go:InitGetRetriggerChecks`

```
1. Receive GET request with :branch parameter
2. Open existing local repo (or clone if not present)
3. Fetch the specified branch from origin
4. Force-checkout the branch
5. Push an empty commit with force-with-lease
6. (No success response currently sent)
```

## Cross-References

- [Business Logic](business-logic.md)
- [Sequence Diagrams](../diagrams/behavioral/)
