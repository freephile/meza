# Meza - MediaWiki EZ Admin

**The leading MediaWiki deployment automation platform**

## Usage

```bash
meza COMMAND [directives]
```

## Quick Multi-Server Setup

To set up a multi-server environment:

```bash
# 1. Setup the environment (follow prompts)
meza setup env

# 2. Edit configuration files as required:
sudo vi /opt/conf-meza/secret/<env-name>/hosts
sudo vi /opt/conf-meza/secret/<env-name>/secret.yml

# 3. Deploy the environment
sudo meza deploy <env-name>
```

## Command Reference

| Command | Directives | Description |
|---------|------------|-------------|
| **install** | `dev-networking` | Setup networking on VM |
| | `monolith` | Install server on this machine |
| | `docker` | Install Docker (CentOS only) |
| **deploy** | `<environment>` | Deploy your server |
| **setup** | `env` | Setup an environment |
| | `dev` | Setup dev features (Git, FTP) |
| **create** | `wiki` | Create a wiki |
| | `wiki-promptless` | Create a wiki without prompts |
| **backup** | `<environment>` | Create a backup of an environment |
| **docker** | `run` | 🧪 (experimental) Start container |
| | `exec` | Execute command on container |

## Getting Help

Every command has directives. If you run any command without directives, it will provide help for that command.

```bash
# Get help for specific commands
meza install --help
meza deploy --help
meza create --help
```

## Architecture Overview

- **Environment**: Complete MediaWiki deployment (production, development, etc.)
- **Wiki**: Individual wiki within an environment  
- **Monolith**: Single-server environment (ideal for development)
- **Multi-server**: Distributed deployment across multiple servers

## Configuration Locations

- **Public config**: `/opt/conf-meza/public/<environment>/`
- **Secret config**: `/opt/conf-meza/secret/<environment>/`
- **Core defaults**: `/opt/meza/config/defaults.yml`

## See Also

- [Complete Command Index](index.md) - Detailed documentation for all commands
- [Installation Guide](install.md) - Get started with Meza
- [Setup Guide](setup.md) - Environment configuration