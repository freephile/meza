# meza deploy-log

Display the deployment log file path for an environment.

## Synopsis

```bash
meza deploy-log <environment>
```

## Description

The `meza deploy-log` command outputs the full path to the deployment log file for a specified environment. This is useful for accessing deployment logs directly or integrating with other tools and scripts.

The command returns the path to the active deployment log, which includes a timestamp to ensure uniqueness for each deployment session.

## Usage

```bash
meza deploy-log <environment>
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `environment` | Name of the environment | Yes |

## Examples

### Get Production Log Path
```bash
meza deploy-log production
```

### Get Development Log Path
```bash
meza deploy-log monolith
```

## Output

The command outputs the full path to the deployment log file:

```bash
$ meza deploy-log production
/opt/data-meza/logs/deploy-output/production-20251020-153045.log
```

## Log File Format

Deployment logs are stored with the following naming convention:
```
/opt/data-meza/logs/deploy-output/<environment>-<timestamp>.log
```

Where:
- `<environment>`: The environment name (e.g., "production", "monolith")
- `<timestamp>`: Deployment start timestamp in `YYYYMMDD-HHMMSS` format

## Use Cases

### View Current Deployment Log
```bash
# Get log path and view contents
LOG_PATH=$(meza deploy-log production)
less "$LOG_PATH"
```

### Monitor Deployment Progress
```bash
# Follow deployment log in real-time
tail -f "$(meza deploy-log production)"
```

### Archive Deployment Logs
```bash
#!/bin/bash
ENV="production"
LOG_PATH=$(meza deploy-log $ENV)
ARCHIVE_DIR="/backup/deployment-logs"

# Copy log to archive
cp "$LOG_PATH" "$ARCHIVE_DIR/$(basename $LOG_PATH)"
```

### Extract Deployment Information
```bash
# Get specific information from deployment log
LOG_PATH=$(meza deploy-log production)

# Find errors in deployment
grep -i error "$LOG_PATH"

# Check deployment duration
head -1 "$LOG_PATH"
tail -1 "$LOG_PATH"

# Count tasks executed
grep -c "TASK \[" "$LOG_PATH"
```

### Integration with Monitoring Tools
```bash
#!/bin/bash
# Send deployment log to monitoring system
ENV="production"
LOG_PATH=$(meza deploy-log $ENV)

if [ -f "$LOG_PATH" ]; then
    # Send to log aggregation system
    rsyslog -f "$LOG_PATH" monitoring-server:5000
fi
```

## Log Content

Deployment logs contain detailed Ansible output including:

- **Task execution**: Each Ansible task with results
- **Variable values**: Configuration values used during deployment
- **Error messages**: Detailed error information and stack traces
- **Timing information**: Task execution duration
- **System output**: Command outputs and system responses

## Prerequisites

The command requires:
- **Active deployment**: An active or recent deployment must exist for the environment
- **Read permissions**: Access to `/opt/data-meza/logs/deploy-output/`

## Error Handling

### Environment Not Deploying
If no deployment is active or recent:
```bash
$ meza deploy-log nonexistent
# Command may fail or return empty result
```

### Log File Missing
If the log file has been removed or archived:
```bash
# Check if log directory exists
ls -la /opt/data-meza/logs/deploy-output/

# Look for other log files
ls -la /opt/data-meza/logs/deploy-output/*production*
```

## Related Commands

- [`meza deploy-tail`](deploy-tail.md) - Follow deployment logs in real-time
- [`meza deploy-check`](deploy-check.md) - Check if deployment is running
- [`meza deploy`](deploy.md) - Start deployment (creates log)
- [`meza debug`](debug.md) - Debug deployment configuration

## Log Management

### View Recent Logs
```bash
# List recent deployment logs
ls -lt /opt/data-meza/logs/deploy-output/

# View last 50 lines of current deployment
tail -50 "$(meza deploy-log production)"
```

### Search Logs
```bash
# Search for specific errors
LOG_PATH=$(meza deploy-log production)
grep -A 5 -B 5 "FAILED" "$LOG_PATH"

# Find specific tasks
grep "TASK \[.*mediawiki" "$LOG_PATH"
```

### Log Rotation
```bash
# Archive old deployment logs
find /opt/data-meza/logs/deploy-output/ -name "*.log" -mtime +30 -exec gzip {} \;

# Clean up very old logs
find /opt/data-meza/logs/deploy-output/ -name "*.log.gz" -mtime +90 -delete
```

## Automation Examples

### Deployment Success Check
```bash
#!/bin/bash
ENV="production"
LOG_PATH=$(meza deploy-log $ENV)

if grep -q "PLAY RECAP" "$LOG_PATH" && ! grep -q "failed=" "$LOG_PATH"; then
    echo "Deployment succeeded"
    exit 0
else
    echo "Deployment failed or incomplete"
    exit 1
fi
```

### Extract Deployment Summary
```bash
#!/bin/bash
ENV="production"
LOG_PATH=$(meza deploy-log $ENV)

echo "Deployment Summary for $ENV:"
echo "============================="

# Show start time
echo "Started: $(head -1 "$LOG_PATH" | cut -d' ' -f1-2)"

# Show task counts
echo "Tasks executed: $(grep -c "TASK \[" "$LOG_PATH")"
echo "Changed tasks: $(grep -c "changed:" "$LOG_PATH")"
echo "Failed tasks: $(grep -c "failed:" "$LOG_PATH")"

# Show end time if completed
if grep -q "PLAY RECAP" "$LOG_PATH"; then
    echo "Completed: $(grep "PLAY RECAP" "$LOG_PATH" -A 10 | tail -1 | cut -d' ' -f1-2)"
fi
```

## Best Practices

1. **Use in scripts** to access deployment logs programmatically
2. **Monitor log size** - deployment logs can be large
3. **Archive old logs** to prevent disk space issues
4. **Combine with other tools** like `grep`, `awk`, `tail` for analysis
5. **Set up log rotation** for long-running environments

## Troubleshooting

### Command Returns Nothing
```bash
# Check if environment is/was deploying
meza deploy-check production

# Look for log files manually
ls -la /opt/data-meza/logs/deploy-output/
```

### Permission Denied
```bash
# Check log directory permissions
ls -la /opt/data-meza/logs/

# Fix permissions if needed
sudo chown -R meza:meza /opt/data-meza/logs/
```