# Meza Configuration Management

## No `meza config` Command Available

There is no `meza config` command in the current implementation. Such a command would require:

- A complex configuration management system
- Direct YAML file manipulation capabilities
- Environment-aware key/value storage
- Integration with Meza's multi-layered configuration hierarchy

This level of complexity doesn't align with Meza's current architecture, which is designed around direct file editing and Ansible-based configuration management.

## Managing config in Meza

Here is how Meza provides configuration management (get/set/apply):

### View Configuration Values

Use the `meza debug` command to view any configuration variable:

```bash
# View a specific configuration value
meza debug monolith mediawiki_version

# View database configuration
Meza database configuration starts with the 'inventory' file

# View all wikis configured
meza debug production list_of_wikis

# View backup settings
meza debug monolith m_backup_retention_days
```

Remember that it is fast and useful to just grep the two config hierarchies:
`grep -r is_this_even_real /opt/conf-meza /opt/meza'

### Set Configuration Values

Edit configuration files directly using your preferred editor:

```bash
# Edit public (non-sensitive) farm configuration
sudo vi /opt/conf-meza/public/public.yml

# Edit secret (sensitive) configuration namespaced by environment target
sudo vi /opt/conf-meza/secret/monolith/secret.yml

# Edit global app defaults (affects all environments)
# This is only for changes to the project itself
sudo vi /opt/meza/config/defaults.yml
```

### Apply Configuration Changes

Deploy the environment to apply configuration changes:

```bash
# Apply all configuration changes
meza deploy monolith

# Apply only configuration changes (faster, skips updates)
meza deploy monolith --tags mediawiki --skip-tags latest,update.php
```

## Configuration File Hierarchy

Meza uses a layered configuration system. Variables are loaded in the order below;
**later loads win**, so higher-numbered entries override lower-numbered ones.

| Priority | File | Notes |
|----------|------|-------|
| 5 (highest) | `/opt/conf-meza/secret/<env>/secret.yml` | Per-environment secrets: passwords, keys, FQDN, private networking zone |
| 4 | `/opt/conf-meza/public/public.yml` | Per-environment public config: your primary override file for any default |
| 3 | `/opt/meza/config/defaults.yml` | Global defaults for all Meza installations |
| 2 | `/opt/meza/config/paths.yml` | Path variable definitions (loaded before defaults since defaults references them) |
| 1 (lowest) | `/opt/meza/config/RedHat.yml` or `Debian.yml` | OS-family variables (loaded before paths/defaults so they can seed those values) |

> **Implementation reference**: `src/roles/set-vars/tasks/main.yml` is the authoritative
> source for this load order. Variables are loaded via `ansible.builtin.include_vars`;
> a variable defined in a later file completely replaces the same variable from an
> earlier file.

### What to override and where
- **`secret.yml`** — sensitive values only: passwords, API keys, FQDN, SSL config.
- **`public.yml`** — the intended place for all local customization: MediaWiki version,
  auth type, email settings, wiki definitions, extension exclusions, profiling, etc.
- **`defaults.yml`** — Meza project defaults; edit only when contributing upstream changes.
- **OS-family YAMLs** — package names and OS-specific paths; rarely edited directly.

## Common Configuration Examples

### MediaWiki Version
```yaml
# In /opt/conf-meza/public/public.yml
mediawiki_version: "1.39.4"
```

### Backup Configuration
```yaml
# In /opt/conf-meza/public/public.yml
m_backup_retention_days: 30
m_backup_enable: true
```

## See Also

- [`meza debug`](debug.md) - View configuration values and variables
- [`meza deploy`](deploy.md) - Apply configuration changes
- [`meza setup`](setup.md) - Environment setup and initial configuration
