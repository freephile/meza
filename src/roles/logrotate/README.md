# Meza Logrotate Retention Policy

## Overview

The Meza logrotate role provides comprehensive log rotation and backup file management for the Meza MediaWiki platform. This document outlines the retention policies for different types of logs and files managed by the system.

## 📋 Retention Policy Summary

### **Deployment & System Logs**

#### Deployment Logs
- **Location**: `/opt/data-meza/logs/deploy-output/*.log`
- **Retention**: 📅 **30 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Purpose**: Individual deployment session logs for troubleshooting recent deployments

#### Main Deploy Log
- **Location**: `/opt/data-meza/logs/deploy/deploy.log`
- **Retention**: 📅 **52 weeks (1 year)**
- **Rotation**: Weekly
- **Compression**: 🗜️ After 7 days
- **Purpose**: Ongoing deployment history for long-term audit trail

### **Backup Management**

#### SQL Backup Files
- **Location**: `/opt/data-meza/backups/*.sql`
- **Retention**: 📅 **90 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Extended Cleanup**: 🧹 Compressed files removed after 180 days
- **Purpose**: Database backup files with automated compression and cleanup

#### Backup Operation Logs
- **Location**: `/opt/data-meza/logs/backup/*.log`
- **Retention**: 📅 **12 weeks (3 months)**
- **Rotation**: Weekly
- **Compression**: 🗜️ After 7 days
- **Purpose**: Backup operation status and error logs

### **Application Logs**

#### MediaWiki Debug Logs
- **Location**: `/opt/data-meza/logs/mediawiki/*.log`
- **Retention**: 📅 **7 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Services**: PHP-FPM reload after rotation
- **Purpose**: MediaWiki application debug and error logs

#### Job Queue Logs
- **Location**: `/opt/data-meza/logs/jobqueue/*.log`
- **Retention**: 📅 **7 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Purpose**: MediaWiki background job processing logs

#### PHP Logs
- **Location**: `/opt/data-meza/logs/php/*.log`
- **Retention**: 📅 **7 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Services**: PHP-FPM reload after rotation
- **Purpose**: PHP error and access logs

### **Infrastructure Logs**

#### Apache/Web Server Logs
- **Location**: `/opt/data-meza/logs/apache/*.log`
- **Retention**: 📅 **14 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Services**: 🔄 Apache/httpd reload after rotation
- **Purpose**: Web server access and error logs

#### Elasticsearch Logs
- **Location**: `/opt/data-meza/logs/elasticsearch/*.log`
- **Retention**: 📅 **14 days**
- **Rotation**: Daily
- **Compression**: 🗜️ After 1 day
- **Purpose**: Search engine operation and error logs

### **Maintenance Logs**

#### Cleanup Logs
- **Location**: `/opt/data-meza/logs/cleanup/*.log`
- **Retention**: 📅 **4 weeks**
- **Rotation**: Weekly
- **Compression**: 🗜️ After 7 days
- **Purpose**: System cleanup operation logs

## 🔧 Global Configuration

### Standard Features
- ✅ **Compression enabled** with delayed compression (compress old files, not current)
- ✅ **Date extensions** for rotated files (YYYYMMDD format)
- ✅ **Missing file tolerance** (won't fail if logs don't exist)
- ✅ **Empty file handling** (won't rotate empty logs)
- ✅ **Automatic testing** of logrotate configuration after deployment

### Service Integration
- **Apache/httpd**: Graceful reload after log rotation
- **PHP-FPM**: Reload to release file handles
- **File permissions**: Intelligent fallback when apache user/group doesn't exist

## 📊 Retention Summary by Priority

| Priority | Duration | Log Types |
|----------|----------|-----------|
| **Critical** | 1 year | Main deployment logs |
| **Important** | 90 days | SQL backup files |
| **Standard** | 2-4 weeks | Infrastructure logs (Apache, Elasticsearch) |
| **Debug** | 1 week | Application debug logs (MediaWiki, PHP, Job Queue) |

## 🛠️ Configuration Variables

All retention policies can be customized by overriding variables in:
- `/opt/conf-meza/public/<env>/public.yml`
- `/opt/conf-meza/secret/<env>/secret.yml`

### Example Customization
```yaml
# Extend MediaWiki log retention to 14 days
logrotate_mediawiki_logs:
  enabled: true
  frequency: daily
  rotate: 14
  compress_after_days: 1
  create_mode: "0644"
  create_owner: "{{ user_apache }}"
  create_group: "{{ group_apache }}"

# Increase SQL backup retention to 180 days
logrotate_backup_files:
  enabled: true
  frequency: daily
  rotate: 180
  compress_after_days: 1
  cleanup_old_compressed_days: 365
```

## 🚀 Automated Features

### Backup File Management
- **Compression**: SQL files compressed after 1 day to save disk space
- **Cleanup**: Automated removal of old compressed backup files
- **Cron scheduling**: Daily cleanup runs at 2:30 AM

### Fault Tolerance
- **Missing users**: Falls back to root ownership when apache user doesn't exist
- **Missing files**: Continues operation if log files are missing
- **Configuration testing**: Validates logrotate config after deployment

## 📈 Disk Space Optimization

This policy balances operational needs with disk space efficiency:

1. **High-volume debug logs** (MediaWiki, PHP) are kept for short periods (1 week)
2. **Infrastructure logs** (Apache, Elasticsearch) are kept for operational visibility (2 weeks)
3. **Critical audit logs** (deployments) are kept for compliance (1 year)
4. **Backup files** are compressed quickly and cleaned up automatically

## 🔍 Monitoring and Alerting

The logrotate configuration includes:
- **Automatic testing** after configuration changes
- **Error handling** for missing users/groups during early deployment
- **Cron job scheduling** for backup cleanup automation
- **Service reload** integration to prevent file handle issues

## 📚 Related Documentation

- [Logrotate Role Tasks](https://github.com/freephile/meza/blob/dev/src/roles/logrotate/tasks/main.yml)
- [Logrotate Default Variables](https://github.com/freephile/meza/blob/dev/src/roles/logrotate/defaults/main.yml)
- [Logrotate Templates](https://github.com/freephile/meza/blob/dev/src/roles/logrotate/templates/)
  - See the generated configuration for logrotate at `/etc/logrotate.d/meza-logs`
  - The [cleanup-backups.sh script](https://github.com/freephile/meza/blob/dev/src/scripts/cleanup-backups.sh) is output to the 'scripts' directory.
- [Backup Cleanup Script Documentation](https://github.com/freephile/meza/blob/dev/src/scripts/cleanup-backups.md) (markdown) is side-by-side in the 'scripts' directory.

---

*This documentation is automatically maintained as part of the Meza logrotate role. Last updated: October 22, 2025*
