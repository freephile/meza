# Meza Installation Guide

To install meza, use the [getmeza.sh](../../src/scripts/getmeza.sh) script ([docs](../../src/scripts/getmeza.md))

## ⚠️ Important Note

**There is no `meza install` command.** This documentation previously described a non-existent command.

## Correct Commands for Installation Tasks

### Single Machine Deployment

To set up Meza on a single machine (formerly `install monolith`):

```bash
meza deploy monolith
```

**What it does:**
- Deploys all Meza dependencies
- Sets up MediaWiki and required services
- Configures single-server environment
- Creates the complete MediaWiki deployment

### VirtualBox VM Networking Setup

To configure networking for VirtualBox VMs (formerly `install dev-networking`):

```bash
meza setup dev-networking
```

**What it does:**
- Configures VM network interfaces
- Sets up development-friendly networking
- Enables proper host-guest communication

### Docker Installation

To install Docker container runtime (formerly `install docker`):

```bash
meza setup docker
```

**What it does:**
- Installs Docker engine
- Configures Docker service
- Sets up container environment
- **Note:** Currently supported on CentOS only

## Quick Start for New Users

For a complete single-machine MediaWiki setup:

```bash
# Deploy monolith environment (creates 'demo' wiki automatically)
meza deploy monolith

# Create additional wikis
meza create wiki monolith mywiki "My Wiki"
```

## Notes

- Deployment requires root or sudo privileges
- `monolith` is the most common environment type for new setups
- Different setup commands may have OS-specific requirements
- Deployment process may take time depending on internet connection

## See Also

- [`meza deploy`](deploy.md) - Deploy environments
- [`meza setup`](setup.md) - Set up system components
- [`meza create`](create.md) - Create wikis after deployment
