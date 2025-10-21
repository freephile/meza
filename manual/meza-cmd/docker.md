# Meza Command: `docker`

## Description

🧪 **Experimental Docker container management for Meza environments.**

## Usage

```bash
meza docker [directive]
```

## Directives

### `run` - Start Docker Container

Start a Docker container for Meza. Optionally specify a Docker image to use.

```bash
meza docker run [image]
```

**Examples:**
```bash
# Start with default image
meza docker run

# Start with specific image
meza docker run centos:7
meza docker run ubuntu:20.04
```

### `exec` - Execute Commands

Execute a command on your Docker container.

```bash
meza docker exec <container_id> <command> [args...]
```

**Examples:**
```bash
# Execute bash shell
meza docker exec abc123 bash

# Run specific command
meza docker exec abc123 ls -la /opt/meza

# Check system status
meza docker exec abc123 systemctl status httpd
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `[directive]` | Docker operation to perform | No |
| `[image]` | Docker image name (for run) | No |
| `<container_id>` | Container ID (for exec) | ✓ (for exec) |
| `<command>` | Command to execute (for exec) | ✓ (for exec) |
| `[args...]` | Command arguments (for exec) | No |

## ⚠️ Experimental Status

**These Docker commands are experimental and may:**
- Have limited functionality
- Change without notice
- Not be suitable for production use
- Require additional setup or dependencies

## Prerequisites

- Docker must be installed on the system
- User must have Docker permissions
- Container must be running (for exec commands)

## Notes

- Docker functionality is still under development
- Use standard Meza installation for production environments
- Container state is not persistent by default
- For production deployments, use `meza install monolith` instead

## See Also

- [`meza install`](install.md) - Production installation methods
- [`meza deploy`](deploy.md) - Deploy environments
- [`meza setup`](setup.md) - Environment setup