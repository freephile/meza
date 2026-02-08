# configure-wiki role

Creates the configuration scaffold for a new wiki in Meza.

## Overview

This role is invoked by `meza create wiki <env>` and sets up all necessary
configuration files and directories for a new wiki **without** actually deploying
it to servers or creating database tables.

## What It Does

1. Creates `/opt/conf-meza/public/wikis/<wiki_id>/` directory structure
2. Copies default assets: logos (PNG/SVG), favicons, apple-touch-icons
3. Creates customization directories:
   - `preLocalSettings.d/` - PHP code loaded before MediaWiki LocalSettings.php
   - `postLocalSettings.d/` - PHP code loaded after MediaWiki LocalSettings.php
   - `samlAuthorizations.d/` - SAML authorization rules
4. Generates starter templates with examples and documentation
5. Registers wiki in `public.yml` for declarative configuration
6. Creates the `.smw.json` setup information file for Semantic MediaWiki

## What It Does NOT Do

- Does not create database tables (handled by `setup-wiki` role during deploy)
- Does not modify app servers (handled by `sync-configs` + deployment)
- Does not configure web server (handled by `apache-php` role)

## Requirements

- Meza installed at `/opt/meza/`
- Configuration directory at `/opt/conf-meza/`
- `set-vars` role must run first

## Role Variables

```yaml
# Required (passed by meza CLI)
wiki_id: "demo"           # Short identifier (alphanumeric, no spaces)
wiki_name: "Demo Wiki"    # Human-readable display name

# Inherited from set-vars/defaults
m_config_public_dir: "/opt/conf-meza/public"
user_apache: "apache"     # or "www-data" on Debian
group_apache: "apache"
```

## Dependencies

- `set-vars` role (for path/user variable initialization)

## Example Usage

### Via CLI (Normal Usage)
```bash
meza create wiki monolith
meza deploy monolith
```

### Direct Playbook (Testing/Development)
```yaml
- hosts: localhost
  roles:
    - set-vars
    - role: configure-wiki
      vars:
        wiki_id: testwiki
        wiki_name: "Test Wiki"
```

## Workflow Integration

```
meza create wiki <env>
    ↓
configure-wiki role (creates /opt/conf-meza/public/wikis/<id>/)
    ↓
User customizes preLocalSettings.d/, logos, etc.
    ↓
meza deploy <env>
    ↓
sync-configs → setup-wiki → update.php
    ↓
Wiki live on servers
```

## Customization After Creation

After running `meza create wiki`, customize your wiki by editing:

- **Logos**: Replace PNG/SVG files in `/opt/conf-meza/public/wikis/<id>/`
- **PHP settings**: Add files to `preLocalSettings.d/` or `postLocalSettings.d/`
- **SAML auth**: Edit `samlAuthorizations.d/base.php`
- **Declarative config**: Edit `/opt/conf-meza/public/public.yml`

## File Permissions Note

The role sets `mode: '0775'` for directories and `mode: 'u=rw,g=rw,o=r'` for
`.smw.json` to allow:
- Apache to read/write PHP files
- meza-ansible (apache group) to also write configurations

## See Also

- `setup-wiki` role - Actually creates wiki in MediaWiki/database
- `sync-configs` role - Syncs configs from controller to app servers
- `meza create wiki` command - CLI wrapper for this role
