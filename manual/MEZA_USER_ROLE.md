# Meza User Ansible Role

## Overview

The `meza-user` Ansible role replaces the previous bash scripts (`linux-user.sh`, `setup-master-user.sh`) for managing the meza-ansible user. This provides better idempotency, testability, and integration with the Ansible deployment workflow.

## Features

The role handles all aspects of the meza-ansible user configuration:

1. **User Creation**: Creates the `meza-ansible` user with:
   - Non-standard home directory: `/opt/conf-meza/users/meza-ansible`
   - Umask set via `m_umask` variable (0002 by default)
   - Shell set to `/bin/bash`

2. **SSH Key Management**:
   - Generates RSA SSH key pair (4096-bit)
   - Configures authorized_keys for self-SSH capability
   - Sets proper permissions on `.ssh` directory and files

3. **Group Membership**:
   - **apache/www-data**: Enables group-writable access to MediaWiki files
   - **wheel/sudo**: Enables privilege escalation for administrative tasks

4. **Shell Initialization**:
   - Creates `.bash_profile` for login shells
   - Creates `.bashrc` for interactive shells
   - Both files:
     - Source system defaults (`/etc/profile`, `/etc/bashrc`)
     - Set PATH defensively (preserve existing, add meza paths)
     - Set umask via `{{ m_umask }}` variable

5. **Sudo Configuration**:
   - Configures passwordless sudo for meza-ansible user
   - Creates `/etc/sudoers.d/meza-ansible` with proper permissions

## Integration Points

### Bootstrap (getmeza.sh)

The role is called during initial installation via [src/scripts/getmeza.sh](../src/scripts/getmeza.sh):

```bash
ANSIBLE_CONFIG="${m_install}/meza/config/ansible.cfg" \
ansible-playbook -i localhost, --connection=local \
    "${m_install}/meza/src/playbooks/setup-meza-user.yml"
```

**Fallback**: If Ansible fails, the script falls back to the legacy bash scripts (EOL 7/2026).

### Deployment (site.yml)

TBD The intention architecturally is to have user creation done during an early bootstrap and provisioning phase; not neccessarily be integrated into site.yml

The role **could** run on every deployment via [src/playbooks/site.yml](../src/playbooks/site.yml) with appropriate tags like:

```yaml
- name: Ensure meza-ansible user configuration
  hosts: all:!exclude-all:!exclude-appservers:!exclude-parsoid:!exclude-memcached
  become: true
  roles:
    - set-vars
    - meza-user
  tags:
    - meza-user
    - user-setup
```

### Vagrant Development

[Vagrantfile](../Vagrantfile) relies on the role during provisioning:

```ruby
# Apache group membership and shell init files are now handled by
# the meza-user Ansible role during getmeza.sh or first deploy
```

## File Structure

```
src/roles/meza-user/
├── tasks/
│   └── main.yml              # Main task file (200 lines)
├── templates/
│   ├── bash_profile.j2       # Login shell initialization
│   └── bashrc.j2             # Interactive shell initialization
└── defaults/
    └── main.yml              # Role variables
```

## Variables

Defined in [src/roles/meza-user/defaults/main.yml](../src/roles/meza-user/defaults/main.yml):

- `ansible_user`: Username (default: "meza-ansible")
- `meza_ansible_home`: Home directory (default: "{{ m_config_vault }}/users/{{ ansible_user }}")

Additional variables from `set-vars` role:
- `m_umask`: Umask value (default: "0002")
- `m_meza`: Path to meza installation
- `m_config_vault`: Path to conf-meza directory
- `apache_user`: Web server user (apache/www-data)
- `wheel_group`: Sudo group (wheel/sudo)

## Usage

### Standalone Playbook

Run the setup-meza-user playbook independently:

```bash
cd /opt/meza
ANSIBLE_CONFIG=/opt/meza/config/ansible.cfg \
ansible-playbook -i localhost, --connection=local \
    /opt/meza/src/playbooks/setup-meza-user.yml
```

### During Deployment

The role automatically runs during `meza deploy`:

```bash
meza deploy <env>
```

### Selective Execution

Run just the meza-user role:

```bash
cd /opt/meza
ANSIBLE_CONFIG=/opt/meza/config/ansible.cfg \
ansible-playbook src/playbooks/site.yml \
    --tags meza-user \
    -e env=<environment>
```

## Idempotency

The role is fully idempotent and can be run multiple times safely:

- User creation checks if user already exists
- SSH key generation skips if key exists
- Group membership only adds missing groups
- Shell initialization files only created if missing or different
- Sudoers configuration only updated if changed

## Cross-Platform Compatibility

The role works on:
- **RHEL/Rocky/CentOS**: Uses `wheel` group, `/etc/bashrc`
- **Debian/Ubuntu**: Uses `sudo` group, `/etc/bash.bashrc`

Platform detection is handled by the `set-vars` role which sets:
- `ansible_os_family`: "RedHat" or "Debian"
- `apache_user`: "apache" or "www-data"
- `wheel_group`: "wheel" or "sudo"

## Testing

### Linting

All role files pass ansible-lint production profile:

```bash
./src/scripts/lint-files.sh \
    src/roles/meza-user/tasks/main.yml \
    src/roles/meza-user/defaults/main.yml \
    src/roles/meza-user/templates/*.j2 \
    src/playbooks/setup-meza-user.yml
```

### Fresh Installation

Test on a clean Vagrant VM:

```bash
vagrant destroy -f
vagrant up
vagrant ssh
```

Verify:
```bash
# Check user exists
id meza-ansible

# Check groups
groups meza-ansible
# Should show: meza-ansible apache wheel (or www-data sudo on Ubuntu) and vboxsf on Vagrant

# Check SSH keys
ls -la /opt/conf-meza/users/meza-ansible/.ssh/
# Should show: id_rsa, id_rsa.pub, authorized_keys

# Check shell init files
ls -la /opt/conf-meza/users/meza-ansible/
# Should show: .bash_profile, .bashrc

# Check umask
su - meza-ansible -c 'umask'
# Should show: 0002

# Check sudo
sudo -l -U meza-ansible
# Should show: (ALL) NOPASSWD: ALL
```

### Deployment Test

Test role during deployment:

```bash
vagrant ssh
sudo meza deploy vagrant -vvv
```

The role should run without errors and all user configuration should remain correct.

## Migration from Bash Scripts

### Deprecated Functions

The following bash functions are replaced by the meza-user role:

From [src/scripts/shell-functions/linux-user.sh](../src/scripts/shell-functions/linux-user.sh):
- `mf_add_ssh_user()`: User creation, SSH keys, groups → Ansible tasks
- Shell initialization (lines 180-255) → Jinja2 templates

From [src/scripts/ssh-users/setup-master-user.sh](../src/scripts/ssh-users/setup-master-user.sh):
- Entire script → `setup-meza-user.yml` playbook

### Backward Compatibility

The bash scripts remain in place as fallback during the transition period (6 months):

1. **getmeza.sh** tries Ansible first, falls back to bash on failure
2. **Vagrantfile** relies on role but bash scripts still exist
3. **Manual installations** can still use bash scripts if needed

### Deprecation Timeline

After validation period (recommended 3-6 months):
1. Remove fallback mechanism from getmeza.sh
2. Mark bash scripts as deprecated with warning messages
3. Eventually remove bash scripts entirely

## Troubleshooting

### Role Not Found

**Error**: `the role 'meza-user' was not found`

**Solution**: Ensure `ANSIBLE_CONFIG` points to [config/ansible.cfg](../config/ansible.cfg):

```bash
export ANSIBLE_CONFIG=/opt/meza/config/ansible.cfg
export ANSIBLE_ROLES_PATH=/opt/meza/src/roles
```

### Permission Denied

**Error**: SSH or file permission errors

**Solution**: Verify umask is set correctly:
```bash
su - meza-ansible -c 'umask'
grep umask /opt/conf-meza/users/meza-ansible/.bash_profile
```

### Group Membership Issues

**Error**: Cannot write to MediaWiki directories

**Solution**: Verify group membership:
```bash
groups meza-ansible
# Should include apache (or www-data), wheel (or sudo), and vboxsf on Vagrant

# If missing, re-run the role
ansible-playbook src/playbooks/site.yml --tags meza-user
```

## Related Documentation

- [Issue #272: umask and PATH consistency](https://github.com/freephile/meza/issues/272)
- [PATH_FIX.md](PATH_FIX.md): Shell initialization and PATH configuration
- [LINTING.md](../LINTING.md): Code quality requirements

## Benefits Over Bash Scripts

1. **Declarative**: Describes desired state rather than imperative steps
2. **Idempotent**: Can run multiple times safely without side effects
3. **Testable**: Ansible role structure enables better testing
4. **Maintainable**: Easier to read, modify, and extend
5. **Integrated**: Natural fit in deployment workflow
6. **Cross-platform**: Ansible abstracts OS differences
7. **Documented**: Self-documenting with task names and tags
8. **Version controlled**: Role changes tracked in git
9. **Reusable**: Can be imported by other playbooks
10. **Auditable**: Ansible logs show exactly what changed
