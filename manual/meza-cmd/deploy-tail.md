# meza deploy-tail

Follow deployment logs in real-time for an environment.

## Synopsis

```bash
meza deploy-tail <environment>
```

## Description

The `meza deploy-tail` command displays and follows the deployment log for a specified environment in real-time. This is the most effective way to monitor active deployments and troubleshoot deployment issues as they occur.

The command uses `tail -f` to continuously display new log entries as they are written, making it ideal for monitoring deployment progress.

## Usage

```bash
meza deploy-tail <environment>
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `environment` | Name of the environment to monitor | Yes |

## Examples

### Monitor Production Deployment
```bash
meza deploy-tail production
```

### Monitor Development Deployment
```bash
meza deploy-tail monolith
```

## Output

The command displays live Ansible deployment output:

```bash
$ meza deploy-tail production

TASK [mediawiki : Install MediaWiki via Composer] *****************************
changed: [production-web-01]

TASK [mediawiki : Set MediaWiki file permissions] *****************************
ok: [production-web-01]

TASK [configure-wiki : Generate LocalSettings.php] ***************************
changed: [production-web-01]
...
```

## Live Monitoring Features

- **Real-time updates**: New log entries appear immediately
- **Task progress**: Shows current Ansible task being executed
- **Error visibility**: Errors and failures appear as they happen
- **Timing information**: Shows task execution duration
- **Status indicators**: `ok`, `changed`, `failed`, `skipped` status for each task

## Control Options

### Exit Monitoring
- **Ctrl+C**: Stop following the log (deployment continues)
- **Ctrl+Z**: Suspend the tail command

### Terminal Management
```bash
# Run in background to continue using terminal
meza deploy-tail production &

# Monitor in separate terminal window
gnome-terminal -e "meza deploy-tail production"

# Use screen/tmux for persistent monitoring
screen -S deploy-monitor meza deploy-tail production
```

## Use Cases

### Active Deployment Monitoring
```bash
# Start deployment in one terminal
meza deploy production

# Monitor progress in another terminal
meza deploy-tail production
```

### Troubleshooting Deployments
```bash
# Monitor for errors during deployment
meza deploy-tail development | grep -i error

# Save deployment output while monitoring
meza deploy-tail production | tee deployment-$(date +%Y%m%d-%H%M).log
```

### Deployment Status Checking
```bash
# Check if deployment is progressing
meza deploy-tail production
# Look for recent activity or if it's stuck on a task
```

### Team Collaboration
```bash
# Multiple team members can monitor same deployment
# Each person runs in their own terminal:
meza deploy-tail production
```

## Log Content Interpretation

### Normal Progress Indicators
```
TASK [role-name : Task description] ************************************
ok: [server-name]                    # Task completed successfully, no changes
changed: [server-name]               # Task completed successfully, made changes
skipping: [server-name]              # Task skipped due to conditions
```

### Error Indicators
```
failed: [server-name]                # Task failed
fatal: [server-name]                 # Fatal error, deployment stopped
FAILED - RETRYING: [server-name]     # Task failed, retrying
```

### Progress Markers
```
PLAY [Play name] ********************************************************
TASK [role : task name] *************************************************
PLAY RECAP **************************************************************
```

## Prerequisites

- **Active deployment**: Must have a running or recent deployment
- **Log file exists**: Deployment log must be present
- **Read permissions**: Access to deployment log directory

## Troubleshooting

### No Output Displayed
```bash
# Check if deployment is active
meza deploy-check production

# Verify log file exists
ls -la "$(meza deploy-log production)"

# Check for recent log files
ls -lt /opt/data-meza/logs/deploy-output/
```

### Permission Denied
```bash
# Check log file permissions
ls -la "$(meza deploy-log production)"

# Fix permissions if needed
sudo chmod 644 "$(meza deploy-log production)"
```

### File Not Found
```bash
# Check if environment name is correct
ls /opt/conf-meza/secret/

# Look for existing log files
ls -la /opt/data-meza/logs/deploy-output/
```

## Advanced Usage

### Filter Specific Content
```bash
# Monitor only errors
meza deploy-tail production | grep -i "error\|failed\|fatal"

# Monitor specific role
meza deploy-tail production | grep "TASK \[mediawiki"

# Monitor with timestamps
meza deploy-tail production | while read line; do
    echo "$(date): $line"
done
```

### Multiple Environment Monitoring
```bash
# Monitor multiple environments (requires multiple terminals)
# Terminal 1:
meza deploy-tail production

# Terminal 2:
meza deploy-tail staging

# Or use split screen tools like tmux
```

### Save and Monitor
```bash
# Save deployment log while monitoring
meza deploy-tail production | tee "deploy-$(date +%Y%m%d-%H%M).log"

# Monitor and send alerts on errors
meza deploy-tail production | while read line; do
    if echo "$line" | grep -qi "failed\|error"; then
        echo "ALERT: $line" | mail admin@example.com
    fi
done
```

## Integration Examples

### Slack/Teams Notifications
```bash
#!/bin/bash
meza deploy-tail production | while read line; do
    if echo "$line" | grep -q "PLAY RECAP"; then
        curl -X POST -H 'Content-type: application/json' \
            --data '{"text":"Production deployment completed"}' \
            YOUR_SLACK_WEBHOOK_URL
    fi
done
```

### Deployment Dashboard
```bash
#!/bin/bash
# Simple deployment status dashboard
while true; do
    clear
    echo "Deployment Status Dashboard"
    echo "=========================="
    echo "Last 10 log entries:"
    meza deploy-tail production | tail -10
    sleep 5
done
```

## Related Commands

- [`meza deploy-log`](deploy-log.md) - Get deployment log file path
- [`meza deploy-check`](deploy-check.md) - Check if deployment is running
- [`meza deploy-kill`](deploy-kill.md) - Kill stuck deployment
- [`meza deploy`](deploy.md) - Start deployment to monitor

## Best Practices

### Monitoring Strategy
1. **Start monitoring before deployment** to catch early issues
2. **Use separate terminal** to maintain control of deployment
3. **Look for patterns** in failures or slow tasks
4. **Monitor resource usage** during intensive tasks

### Error Response
1. **Don't panic** on first error - Ansible often retries
2. **Look for context** - errors often have detailed explanations
3. **Check previous tasks** - failures might be cascading
4. **Save error output** for later analysis

### Team Workflows
1. **Designated monitor** for critical deployments
2. **Share observations** with team during deployment
3. **Document recurring issues** for process improvement
4. **Use consistent monitoring practices** across environments

## Performance Considerations

- **Large deployments** generate significant log output
- **Network latency** may affect real-time display
- **Terminal buffer** may limit scrollback history
- **Log file size** can grow quickly during long deployments

## Recovery Actions

If monitoring reveals issues:

```bash
# For stuck tasks - wait and observe
# For repeated failures - consider killing deployment
meza deploy-kill production

# For critical errors - assess and fix before retry
meza debug production
```