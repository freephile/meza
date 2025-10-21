# Meza Command: `config`

## Description

Get or set configuration values for Meza environments.

## Usage

```bash
meza config <key> [value]
```

## Examples

```bash
# Get current value of a configuration key
meza config database_host

# Set a configuration value
meza config database_host "db.example.com"

# Get MediaWiki version setting
meza config mediawiki_version

# Set environment-specific setting
meza config backup_retention_days 30
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<key>` | Configuration key to get or set | ✓ |
| `[value]` | Value to set (omit to get current value) | No |

## Behavior

- **With value**: Sets the configuration key to the specified value
- **Without value**: Displays the current value of the configuration key (if it exists)

## Notes

- Configuration changes may require redeployment to take effect
- Some configuration keys are environment-specific
- Critical settings should be verified before deployment
- Use `meza deploy` to apply configuration changes

## Common Configuration Keys

| Key | Description | Example |
|-----|-------------|---------|
| `database_host` | Database server hostname | `db.example.com` |
| `mediawiki_version` | MediaWiki version to deploy | `1.39.4` |
| `backup_retention_days` | Days to keep backups | `30` |
| `php_version` | PHP version to use | `8.1` |

## See Also

- [`meza deploy`](deploy.md) - Apply configuration changes
- [`meza setup`](setup.md) - Environment setup
- [`meza debug`](debug.md) - Debug configuration values