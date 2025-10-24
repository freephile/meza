# Meza Command Reference

Meza is a comprehensive MediaWiki deployment automation platform. Use these commands to manage your MediaWiki environments.

## Core Commands

### Environment Management
- [`meza install`](install.md) - Install Meza components and dependencies
- [`meza setup`](setup.md) - Set up environments and development tools
- [`meza deploy`](deploy.md) - Deploy MediaWiki environments
- [`meza update`](update.md) - Update Meza to specific version or branch

### Wiki Operations
- [`meza create`](create.md) - Create new wikis
- [`meza delete`](delete.md) - Delete wikis and components
- [`meza list-wikis`](list-wikis.md) - List all wikis in an environment

### Maintenance & Backup
- [`meza backup`](backup.md) - Create environment backups
- [`meza maint`](maint.md) - Run maintenance operations (jobs, rebuild, cleanup, encryption)
- [`meza debug`](debug.md) - Debug Ansible variables and configuration

### Deployment Management
- [`meza deploy-check`](deploy-check.md) - Check if environment is deploying
- [`meza deploy-lock`](deploy-lock.md) - Manually lock environment for deployment
- [`meza deploy-unlock`](deploy-unlock.md) - Remove deployment lock from environment
- [`meza deploy-kill`](deploy-kill.md) - Kill running deployment and remove lock
- [`meza deploy-log`](deploy-log.md) - Get deployment log file path
- [`meza deploy-tail`](deploy-tail.md) - Follow deployment logs in real-time

## Quick Start

1. **Install Meza:**
   ```bash
   # Download and install Meza
   # This approach does not work yet.
   curl -L https://raw.githubusercontent.com/nasa/meza/master/src/scripts/getmeza.sh | bash

   # Run the installer from a locally cloned repository:
   sudo bash src/scripts/getmeza.sh
   ```

2. **Deploy default environment:**
   ```bash
   meza deploy monolith
   ```

3. **Create your first wiki:**
   ```bash
   meza create wiki monolith
   ```

## Common Workflows

### Development Setup
```bash
# Download and install Meza first
sudo bash src/scripts/getmeza.sh
meza setup dev                    # Set up development tools
meza deploy monolith             # Deploy local environment
meza create wiki monolith        # Create test wiki
```

### Production Deployment
```bash
meza setup env production        # Set up production environment
meza backup production           # Backup before changes
meza deploy production           # Deploy to production
meza deploy-tail production      # Monitor deployment progress
```

### Wiki Management
```bash
meza list-wikis production       # List existing wikis
meza create wiki production      # Add new wiki
meza backup production           # Backup before deletion
meza delete wiki production      # Remove wiki
```

### Deployment Monitoring & Control
```bash
meza deploy-check production     # Check if deployment is running
meza deploy-tail production      # Follow deployment logs in real-time
meza deploy-kill production      # Kill stuck deployment if needed
meza deploy-unlock production    # Remove deployment lock after issues
```

### Version Management
```bash
meza update                      # List available versions
meza update 43.39.5             # Update to specific version
meza deploy production           # Deploy version changes
```

### Maintenance Operations
```bash
meza maint run-jobs production   # Run MediaWiki job queue
meza maint rebuild production    # Rebuild search index and SMW
meza maint cleanuploadstash production  # Clean upload stash
meza maint encrypt-string production "secret"  # Encrypt sensitive data
meza maint decrypt-string production "encrypted"  # Decrypt data
```

## Getting Help

- Use `meza <command> --help` for detailed command help
- Check `/opt/meza/manual/` for additional documentation
- See project documentation at the Meza repository

## Environment Concepts

- **Environment**: A complete MediaWiki deployment (e.g., "production", "development")
- **Wiki**: Individual wiki within an environment
- **Monolith**: Single-server environment (default for development)

## Configuration

- **Public config**: `/opt/conf-meza/public/<environment>/`
- **Secret config**: `/opt/conf-meza/secret/<environment>/`
- **Core defaults**: `/opt/meza/config/defaults.yml`
