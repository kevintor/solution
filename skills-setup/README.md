# Skills Setup

## Overview
Complete skill ecosystem for AI agent operations.

## Installed Skills

### 1. GitHub (v1.0.0)
**Source**: ClawHub
**Purpose**: GitHub CLI operations

**Configuration**:
- CLI: `/usr/bin/gh` (v2.45.0)
- Auth: Token-based (user: kevintor)
- Skill path: `~/.openclaw/workspace/skills/github/`

**Key Commands**:
```bash
gh repo view              # View repository info
gh issue list             # List issues
gh pr list                # List PRs
gh pr checkout <num>     # Checkout PR
gh workflow list          # List CI workflows
gh run list               # List runs
```

### 2. Context Doctor (v1.2.0)
**Source**: ClawHub
**Purpose**: Context window diagnostics

**Usage**:
```bash
# Terminal output
python3 ~/.openclaw/workspace/skills/context-doctor/scripts/context-doctor.py

# Generate PNG image
python3 ~/.openclaw/workspace/skills/context-doctor/scripts/context-doctor.py --png /tmp/context-doctor.png
```

### 3. Self-Improving Agent (v3.0.0)
**Source**: ClawHub
**Purpose**: Continuous improvement logging

**Structure**:
```
~/.openclaw/workspace/.learnings/
├── LEARNINGS.md      # Corrections, best practices
├── ERRORS.md         # Command failures
└── FEATURE_REQUESTS.md  # User feature requests
```

### 4. Capability Evolver (v1.27.3)
**Source**: ClawHub
**Purpose**: Self-evolution engine

**Configuration**:
- EvoMap Node: `node_99707cf6a709e4452ee683270a7ebc25`
- Strategy: balanced

**Usage**:
```bash
cd ~/.openclaw/workspace/skills/capability-evolver

# Standard run
node index.js

# Review mode
node index.js --review

# Continuous loop
node index.js --loop

# Lifecycle management
node src/ops/lifecycle.js start
node src/ops/lifecycle.js status
```

**Strategies**:
| Strategy | Innovation | Optimization | Repair |
|----------|-----------|--------------|--------|
| balanced | 50% | 30% | 20% |
| innovate | 80% | 15% | 5% |
| harden | 20% | 40% | 40% |
| repair-only | 0% | 20% | 80% |

### 5. Find Skills (v0.1.0)
**Source**: ClawHub
**Purpose**: Skill discovery

**Usage**:
```bash
npx skills find <query>    # Search skills
npx skills add <package>   # Install skill
npx skills check            # Check updates
npx skills update           # Update all
```

### 6. Himalaya Email (v1.2.0)
**Source**: System bundled
**Purpose**: IMAP/SMTP email client

**Binary**: `/usr/local/bin/himalaya`

**Configuration** (`~/.config/himalaya/config.toml`):
```toml
[accounts.gmail]
email = "kewei.zhang2026@gmail.com"
display-name = "虾头"
default = true

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
```

**Commands**:
```bash
himalaya folder list          # List folders
himalaya envelope list        # List emails
himalaya message read <id>   # Read email
himalaya message write        # Compose email
himalaya message send         # Send raw message
himalaya template send        # Send template
```

## Bundled Skills

### Healthcheck
Security hardening and risk assessment.

### Skill Creator
Create and package custom skills.

### Tmux
Remote terminal session control.

### Weather
Weather queries via wttr.in.

### Daily Report
Generate daily intelligence PDF briefs.

### MD to PDF
Convert Markdown to PDF.

## Skill Management

### Install from ClawHub
```bash
clawhub install <skill-name>
clawhub install <skill-name> --version 1.2.3
```

### Update Skills
```bash
clawhub update <skill-name>
clawhub update --all
```

### List Installed
```bash
clawhub list
openclaw skills list
```
