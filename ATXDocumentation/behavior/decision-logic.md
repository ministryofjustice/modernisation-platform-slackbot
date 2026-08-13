> ⚠️ **Early Access**: Behavior documentation is in early access. Please review critically.

# Decision Logic

## API Decision Points

### Check Run Status Decision (`pull_requests/check_pr.go:CheckPRStatus`)

```
For each check run:
├── status == "completed"
│   └── Evaluate conclusion (CompletedCheck)
├── status == "in_progress"
│   └── Evaluate time since start (InProgressCheck)
└── status == "queued"
    └── Evaluate time since start (QueuedCheck)
```

### Completed Check Conclusion Decision (`pull_requests/complete_check.go`)

```
conclusion:
├── "success" → Skip (not invalid)
├── "skipped" → Skip (not invalid)
├── "failure" → InvalidCheck(Failure)
├── "action_required" → InvalidCheck(Failure)
├── "cancelled" → InvalidCheck(Failure)
├── "timed_out" → InvalidCheck(Failure)
├── "stale" → InvalidCheck(Failure)
└── default → InvalidCheck(Failure, "unaccounted for state")
```

### Time-Based Decision (`utils/time_since.go:TimeSince`)

```
timeSinceStart = getTimeSince(startedAt)
├── timeSinceStart < 10 minutes
│   └── return (true, rounded, tenMins) → "young" — can retry
└── timeSinceStart >= 10 minutes
    └── return (false, rounded, tenMins) → "old" — something wrong
```

### URL Parsing Decision (`routes/init.go:parseRepoOwnerAndName`)

```
Parse URL:
├── Valid URL with >= 2 path parts
│   └── return (parts[0], parts[1])
└── Invalid or insufficient path
    └── fallback to ("ministryofjustice", "cloud-platform-environments")
```

## Slackbot Decision Points

### Message Reaction Decision (`slackbot/app.py:handle_pull_request_message`)

```
After API response:
├── data is empty (all checks pass)
│   └── Add ✨ → DONE
├── Any configured check has Status == 1 (failure)
│   └── Add ❌ + post summary → DONE
├── Configured checks with Status == 2 AND RetryInNanoSec > 0
│   └── Add 🔄 + schedule retry → DONE
├── Configured checks queued > 10min (status==2, retry==0, "queued" in message)
│   └── Add ⏳ + post blocking message → DONE
└── Configured checks pending (status==2)
    └── Add ⏳ + post "still running" message
```

### API URL Normalization Decision (`slackbot/app.py:normalize_api_url`)

```
raw_url:
├── Contains "://" → return as-is
├── Host is local (localhost, 127.0.0.1, 0.0.0.0, api, host.docker.internal)
│   └── Prepend "http://"
└── Host is not local
    └── Prepend "https://"
```

### Check Categorization Decision (`slackbot/app.py:get_configured_checks`)

```
For each check in all_checks:
├── Check name matches any pattern in checks_config.json
│   └── Add to corresponding category
└── No pattern match
    └── Uncategorized (ignored for reaction logic)
```

## Cross-References

- [Business Logic](business-logic.md)
- [Workflows](workflows.md)
