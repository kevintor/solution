# OpenClaw Setup

## Overview
Complete OpenClaw agent configuration with multi-bot Telegram, GitHub integration, ClawHub skills, and cross-agent communication.

## Date
2026-03-10

## Components

### 1. Telegram Configuration
- **Main Bot**: Direct message handler
- **Bot2 (zaixiang)**: Group chat assistant
- **Bot3 (shangshu)**: Specialized tasks

### 2. Installed Skills
| Skill | Version | Purpose |
|-------|---------|---------|
| github | 1.0.0 | GitHub CLI operations |
| context-doctor | 1.2.0 | Context window diagnostics |
| self-improving-agent | 3.0.0 | Continuous improvement |
| capability-evolver | 1.27.3 | Self-evolution engine |
| find-skills | 0.1.0 | Skill discovery |
| himalaya | 1.2.0 | Email client |
| healthcheck | bundled | Security hardening |
| skill-creator | bundled | Create custom skills |
| tmux | bundled | Terminal multiplexing |
| weather | bundled | Weather queries |
| daily-report | managed | Daily intelligence brief |
| md-to-pdf | managed | Markdown to PDF |

### 3. EvoMap Configuration
- **Node ID**: `node_99707cf6a709e4452ee683270a7ebc25`
- **Hub URL**: https://evomap.ai
- **Strategy**: balanced

### 4. Environment Variables
```bash
# API Keys (set in ~/.openclaw/openclaw.json)
KIMI_API_KEY=<redacted>
KIMI_PLUGIN_API_KEY=<redacted>

# EvoMap
A2A_NODE_ID=node_99707cf6a709e4452ee683270a7ebc25
A2A_HUB_URL=https://evomap.ai
EVOLVE_STRATEGY=balanced
```

## Configuration Files

### openclaw.json Structure
```json
{
  "env": { /* API keys and tokens */ },
  "browser": {
    "executablePath": "/usr/bin/google-chrome",
    "headless": true,
    "noSandbox": true
  },
  "agents": { /* Multi-agent setup */ },
  "tools": {
    "sessions": { "visibility": "all" },
    "agentToAgent": { "enabled": true }
  },
  "channels": { /* Telegram bots */ }
}
```

## Cross-Agent Communication

Enabled features:
- `sessions.visibility: all` - View all sessions
- `agentToAgent.enabled: true` - Direct agent communication

## Security Notes

### Warnings
- Telegram groupPolicy is "open" (consider changing to "allowlist")
- plugins.allow is not set (should explicitly list trusted plugins)

### Token Storage
All sensitive tokens are stored in `~/.openclaw/openclaw.json` with file permissions 600.

## Quick Commands

```bash
# Check status
openclaw status

# List skills
clawhub list

# Run capability evolver
cd ~/.openclaw/workspace/skills/capability-evolver
node index.js

# Context diagnostic
python3 ~/.openclaw/workspace/skills/context-doctor/scripts/context-doctor.py
```

## References
- [OpenClaw Docs](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.com)
- [EvoMap](https://evomap.ai)
