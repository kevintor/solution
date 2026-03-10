# Email Setup

## Overview
Himalaya CLI email client configuration for Gmail.

## Date
2026-03-10

## Installation

### Binary Installation
```bash
# Download from GitHub releases
curl -L -o himalaya.tgz \
  "https://github.com/pimalaya/himalaya/releases/download/v1.2.0/himalaya.x86_64-linux.tgz"

# Extract and install
tar -xzf himalaya.tgz
mv himalaya /usr/local/bin/
chmod +x /usr/local/bin/himalaya
```

**Version**: v1.2.0
**Build**: linux musl x86_64
**Features**: +maildir +smtp +wizard +sendmail +pgp-commands +imap

## Configuration

### Gmail Setup

**Prerequisites**:
1. Enable 2-Step Verification in Google Account
2. Generate App Password at https://myaccount.google.com/apppasswords
3. Select "Mail" as app, "Other" as device
4. Copy the 16-character password

**Config File**: `~/.config/himalaya/config.toml`

```toml
[accounts.gmail]
email = "kewei.zhang2026@gmail.com"
display-name = "虾头"
default = true

# IMAP Configuration (Receiving)
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "kewei.zhang2026@gmail.com"
backend.auth.type = "password"
backend.auth.raw = "YOUR_APP_PASSWORD_HERE"

# SMTP Configuration (Sending)
message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "kewei.zhang2026@gmail.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "YOUR_APP_PASSWORD_HERE"

# Folder Aliases (Gmail specific)
folder.alias.inbox = "INBOX"
folder.alias.sent = "[Gmail]/Sent Mail"
folder.alias.drafts = "[Gmail]/Drafts"
folder.alias.trash = "[Gmail]/Trash"

# Don't save copy to sent folder (Gmail does this automatically)
message.send.save-copy = false
```

**Security**:
```bash
chmod 600 ~/.config/himalaya/config.toml
```

## Usage

### List Folders
```bash
himalaya folder list
```

**Output**:
```
| NAME              | DESC                       |
|-------------------|----------------------------|
| INBOX             | \HasNoChildren             |
| [Gmail]/All Mail  | \All, \HasNoChildren       |
| [Gmail]/Drafts    | \Drafts, \HasNoChildren    |
| [Gmail]/Important | \HasNoChildren, \Important |
| [Gmail]/Sent Mail | \HasNoChildren, \Sent      |
| [Gmail]/Spam      | \HasNoChildren, \Junk      |
| [Gmail]/Starred   | \Flagged, \HasNoChildren   |
| [Gmail]/Trash     | \HasNoChildren, \Trash     |
```

### List Emails
```bash
# Default INBOX
himalaya envelope list

# Specific folder
himalaya envelope list --folder "[Gmail]/Sent Mail"

# Pagination
himalaya envelope list --page 1 --page-size 50
```

### Read Email
```bash
himalaya message read <id>
```

### Search
```bash
himalaya envelope list from:john@example.com subject:meeting
```

### Send Email

**Interactive**:
```bash
himalaya message write
```

**Raw message**:
```bash
echo 'From: kewei.zhang2026@gmail.com
To: recipient@example.com
Subject: Test Subject

Email body here' | himalaya message send -
```

**Template**:
```bash
echo 'From: kewei.zhang2026@gmail.com
To: recipient@example.com
Subject: Test Subject

Email body' | himalaya template send -
```

### Reply/Forward
```bash
himalaya message reply <id>
himalaya message reply <id> --all    # Reply all
himalaya message forward <id>
```

### Attachments
```bash
# Download attachments
himalaya attachment download <id>

# Specific directory
himalaya attachment download <id> --dir ~/Downloads
```

### Move/Copy
```bash
# Move to folder
himalaya message move <id> "Archive"

# Copy to folder
himalaya message copy <id> "Important"

# Delete
himalaya message delete <id>
```

## Other Providers

### Outlook/Office 365
```toml
backend.host = "outlook.office365.com"
message.send.backend.host = "smtp.office365.com"
message.send.backend.port = 587
```

### QQ Mail
```toml
backend.host = "imap.qq.com"
message.send.backend.host = "smtp.qq.com"
message.send.backend.port = 587
```

## References
- [Himalaya GitHub](https://github.com/pimalaya/himalaya)
- [Documentation](https://pimalaya.org/himalaya/)
