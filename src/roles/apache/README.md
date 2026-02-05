# Apache Role

This role installs and configures the Apache HTTP Server for Meza MediaWiki deployments.

## Description

The Apache role handles:
- Apache package installation (httpd/apache2)
- Apache modules configuration (SSL, proxy, rewrite)
- Virtual host configuration
- Service management
- Directory permissions for web content

This role is designed to be composable and can be used independently of PHP, allowing for flexible deployment scenarios including PHP-FPM with separate PHP installations.

## Requirements

- Ansible 2.10 or higher
- Red Hat Enterprise Linux 8, Rocky Linux 8, or Debian-based systems
- The `set-vars` role must run first to establish path variables

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Apache package names (OS-specific, defined in set-vars)
package_apache: httpd  # RedHat
package_apache: apache2  # Debian

# Apache service name (OS-specific)
service_apache: httpd  # RedHat
service_apache: apache2  # Debian

# Apache user/group (OS-specific)
user_apache: apache  # RedHat
user_apache: www-data  # Debian
group_apache: apache  # RedHat
group_apache: www-data  # Debian

# Apache configuration paths (OS-specific)
path_apache_conf: /etc/httpd/conf/httpd.conf  # RedHat
path_apache_startup_config: /etc/sysconfig/httpd  # RedHat
```

## Dependencies

- `set-vars`: Provides core path and variable definitions

## Example Playbook

```yaml
- hosts: webservers
  become: true
  roles:
    - set-vars
    - apache
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

## Future Plans

This role is designed with migration to community-maintained roles in mind. Consider using `geerlingguy.apache` for more comprehensive Apache management in the future.

## License

GPL-3.0-or-later

## Author Information

This role was created by Greg Rundlett for the Meza MediaWiki E-Z Administration platform.
- GitHub: https://github.com/freephile/meza
- Issues: https://github.com/freephile/meza/issues/287
