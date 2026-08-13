# Data Models

## Go Types

### Status Enum (`pull_requests/check_pr.go`)
```go
type Status int

const (
    Success Status = iota  // 0
    Failure                // 1
    Pending                // 2
)
```

### InvalidChecks (`pull_requests/check_pr.go`)
```go
type InvalidChecks struct {
    Name       string        // Check run name
    Message    string        // Human-readable status message
    Status     Status        // Success/Failure/Pending
    RetryAfter time.Duration // Nanoseconds until retry (0 = no retry)
    URL        string        // Link to check run on GitHub
}
```

### PrChecks (`routes/check_pr.go`)
```go
type PrChecks struct {
    ID            string                      `json:"Id"`
    Branch        string                      `json:"Branch"`
    InvalidChecks []pull_requests.InvalidChecks
}
```

### GitHub (`utils/github_data.go`)
```go
type GitHub struct {
    Mode   string           // Gin mode (debug/release/test)
    Token  string           // GitHub personal access token
    URL    string           // Repository URL
    User   string           // GitHub username
    Repo   *git.Repository  // Local git repository handle
    Client *github.Client   // GitHub API client
}
```

### Response (`utils/response.go`)
```go
type Response struct {
    Status  int      `json:"status,omitempty"`
    Message []string `json:"message,omitempty"`
    Error   []string `json:"error,omitempty"`
    Data    any      `json:"data,omitempty"`
}
```

## Python Types

### Checks Config Schema (`slackbot/checks_config.json`)
```json
{
  "<category_name>": {
    "name_patterns": ["<regex_pattern>", ...]
  }
}
```

### API Response Model (consumed by slackbot)
```python
# List of PR check objects
[
    {
        "Id": str,           # PR number
        "Branch": str,       # Base branch
        "InvalidChecks": [
            {
                "Name": str,           # Check name
                "Message": str,        # Status message
                "Status": int,         # 0=success, 1=failure, 2=pending
                "RetryInNanoSec": int,  # Nanoseconds (serialized from RetryAfter)
                "URL": str             # GitHub check URL
            }
        ]
    }
]
```

## Kubernetes/Helm Data Models

### Environment Variables (from Helm values + secrets)
| Variable | Source | Service |
|----------|--------|---------|
| `GITHUB_TOKEN` | K8s Secret | API |
| `GITHUB_URL` | K8s Secret | API, Slackbot |
| `GITHUB_USER` | K8s Secret | API |
| `GIN_MODE` | Static value | API |
| `SLACK_BOT_TOKEN` | K8s Secret | Slackbot |
| `SLACK_SIGNING_SECRET` | K8s Secret | Slackbot |
| `SLACK_APP_TOKEN` | K8s Secret | Slackbot |
| `SLACK_CHANNEL_ID` | K8s Secret | Slackbot |
| `API_URL` | K8s Secret | Slackbot |
| `ENVIRONMENT` | Helm value | Slackbot |

## Cross-References

- [Interfaces](interfaces.md)
- [API Reference](api-reference.md)
