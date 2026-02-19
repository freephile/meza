# Meza Ansible Roles

This directory contains all Ansible roles used by the Meza deployment platform.
Roles are listed alphabetically with a brief description of each.

## Third-party / vendor roles

| Role | Description |
|------|-------------|
| `ansible-role-certbot` | Upstream role (geerlingguy) — installs and configures Certbot for Let's Encrypt SSL certificates. |
| `ansible-role-certbot-meza` | Meza-specific customization of `ansible-role-certbot`, adapting it for Meza deployments. |
| `composer` | Adapted upstream role (geerlingguy) — installs PHP Composer for managing MediaWiki PHP dependencies. |
| `database` | Adapted upstream MySQL role (geerlingguy) — installs and configures MariaDB/MySQL for MediaWiki. |
| `geerlingguy.kibana` | Upstream role (geerlingguy) — installs Kibana on RedHat/CentOS or Debian/Ubuntu. |

## Infrastructure / system roles

| Role | Description |
|------|-------------|
| `apache` | Installs and configures Apache HTTP Server for Meza MediaWiki deployments. |
| `apache-php` | **Deprecated.** Legacy combined Apache+PHP role, retained for backward compatibility. Migrate to `apache` + `php`. |
| `base` | Sets up foundational system users (`meza-ansible`, `alt-meza-ansible`), groups, and wheel membership. |
| `base-config-scripts` | Writes shared config variables out as PHP and shell files for use by non-Ansible components. |
| `base-extras` | Installs OS-specific extra packages (e.g., RHEL 7/8+, Debian). |
| `cron` | Ensures the cron service is enabled and running. |
| `elasticsearch` | Installs and configures Elasticsearch (pinned version) for MediaWiki CirrusSearch/Elastica. |
| `essential-vars` | Sets critical variables (e.g., `group_wheel`, `ansible_user`) needed before `set-vars` runs. |
| `firewall_port` | Library role — opens or closes a specific firewall port using firewalld (RedHat) or UFW (Debian). |
| `firewall_service` | Library role — allows or blocks a named firewalld service for specific IP addresses (RedHat/CentOS). |
| `firewalld` | Base firewalld library; provides reusable firewall tasks called by other roles. |
| `gluster` | Installs and configures GlusterFS distributed filesystem for shared uploads in multi-server deployments. |
| `haproxy` | Installs and configures HAProxy for load balancing across app servers. |
| `htdocs` | Manages web-accessible content in Apache's document root. |
| `imagemagick` | Installs ImageMagick (removing old Meza-packaged RPMs first on RedHat), used for image processing. |
| `logrotate` | Configures log rotation and backup file retention policies for all Meza-managed logs. |
| `lua` | Installs Lua and LuaSandbox (from Wikimedia git) for MediaWiki Scribunto extension support. |
| `memcached` | Installs and configures Memcached for MediaWiki object caching. |
| `meza-log` | Creates and manages a server-level log database in MariaDB. |
| `meza-user` | Creates and configures the `meza-ansible` service account used by all Ansible operations. |
| `netdata` | Installs and configures Netdata system monitoring. |
| `php` | Installs and configures PHP and PHP-FPM for MediaWiki. |
| `saml` | Installs and configures SimpleSAMLphp and the MediaWiki SimpleSAMLphp extension for SSO. |
| `umask-set` | Sets a restrictive umask via `/etc/profile.d/` at the start of a deploy. |
| `umask-unset` | Removes the umask profile script set by `umask-set` at the end of a deploy. |

## Meza orchestration roles

| Role | Description |
|------|-------------|
| `autodeployer` | Installs a cron-based auto-deploy mechanism; optionally forces redeploys on a schedule. |
| `enforce-meza-version` | Ensures the deployed Meza code matches the expected git version/tag. |
| `essential-vars` | Sets critical bootstrap variables before the main `set-vars` role runs. |
| `init-controller-config` | Initializes or syncs local controller config from app servers on first run. |
| `key-transfer` | Manages SSH key distribution between servers. |
| `mediawiki` | Core MediaWiki orchestration role — sync configs, install/update MediaWiki code, extensions, skins, and per-wiki tasks. |
| `set-vars` | Resolves all Meza path and config variables from the install path and config hierarchy. Always runs first. |
| `setup-env` | Creates the environment's secret config directory structure and initial configuration files. |
| `sync-configs` | Synchronizes public configuration from the Ansible controller to all app servers. |
| `verify-permissions` | Verifies and corrects MediaWiki directory ownership, group memberships, and critical file permissions. |

## Wiki lifecycle roles

| Role | Description |
|------|-------------|
| `configure-wiki` | Creates the configuration scaffold (directories, LocalSettings.php overrides) for a new wiki. |
| `create-wiki-wrapper` | Validates wiki ID input and wraps the create-wiki playbook; handles prompts and variable scoping. |
| `delete-wiki-wrapper` | Removes a wiki's config directory from the controller and syncs the deletion to app servers. |
| `migrate-to-declarative-wikis` | One-time migration role that converts directory-based wiki discovery to declarative `wikis:` config in `public.yml`. |
| `update.php` | Backs up a wiki's database, then runs MediaWiki `maintenance/run update` for that wiki. Logs output and retries on multi-content revisions errors. See [update.php/README.md](update.php/README.md). |
| `verify-wiki` | Per-wiki setup: ensures localization cache, htdocs symlinks, database existence/restore, and uploads directory configuration. |

## Backup roles

| Role | Description |
|------|-------------|
| `backup-config` | Ensures MariaDB client is installed on backup servers; prepares backup infrastructure. |
| `backup-db-wikis` | Dumps all wiki databases to the backup server. |
| `backup-db-wikis-push` | Pushes wiki database dumps from the app server to a remote backup target. |
| `backup-uploads` | Copies all wiki upload directories to the backup server. |
| `backup-uploads-push` | Pushes wiki upload backups to a remote backup target. |
| `backups-cleanup` | Installs a cleanup script to prune old backup files per retention policy. |
| `dump-db-wikis` | Dumps wiki databases (without the full backup orchestration of `backup-db-wikis`). |
| `sql-backup-cleanup` | Prunes old SQL backup files for a specific wiki, keeping only the latest. |

## Utility / library roles

| Role | Description |
|------|-------------|
| `remote-dir-check` | Library role — checks whether a directory exists on a remote server via SSH. |
| `remote-mysqldump` | Library role — performs a MySQL dump from one server and places the file on another. |
| `rsync` | Library role — rsync-pulls files from a remote server to the local server. |
| `rsync-push` | Library role — rsync-pushes files from the local server to a remote server. |
