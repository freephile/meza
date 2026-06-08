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
- Routine `meza deploy <environment>` runs do not rebuild CirrusSearch or Semantic MediaWiki data by default
- The deploy-time rebuild tasks are tagged with `search-index`/`smw-data` and `never`, so operators must explicitly request them, for example:

```bash
meza deploy <environment> --tags search-index
meza deploy <environment> --tags smw-data
```

- If you want the operator-facing full rebuild workflow instead of a tagged deploy, use `meza maint rebuild <environment>`
- As with `meza maint rebuild`, a search rebuild run via deploy tags can finish with some CirrusSearch jobs still queued; this is normal MediaWiki job-queue behavior, not automatically a failure.

## See Also

- [`meza backup`](backup.md) - Create environment backups
- [`meza setup-env`](setup.md) - Set up environment configuration
- [`meza list-wikis`](list-wikis.md) - List wikis in environment