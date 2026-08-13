# Interfaces and Contracts

## Go Interfaces (Implicit)

Go uses structural typing. The following implicit interfaces are relied upon:

### Function Type Contracts

**Time function injection:**
```go
type TimeSinceFunc = func(time.Time) time.Duration
```
Used by: `CheckPRStatus`, `InProgressCheck`, `QueuedCheck`, `CheckPendingStatus`  
Production implementation: `time.Since`  
Test implementation: custom mock functions

### Struct Contracts

**`utils.GitHub`** — Central configuration aggregate:
```go
type GitHub struct {
    Mode, Token, URL, User string
    Repo   *git.Repository
    Client *github.Client
}
```
Consumers: `routes.InitRouter`, `routes.InitGetRetriggerChecks`

**`utils.Response`** — Standardized API response:
```go
type Response struct {
    Status  int      `json:"status,omitempty"`
    Message []string `json:"message,omitempty"`
    Error   []string `json:"error,omitempty"`
    Data    any      `json:"data,omitempty"`
}
```
Consumers: All route handlers

**`pull_requests.InvalidChecks`** — Check status report:
```go
type InvalidChecks struct {
    Name       string
    Message    string
    Status     Status
    RetryAfter time.Duration
    URL        string
}
```
Consumers: Routes package, Slackbot (via JSON)

**`routes.PrChecks`** — Aggregated PR response:
```go
type PrChecks struct {
    ID            string `json:"Id"`
    Branch        string `json:"Branch"`
    InvalidChecks []pull_requests.InvalidChecks
}
```

## Service-to-Service Contract

### API → Slackbot (JSON over HTTP)

**Request**: `GET /check-pr?id=<comma-separated-ids>`

**Response** (JSON array):
```json
[
  {
    "Id": "123",
    "Branch": "main",
    "InvalidChecks": [
      {
        "Name": "check-name",
        "Message": "description",
        "Status": 1,
        "RetryAfter": 300000000000,
        "URL": "https://github.com/..."
      }
    ]
  }
]
```

**Status codes in InvalidChecks:**
- `0` = Success
- `1` = Failure
- `2` = Pending

**RetryAfter field:**
- `> 0` nanoseconds = check is recent, retry after this duration
- `0` = check is old or failed, no retry

## Cross-References

- [API Reference](api-reference.md)
- [Data Models](data-models.md)
