# meza update

Update the Meza repository to a specific version or branch.

## Synopsis

```bash
meza update [version]
```

## Description

The `meza update` command manages Meza version updates by interacting with the Git repository. It can display available versions or update to a specific version/branch.

**Important:** This command operates on the Meza installation itself (`/opt/meza`) and requires a clean Git working directory.

## Usage

### List Available Versions
```bash
sudo meza update
```

Shows all available version 43.x releases, sorted numerically. Example output:
```
The following versions are available:
43.0.0
43.0.1
43.4.1
43.10.1
43.25.11
43.36.1
43.39.5

You are currently on version 43.39.5-13-gf0acdaf
To change versions, do 'sudo meza update <version>'
```

### Update to Specific Version
```bash
sudo meza update <version>
```

Updates to the specified version tag or branch.

## Examples

### Check Available Versions
```bash
sudo meza update
```

### Update to Latest Stable Release
```bash
sudo meza update 43.39.5
```

### Update to Development Branch
```bash
sudo meza update dev
```

### Update to Release Branch
```bash
sudo meza update REL1_39
```

## Version Filtering

The command automatically filters and displays only versions starting with "43." and sorts them numerically to ensure proper version ordering (43.36.x appears after 43.4.x, not before).

## Prerequisites

- **Root privileges**: Command must be run with `sudo`
- **Clean working directory**: Git status must be clean with no uncommitted changes
- **Network access**: Required to fetch latest tags and commits from remote repository

## Workflow

1. **Remote setup**: Configures `mezaremote` pointing to `https://github.com/nasa/meza.git`
2. **Fetch updates**: Downloads latest commits and tags from remote repository
3. **Version check**: Validates requested version exists as tag or branch
4. **Update**: Checks out specified version or branch
5. **Confirmation**: Displays success message with next steps

## Error Handling

### Uncommitted Changes
```
Files have been modified in /opt/meza. Clean them up before proceeding.
MSG: M src/scripts/meza.py
```

**Solution:** Commit or stash changes before updating.

### Invalid Version
```
invalid-version is not a valid version or branch
```

**Solution:** Use `meza update` to see available versions.

### Network Issues
If tag fetching fails due to conflicts, the command automatically retries with `--force` option.

## Post-Update Steps

After updating Meza:

1. **Deploy changes** to apply updates:
   ```bash
   sudo meza deploy <environment>
   ```

2. **Test functionality** in development environment first

3. **Review release notes** for breaking changes

## Related Commands

- [`meza deploy`](deploy.md) - Deploy environment updates after version change
- [`meza backup`](backup.md) - Backup before updating (recommended)
- [`meza debug`](debug.md) - Debug configuration after updates

## Notes

- Only displays version 43.x releases (filtered automatically)
- Versions are sorted numerically for proper ordering
- Command changes the entire Meza installation, affecting all environments
- Always test updates in development environment before production
- Consider backing up environments before major version updates

## Troubleshooting

### Git Repository Issues
```bash
# Check repository status
cd /opt/meza
git status

# Reset to clean state (caution: loses changes)
git reset --hard HEAD
git clean -fd
```

### Permission Issues
Ensure the command is run with `sudo` and the user has appropriate permissions to modify `/opt/meza`.