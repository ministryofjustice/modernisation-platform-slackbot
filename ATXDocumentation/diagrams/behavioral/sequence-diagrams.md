# Behavioral Diagrams

## Sequence Diagram: PR Check Flow

```
Slack User          Slackbot (Python)         API (Go)           GitHub API
    │                    │                      │                    │
    │ Post PR link       │                      │                    │
    │───────────────────▶│                      │                    │
    │                    │                      │                    │
    │                    │ GET /check-pr?id=42  │                    │
    │                    │─────────────────────▶│                    │
    │                    │                      │                    │
    │                    │                      │ ListCheckRunsForRef│
    │                    │                      │───────────────────▶│
    │                    │                      │                    │
    │                    │                      │◀───────────────────│
    │                    │                      │  Check runs data   │
    │                    │                      │                    │
    │                    │◀─────────────────────│                    │
    │                    │  JSON response       │                    │
    │                    │                      │                    │
    │  ✨ or ❌ reaction │                      │                    │
    │◀───────────────────│                      │                    │
    │                    │                      │                    │
    │  Thread reply      │                      │                    │
    │◀───────────────────│                      │                    │
```

## Sequence Diagram: Retry Flow

```
Slackbot              Timer Thread            API (Go)
    │                      │                    │
    │ Schedule retry       │                    │
    │─────────────────────▶│                    │
    │                      │                    │
    │ Add 🔄 emoji         │                    │
    │                      │ (wait N seconds)   │
    │                      │                    │
    │                      │ GET /check-pr      │
    │                      │───────────────────▶│
    │                      │                    │
    │                      │◀───────────────────│
    │                      │                    │
    │ Remove 🔄 emoji      │                    │
    │◀─────────────────────│                    │
    │                      │                    │
    │ Add ✨ or ❌         │                    │
    │◀─────────────────────│                    │
```

## Activity Diagram: Message Processing

```
                    ┌───────────────────┐
                    │ Message received  │
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │ Contains PR URL?  │
                    └───┬──────────┬────┘
                     No │          │ Yes
                        ▼          ▼
                    [Ignore]  ┌─────────────┐
                              │ Query API   │
                              └──────┬──────┘
                                     │
                              ┌──────▼──────┐
                              │ All pass?   │
                              └──┬──────┬───┘
                              Yes│      │ No
                                 ▼      ▼
                            [Add ✨] ┌────────────┐
                                     │ Any fail?  │
                                     └──┬─────┬───┘
                                     Yes│     │ No
                                        ▼     ▼
                                   [Add ❌] ┌───────────┐
                                            │ Recent    │
                                            │ pending?  │
                                            └──┬────┬───┘
                                            Yes│    │ No
                                               ▼    ▼
                                          [Retry] [⏳ emoji]
```

## State Machine: Check Status

```
                    ┌───────────┐
                    │  Queued   │
                    └─────┬─────┘
                          │
              ┌───────────▼───────────┐
              │    In Progress        │
              └───┬───────────────┬───┘
                  │               │
         ┌────────▼────┐   ┌─────▼────────┐
         │  Completed  │   │  Timed Out   │
         └──┬──┬──┬──┬─┘   │  (>10 min)   │
            │  │  │  │     └──────────────┘
            ▼  ▼  ▼  ▼
    [success][failure][cancelled][skipped]
```
