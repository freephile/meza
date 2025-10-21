# meza deploy-unlock

Remove a deployment lock from an environment.

## Synopsis

```bash
meza deploy-unlock <environment>
```

## Description

The `meza deploy-unlock` command removes deployment locks from a specified environment, allowing new deployments to proceed. This command is used to clean up locks after deployments complete or to recover from stuck deployments.

## Usage

```bash
meza deploy-unlock <environment>
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `environment` | Name of the environment to unlock | Yes |

## Examples

### Unlock Production Environment
```bash
meza deploy-unlock production
```

### Unlock Development Environment
```bash
meza deploy-unlock monolith
```

## Exit Codes

| Exit Code | Status | Description |
|-----------|--------|-------------|
| `0` | Success | Lock successfully removed |
| `1` | No Lock Found | Environment was not locked |

## Output

### Successful Unlock
```bash
$ meza deploy-unlock production
Environment 'production' deploy lock removed
$ echo $?
0
```

### No Lock Present
```bash
$ meza deploy-unlock production
Environment 'production' is not deploying
$ echo $?
1
```

## Lock File Location

Removes deployment lock from:
```
/opt/data-meza/env-<environment>-deploy.lock
```

## Use Cases

### Clean Up After Failed Deployment
```bash
# Check if deployment is stuck
meza deploy-check production

# If locked but no deployment running, unlock
meza deploy-unlock production

# Retry deployment
meza deploy production
```

### Manual Lock Cleanup
```bash
# After maintenance operations
meza deploy-lock production
# ... perform maintenance ...
meza deploy-unlock production
```

### Recovery from Interrupted Deployments
```bash
# Check for orphaned locks
ps aux | grep ansible-playbook
meza deploy-check production

# If no process but lock exists, safely unlock
meza deploy-unlock production
```

## Safety Considerations

⚠️ **Verify no deployment is running** before unlocking:
```bash
# Check for active deployment processes
ps aux | grep -E "(ansible-playbook|meza deploy)"

# Check deployment logs for activity
meza deploy-tail production
```

⚠️ **Use deploy-kill for active deployments**: If a deployment is actually running, use [`meza deploy-kill`](deploy-kill.md) instead to properly terminate it.

## When to Use

### ✅ Safe to Unlock
- Deployment completed but lock remained
- Manual lock after maintenance is complete
- Process crashed leaving orphaned lock
- Lock file confirmed as stale

### ❌ Do NOT Unlock
- Active deployment is running
- Uncertain about deployment status
- Another user may be deploying

## Verification

After unlocking, verify the environment is ready:
```bash
# Confirm lock is removed
meza deploy-check production

# Check for any residual processes
ps aux | grep ansible

# Verify environment status
meza debug production
```

## Related Commands

- [`meza deploy-check`](deploy-check.md) - Verify lock status before unlocking
- [`meza deploy-lock`](deploy-lock.md) - Create deployment lock
- [`meza deploy-kill`](deploy-kill.md) - Kill active deployment and unlock
- [`meza deploy`](deploy.md) - Start new deployment after unlocking
- [`meza deploy-log`](deploy-log.md) - Check deployment logs for activity

## Common Scenarios

### Stuck Deployment Recovery
```bash
# 1. Check current status
meza deploy-check production

# 2. Look for running processes
ps aux | grep ansible-playbook

# 3. If no process but locked, unlock
meza deploy-unlock production

# 4. Retry deployment
meza deploy production
```

### Post-Maintenance Cleanup
```bash
# 1. Complete maintenance tasks
# ... maintenance work ...

# 2. Remove manual lock
meza deploy-unlock production

# 3. Verify environment is ready
meza deploy-check production
```

### Automation Script Error Handling
```bash
#!/bin/bash
deploy_env="production"

# Ensure clean state before deployment
if ! meza deploy-check $deploy_env; then
    echo "Environment locked, attempting unlock..."
    if meza deploy-unlock $deploy_env; then
        echo "Successfully unlocked $deploy_env"
    else
        echo "Failed to unlock $deploy_env"
        exit 1
    fi
fi

# Proceed with deployment
meza deploy $deploy_env
```

## Best Practices

1. **Always check first** with `meza deploy-check` before unlocking
2. **Verify no processes** are actually running the deployment
3. **Document the reason** for manual unlocking in team communications  
4. **Use deploy-kill** if you need to stop an active deployment
5. **Test environment** after unlocking to ensure it's in good state

## Troubleshooting

### Lock File Permissions
```bash
# Check lock file permissions
ls -la /opt/data-meza/env-*-deploy.lock

# Fix permissions if needed (as root)
sudo chown meza:meza /opt/data-meza/env-*-deploy.lock
```

### Persistent Lock Issues
```bash
# Check file system
df -h /opt/data-meza

# Verify directory permissions
ls -la /opt/data-meza/

# Manual lock file removal (last resort)
sudo rm /opt/data-meza/env-production-deploy.lock
```