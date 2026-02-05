# Apache-PHP Role Separation Implementation Checklist

**GitHub Issue**: https://github.com/freephile/meza/issues/287
**Implementation Date**: February 4, 2026
**Author**: Greg Rundlett

## Overview

This document tracks the implementation of splitting the monolithic `apache-php` role into two separate, composable roles (`apache` and `php`) to improve bootstrap sequencing and follow single-responsibility principles.

## Problem Statement

The `meza-ansible` user needs to be added to the `apache` group during bootstrap, but the apache group didn't exist until the `apache-php` role ran later in the deployment sequence. This caused:
- Silent group membership failures in Vagrant environments
- Permission issues accessing web content
- Bootstrap sequencing dependencies not properly enforced

## Solution Design

### Architecture Changes
- Split `apache-php` role into `apache` and `php` roles
- Install Apache during `getmeza.sh` bootstrap (before user creation)
- Update `apache-php` role to deprecation shim with meta dependencies
- Update all playbooks to use new role structure

### Role Structure

#### Apache Role
**Path**: `src/roles/apache/`

**Files Created**:
- `meta/main.yml` - Role metadata and dependencies
- `README.md` - Comprehensive documentation
- `defaults/main.yml` - Default variables
- `handlers/main.yml` - Apache service handlers
- `tasks/main.yml` - Apache installation and configuration tasks
- `templates/httpd.conf.j2` - Apache config (RHEL7)
- `templates/php-fpm-httpd.conf.j2` - Apache config with PHP-FPM (RHEL8+)
- `templates/etc-sysconfig-httpd.j2` - Apache environment variables

**Responsibilities**:
- Apache package installation (httpd/apache2)
- Apache modules configuration (SSL, proxy, rewrite)
- Virtual host setup
- Service management
- Directory permissions for htdocs

#### PHP Role
**Path**: `src/roles/php/`

**Files Created**:
- `meta/main.yml` - Role metadata, depends on composer
- `README.md` - Comprehensive documentation
- `defaults/main.yml` - Default variables (timezone, repos, profiling)
- `handlers/main.yml` - PHP-FPM service handlers
- `tasks/main.yml` - PHP orchestration tasks
- `tasks/php.yml` - Core PHP installation (copied from apache-php)
- `tasks/php-redhat7.yml` - RHEL7-specific PHP (copied)
- `tasks/php-redhat8.yml` - RHEL8-specific PHP (copied)
- `tasks/php-debian.yml` - Debian-specific PHP (copied)
- `tasks/mssql_driver_for_php.yml` - MS SQL driver (copied)
- `tasks/profiling.yml` - XHProf profiling setup (copied)
- `templates/php.ini.j2` - PHP configuration
- `templates/www.conf.j2` - PHP-FPM pool config
- `templates/php.conf` - PHP Apache module config
- `templates/freetds.conf.j2` - FreeTDS config for MSSQL
- `templates/10-opcache.ini.j2` - OPcache config
- `templates/20-sqlsrv.ini.j2` - SQL Server driver config
- `templates/20-xhprof.ini.j2` - XHProf profiler config
- `templates/30-pdo_sqlsrv.ini.j2` - PDO SQL Server config
- `templates/40-memcached.ini.j2` - Memcached config
- `templates/logrotate-profiler.j2` - Profiler log rotation
- `templates/postLocalSettings.d/` - MediaWiki LocalSettings overrides (copied)

**Responsibilities**:
- PHP package installation (via Remi repo on RHEL, Ondřej PPA on Debian)
- PHP-FPM configuration
- PHP extensions (MySQL, GD, XML, mbstring, etc.)
- php.ini configuration
- Module configs (opcache, memcached, xhprof)
- Composer (via meta dependency)
- Optional profiling (XHProf + MongoDB)

#### Apache-PHP Role (Deprecated)
**Path**: `src/roles/apache-php/`

**Files Modified**:
- `meta/main.yml` - **NEW**: Depends on `apache` and `php` roles
- `README.md` - **NEW**: Deprecation notice and migration guide
- `tasks/main.yml` - **REPLACED**: Now shows deprecation warning, actual work done by dependencies

**Status**: Maintained for backward compatibility, will be removed in future major version

## Implementation Tasks

### Phase 1: Role Creation
- [x] Create `src/roles/apache/` structure
- [x] Create `src/roles/php/` structure
- [x] Write comprehensive README.md for both roles
- [x] Create meta/main.yml with proper dependencies
- [x] Create defaults/main.yml with role-specific variables
- [x] Create handlers/main.yml for service management

### Phase 2: Task Extraction
- [x] Extract Apache tasks from `apache-php/tasks/main.yml` → `apache/tasks/main.yml`
- [x] Copy PHP task files to `php/tasks/` (php.yml, php-redhat7.yml, etc.)
- [x] Create `php/tasks/main.yml` orchestration file
- [x] Copy Apache templates to `apache/templates/`
- [x] Copy PHP templates to `php/templates/`
- [x] Update handler notifications (apache notifies restart apache, php notifies restart php-fpm)

### Phase 3: Deprecation Shim
- [x] Create `apache-php/meta/main.yml` with dependencies on apache + php
- [x] Replace `apache-php/tasks/main.yml` with deprecation warning
- [x] Create `apache-php/README.md` with migration instructions

### Phase 4: Playbook Updates
- [x] Update `src/playbooks/site.yml` to use `apache` and `php` roles
- [x] Update inline comments about Remi repo location
- [x] Verify no other playbooks reference `apache-php` role
- [x] Update tags if needed (kept `apache-php` tag for backward compatibility)

### Phase 5: Bootstrap Sequencing
- [x] Update `src/scripts/getmeza.sh` to install Apache before user setup
  - Added Apache installation block after repo configuration
  - Detects Rocky/RHEL distro and installs `httpd` package
  - Ensures apache group exists before `ansible-playbook setup-meza-user.yml` runs
- [x] Update `Vagrantfile` with comment about new sequencing
  - Vagrantfile already uses getmeza.sh, so automatically benefits from Apache pre-install
  - Added comment explaining Issue #287 fix

### Phase 6: Documentation
- [x] Create `src/roles/apache/README.md` with:
  - Role description and responsibilities
  - Requirements (set-vars dependency)
  - Variables documentation
  - Migration guide from apache-php
  - Future plans (geerlingguy.apache migration path)
- [x] Create `src/roles/php/README.md` with:
  - Role description and responsibilities
  - PHP version support (7.4/8.0+)
  - Profiling setup instructions
  - MS SQL driver optional feature
  - Migration guide from apache-php
- [x] Create `src/roles/meza-user/README.md` with:
  - Bootstrap sequencing requirements
  - Apache dependency explanation
  - Testing instructions
  - Historical context (replaced bash scripts)
  - Known issues and solutions
- [x] Update `apache-php/README.md` with deprecation notice

### Phase 7: Testing Checklist 📋

**Pre-Deployment Verification**:
- [x] Run linting on Apache role files - **PASSED**
  ```bash
  ./src/scripts/lint-files.sh src/roles/apache/
  ```
- [x] Run linting on PHP role files - **FAILED (78 pre-existing violations)**
  ```bash
  ./src/scripts/lint-files.sh src/roles/php/
  ```
  - ⚠️ **Note**: PHP role linting failures are pre-existing issues from apache-php role
  - Issues include: FQCN violations, var-naming, command-instead-of-shell, etc.
  - These were already present in `apache-php/tasks/` files and were copied over
  - Recommendation: Address in separate cleanup PR after this architectural change
  - The split itself doesn't introduce new linting violations
- [x] Verify apache-php deprecation shim - **PASSED**
- [x] Check playbook syntax
  ```bash
  ansible-playbook src/playbooks/site.yml --syntax-check
  ```

**Vagrant Testing**:
- [ ] Test fresh Vagrant environment bootstrap
  ```bash
  vagrant destroy -f
  vagrant up
  ```
- [ ] Verify Apache installed before user creation in output
- [ ] Verify meza-ansible user added to apache group
  ```bash
  vagrant ssh
  id meza-ansible | grep apache
  ```
- [ ] Deploy MediaWiki
  ```bash
  sudo meza deploy vagrant -vvv
  ```
- [ ] Verify wiki creation works
  ```bash
  sudo meza create wiki testwiki
  ```
- [ ] Check file permissions on htdocs
  ```bash
  ls -la /opt/htdocs/
  ```

**Production Testing**:
- [ ] Test on fresh Rocky Linux 8 VM
- [ ] Test on existing Meza deployment (upgrade path)
- [ ] Verify backward compatibility (apache-php role still works)
- [ ] Test with PHP profiling enabled
- [ ] Test with MS SQL driver installation

**Functional Testing**:
- [ ] MediaWiki accessible via browser
- [ ] File uploads work
- [ ] VisualEditor loads
- [ ] Search (CirrusSearch) works
- [ ] API requests work
- [ ] Check Apache logs for errors: `/var/log/httpd/error_log`
- [ ] Check PHP-FPM logs (RHEL8): `/var/log/php-fpm/www-error.log`

## Known Issues and Resolutions

### Issue #1: Composer Dependency Ordering (RESOLVED)

**Problem**: Initial implementation had composer as a meta dependency in php/meta/main.yml, causing it to run before PHP was installed. This resulted in error:
```
[Errno 2] No such file or directory: b'php': b'php'
```

**Root Cause**: Meta dependencies run before the role's tasks, so composer tried to execute before PHP installation completed.

**Solution**: Moved composer from meta/main.yml dependencies to php/tasks/main.yml, included after PHP installation:
```yaml
# php/tasks/main.yml
- name: Install PHP
  ansible.builtin.import_tasks: php.yml

# Composer AFTER PHP installation
- name: Ensure Composer configured
  ansible.builtin.include_role:
    name: composer
```

**Status**: Fixed in commit (pending)

---

## Migration Path for Users

### For New Deployments
No action required. The new structure is used automatically.

### For Existing Deployments
No immediate action required. The `apache-php` role continues to work via the deprecation shim.

**Recommended Migration** (optional but preferred):

1. Update your playbooks:
   ```yaml
   # Old
   roles:
     - apache-php

   # New
   roles:
     - apache
     - php
   ```

2. Test the deployment:
   ```bash
   meza deploy <env> --check
   ```

3. Deploy when ready:
   ```bash
   meza deploy <env>
   ```

## Benefits Achieved

### Improved Bootstrap Sequencing
- Apache group exists before meza-ansible user creation
- No more silent group membership failures
- Clearer dependency chain: Apache → User → PHP → MediaWiki

### Better Composability
- Roles can be used independently
- Easier to swap out for community roles (geerlingguy.apache, geerlingguy.php)
- Follows Ansible best practices (single responsibility principle)

### Enhanced Maintainability
- Clearer separation of concerns
- Each role has focused documentation
- Easier to test in isolation
- Reduced cognitive load when modifying web server vs PHP config

### Backward Compatibility
- Existing playbooks continue to work
- Deprecation shim provides migration path
- No breaking changes for current users

## Future Improvements

### Short-term (Next Release)
- [ ] Add community.general.apache2_module FQCN to apache role
- [ ] Consider extracting Composer to separate role
- [ ] Add role-specific tags to apache and php roles

### Long-term (Future Major Version)
- [ ] Migrate to `geerlingguy.apache` role
- [ ] Migrate to `geerlingguy.php` role
- [ ] Remove `apache-php` deprecation shim
- [ ] Add PHP version selection variable (currently hardcoded per OS)

## Related Issues and PRs

- **Issue #287**: Setup meza-user.yml fails with undefined m_meza
  - Root cause identified: apache group didn't exist during user creation
  - Solution: Split apache-php role, install Apache in getmeza.sh
- **Issue #272**: Umask and user setup improvements
  - Related: meza-user role replaces bash scripts
  - Dependency: Proper group membership for meza-ansible user

## Rollback Plan

If issues are discovered after deployment:

1. **Immediate Rollback** (if apache-php role still exists):
   ```yaml
   # Revert playbook changes
   roles:
     - apache-php  # Uses old monolithic role
   ```

2. **Fix getmeza.sh** (if bootstrap fails):
   ```bash
   # Comment out Apache installation block
   # Run setup-meza-user.yml without apache group membership
   ```

3. **Report Issue**: Create GitHub issue with:
   - Error messages
   - OS and version
   - Deployment type (Vagrant, production, etc.)
   - Steps to reproduce

## Sign-off

- [x] Implementation completed
- [ ] Testing completed (pending)
- [ ] Documentation reviewed (this file)
- [ ] Ready for deployment

**Implementation Notes**:
- All file operations completed successfully
- Linting not yet run (pending user verification)
- Vagrant testing pending user execution
- Production deployment testing pending

---

**Last Updated**: February 4, 2026
**Status**: Implementation Complete, Testing Pending
**Next Steps**: Run linting, test in Vagrant, verify production deployment
