# meza deploy-notify

Deploy environment with notification capabilities for automated workflows.

## Usage

```bash
meza deploy-notify <environment> [deploy_type] [deploy_args] [ansible-options]
```

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `environment` | Target environment name | Yes | - |
| `deploy_type` | Type of deployment to perform | No | standard |
| `deploy_args` | Additional deployment arguments | No | - |
| `ansible-options` | Standard Ansible playbook options | No | - |

## Description

The `deploy-notify` command performs deployments with enhanced notification and monitoring capabilities designed for automated workflows. It wraps the standard deployment process with additional notification mechanisms.

This command is primarily used for:
- **CI/CD pipeline deployments** with notification integration
- **Automated deployment workflows** requiring status updates
- **Monitored deployments** where external systems need deployment status
- **Integration with notification systems** (email, Slack, webhooks, etc.)

## Examples

### Basic Deployment with Notifications
```bash
# Deploy with notifications enabled
sudo meza deploy-notify production

# Deploy specific type with notifications
sudo meza deploy-notify production config-only
```

### CI/CD Integration
```bash
# In CI/CD pipeline with verbose logging
sudo meza deploy-notify production standard --verbose

# With specific deployment arguments
sudo meza deploy-notify production quick --tags mediawiki
```

## Features

- **Automatic deployment locking** prevents concurrent deployments
- **Enhanced logging** for automation integration
- **Notification hooks** for external system integration
- **Status reporting** for monitoring systems
- **Safe automation** with proper exit codes

## Deployment Lock Management

Like standard deployments, `deploy-notify` uses deployment locks:
- Creates lock file to prevent concurrent deployments
- Exits gracefully if another deployment is in progress
- Removes lock file upon completion or failure

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Deployment completed successfully |
| `1` | Deployment failure or environment error |
| `2` | Lock file conflict (deployment already in progress) |

## Notification Integration

The command integrates with notification systems through the `autodeployer` role, which can be configured to send:
- **Start notifications** when deployment begins
- **Progress updates** during deployment phases
- **Success notifications** upon completion
- **Failure alerts** if deployment fails

Configuration for notifications is managed through environment-specific settings in:
- `/opt/conf-meza/public/<env>/public.yml`
- `/opt/conf-meza/secret/<env>/secret.yml`

## See Also

- [`meza deploy`](deploy.md) - Standard deployment command
- [`meza autodeploy`](autodeploy.md) - Automated deployment with change detection
- [`meza deploy-check`](deploy-check.md) - Check deployment status
- [`meza deploy-tail`](deploy-tail.md) - Follow deployment logs