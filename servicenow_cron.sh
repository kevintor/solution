#!/bin/bash
# ServiceNow Learning Cron Job
# Runs every Tuesday and Friday at 9:00 AM

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export HOME=/root

cd /root/.openclaw/workspace/solution

# Run the learning script
/usr/bin/node servicenow_learning_script.js >> /var/log/servicenow_learning.log 2>&1

# Commit new knowledge to GitHub
if [ -d "servicenow_knowledge" ]; then
    git add servicenow_knowledge/
    git commit -m "Auto-update: ServiceNow knowledge $(date +%Y-%m-%d)"
    git push origin master
fi
