# Meza - MediaWiki EZ Admin

**The leading MediaWiki deployment automation platform**

## Usage

```bash
meza COMMAND [directives]
```

## Quick Start

### Single Machine Development Setup
```bash
# Deploy monolith environment (creates 'demo' wiki automatically)
meza deploy monolith

# Create additional wikis
meza create wiki monolith
```

### Multi-Server Production Setup
```bash
# 1. Setup the environment (follow prompts)
meza setup env production

# 2. Edit configuration files as required:
sudo vi /opt/conf-meza/secret/production/hosts
sudo vi /opt/conf-meza/secret/production/secret.yml

# 3. Deploy the environment
sudo meza deploy production

# 4. Monitor deployment progress
meza deploy-tail production
```

### Common Management Tasks
```bash
# List existing wikis
meza list-wikis monolith

# Backup before changes
meza backup monolith

# Run maintenance jobs
meza maint run-jobs monolith

# Check deployment status
meza deploy-check production
```

## Command Reference

### Environment Management
| Command | Directives | Description |
|---------|------------|-------------|
| **setup** | `env` | Setup a new environment |
| | `dev-networking` | Configure VirtualBox VM networking |
| | `docker` | Install Docker (CentOS only) |
| **deploy** | `<environment>` | Deploy MediaWiki to environment |
| **update** | `[version]` | Update Meza to version or branch |

### Wiki Operations
| Command | Directives | Description |
|---------|------------|-------------|
| **create** | `wiki` | Create a new wiki (interactive) |
| | `wiki-promptless` | Create wiki without prompts |
| **delete** | `wiki` | Delete a wiki (interactive) |
| | `wiki-promptless` | Delete wiki without prompts |
| | `elasticsearch` | Delete Elasticsearch data |
| **list-wikis** | `<environment>` | List all wikis in environment |

### Maintenance & Backup
| Command | Directives | Description |
|---------|------------|-------------|
| **backup** | `<environment>` | Create environment backup |
| **push-backup** | `<environment>` | Push backup to remote location |
| **maint** | `run-jobs` | Run MediaWiki job queue |
| | `rebuild` | Rebuild search index and SMW |
| | `cleanuploadstash` | Clean upload stash |
| | `encrypt-string` | Encrypt sensitive data |
| | `decrypt-string` | Decrypt data |

### Deployment Management
| Command | Directives | Description |
|---------|------------|-------------|
| **deploy-check** | `<environment>` | Check if environment is deploying |
| **deploy-lock** | `<environment>` | Lock environment for deployment |
| **deploy-unlock** | `<environment>` | Remove deployment lock |
| **deploy-kill** | `<environment>` | Kill deployment and remove lock |
| **deploy-log** | `<environment>` | Get deployment log file path |
| **deploy-tail** | `<environment>` | Follow deployment logs real-time |

### Development & Debug
| Command | Directives | Description |
|---------|------------|-------------|
| **debug** | `<environment> [variable]` | Debug Ansible variables |
| **docker** | `run` | 🧪 Start development container |
| | `exec` | Execute command on container |
| **migrate-wikis** | `<environment>` | Migrate wiki IDs to declarative YAML |

## Getting Help

Every command has directives. If you run any command without directives, it will provide help for that command.

```bash
# Get help for main commands
meza deploy --help
meza setup --help
meza create --help
meza maint --help

# Get help for deployment management
meza deploy-check --help
meza deploy-tail --help

# Run commands without arguments for specific help
meza backup
meza debug
meza delete
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

- [Index](index.md) - Overview documentation for all commands
- [Setup Guide](setup.md) - Environment configuration
