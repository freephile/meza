# Meza Command: `setup`

## Description

Set up and configure Meza environments and system components.

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

### `dev-networking` - VM Networking Setup

Configure VirtualBox VM networking for local development.

```bash
meza setup dev-networking
```

**What it does:**
- Configures VM network interfaces
- Sets up development-friendly networking
- Enables proper host-guest communication

### `docker` - Docker Installation

Install Docker runtime on supported systems.

```bash
meza setup docker
```

**What it does:**
- Installs Docker engine
- Configures Docker service
- Sets up container environment
- **Note:** Currently supported on CentOS only

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `[directive]` | Setup operation to perform | Yes |
| `<environment_name>` | Environment name (for env directive) | ✓ (for env) |

## Notes

- Environment names should be descriptive (production, development, staging, etc.)
- Each environment gets its own configuration in `/opt/conf-meza/`
- Development setup for Vagrant is documented in [manual/DEVELOPING.md](../DEVELOPING.md)
- Environment setup is required before deploying to a new environment

## See Also

- [`meza deploy`](deploy.md) - Deploy configured environments
- [`meza create`](create.md) - Create wikis in environments
- [`meza backup`](backup.md) - Backup environments
