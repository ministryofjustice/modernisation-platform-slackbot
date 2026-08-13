# API Reference

## Go API Endpoints

### GET /check-pr

**Purpose**: Query GitHub check run statuses for one or more pull requests.

**Parameters**:
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| `id` | string | Query | Comma-separated PR numbers |

**Response** (200 OK):
```json
[
  {
    "Id": "42",
    "Branch": "main",
    "InvalidChecks": [
      {
        "Name": "plan / environments (dev)",
        "Message": "this check failed, check your pr and amend",
        "Status": 1,
        "RetryAfter": 0,
        "URL": "https://github.com/org/repo/actions/runs/..."
      }
    ]
  }
]
```

**Error Response**:
```json
{"error": "error message"}
```

**Source**: `api/routes/check_pr.go:InitGetCheckPR`

---

### GET /retrigger-checks/:branch

**Purpose**: Retrigger CI checks by pushing an empty commit to the specified branch.

**Parameters**:
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| `branch` | string | Path | Branch name to retrigger |

**Response**: No explicit success response (BUG)

**Error Response**:
```json
{"error": "an error occurred at clone: ..."}
```

**Source**: `api/routes/retrigger_checks.go:InitGetRetriggerChecks`

---

### GET /healthz

**Purpose**: Kubernetes health check endpoint.

**Response**: `200 OK` (empty body)

**Source**: `api/routes/init.go:InitRouter`

---

## Go Public Functions

### Package `commit`
| Function | Signature | Description |
|----------|-----------|-------------|
| `CloneRepo` | `(url string) (*git.Repository, error)` | Shallow clone to /app/environments |
| `OpenRepo` | `() (*git.Repository, error)` | Open existing repo at /app/environments |
| `FetchBranch` | `(r *git.Repository, branch string) error` | Fetch specific branch |
| `CheckoutBranch` | `(r *git.Repository, branch string) error` | Force checkout branch |
| `PushCommit` | `(r *git.Repository, user, token, branch string) error` | Create and push empty commit |

### Package `init_app`
| Function | Signature | Description |
|----------|-----------|-------------|
| `InitEnvVars` | `() (string, string, string, string)` | Load env vars (ginMode, token, url, user) |
| `InitGH` | `(token string) (*github.Client, error)` | Create GitHub client |
| `InitCommit` | `(url string) (*git.Repository, error)` | Open or clone repository |
| `InitGin` | `(mode string, gh utils.GitHub) *gin.Engine` | Configure Gin engine |

### Package `pull_requests`
| Function | Signature | Description |
|----------|-----------|-------------|
| `CheckPRStatus` | `(checks *github.ListCheckRunsResults, getTimeSince func(time.Time) time.Duration) []InvalidChecks` | Evaluate all check runs |
| `CheckPendingStatus` | `(c *gin.Context, ghClient *github.Client, prNumber string, getTimeSince func(time.Time) time.Duration) (func() InvalidChecks, *github.Response, error)` | Check combined status |
| `CheckCombinedStatus` | `(status *github.CombinedStatus, checkPendingFn func() InvalidChecks) []InvalidChecks` | Evaluate combined status |
| `GetBranch` | `(ghClient *github.Client, owner, repository, prNumber string) (string, error)` | Get PR base branch |
| `CompletedCheck` | `(check *github.CheckRun, prStatus []InvalidChecks) []InvalidChecks` | Handle completed check |
| `InProgressCheck` | `(check *github.CheckRun, prStatus []InvalidChecks, getTimeSince func(time.Time) time.Duration) []InvalidChecks` | Handle in-progress check |
| `QueuedCheck` | `(check *github.CheckRun, prStatus []InvalidChecks, getTimeSince func(time.Time) time.Duration) []InvalidChecks` | Handle queued check |

### Package `routes`
| Function | Signature | Description |
|----------|-----------|-------------|
| `InitRouter` | `(r *gin.Engine, gh utils.GitHub)` | Register all routes |
| `InitLogger` | `(r *gin.Engine)` | Configure Zap logging |
| `InitGetCheckPR` | `(r *gin.Engine, ghClient *github.Client, owner, repository string)` | Register check-pr route |
| `InitGetRetriggerChecks` | `(r *gin.Engine, gh utils.GitHub)` | Register retrigger route |

### Package `utils`
| Function | Signature | Description |
|----------|-----------|-------------|
| `SendResponse` | `(c *gin.Context, response Response)` | Send standardized JSON response |
| `TimeSince` | `(startedAt time.Time, getTimeSince func(time.Time) time.Duration) (bool, time.Duration, time.Duration)` | Calculate 10-min threshold |

## Cross-References

- [Interfaces](interfaces.md)
- [Data Models](data-models.md)
- [Components](../architecture/components.md)
