# htdocs role

Manages web-accessible content in Apache's document root for Meza deployments.

## Overview

This role runs on **app servers** during every `meza deploy` and synchronizes
monitoring tools, optional backup interfaces, and core web server configuration
files to `/opt/htdocs/`. Unlike `configure-wiki` (which creates configuration
directory and file scaffolding on localhost), this role deploys runtime web
content to web application servers.

## What It Does

### Always Deployed
1. **ServerPerformance monitoring dashboard** (`/opt/htdocs/ServerPerformance/`)
   - PHP-based system performance monitoring UI
   - Accessible at `https://your-server/ServerPerformance/`
   - Synced from `files/ServerPerformance/` using rsync

2. **Core web server files** (generated from templates)
   - `.htaccess` - Apache access controls and URL rewrites
   - `index.php` - Landing page with wiki links
   - `office.html` - Optional office hours/contact page
   - `robots.txt` - Search engine crawler directives

### Conditionally Deployed
3. **BackupDownload interface** (`/opt/htdocs/BackupDownload/`)
   - Only deployed if `allow_backup_downloads: true`
   - Web UI for downloading wiki backup files
   - Automatically **removed** if `allow_backup_downloads: false`

## What It Does NOT Do

- Does not create MediaWiki wikis (handled by `configure-wiki` + `setup-wiki`)
- Does not manage Apache virtual hosts (handled by `apache-php` role)

## Requirements

- Apache/httpd installed and running
- `m_htdocs` directory exists (created by `apache-php` role)
- `set-vars` role must run first for path resolution

## Role Variables

```yaml
# Control backup download web interface
allow_backup_downloads: false    # Default: disabled for security

# Paths (typically set by set-vars role)
m_htdocs: "/opt/htdocs"          # Apache DocumentRoot
m_app_dir: "/opt/meza"              # Meza installation directory

# Apache user/group (OS-specific)
user_apache: "apache"            # RedHat/Rocky
# user_apache: "www-data"        # Debian
group_apache: "apache"
```

## Dependencies

- `set-vars` - Path and variable initialization
- `apache-php` - Must create `/opt/htdocs/` directory first

## Example Usage

### Via Standard Deployment (Normal Usage)
```bash
# Runs automatically during deployment
meza deploy <env> (e.g. 'monolith')

# To enable backup downloads
# In /opt/conf-meza/public/public.yml:
allow_backup_downloads: true
```

### Targeted Deployment (Testing)
```bash
# Deploy only htdocs changes
meza deploy monolith --tags htdocs

# Skip htdocs during deployment
meza deploy monolith --skip-tags htdocs
```

## Workflow Integration

```
meza deploy <env>
    ↓
apache-php role (creates /opt/htdocs/)
    ↓
htdocs role (syncs web content)
    ↓
mediawiki role (deploys wikis)
    ↓
Web server ready with monitoring + wikis
```

## File Synchronization Details

### Rsync Options
- `--delete` - Remove files not in source (keeps htdocs clean)
- `--exclude=.git` - Skip Git metadata
- `--no-motd` - Suppress message of the day

### Template Variables Available
Templates in `templates/*.j2` have access to:
- `{{ m_htdocs }}` - DocumentRoot path
- `{{ m_app_dir }}` - Meza installation path
- `{{ wikis }}` - List of configured wikis (for index.php)
- `{{ env }}` - Current environment name
- All variables from `config/defaults.yml` and environment configs

## Security Considerations

### Backup Downloads
**⚠️ Security Warning**: Enabling `allow_backup_downloads` exposes wiki backup
files via HTTP. Only enable on trusted networks or with additional authentication.

```yaml
# In secret.yml or public.yml
allow_backup_downloads: true   # ⚠️ Use with caution
```

### File Permissions
- All files owned by `root:root` (prevents Apache from modifying)
- Mode `0755` (readable by Apache, writable only by root)
- `.htaccess` controls public access to specific directories

## Comparison with configure-wiki Role

| Aspect | `htdocs` | `configure-wiki` |
|--------|----------|------------------|
| **Runs on** | App servers | Localhost (controller) |
| **Frequency** | Every deploy | Only on wiki creation |
| **Target** | `/opt/htdocs/` (public web) | `/opt/conf-meza/public/wikis/` (config) |
| **Purpose** | Runtime web content | Configuration templates |
| **Files** | Monitoring tools, landing pages | Logos, PHP settings, SAML config |
| **Sync method** | rsync (copy from role) | ansible.builtin.copy (controller → servers) |

Both roles have **good separation of concerns**:
- `htdocs` = Infrastructure web content (monitoring, backups, landing pages)
- `configure-wiki` = Wiki-specific configuration (logos, LocalSettings)

## Customization

### Add Custom Landing Page
1. Create template: `templates/my-page.html.j2`
2. Add to task list:
```yaml
- name: Ensure custom page configured
  ansible.builtin.template:
    src: "my-page.html.j2"
    dest: "{{ m_htdocs }}/my-page.html"
    owner: root
    group: root
    mode: '0755'
```

### Modify ServerPerformance UI
Files are synced from `files/ServerPerformance/` - edit those source files and
redeploy. Changes are overwritten on each deploy (no manual server edits).

## Troubleshooting

### ServerPerformance not accessible
```bash
# Check file permissions
ls -la /opt/htdocs/ServerPerformance/

# Check Apache configuration
httpd -t
systemctl status httpd

# Check .htaccess rules
cat /opt/htdocs/.htaccess
```

### BackupDownload not appearing
```bash
# Verify variable is set
grep allow_backup_downloads /opt/conf-meza/public/public.yml

# Check directory exists
ls -la /opt/htdocs/BackupDownload/

# Re-deploy with verbose output
meza deploy monolith --tags htdocs -vvv
```

## See Also

- `apache-php` role - Creates `/opt/htdocs/` directory and configures httpd
- `configure-wiki` role - Wiki-specific configuration files
- `mediawiki` role - Deploys actual MediaWiki wikis
- `sync-configs` role - Syncs controller configs to app servers
