# Meza Command: `setup`

## Description

Set up and configure Meza environments and development tools.

## Usage

```bash
meza setup [directive]
```

## Directives

### `env` - Environment Setup

Set up a new environment configuration.

```bash
meza setup env <environment_name>
```

**Examples:**
```bash
meza setup env production
meza setup env development
meza setup env staging
```

**What it does:**
- Creates environment configuration directories
- Sets up initial configuration templates
- Prepares secret and public configuration files
- Initializes environment-specific settings

### `dev` - Development Setup

Set up development tools and configuration for easier development workflow.

```bash
meza setup dev
```

**What it does:**
- Configures Git user settings
- Sets up FTP access for development
- Prepares development environment tools
- Streamlines developer workflow

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `[directive]` | Setup operation to perform | No |
| `<environment_name>` | Environment name (for env directive) | ✓ (for env) |

## Notes

- Environment names should be descriptive (production, development, staging, etc.)
- Each environment gets its own configuration in `/opt/conf-meza/`
- Development setup is typically run once per developer workstation
- Environment setup is required before deploying to a new environment

## See Also

- [`meza deploy`](deploy.md) - Deploy configured environments
- [`meza create`](create.md) - Create wikis in environments
- [`meza backup`](backup.md) - Backup environments