# Components

## API Service Components

### 1. Main Entry Point (`api/main.go`)
- Initializes environment variables, GitHub client, and git repository
- Creates the `GitHub` struct aggregating all configuration
- Starts the Gin HTTP server on port 3000

### 2. Init App Package (`api/init_app/`)

| File | Function | Responsibility |
|------|----------|---------------|
| `init_env_vars.go` | `InitEnvVars()` | Loads and validates `GITHUB_TOKEN`, `GIN_MODE`, `GITHUB_URL`, `GITHUB_USER` |
| `init_gh.go` | `InitGH(token)` | Creates authenticated GitHub API client via OAuth2 |
| `init_commit.go` | `InitCommit(url)` | Opens or clones the target git repository |
| `init_app.go` | `InitGin(mode, gh)` | Configures Gin engine with logger and routes |

### 3. Routes Package (`api/routes/`)

| File | Function | Responsibility |
|------|----------|---------------|
| `init.go` | `InitRouter(r, gh)` | Registers all route handlers; parses owner/repo from URL |
| `init.go` | `InitLogger(r)` | Configures Zap structured logging middleware |
| `check_pr.go` | `InitGetCheckPR(r, client, owner, repo)` | `GET /check-pr?id=` — queries GitHub check runs for PRs |
| `retrigger_checks.go` | `InitGetRetriggerChecks(r, gh)` | `GET /retrigger-checks/:branch` — pushes empty commit to retrigger CI |

### 4. Pull Requests Package (`api/pull_requests/`)

| File | Function | Responsibility |
|------|----------|---------------|
| `check_pr.go` | `CheckPRStatus(checks, timeFn)` | Evaluates all check runs and returns invalid checks |
| `check_pr.go` | `CheckPendingStatus(c, client, prNum, timeFn)` | Checks combined status for pending PRs |
| `check_pr.go` | `CheckCombinedStatus(status, pendingFn)` | Evaluates combined commit status |
| `check_pr.go` | `GetBranch(client, owner, repo, prNum)` | Retrieves base branch for a PR |
| `complete_check.go` | `CompletedCheck(check, prStatus)` | Handles completed check conclusions |
| `none_completed_check.go` | `InProgressCheck(check, prStatus, timeFn)` | Handles in-progress checks |
| `none_completed_check.go` | `QueuedCheck(check, prStatus, timeFn)` | Handles queued checks |

### 5. Commit Package (`api/commit/`)

| File | Function | Responsibility |
|------|----------|---------------|
| `commit.go` | `CloneRepo(url)` | Shallow clones the repository to `/app/environments` |
| `commit.go` | `OpenRepo()` | Opens an existing local repository |
| `commit.go` | `FetchBranch(r, branch)` | Fetches a specific branch from origin |
| `commit.go` | `CheckoutBranch(r, branch)` | Checks out a branch with force |
| `commit.go` | `PushCommit(r, user, token, branch)` | Creates and pushes an empty commit |

### 6. Utils Package (`api/utils/`)

| File | Function | Responsibility |
|------|----------|---------------|
| `github_data.go` | `GitHub` struct | Aggregates GitHub configuration (token, URL, user, repo, client) |
| `response.go` | `SendResponse(c, response)` | Standardized JSON response helper |
| `time_since.go` | `TimeSince(startedAt, timeFn)` | Calculates if a check is younger/older than 10 minutes |

## Slackbot Service Components

### 1. App Entry Point (`slackbot/app.py`)

| Component | Responsibility |
|-----------|---------------|
| Configuration loading | Reads env vars, normalizes API URL, compiles regex patterns |
| `checks_config.json` | Defines patterns for categorizing CI check names |
| `handle_pull_request_message()` | Main event handler — detects PR links, queries API, posts reactions |
| `get_status(ids)` | Calls the Go API's `/check-pr` endpoint |
| `post_reaction(data, ts)` | Orchestrates success/fail reactions |
| `post_success(data, ts)` | Adds sparkles emoji for all-pass |
| `post_fail(data, ts)` | Adds x emoji and posts failure summary |
| `post_pending_recent(data, ts, ids)` | Schedules retry for recent pending checks |
| `retry_later(ids, ts, ms)` | Timer-based retry mechanism |
| `build_checks_summary(data)` | Formats check results into Slack message |
| `get_configured_checks(all_checks)` | Categorizes checks against config patterns |

## Cross-References

- [System Overview](system-overview.md)
- [API Reference](../reference/api-reference.md)
- [Program Structure](../reference/program-structure.md)
