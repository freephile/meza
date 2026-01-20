# Meza Script: `cleanup-backups.sh`

## Description

Automated cleanup script for managing SQL backup files in the Meza environment. Handles compression and deletion of old backup files to maintain optimal disk space usage while preserving critical backup data.

## Usage

```bash
# Manual execution (normally runs via cron)
/opt/meza/src/scripts/cleanup-backups.sh

# Check cron schedule
crontab -l | grep cleanup-backups
```

## Automated Scheduling

The script runs automatically via cron:

```bash
# Default schedule: Daily at 2:30 AM
30 2 * * * /opt/meza/src/scripts/cleanup-backups.sh > /dev/null 2>&1
```

## Configuration

The script operates with the following default settings:

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Backup Directory** | `/opt/data-meza/backups` | Location of SQL backup files |
| **Compress After** | 1 day | Age threshold for compressing .sql files |
| **Keep Uncompressed** | 90 days | Retention period for .sql files |
| **Keep Compressed** | 180 days | Retention period for .sql.gz files |
| **Log File** | `/opt/data-meza/logs/cleanup/backup-cleanup.log` | Activity log location |

## Cleanup Process

The script performs the following operations in sequence:

### 📊 **Step 1: Disk Usage Assessment**
- Records initial backup directory size
- Logs disk usage for monitoring purposes

### 🗜️ **Step 2: Compression**
- Compresses `.sql` files older than 1 day using gzip
- Reduces storage requirements significantly
- Preserves file integrity and accessibility

### 🧹 **Step 3: Uncompressed Cleanup**
- Removes uncompressed `.sql` files older than 90 days
- Ensures only recent uncompressed backups remain
- Prevents duplicate storage of compressed data

### 🗑️ **Step 4: Compressed Cleanup**
- Removes compressed `.sql.gz` files older than 180 days
- Provides extended retention for compressed backups
- Balances storage efficiency with data retention

### 📈 **Step 5: Final Assessment**
- Records final backup directory size
- Calculates space reclaimed during cleanup
- Maintains cleanup operation logs

## Customization

Override default settings in environment configuration:

```yaml
# In /opt/conf-meza/public/public.yml
logrotate_backup_files:
  enabled: true
  frequency: daily
  rotate: 120  # Keep 120 days instead of 90
  compress_after_days: 2  # Compress after 2 days instead of 1
  cleanup_old_compressed_days: 365  # Keep compressed for 1 year
```

## Safety Features

### 🛡️ **Error Handling**
- **Fail-safe operations**: Uses `set -euo pipefail` for strict error handling
- **Graceful failures**: Continues operation if individual operations fail
- **Directory validation**: Creates missing directories automatically

### 📝 **Comprehensive Logging**
- **Timestamped entries**: All operations logged with precise timestamps
- **Operation counts**: Reports number of files processed
- **Disk usage tracking**: Before/after storage usage comparison
- **Log rotation**: Cleanup logs older than 30 days automatically

### 🔒 **Permission Management**
- **Automatic ownership**: Sets proper ownership on created directories
- **Access control**: Maintains secure file permissions
- **Service account**: Runs with appropriate system privileges

## Examples

### Manual Execution

```bash
# Run cleanup manually (useful for testing)
sudo /opt/meza/src/scripts/cleanup-backups.sh

# View recent cleanup activity
tail -f /opt/data-meza/logs/cleanup/backup-cleanup.log

# Check disk usage
du -sh /opt/data-meza/backups/
```

### Monitoring Output

```bash
# Example log output
2025-10-22 02:30:01: Starting Meza backup cleanup process
2025-10-22 02:30:01: Initial backup directory usage: 2.4G /opt/data-meza/backups
2025-10-22 02:30:01: Compressing SQL files older than 1 days in /opt/data-meza/backups
2025-10-22 02:30:05: Compressed 12 SQL files
2025-10-22 02:30:05: Removing uncompressed SQL files older than 90 days in /opt/data-meza/backups
2025-10-22 02:30:05: Removed 3 old uncompressed SQL files
2025-10-22 02:30:05: Removing compressed SQL files older than 180 days in /opt/data-meza/backups
2025-10-22 02:30:05: Removed 8 old compressed SQL files
2025-10-22 02:30:06: Final backup directory usage: 1.1G /opt/data-meza/backups
2025-10-22 02:30:06: Meza backup cleanup process completed
```

## Integration

This script is automatically deployed and configured by the **logrotate** Ansible role:

- **Template**: `/opt/meza/src/roles/logrotate/templates/cleanup-backups.sh.j2`
- **Deployment**: Installed during `meza deploy` operations
- **Scheduling**: Cron job created automatically
- **Configuration**: Variables sourced from logrotate role defaults

## Troubleshooting

### Common Issues

**Script not running**:
```bash
# Check cron service
systemctl status crond

# Verify cron job exists
crontab -l | grep cleanup-backups
```

**Permission errors**:
```bash
# Check script permissions
ls -la /opt/meza/src/scripts/cleanup-backups.sh

# Verify backup directory ownership
ls -la /opt/data-meza/backups/
```

**Disk space issues**:
```bash
# Check available disk space
df -h /opt/data-meza/

# Monitor cleanup effectiveness
du -sh /opt/data-meza/backups/
```

## Performance Impact

- **Low system load**: Designed for off-peak execution (2:30 AM)
- **Incremental processing**: Only processes files meeting age criteria
- **Efficient compression**: Uses gzip for optimal compression ratios
- **Background operation**: Runs with minimal impact on system resources

## See Also

- [`meza backup`](backup.md) - Create database and file backups
- [`meza deploy`](deploy.md) - Deploy environments with backup management
- [Logrotate Role README](/opt/meza/src/roles/logrotate/README.md) - Comprehensive log management
- [Meza Backup Strategy Documentation](/opt/meza/manual/) - Backup best practices
