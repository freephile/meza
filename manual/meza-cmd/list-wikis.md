# Meza Command: `list-wikis`

## Description

List all wikis in the specified environment.

## Usage

```bash
meza list-wikis [environment]
```

## Examples

```bash
# List wikis in default environment (monolith)
meza list-wikis

# List wikis in specific environment
meza list-wikis production
meza list-wikis development
```

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `[environment]` | Environment name | No | `monolith` |

## Output

Displays a list of all configured wikis in the environment, showing:
- Wiki IDs
- Wiki display names
- Configuration status

## Notes

- Uses Ansible to query the environment configuration
- Reads wiki definitions from the environment's configuration files
- Helpful for verifying wiki setup before operations

## See Also

- [`meza create`](create.md) - Create new wikis
- [`meza delete`](delete.md) - Delete wikis
- [`meza deploy`](deploy.md) - Deploy environment