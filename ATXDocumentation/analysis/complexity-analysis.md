# Complexity Analysis

## Cyclomatic Complexity Hotspots

### High Complexity

**`slackbot/app.py:handle_pull_request_message`** — Complexity: High
- Multiple sequential decision branches
- Calls several functions with side effects
- Nested conditional logic for check categorization

### Medium Complexity

**`api/pull_requests/check_pr.go:CheckPRStatus`** — Complexity: Medium
- Loop with 3-way branch (completed/in_progress/queued)
- Delegates to separate functions for each branch

**`api/pull_requests/complete_check.go:CompletedCheck`** — Complexity: Medium
- Switch statement with 7 cases

**`api/routes/check_pr.go:InitGetCheckPR` (handler closure)** — Complexity: Medium
- Loop with multiple early returns
- Error handling at each step

### Low Complexity

All other functions have low cyclomatic complexity (1-3 paths).

## Cognitive Complexity

| Component | Cognitive Load | Reason |
|-----------|---------------|--------|
| Slackbot message handler | High | Sequential decision cascade with side effects |
| Check PR route handler | Medium | Loop with error handling at each step |
| Retrigger checks handler | Medium | Sequential git operations with error handling |
| Time-based check evaluation | Low | Simple threshold comparison |
| Response utility | Low | Simple conditional dispatch |

## Coupling Analysis

| Package | Afferent (incoming) | Efferent (outgoing) | Instability |
|---------|--------------------|--------------------|-------------|
| `utils` | 4 (all packages use it) | 2 (gin, go-git) | Low |
| `pull_requests` | 1 (routes) | 2 (utils, go-github) | Medium |
| `commit` | 2 (routes, init_app) | 1 (go-git) | Low |
| `routes` | 1 (init_app) | 4 (commit, pull_requests, utils, gin) | High |
| `init_app` | 1 (main) | 4 (commit, routes, utils, go-git) | High |

## Recommendations

1. The slackbot's `handle_pull_request_message` would benefit from extraction into smaller functions for each decision branch
2. The `routes` and `init_app` packages have high instability (many outgoing dependencies) which is appropriate for orchestration layers

## Cross-References

- [Code Metrics](code-metrics.md)
- [Maintenance Burden](../technical-debt/maintenance-burden.md)
