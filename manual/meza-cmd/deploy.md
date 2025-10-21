# Meza Command: `deploy`

## Description

Deploy MediaWiki environments using Ansible automation.

## Usage

```bash
meza deploy <environment> [options]
```

## Examples

```bash
# Basic deployment
meza deploy monolith
meza deploy production

# Backup production, then deploy test with production data
meza backup production
meza deploy test --data-from=production --force
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<environment>` | Environment name to deploy | ✓ |

## Options

| Option | Description | Status |
|--------|-------------|--------|
| `--data-from=<env>` | Get data from backup of another environment | 🚧 Not yet implemented |
| `--force` | Overwrite with data from backups | 🚧 Not yet implemented |

## Notes

- Deployment process is orchestrated through Ansible playbooks
- Creates deployment locks to prevent concurrent deployments
- Supports both single-server and multi-server configurations
- Uses configuration from `/opt/conf-meza/` directories

## See Also

- [`meza backup`](backup.md) - Create environment backups
- [`meza setup-env`](setup.md) - Set up environment configuration
- [`meza list-wikis`](list-wikis.md) - List wikis in environment