# meza deploy-kill

Terminate a running Meza deployment process and remove its lock.

## Synopsis

```bash
meza deploy-kill <environment>
```

## Description

The `meza deploy-kill` command forcefully terminates an active deployment process for a specified environment and removes the deployment lock. This command should be used when a deployment is stuck, unresponsive, or needs to be stopped immediately.

⚠️ **Use with caution:** This command forcefully kills deployment processes and may leave the environment in an inconsistent state.

## Usage

```bash
meza deploy-kill <environment>
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `environment` | Name of the environment with running deployment | Yes |

## Examples

### Kill Production Deployment
```bash
meza deploy-kill production
```

### Kill Development Deployment
```bash
meza deploy-kill monolith
```

## Exit Codes

| Exit Code | Status | Description |
|-----------|--------|-------------|
| `0` | Success | Deployment killed and lock removed |
| `1` | No Deployment | No active deployment found |

## Output

### Successful Kill
```bash
$ meza deploy-kill production
Meza environment production deploying; killing...
$ echo $?
0
```

### No Active Deployment
```bash
$ meza deploy-kill production
Meza environment 'production' not deploying
$ echo $?
1
```

## Process

When executed, `meza deploy-kill`:

1. **Verifies deployment lock** exists for the environment
2. **Reads process information** from the lock file
3. **Kills child processes** of the deployment
4. **Waits briefly** for graceful termination
5. **Sends wall message** to all logged-in users about termination
6. **Removes deployment lock** automatically

## System Notification

The command sends a system-wide message to all users:
```
Broadcast message from root@hostname (pts/0) (Mon Oct 20 15:30:00 2025):

Meza deploy terminated using 'meza deploy-kill' command.
```

## Use Cases

### Stuck Deployment
```bash
# Check deployment status
meza deploy-tail production

# If deployment appears hung, kill it
meza deploy-kill production

# Clean up and retry
meza deploy production
```

### Emergency Stop
```bash
# Stop deployment immediately
meza deploy-kill production

# Assess environment state
meza debug production

# Fix any issues and redeploy
meza deploy production
```

### Timeout Handling
```bash
#!/bin/bash
# Start deployment in background
meza deploy production &
DEPLOY_PID=$!

# Wait with timeout
if ! timeout 3600 wait $DEPLOY_PID; then
    echo "Deployment timed out, killing..."
    meza deploy-kill production
fi
```

## Post-Kill Cleanup

After killing a deployment, verify environment state:

```bash
# 1. Confirm deployment stopped
meza deploy-check production

# 2. Check for orphaned processes
ps aux | grep ansible

# 3. Review deployment logs
meza deploy-log production

# 4. Verify environment integrity
meza debug production

# 5. Check for incomplete changes
# Review any partially deployed configurations
```

## Potential Side Effects

⚠️ **Incomplete deployment**: Environment may be left in partially deployed state

⚠️ **Database inconsistency**: Database updates may be incomplete

⚠️ **File system state**: Files may be partially updated

⚠️ **Service disruption**: Running services may be in inconsistent state

## Recovery Steps

After using `deploy-kill`, follow these recovery steps:

### 1. Assess Environment State
```bash
meza debug production
meza deploy-log production | tail -50
```

### 2. Check Service Status
```bash
# Check critical services
systemctl status httpd
systemctl status mariadb
systemctl status elasticsearch
```

### 3. Verify Database Integrity
```bash
# Check MediaWiki database state
# Look for incomplete schema updates
```

### 4. Clean Redeploy
```bash
# Perform full deployment to ensure consistency
meza deploy production --tags all
```

## Related Commands

- [`meza deploy-check`](deploy-check.md) - Check if deployment is running before killing
- [`meza deploy-unlock`](deploy-unlock.md) - Remove lock without killing (if no process)
- [`meza deploy-log`](deploy-log.md) - Review deployment progress before killing
- [`meza deploy-tail`](deploy-tail.md) - Monitor deployment in real-time
- [`meza deploy`](deploy.md) - Restart deployment after killing

## Best Practices

### Before Using Deploy-Kill

1. **Check deployment logs** with `meza deploy-tail` to confirm it's actually stuck
2. **Wait reasonable time** - some deployment tasks take a long time
3. **Consider deployment phase** - killing during database updates is risky
4. **Document the reason** for killing the deployment

### After Using Deploy-Kill

1. **Verify environment state** thoroughly
2. **Check all services** are running correctly
3. **Review logs** for any errors or incomplete operations
4. **Test critical functionality** before declaring environment ready
5. **Communicate status** to team members

## When NOT to Use

❌ **Normal deployment progress** - even if it seems slow
❌ **Database migration phase** - high risk of corruption
❌ **First deployment** - initial setups take longer
❌ **Without checking logs** - deployment might be progressing normally

## Alternative Approaches

### For Slow Deployments
```bash
# Monitor progress instead of killing
meza deploy-tail production

# Check specific deployment phase
tail -f /opt/data-meza/logs/deploy/deploy.log
```

### For Stuck Deployments
```bash
# Try graceful approaches first
# Check if it's just a slow task
# Look for specific error messages
# Consider network/resource issues
```

## Troubleshooting

### Kill Command Fails
```bash
# Check if lock file exists
ls -la /opt/data-meza/env-*-deploy.lock

# Manually check for processes
ps aux | grep ansible-playbook

# Manual process termination (last resort)
sudo killall ansible-playbook
sudo rm /opt/data-meza/env-production-deploy.lock
```

### Environment Issues After Kill
```bash
# Check system logs
journalctl -xe

# Verify service states
systemctl --failed

# Check Meza logs
tail -100 /opt/data-meza/logs/deploy/deploy.log
```