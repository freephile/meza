# meza deploy-check

Check if a Meza environment is currently deploying.

## Synopsis

```bash
meza deploy-check <environment>
```

## Description

The `meza deploy-check` command verifies whether a specific environment is currently undergoing deployment by checking for the presence of a deployment lock file.

This command is useful for:
- **Automation scripts** that need to wait for deployments to complete
- **Monitoring systems** checking deployment status
- **Manual verification** before starting operations that conflict with deployments

## Usage

```bash
meza deploy-check <environment>
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `environment` | Name of the environment to check | Yes |

## Examples

### Check Production Environment
```bash
meza deploy-check production
```

### Check Development Environment
```bash
meza deploy-check monolith
```

## Exit Codes

The command uses exit codes to indicate deployment status:

| Exit Code | Status | Description |
|-----------|--------|-------------|
| `0` | Not deploying | Environment is available for deployment |
| `1` | Currently deploying | Environment has active deployment lock |

## Output

### Environment Not Deploying
```bash
$ meza deploy-check production
Meza environment 'production' not deploying
$ echo $?
0
```

### Environment Currently Deploying
```bash
$ meza deploy-check production
Meza environment 'production' deploying; /opt/data-meza/env-production-deploy.lock exists
$ echo $?
1
```

## Lock File Location

Deployment locks are stored at:
```
/opt/data-meza/env-<environment>-deploy.lock
```

## Use Cases

### Script Automation
```bash
#!/bin/bash
if meza deploy-check production; then
    echo "Starting backup - no deployment in progress"
    meza backup production
else
    echo "Deployment in progress, skipping backup"
    exit 1
fi
```

### Wait for Deployment Completion
```bash
#!/bin/bash
while ! meza deploy-check production; do
    echo "Waiting for deployment to complete..."
    sleep 30
done
echo "Deployment finished, proceeding with next steps"
```

### Monitoring Integration
```bash
# Check multiple environments
for env in production staging development; do
    if ! meza deploy-check $env; then
        echo "ALERT: $env is currently deploying"
    fi
done
```

## Related Commands

- [`meza deploy`](deploy.md) - Deploy environment (creates deployment lock)
- [`meza deploy-lock`](deploy-lock.md) - Manually create deployment lock
- [`meza deploy-unlock`](deploy-unlock.md) - Remove deployment lock
- [`meza deploy-kill`](deploy-kill.md) - Kill running deployment and unlock
- [`meza deploy-log`](deploy-log.md) - View deployment logs
- [`meza deploy-tail`](deploy-tail.md) - Follow deployment logs in real-time

## Notes

- **Non-destructive**: This command only reads lock file status
- **No permissions required**: Can be run by any user (no sudo needed)
- **Instant response**: Very fast operation, suitable for frequent polling
- **Automation-friendly**: Designed for use in scripts and monitoring systems

## Best Practices

1. **Use in scripts** before performing environment operations
2. **Check before manual deployments** to avoid conflicts
3. **Monitor deployment status** in production environments
4. **Combine with sleep loops** for waiting scenarios