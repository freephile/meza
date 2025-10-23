# meza autodeploy

Perform automated deployment with change detection for continuous integration/deployment workflows.

## Usage

```bash
meza autodeploy <environment> [deploy_type] [deploy_args] [ansible-options]
```

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `environment` | Target environment name | Yes | - |
| `deploy_type` | Type of deployment to perform | No | standard |
| `deploy_args` | Additional deployment arguments | No | - |
| `ansible-options` | Standard Ansible playbook options | No | - |

## Description

The `autodeploy` command is designed for automated deployment scenarios, particularly useful for:

- **Continuous Integration/Deployment (CI/CD)** pipelines
- **Cron-based automated deployments** that check for changes
- **Scheduled maintenance deployments** with change detection
- **Remote deployment triggers** from external systems

This command differs from regular `deploy` in that it:
- Includes built-in change detection mechanisms
- Can be safely run repeatedly (only deploys when changes detected)
- Optimized for unattended/automated execution
- Includes additional logging for automation workflows

## Examples

### Basic Autodeploy
```bash
# Autodeploy to production environment
sudo meza autodeploy production

# Autodeploy with specific deployment type
sudo meza autodeploy production config-only
```

### CI/CD Integration
```bash
# In CI/CD pipeline with verbose logging
sudo meza autodeploy production standard --verbose >> /var/log/meza-autodeploy.log 2>&1

# With specific tags for faster deployment
sudo meza autodeploy production quick --tags mediawiki,sync-configs
```

### Cron Job Usage
```bash
# Example cron entry for nightly automates deployments
# Check for changes and deploy if needed every night at 2 AM
0 2 * * * /usr/local/bin/meza autodeploy production >> /var/log/meza-cron.log 2>&1
```

## Deploy Types

| Type | Description | Use Case |
|------|-------------|----------|
| `standard` | Full deployment with all checks | Default automated deployment |
| `config-only` | Configuration changes only | Quick config updates |
| `quick` | Skip time-intensive verification | Fast deployments |
| `maintenance` | Include maintenance tasks | Scheduled maintenance windows |

## Deployment Lock Behavior

- **Automatic lock management**: Creates deployment locks to prevent concurrent runs
- **Lock detection**: Exits gracefully if another deployment is in progress
- **Safe for automation**: Won't interfere with manual deployments

## Change Detection

The autodeploy command includes intelligent change detection:
- **Git repository changes** in Meza core
- **Configuration file modifications** in conf-meza
- **Environment-specific changes** in secret and public configs

## Logging and Monitoring

All autodeploy operations include enhanced logging:
- **Deployment logs**: Written to standard Meza log locations
- **Change detection logs**: Details about what triggered the deployment
- **Exit codes**: Proper return codes for automation integration

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success (deployment completed or no changes detected) |
| `1` | Deployment failure or environment error |
| `2` | Lock file conflict (another deployment in progress) |

## Security Considerations

- **Run as privileged user**: Requires sudo/root access
- **Vault password access**: Must have access to environment vault passwords
- **SSH key access**: Requires SSH keys for multi-server deployments

## Troubleshooting

### Common Issues

**Deployment locks stuck:**
```bash
# Check lock status
sudo meza deploy-check production

# Remove stuck lock if needed
sudo meza deploy-unlock production
```

**Permission errors:**
```bash
# Ensure proper ownership of config files
sudo chown -R meza-ansible:wheel /opt/conf-meza/
```

**Change detection not working:**
```bash
# Manually verify git status
cd /opt/meza && git status
cd /opt/conf-meza && git status
```

## See Also

- [`meza deploy`](deploy.md) - Manual deployment command
- [`meza deploy-check`](deploy-check.md) - Check deployment status
- [`meza deploy-lock`](deploy-lock.md) - Manual deployment locking
- [`meza backup`](backup.md) - Create backups before deployment

## Integration Examples

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                sh 'sudo meza autodeploy production'
            }
        }
    }
}
```

### GitHub Actions
```yaml
- name: Autodeploy Meza
  run: sudo meza autodeploy production
  env:
    ANSIBLE_HOST_KEY_CHECKING: False
```
