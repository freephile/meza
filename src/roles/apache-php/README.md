# Apache-PHP Role (DEPRECATED)

⚠️ **This role is deprecated and maintained for backward compatibility only.**

## Migration Required

Please update your playbooks to use the `apache` and `php` roles directly:

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

## Why This Change?

The monolithic `apache-php` role has been split into two separate, composable roles to:

1. **Follow Single Responsibility Principle**: Each role now has a clear, focused purpose
2. **Fix Bootstrap Sequencing**: Apache can now be installed before user setup, ensuring the apache group exists when needed
3. **Improve Composability**: Roles can be used independently or with different combinations
4. **Enable Future Migration**: Structured for easier migration to community roles (e.g., `geerlingguy.apache`, `geerlingguy.php`)

## What This Role Does Now

This role automatically includes both the `apache` and `php` roles as dependencies (see `meta/main.yml`). Your existing playbooks will continue to work without modification, but you should plan to migrate to the new structure.

## Timeline

- **Current**: This deprecation shim is fully functional
- **Future (TBD)**: This role will be removed in a future major version of Meza

## Related Issues

- GitHub Issue: https://github.com/freephile/meza/issues/287

## New Roles Documentation

- [Apache Role Documentation](../apache/README.md)
- [PHP Role Documentation](../php/README.md)
