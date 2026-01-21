---
name: agent-browser
description: Browser automation using agent-browser CLI. Use when asked to automate web interactions, scrape content, fill forms, test web apps, or interact with browser-based UIs. Provides deterministic element selection via accessibility tree refs.
---

# Agent Browser Automation

## Overview

Use `agent-browser` CLI for fast, reliable browser automation. The tool returns accessibility trees with ref tags (`@e1`, `@e2`, etc.) enabling deterministic element selection without fragile CSS selectors.

## Core Workflow

### 1) Navigate and snapshot

```bash
agent-browser open <url>
agent-browser snapshot -i
```

The `-i` flag returns only interactive elements. Use `-c` for compact output removing empty structural elements.

### 2) Interact using refs

After taking a snapshot, use the ref tags to interact with elements:

```bash
agent-browser click @e2
agent-browser fill @e3 "user@example.com"
agent-browser type @e4 "search query"
```

Always prefer refs over CSS selectors for reliability.

### 3) Verify state changes

After interactions, take a new snapshot to verify the page state changed as expected:

```bash
agent-browser snapshot -i
```

## Common Patterns

### Form filling

```bash
agent-browser open "https://example.com/login"
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait 2000
agent-browser snapshot -i
```

### Data extraction

```bash
agent-browser open "https://example.com/data"
agent-browser snapshot
agent-browser get text @e5
agent-browser get html @e5
```

### Screenshot capture

```bash
agent-browser screenshot output.png
agent-browser screenshot --full page.png
```

### Waiting for elements or time

```bash
agent-browser wait 2000              # Wait 2 seconds
agent-browser wait "#element-id"     # Wait for element
```

## Session Management

Use named sessions for isolated browser instances:

```bash
agent-browser --session auth1 open "https://app.example.com"
agent-browser --session auth2 open "https://app.example.com"
```

Sessions persist between commands. Use `session list` to see active sessions.

## Debugging

### Visual debugging

```bash
agent-browser --headed open "https://example.com"
agent-browser highlight @e3
```

### Console and errors

```bash
agent-browser console
agent-browser errors
```

### Tracing

```bash
agent-browser trace start
# ... perform actions ...
agent-browser trace stop trace.zip
```

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `open <url>` | Navigate to URL |
| `snapshot -i` | Get interactive elements with refs |
| `click @ref` | Click element |
| `fill @ref <text>` | Clear and fill input |
| `type @ref <text>` | Type into element |
| `press <key>` | Press key (Enter, Tab, etc.) |
| `get text @ref` | Extract text content |
| `screenshot [path]` | Capture screenshot |
| `wait <ms\|selector>` | Wait for time or element |
| `scroll <dir> [px]` | Scroll page |

## Snapshot Options

| Flag | Effect |
|------|--------|
| `-i, --interactive` | Only interactive elements |
| `-c, --compact` | Remove empty structural elements |
| `-d, --depth <n>` | Limit tree depth |
| `-s, --selector <sel>` | Scope to CSS selector |

## Best Practices

1. **Always snapshot first** - Get refs before interacting
2. **Use refs, not selectors** - Refs are deterministic from the snapshot
3. **Verify after actions** - Take a new snapshot to confirm state changes
4. **Use sessions for auth** - Keep authenticated sessions separate
5. **Wait appropriately** - Use element waits over fixed delays when possible
6. **Use --headed for debugging** - See the browser when troubleshooting
