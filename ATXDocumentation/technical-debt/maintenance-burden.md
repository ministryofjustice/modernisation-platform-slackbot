# Maintenance Burden

## Overview

The maintenance burden for this project is low due to its small size and clear architecture. Key areas requiring ongoing attention:

## Areas of Concern

### 1. Git Operations in API (Medium Effort)

**Location**: `api/commit/commit.go`, `api/routes/retrigger_checks.go`

The retrigger-checks endpoint performs synchronous git clone/fetch/checkout/push operations. This creates:
- Potential blocking under concurrent requests
- Filesystem state management concerns (shared `/app/environments` directory)
- No cleanup of stale cloned repositories

### 2. Hardcoded Repository Configuration (Low Effort)

**Location**: `api/pull_requests/check_pr.go` (line referencing "ministryofjustice" and "cloud-platform-environments")

The `CheckPendingStatus` function hardcodes the owner and repository name, making it inflexible for use with other repositories. The `routes/init.go` correctly parses the URL, but this older function does not use that pattern.

### 3. Slack API Interactions (Low Effort)

**Location**: `slackbot/app.py`

- Threading timer for retry logic — if the slackbot crashes during a retry wait, pending retries are lost
- No persistence of message state between restarts
- `SLACK_CHANNEL_ID` is a single channel; no multi-channel support

### 4. Configuration Management (Low Effort)

**Location**: `slackbot/checks_config.json`

The checks configuration is loaded from a static JSON file. Changes require redeployment. No hot-reload capability.

## Maintenance Metrics

| Area | Files Affected | Complexity | Change Frequency |
|------|---------------|------------|-----------------|
| PR Check Logic | 4 Go files | Medium | Low |
| Slack Integration | 1 Python file | Medium | Low |
| Deployment Config | 6 YAML files | Low | Low |
| Git Operations | 2 Go files | Medium | Low |

## Cross-References

- [Components Documentation](../architecture/components.md)
- [Technical Debt Summary](summary.md)
