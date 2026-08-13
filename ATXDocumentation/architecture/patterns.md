# Architectural Patterns

## Design Patterns Identified

### 1. Service Separation Pattern
The application separates concerns into two independently deployable services:
- **API Service**: Pure data retrieval and processing (GitHub API interactions)
- **Slackbot Service**: Event handling and user-facing communication

### 2. Dependency Injection via Struct Composition
The `utils.GitHub` struct aggregates all GitHub-related configuration and is passed through the application:
```go
type GitHub struct {
    Mode, Token, URL, User string
    Repo   *git.Repository
    Client *github.Client
}
```
This struct is created once in `main.go` and threaded through to route handlers.

### 3. Functional Options / Time Injection
Time-dependent functions accept a `getTimeSince func(time.Time) time.Duration` parameter, enabling testability:
```go
func CheckPRStatus(checks *github.ListCheckRunsResults, getTimeSince func(time.Time) time.Duration)
```

### 4. Event-Driven Architecture (Slackbot)
The Slack Bolt framework uses event decorators to handle incoming messages:
- `@app.message(PULL_URL_PATTERN)` — pattern-matched message handler
- `@app.event({"type": "message", "subtype": "..."})` — event type handlers

### 5. Retry with Timer Pattern
The slackbot implements a delayed retry mechanism for pending checks:
```python
timer = threading.Timer(retry_in_ms / 1000.0, _retry)
timer.daemon = True
timer.start()
```

### 6. Builder/Initialization Pattern
The `init_app` package separates initialization concerns into discrete functions called sequentially from `main()`.

## Anti-Patterns Identified

### 1. Hardcoded Paths
The commit package hardcodes `/app/environments` as the repository path, coupling to the container filesystem structure.

### 2. Missing Error Propagation
In `retrigger_checks.go`, error responses use `Status: 0` instead of proper HTTP status codes.

### 3. Synchronous Blocking Operations
The retrigger-checks endpoint performs git clone/fetch/push synchronously, blocking the request thread.

## Framework Patterns

### Gin Framework Usage
- Middleware chain: `ginzap.Ginzap` → `ginzap.RecoveryWithZap` → route handlers
- Route registration via engine method calls (`r.GET(...)`)
- Context-based request handling

### Slack Bolt Usage
- Socket Mode (WebSocket) for receiving events
- Event-based message handling with regex pattern matching
- Reactions and threaded replies via the Slack Web API client

## Cross-References

- [System Overview](system-overview.md)
- [Business Logic](../behavior/business-logic.md)
