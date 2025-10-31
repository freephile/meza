# getmeza.sh - Meza Bootstrap Installation Script

## Overview

The `getmeza.sh` script is the primary bootstrap installer for the Meza MediaWiki deployment platform. It performs initial system setup, installs dependencies, clones the Meza repository, and prepares the system for MediaWiki deployment automation.

## Purpose

This script serves as the entry point for installing Meza on a fresh Linux system. It handles:

- Operating system detection and compatibility checking
- Installation of required system packages and repositories
- Git repository cloning and initial configuration
- User account creation and permissions setup
- Ansible environment preparation

## Usage

```bash
# Standard installation (requires root privileges)
sudo bash getmeza.sh

# Skip internet connectivity check (useful for offline/restricted environments)
sudo bash getmeza.sh --skip-conn-check
```

### Requirements

- **Root privileges**: Must be run as root or with sudo
- **Internet connection**: Required for package installation and git cloning (unless `--skip-conn-check` is used)
- **Supported OS**: Red Hat Enterprise Linux, or Rocky Linux

## Command Line Options

| Option | Description |
|--------|-------------|
| `--skip-conn-check` | Skip internet connectivity verification (use for Continuous Integration like GitHub Actions) |

## Environment Variables

The script respects the following environment variables for customization:

| Variable | Default | Description |
|----------|---------|-------------|
| `MEZA_REPOSITORY_URL` | `https://github.com/nasa/meza.git` | Git repository URL to clone from |
| `MEZA_BRANCH_NAME` | `main` | Git branch to checkout |

### Example with Custom Repository

```bash
export MEZA_REPOSITORY_URL='https://github.com/freephile/meza.git'
export MEZA_BRANCH_NAME='REL1_39'
sudo bash getmeza.sh
```

## What the Script Does

### 1. Root Permission Check
- Verifies the script is running as root
- Exits with error message if not running with sufficient privileges

### 2. Internet Connectivity Validation
- Tests connection to `cdn.redhat.com` with up to 100 retry attempts
- Provides detailed feedback on connection status
- Can be skipped with `--skip-conn-check` flag

### 3. Operating System Detection
- Identifies Red Hat variants (RHEL, Rocky Linux)
- Determines version numbers for package management decisions
- Exits if unsupported OS is detected

### 4. Directory Structure Creation
```
/opt/conf-meza/          # Configuration directory (755 permissions)
/opt/conf-meza/secret/   # Secret configuration (775 permissions) 
/opt/data-meza/          # Data directory for locks and runtime files
/opt/.deploy-meza/       # Deployment configuration (755 permissions)
```

### 5. Repository Installation (EPEL)
- **Rocky Linux**: Enables PowerTools repository and installs EPEL
- **RHEL**: Enables CodeReady Builder and Ansible repositories based on version

### 6. Package Installation
Installs core dependencies based on OS:
- **Git**: Version control for Meza repository
- **Ansible**: Automation framework for deployments  
- **Python**: Runtime environment and SELinux bindings
- **libselinux-python/python3-libselinux**: SELinux integration

### 7. Repository Cloning
- Clones Meza repository to `/opt/meza`
- Uses configurable repository URL and branch
- Sets appropriate file permissions (readable by all users, executable directories)

### 8. System Integration
- Creates symbolic link: `/usr/bin/meza` → `/opt/meza/src/scripts/meza.py`
- Generates a shell version of meza's configuration variables at `/opt/.deploy-meza/config.sh`

### 9. User Account Management
- Creates or updates `meza-ansible` user account
- Migrates home directory from `/home/meza-ansible` to `/opt/conf-meza/users/meza-ansible`
- Sets up proper ownership and permissions for Meza directories

### 10. System Security Configuration
- Disables TTY requirement for sudo operations
- Removes visible password requirement for sudo
- Configures permissions for ansible operations

### 11. Ansible Environment Setup
- Installs Ansible in the meza-ansible user's Python environment
- Installs required Ansible collections from `requirements.yml`

## File Locations

| Path | Purpose |
|------|---------|
| `/opt/meza/` | Main Meza installation directory |
| `/opt/conf-meza/` | Configuration files and secrets |
| `/opt/data-meza/` | Runtime data and lock files |
| `/opt/.deploy-meza/config.sh` | Basic deployment configuration |
| `/usr/bin/meza` | System-wide meza command symlink |

## Supported Operating Systems

### Red Hat Enterprise Linux (RHEL)
- **Version 7.x**: Uses YUM package manager
- **Version 8.x**: Uses DNF, enables specific repositories and PHP modules

### CentOS
- Uses YUM package manager
- Installs EPEL repository automatically

### Rocky Linux  
- Uses DNF package manager
- Enables PowerTools repository
- Configures PHP and Python exclusions
- Resets and enables PHP 7.4 module

## Security Considerations

- **Root Execution**: Script requires root privileges for system-wide changes
- **Network Access**: Downloads packages and repositories from internet
- **User Creation**: Creates system user `meza-ansible` with sudo access
- **Sudo Configuration**: Modifies sudoers file to disable TTY requirements
- **File Permissions**: Sets specific permissions on configuration directories

## Error Handling

The script includes comprehensive error handling:

- **Exit Code 1**: Not running as root
- **Exit Code 187**: Unsupported RedHat version or unknown distro
- **Exit Code 188**: Unsupported RedHat version during package installation  
- **Exit Code 189**: Cannot determine OS distro/version during package installation

## Next Steps

After successful completion, the script displays:

```
meza command installed. Use it:
  sudo meza deploy monolith -vvv
```

This indicates the system is ready for MediaWiki deployment using the Meza automation platform.

## Development Notes

- **TODO**: Refactor and document script better (see [Issue #172](https://github.com/freephile/meza/issues/172#issuecomment-3141998590))
- **Umask**: Sets umask 002 to ensure proper permissions for git operations
- **Compatibility**: Designed for restrictive systems where permission management is critical

## Related Documentation

- [Meza Installation Guide](../../manual/meza-cmd/install.md)
- [Meza Setup Documentation](../../manual/meza-cmd/setup.md)
- [Deployment Guide](../../manual/meza-cmd/deploy.md)