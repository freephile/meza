# Meza Command: `backup`

## Description

Create complete backups of a Meza environment including databases, uploads, and configuration.

## Usage

```bash
meza backup <environment>
```

## Examples

```bash
# Backup production environment
meza backup production

# Backup development environment
meza backup development

# Backup local monolith setup
meza backup monolith
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<environment>` | Environment name to backup | ✓ |

## What Gets Backed Up

The backup process includes:

- 📊 **Database dumps** - All wiki databases and user data
- 📁 **Upload files** - All wiki media and file uploads
- ⚙️ **Configuration** - Environment-specific settings
- 🔑 **Secrets** - Encrypted configuration and passwords

## Notes

- Backup process runs automatically before major operations
- Backups are stored in the configured backup directory
- Use backups for disaster recovery or environment migration
- No additional directives are supported - backs up the entire environment

## See Also

- [`meza deploy`](deploy.md) - Deploy environments (can restore from backup)
- [`meza delete`](delete.md) - Delete operations (backup recommended first)
- [`meza setup-env`](setup.md) - Environment setup