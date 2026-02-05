# PHP Role

This role installs and configures PHP and PHP-FPM for Meza MediaWiki deployments.

## Description

The PHP role handles:
- PHP package installation (multiple versions supported)
- PHP-FPM configuration
- PHP extensions installation (MySQL, XML, GD, mbstring, etc.)
- php.ini configuration
- PHP module configuration (opcache, memcached, xhprof, etc.)
- Composer dependency management

This role is designed to be composable and works alongside the Apache role for complete web server setup.

## Requirements

- Ansible 2.10 or higher
- Red Hat Enterprise Linux 7/8, Rocky Linux 8, or Debian-based systems
- The `set-vars` role must run first to establish path variables
- The `composer` role is automatically included as a dependency

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Server timezone for PHP configuration
server_default_timezone: "UTC"

# Remi repository configuration (RedHat/Rocky only)
remi_repo_url: "https://rpms.remirepo.net/enterprise/remi-release-{{ ansible_distribution_major_version }}.rpm"
remi_repo_gpg_key_url: "https://rpms.remirepo.net/enterprise/{{ ansible_distribution_major_version }}/RPM-GPG-KEY-remi"

# PHP profiling with XHProf (disabled by default)
m_setup_php_profiling: false

# MS SQL Server driver installation (disabled by default)
install_ms_sql_driver: false

# PHP-FPM configuration
service_php_fpm: php-fpm

# PHP packages (OS and version specific, defined in set-vars)
package_php_apache_deps7: [...]  # RedHat 7
package_php_apache_deps8: [...]  # RedHat 8
```

## Dependencies

- `set-vars`: Provides core path and variable definitions
- `composer`: PHP dependency management (included after PHP installation in tasks/main.yml)

## Example Playbook

```yaml
- hosts: webservers
  become: true
  roles:
    - set-vars
    - apache
    - php
```

### Enable PHP Profiling

```yaml
- hosts: webservers
  become: true
  vars:
    m_setup_php_profiling: true
  roles:
    - set-vars
    - apache
    - php
```

## Migration from apache-php Role

This role was extracted from the monolithic `apache-php` role to improve composability and follow the single-responsibility principle. The `apache-php` role now serves as a deprecation shim that depends on both `apache` and `php` roles.

If you're using the `apache-php` role, no immediate changes are required. However, we recommend updating to use `apache` and `php` roles directly:

**Old approach:**
```yaml
roles:
  - apache-php
```

**New approach:**
```yaml
roles:
  - apache
  - php
```

## PHP Version Management

The role supports multiple PHP versions through the Remi repository (RedHat/Rocky) and Ondřej Surý's PPA (Debian):

- **RedHat/Rocky 8**: PHP 8.0+ from Remi
- **Debian**: PHP 8.x from Ondřej Surý's PPA

## Profiling

By default, profiling is disabled.

When `m_setup_php_profiling: true`:
- XHProf extension is installed via pecl
- uses MediaWiki's ProfilerXhprof class
- Profiler logs are rotated via logrotate

See [README_PROFILING.md](README_PROFILING.md)

## Future Plans

This role is designed with migration to community-maintained roles in mind. Consider using `geerlingguy.php` for more comprehensive PHP management in the future.

## License

GPL-3.0-or-later

## Author Information

This role was created by Greg Rundlett for the Meza MediaWiki E-Z Administration platform.
- GitHub: https://github.com/freephile/meza
- Issues: https://github.com/freephile/meza/issues/287
