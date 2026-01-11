# PHP Profiling in Meza

Meza uses [xhprof](https://github.com/longxinH/xhprof) with MediaWiki's built-in `ProfilerXhprof` class to enable performance profiling for PHP code. This is useful for developers and performance testing.

## Overview

**What changed from Meza 30.x:**
- **Removed:** MongoDB + XHGui web interface (complex, heavy dependencies)
- **Added:** Simple xhprof + MediaWiki ProfilerXhprof (lightweight, integrated)
- **Benefit:** No database required, simpler configuration, better MediaWiki integration

## Configuration Hierarchy

Profiling is controlled through three levels:

### 1. Environment-Level Control

Set `m_setup_php_profiling` in your environment's `public.yml`:

```yaml
# /opt/conf-meza/public/<env>/public.yml
m_setup_php_profiling: true
```

**When true:** Installs xhprof PHP extension on all servers  
**When false:** Extension not installed, per-wiki settings have no effect

### 2. Per-Wiki Control

Add `enable_profiling` to individual wiki definitions:

```yaml
# /opt/conf-meza/public/<env>/public.yml
wikis:
  - id: demo
    name: Demo Wiki
    enable_profiling: true    # This wiki will be profiled
  - id: production_test
    name: Production Test
    enable_profiling: false   # This wiki will not be profiled
```

**Note:** Per-wiki control only works if `m_setup_php_profiling: true` at environment level.

### 3. Output Format Control

Choose how profiling data is presented:

```yaml
# /opt/conf-meza/public/<env>/public.yml

# Option 1: Display in page footer (default)
m_profiling_output_type: footer

# Option 2: Log to files
m_profiling_output_type: file
m_profiling_file_path: "/opt/data-meza/logs/profiler"
m_profiling_file_retention_days: 1
```

## Common Configurations

### Development Environment (Selective Profiling)

```yaml
# /opt/conf-meza/public/dev/public.yml
m_setup_php_profiling: true
m_profiling_output_type: footer

wikis:
  - id: testwiki
    name: Test Wiki
    enable_profiling: true
  - id: staging
    name: Staging Wiki
    enable_profiling: false
```

### Test Environment (Profile Everything)

```yaml
# /opt/conf-meza/public/test/public.yml
m_setup_php_profiling: true
m_profiling_output_type: file
m_profiling_file_path: "/opt/data-meza/logs/profiler"
```

When global profiling is enabled without per-wiki overrides, all wikis are profiled.

### Production Environment (Profiling Disabled)

```yaml
# /opt/conf-meza/public/prod/public.yml
m_setup_php_profiling: false
```

## Reading Profiling Output

### Footer Output Mode

When `m_profiling_output_type: footer`, profiling data appears at the bottom of each page's HTML.

**How to view:**
1. Load any wiki page
2. View page source (Ctrl+U or right-click → View Source)
3. Scroll to the bottom
4. Look for profiling section with function call data

**Example output:**
```
Profiler output
===============
Function                           Count    Real (ms)    %
---------------------------------------------------------
MediaWiki::main                        1      245.123   100.0
Article::view                          1       89.456    36.5
Parser::parse                          1       67.890    27.7
DatabaseMysqli::query                 23       45.678    18.6
Linker::link                          89       12.345     5.0
...
```

**Interpreting the data:**
- **Function:** Name of the PHP function/method
- **Count:** Number of times it was called
- **Real (ms):** Total time spent in milliseconds
- **%:** Percentage of total execution time

**What to look for:**
- High percentages indicate bottlenecks
- Large counts may indicate inefficient loops
- Compare "Real" times across page loads to identify consistent slowness

### File Output Mode

When `m_profiling_output_type: file`, profiling data is written to log files.

**Log file location:**
```bash
# Default location
/opt/data-meza/logs/profiler/

# Files named by wiki and timestamp
profiler-<wikiId>-<timestamp>.log
```

**Viewing logs:**
```bash
# List recent profiler logs
ls -lth /opt/data-meza/logs/profiler/ | head -20

# View latest profiler log
tail -f /opt/data-meza/logs/profiler/profiler-demo-*.log

# Search for slow functions
grep -h "Parser::" /opt/data-meza/logs/profiler/*.log | sort -k3 -rn | head -10
```

**Log rotation:**
- Runs daily at 2:00 AM via logrotate
- Retains logs for `m_profiling_file_retention_days` (default: 1 day)
- Compressed after rotation to save disk space
- Backup cleanup cron runs daily

### Understanding xhprof Data

**Key metrics to analyze:**

1. **Inclusive Time:** Total time including all sub-function calls
   - Identifies high-level bottlenecks
   - Look for top-level functions with high inclusive time

2. **Exclusive Time:** Time spent only in this function (not sub-calls)
   - Identifies specific inefficient code
   - Look for functions doing heavy computation

3. **Call Count:** Number of times function was called
   - High counts may indicate N+1 query problems
   - Or inefficient loop structures

4. **Memory Usage:** Peak memory used by function
   - Identifies memory-intensive operations
   - Useful for finding memory leaks

## Common Profiling Scenarios

### Scenario 1: Debugging Slow Page Load

**Goal:** Find why a specific page takes 5+ seconds to load

**Steps:**
1. Enable profiling for the wiki
2. Set `m_profiling_output_type: footer`
3. Deploy: `meza deploy <env>`
4. Load the slow page
5. View source and examine profiling output
6. Look for functions with >1000ms in "Real" column
7. Investigate those functions in the code

**Common culprits:**
- Database queries: `DatabaseMysqli::query` or `IDatabase::select`
- Template parsing: `Parser::parse` or `PPFrame::expand`
- Extension hooks: Look for extension-specific function names

### Scenario 2: Testing Extension Performance

**Goal:** Measure performance impact of a new extension

**Steps:**
1. Profile with extension disabled (baseline)
2. Enable extension
3. Profile same pages again
4. Compare function call counts and times
5. Look for new functions introduced by extension

**What to compare:**
- Total page load time
- Database query count
- Memory usage
- New functions in profiler output

### Scenario 3: Production Performance Investigation

**Important:** Use file output mode to avoid exposing data to users.

**Configuration:**
```yaml
m_setup_php_profiling: true
m_profiling_output_type: file
m_profiling_file_retention_days: 1  # Keep logs minimal
```

**Steps:**
1. Enable profiling for short period (1-4 hours)
2. Let normal traffic generate profiling data
3. Analyze logs for patterns
4. Disable profiling after investigation
5. Deploy to remove extension overhead

### Scenario 4: Finding N+1 Query Problems

**Goal:** Identify pages making excessive database queries

**What to look for:**
```
DatabaseMysqli::query              145    1234.56    45.2
```

High query counts (>100) often indicate:
- Loading data in loops instead of batch queries
- Missing caching
- Inefficient extension code

**Investigation:**
1. Look at which functions call the database
2. Check if they're called in loops
3. Consider batch loading or caching solutions

## Security Considerations

### Footer Output Security Risks

**⚠️ WARNING:** Footer output exposes internal application details including:
- Function names and file paths
- Execution timing data
- Database query patterns
- Extension structure

**Recommendations:**
- **Never use footer output in production** unless restricted to admin users
- Use file output if production profiling is necessary
- Consider IP restrictions or authentication
- Disable immediately after investigation

### File Output Best Practices

- Keep `m_profiling_file_retention_days` low (1-3 days)
- Ensure log directory has proper permissions (0755)
- Monitor disk space usage
- Delete logs after analysis in production

## Troubleshooting

### Profiling Not Working

**Check 1: Is xhprof installed?**
```bash
php -m | grep xhprof
```
If not listed, check that `m_setup_php_profiling: true` and re-deploy.

**Check 2: Is extension loaded?**
```bash
ls -l /etc/php.d/20-xhprof.ini
cat /etc/php.d/20-xhprof.ini
```

**Check 3: Is MediaWiki configuration present?**
```bash
cat /opt/conf-meza/public/<env>/postLocalSettings.d/profiling.php
```

**Check 4: Restart services**
```bash
sudo systemctl restart httpd
sudo systemctl restart php-fpm  # Rocky/RHEL 8+
```

### No Output in Footer

**Possible causes:**
1. `m_profiling_output_type` set to `file` instead of `footer`
2. Page cached - profiler may not run on cached pages
3. JavaScript rendering - view HTML source, not rendered page
4. Extension not loaded - check PHP configuration

**Solution:**
Add `?action=purge` to URL to bypass cache, then view source.

### Log Files Not Created

**Check directory exists:**
```bash
ls -ld /opt/data-meza/logs/profiler/
```

**Check ownership:**
```bash
# Directory should be owned by apache/www-data
chown apache:apache /opt/data-meza/logs/profiler/
```

**Check MediaWiki can write:**
```bash
sudo -u apache touch /opt/data-meza/logs/profiler/test.log
```

### Disk Space Issues

**Check profiler log size:**
```bash
du -sh /opt/data-meza/logs/profiler/
```

**Manual cleanup:**
```bash
# Delete logs older than 1 day
find /opt/data-meza/logs/profiler/ -type f -mtime +1 -delete
```

**Adjust retention:**
```yaml
# In public.yml
m_profiling_file_retention_days: 1  # Reduce retention period
```

## Performance Impact

### Overhead When Enabled

Profiling adds overhead to every PHP request:
- **CPU:** ~5-10% additional processing
- **Memory:** ~5-10 MB additional per request
- **I/O:** File writes if using file output mode

**Recommendations:**
- Use sampling for high-traffic wikis (see Advanced Configuration)
- Enable only for specific wikis in multi-wiki environments
- Disable immediately after investigation in production

### Overhead When Disabled

When `m_setup_php_profiling: false`:
- **Zero overhead** - extension not loaded
- No PHP configuration changes
- No MediaWiki profiler overhead

## Advanced Configuration

### Sampling (Reduce Overhead)

Profile only a percentage of requests:

```php
// In postLocalSettings.d/profiling.php (edit template)
if ( $enableProfiling ) {
    $wgProfiler['class'] = 'ProfilerXhprof';
    $wgProfiler['sampling'] = 10;  // Profile 1 out of every 10 requests
    // ... rest of config
}
```

### Function Filtering

Profile only specific functions:

```php
// Include only parser-related functions
$wgProfiler['include'] = [
    'Parser::*',
    'PPFrame::*',
];

// Or exclude utility functions
$wgProfiler['exclude'] = [
    'wfDebug',
    'wfGetCache',
];
```

### Per-User Profiling

Profile only for specific users:

```php
// In postLocalSettings.d/profiling.php (edit template)
$enableProfiling = false;

// Only profile for admin users
if ( $wgUser->isAllowed( 'profiling' ) ) {
    $enableProfiling = true;
}
```

Then grant permission:
```php
$wgGroupPermissions['sysop']['profiling'] = true;
```

## Migration from Legacy XHGui

If you have an old Meza installation with XHGui/MongoDB profiling:

### What Will Happen on Deploy

When you deploy with the modernized profiling:

1. **MongoDB service will be stopped** (if profiling disabled)
2. **Port 8088 and 8089 will be closed** in firewall
3. **XHGui web interface will be inaccessible**
4. **Old profiling data will remain** in `/opt/xhgui/`

### Manual Cleanup (Optional)

If you want to completely remove old profiling infrastructure:

```bash
# Stop and disable MongoDB
sudo systemctl stop mongod
sudo systemctl disable mongod

# Remove MongoDB packages (optional)
sudo yum remove mongodb-org

# Remove XHGui installation
sudo rm -rf /opt/xhgui

# Remove MongoDB repository
sudo rm -f /etc/yum.repos.d/mongo.repo

# Remove profiling data
sudo rm -rf /var/lib/mongo/xhprof*
```

### Preserving Old Profiling Data

If you want to keep historical XHGui data for reference:

```bash
# Archive old profiling data
cd /opt
tar -czf xhgui-archive-$(date +%Y%m%d).tar.gz xhgui/

# Move archive to safe location
mv xhgui-archive-*.tar.gz /opt/data-meza/backups/
```

## Resources

- [MediaWiki Profiling Documentation](https://www.mediawiki.org/wiki/Manual:Profiling)
- [xhprof GitHub Repository](https://github.com/longxinH/xhprof)
- [PHP Performance Profiling Guide](https://www.php.net/manual/en/book.xhprof.php)
- [Meza Configuration Documentation](https://www.mediawiki.org/wiki/Meza)

## Support

For issues or questions:
- Check Meza logs: `/opt/data-meza/logs/`
- Review deployment output: `meza deploy-log <env>`
- Open issue: https://github.com/freephile/meza/issues
