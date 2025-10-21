# meza deploy-lock

Manually create a deployment lock for an environment.

## Synopsis

```bash
meza deploy-lock <environment>
```

## Description

The `meza deploy-lock` command manually creates a deployment lock for a specified environment. This prevents other deployment operations from running concurrently on the same environment.

**Use with caution:** This command should typically only be used for maintenance operations or troubleshooting. Normal deployments create locks automatically.

## Usage

```bash
meza deploy-lock <environment>
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `environment` | Name of the environment to lock | Yes |

## Examples

### Lock Production Environment
```bash
meza deploy-lock production
```

### Lock Development Environment
```bash
meza deploy-lock monolith
```

## Exit Codes

| Exit Code | Status | Description |
|-----------|--------|-------------|
| `0` | Success | Environment successfully locked |
| `1` | Failure | Environment could not be locked (already locked) |

## Output

### Successful Lock
```bash
$ meza deploy-lock production
Environment 'production' locked for deploy
$ echo $?
0
```

### Lock Already Exists
```bash
$ meza deploy-lock production
Environment 'production' could not be locked
$ echo $?
1
```

## Lock File Location

Creates deployment lock at:
```
/opt/data-meza/env-<environment>-deploy.lock
```

## Use Cases

### Maintenance Operations
```bash
# Lock environment during maintenance
meza deploy-lock production

# Perform maintenance tasks
# ... maintenance operations ...

# Unlock when complete
meza deploy-unlock production
```

### Preventing Accidental Deployments
```bash
# Lock environment before major changes
meza deploy-lock production

# Make configuration changes
# ... edit configs ...

# Deploy when ready
meza deploy production  # This will fail due to lock

# Unlock and deploy
meza deploy-unlock production
meza deploy production
```

### Testing Deployment Conflicts
```bash
# Create artificial lock for testing
meza deploy-lock development

# Test deployment behavior with existing lock
meza deploy development  # Should fail gracefully

# Clean up
meza deploy-unlock development
```

## Lock File Contents

The lock file contains metadata about when and why the lock was created:
- **Timestamp**: When the lock was created
- **Process information**: Details about the locking process
- **Purpose**: Manual lock vs automatic deployment lock

## Important Notes

⚠️ **Manual Cleanup Required**: Unlike automatic deployment locks, manual locks do **not** self-remove. You must explicitly unlock them with [`meza deploy-unlock`](deploy-unlock.md).

⚠️ **Blocks All Deployments**: While locked, **all** deployment operations will fail for that environment.

⚠️ **No Timeout**: Manual locks persist indefinitely until explicitly removed.

## Related Commands

- [`meza deploy-check`](deploy-check.md) - Check if environment is locked
- [`meza deploy-unlock`](deploy-unlock.md) - Remove deployment lock
- [`meza deploy-kill`](deploy-kill.md) - Kill deployment and remove lock
- [`meza deploy`](deploy.md) - Deploy environment (creates automatic lock)

## Best Practices

1. **Document why** you're creating manual locks
2. **Set reminders** to unlock when maintenance is complete
3. **Use sparingly** - prefer automatic deployment locking
4. **Check status first** with `meza deploy-check` before locking
5. **Communicate** with team when locking shared environments

## Troubleshooting

### Cannot Create Lock
If locking fails, check:
```bash
# Verify lock doesn't already exist
meza deploy-check production

# Check file system permissions
ls -la /opt/data-meza/env-*-deploy.lock

# Verify environment name is correct
ls /opt/conf-meza/secret/
```

### Orphaned Locks
If you suspect a lock is orphaned:
```bash
# Check lock status
meza deploy-check production

# Check if deployment process is actually running
ps aux | grep ansible

# If no process, safely unlock
meza deploy-unlock production
```