# Component Migration Order

## Overview

If migrating or rewriting this application, components should be addressed in the following order based on dependency relationships.

## Migration Order

### Phase 1: Shared Utilities (No Dependencies)

1. **`utils/` package** — No internal dependencies
   - `time_since.go` — Pure utility
   - `github_data.go` — Data structure definition
   - `response.go` — HTTP response helper

### Phase 2: Business Logic (Depends on utils)

2. **`pull_requests/` package** — Depends on `utils`
   - `check_pr.go` — Core PR evaluation logic
   - `complete_check.go` — Completed check handling
   - `none_completed_check.go` — Pending check handling

3. **`commit/` package** — No internal dependencies (only go-git)
   - `commit.go` — Git operations

### Phase 3: Route Handlers (Depends on Phase 1 + 2)

4. **`routes/` package** — Depends on `utils`, `pull_requests`, `commit`
   - `init.go` — Route registration
   - `check_pr.go` — Check PR endpoint
   - `retrigger_checks.go` — Retrigger endpoint

### Phase 4: Application Initialization (Depends on Phase 1-3)

5. **`init_app/` package** — Depends on `routes`, `commit`, `utils`
6. **`main.go`** — Depends on `init_app`, `utils`

### Phase 5: Slackbot (Independent Service)

7. **`slackbot/app.py`** — Depends only on API via HTTP
   - Can be migrated independently after API is stable

### Phase 6: Infrastructure

8. **Helm chart** (`deploy/`) — Update after both services are migrated
9. **CI/CD workflows** (`.github/workflows/`) — Update for new build/deploy requirements

## Key Principle

The slackbot communicates with the API only via HTTP, making the two services independently migratable. The API's internal packages should be migrated bottom-up (utils → business logic → routes → initialization).

## Cross-References

- [Modules](../reference/modules.md)
- [Dependencies](../architecture/dependencies.md)
