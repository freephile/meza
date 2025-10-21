# Meza Command: `install`

## Description

Install Meza components and set up system dependencies.

## Usage

```bash
meza install [directive]
```

## Directives

### `monolith` - Single Machine Installation

Install Meza on a single machine for development or small-scale deployment.

```bash
meza install monolith
```

**What it does:**
- Installs all Meza dependencies
- Sets up MediaWiki and required services
- Configures single-server environment
- Prepares system for wiki deployment

### `dev-networking` - VirtualBox VM Networking

Set up networking configuration for VirtualBox virtual machines.

```bash
meza install dev-networking
```

**What it does:**
- Configures VM network interfaces
- Sets up development-friendly networking
- Enables proper host-guest communication

### `docker` - Docker Installation

Install Docker container runtime (CentOS only).

```bash
meza install docker
```

**What it does:**
- Installs Docker engine
- Configures Docker service
- Sets up container environment
- **Note:** Currently supported on CentOS only

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `[directive]` | Installation type to perform | No |

## Notes

- Installation requires root or sudo privileges
- `monolith` is the most common installation type for new setups
- Different directives may have OS-specific requirements
- Installation process may take time depending on internet connection

## See Also

- [`meza setup`](setup.md) - Set up environments after installation
- [`meza deploy`](deploy.md) - Deploy environments
- [`meza create`](create.md) - Create wikis after setup