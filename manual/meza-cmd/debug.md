# Meza Command: `debug`

## Description

General-purpose debug command to inspect Ansible variables and environment state.

## Usage

```bash
meza debug <environment> <variable_name>
```

## Examples

```bash
# Debug specific variables
meza debug monolith m_wikis
meza debug production m_install
meza debug development m_mediawiki_version

# Debug environment paths
meza debug monolith m_uploads_dir
meza debug monolith m_conf_meza_public

# Debug database configuration
meza debug production m_db_master_server
meza debug production m_db_slave_servers
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<environment>` | Environment name | ✓ |
| `<variable_name>` | Ansible variable to inspect | ✓ |

## Common Variables

| Variable | Description |
|----------|-------------|
| `m_wikis` | List of configured wikis |
| `m_install` | Meza installation directory |
| `m_uploads_dir` | Wiki uploads directory |
| `m_mediawiki_version` | MediaWiki version |
| `m_conf_meza_public` | Public configuration directory |
| `m_conf_meza_secret` | Secret configuration directory |
| `m_db_master_server` | Database master server |
| `m_db_slave_servers` | Database slave servers |

## Notes

- Uses Ansible's debug module to display variable values
- Loads environment configuration through set-vars role
- Useful for troubleshooting configuration issues
- Can inspect any Ansible variable available in the environment

## See Also

- [`meza list-wikis`](list-wikis.md) - List wikis (uses debug internally)
- [`meza deploy`](deploy.md) - Deploy environment
- [`meza setup-env`](setup.md) - Environment setup