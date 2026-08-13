> ⚠️ **Early Access**: Behavior documentation is in early access. Please review critically.

# Error Handling

## API Service Error Handling

### Startup Errors (`main.go`)
- Missing/empty `GITHUB_TOKEN` → `log.Fatal`
- Missing/empty `GITHUB_URL` → `log.Fatal`
- Missing/empty `GITHUB_USER` → `log.Fatal`
- GitHub client initialization failure → `log.Fatal`
- Git repository clone/open failure → `log.Fatal`
- Port binding failure → `log.Fatal`
- Server start failure → `log.Fatal`

All startup errors terminate the process immediately.

### Request-Level Errors

**`GET /check-pr` (`routes/check_pr.go`)**:
- GitHub API error → returns GitHub's HTTP status code with error message
- Branch lookup error → returns 500 with error message

**`GET /retrigger-checks/:branch` (`routes/retrigger_checks.go`)**:
- Clone failure → returns status 0 with error (BUG: should be proper HTTP code)
- Fetch failure → returns status 0 with error
- Checkout failure → returns status 0 with error
- Push failure → returns status 0 with error

### Panic Recovery
Gin middleware `ginzap.RecoveryWithZap(logger, true)` catches panics in request handlers and logs them with stack traces instead of crashing the server.

## Slackbot Error Handling

### Startup Errors
- Missing `SLACK_BOT_TOKEN` → raises `KeyError` (Python env var access)
- Missing `SLACK_SIGNING_SECRET` → raises `KeyError`
- Missing `SLACK_APP_TOKEN` → raises `KeyError`
- Missing `GITHUB_URL` → raises `KeyError`
- Missing/invalid `checks_config.json` → raises `FileNotFoundError` or `JSONDecodeError`

### Runtime Errors
- API call failure (`get_status`) → `requests.raise_for_status()` raises `HTTPError` — unhandled, will log exception
- Slack API errors (reactions, messages) → Slack Bolt framework handles logging
- Timer callback errors → exceptions in daemon thread, logged but lost

### Error Recovery Patterns

| Pattern | Location | Behavior |
|---------|----------|----------|
| Fatal exit | `main.go` startup | Process terminates, Kubernetes restarts |
| HTTP error response | Route handlers | Client receives error JSON |
| Panic recovery | Gin middleware | Logs stack trace, returns 500 |
| Unhandled exception | Slackbot daemon threads | Thread dies silently |
| Slack API rate limit | Slack Bolt framework | Framework handles backoff |

## Missing Error Handling

1. No timeout on GitHub API calls from the Go API (relies on default HTTP client timeout)
2. No circuit breaker between slackbot and API service
3. No retry logic for failed Slack API calls (emoji reactions, message posts)
4. No error response for successful retrigger-checks operations

## Cross-References

- [Workflows](workflows.md)
- [Security Patterns](../analysis/security-patterns.md)
