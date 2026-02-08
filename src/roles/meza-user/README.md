# Meza User Role

This role creates and configures the `meza-ansible` user for Meza deployments.

## Description

The `meza-user` role handles:
- Creating the `meza-ansible` user with non-standard home directory
- Configuring user groups (wheel, apache, etc.)
- Setting up SSH keys and authorized_keys
- Installing shell initialization files (.bashrc, .bash_profile)
- Configuring sudo permissions
- Managing password settings

## Requirements

- Ansible 2.10 or higher
- Red Hat Enterprise Linux 7/8, Rocky Linux 8, or Debian-based systems
- **Apache must be installed first** to ensure the `apache` group exists

## Bootstrap Sequencing

**IMPORTANT**: This role requires Apache to be installed first so the apache group exists.

The bootstrap sequence is:
1. Apache installation (via `getmeza.sh`)
2. User creation (this role)
3. PHP installation (via `php` role)
4. MediaWiki deployment

This ordering ensures `meza-ansible` user can be added to the `apache` group during creation.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# User name for Ansible operations
ansible_user: meza-ansible

# Home directory for meza-ansible user
meza_ansible_home: "{{ m_conf_users_dir }}/{{ ansible_user }}"

# User groups (apache group requires Apache to be installed first)
meza_user_groups:
  - wheel
  - apache  # Requires Apache installed
  # would be 'sudo', 'www-data' on Debian
```

## Dependencies

None (runs early in bootstrap process).

## Tags

- `meza-user`: All tasks in this role
- `user-setup`: User creation and configuration
- `user-ssh`: SSH key setup
- `user-shell`: Shell initialization files

## Example Playbook

### During Bootstrap (via getmeza.sh)

```yaml
# After Apache is installed
- hosts: localhost
  become: true
  roles:
    - meza-user
```

### Manual User Setup

```bash
# Install Apache first
sudo dnf install -y httpd

# Then run user setup playbook
ansible-playbook src/playbooks/setup-meza-user.yml
```

## Historical Context

This role replaced legacy bash scripts (`setup-master-user.sh`, `linux-user.sh`) to improve:
- Idempotency (can be run multiple times safely)
- Testability (Ansible check mode support)
- Maintainability (declarative configuration vs shell scripts)
- Group membership handling (proper sequencing with Apache)

## Known Issues

### Apache Group Membership

**Problem**: If Apache is not installed when this role runs, the user will not be added to the `apache` group, causing permission issues during deployment.

**Solution**: As of Issue #287, `getmeza.sh` now installs Apache BEFORE calling this role:

```bash
# getmeza.sh sequence
dnf install -y httpd           # Create apache group
ansible-playbook setup-meza-user.yml  # User joins apache group
```

## Testing

```bash
# Check user configuration
id meza-ansible
# Expected output includes: groups=...,apache,...

# Verify home directory
getent passwd meza-ansible | cut -d: -f6
# Expected: /opt/conf-meza/users/meza-ansible

# Check SSH setup
sudo ls -la /opt/conf-meza/users/meza-ansible/.ssh/
# Expected:
drwx------. 2 meza-ansible wheel   80 Feb  5 01:39 .
drwx------. 6 meza-ansible wheel  180 Feb  5 02:10 ..
-rw-r--r--. 1 meza-ansible wheel 1156 Feb  5 01:39 authorized_keys
-rw-------. 1 meza-ansible wheel 2602 Feb  5 01:37 id_rsa
-rw-r--r--. 1 meza-ansible wheel  569 Feb  5 01:37 id_rsa.pub
-rw-------. 1 meza-ansible wheel    0 Feb  5 01:39 known_hosts

```

## Related Roles

- `apache`: Must run before this role (creates apache group)
- `set-vars`: Provides path variables used by this role

## License

GPL-3.0-or-later

## Author Information

This role was created for the Meza MediaWiki E-Z Administration platform.
- GitHub: https://github.com/freephile/meza
- Related Issue: https://github.com/freephile/meza/issues/287
