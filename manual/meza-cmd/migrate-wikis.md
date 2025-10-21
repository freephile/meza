# Meza Command: `migrate-wikis`

## Description

Migrate existing directory-based wikis to declarative configuration format.

## Usage

```bash
meza migrate-wikis <environment>
```

## Examples

```bash
# Migrate production environment wikis
meza migrate-wikis production

# Migrate development environment
meza migrate-wikis development
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<environment>` | Environment name to migrate | ✓ |

## What It Does

The migration process automatically:

1. **📂 Scans** `/opt/conf-meza/public/wikis/` for existing wiki directories
2. **📖 Reads** each wiki's `preLocalSettings.d/base.php` to extract `$wgSitename`
3. **✏️ Creates/updates** `public.yml` with discovered wikis in declarative format
4. **🎯 Sets primary wiki** (first found, or 'demo' if it exists)
5. **💾 Backs up** existing `public.yml` before making changes

## Before Migration

**Legacy directory-based structure:**
```
/opt/conf-meza/public/wikis/
├── wiki1/
│   └── preLocalSettings.d/base.php
├── wiki2/
│   └── preLocalSettings.d/base.php
└── demo/
    └── preLocalSettings.d/base.php
```

## After Migration

**Declarative configuration in `public.yml`:**
```yaml
wikis:
  demo:
    name: "Demo Wiki"
    primary: true
  wiki1:
    name: "Wiki One"
  wiki2:
    name: "Wiki Two"
```

## Benefits of Declarative Configuration

After migration, you can:
- ✅ **Add wikis** by editing `public.yml` or using `meza create wiki`
- ✅ **Remove wikis** by editing `public.yml` or using `meza delete wiki`
- ✅ **Control wiki ordering** and primary wiki designation
- ✅ **Use wiki redirects** and other advanced features
- ✅ **Version control** wiki configuration changes

## Important Notes

- 🔄 **Configuration only**: This command only updates configuration files
- 🚀 **Deploy required**: Run `meza deploy` after migration to apply changes
- 💾 **Backup created**: Existing `public.yml` is automatically backed up
- 🎯 **Primary wiki**: First wiki found becomes primary (or 'demo' if exists)

## Post-Migration Steps

1. **Review the generated configuration:**
   ```bash
   cat /opt/conf-meza/public/<environment>/public.yml
   ```

2. **Deploy changes:**
   ```bash
   meza deploy <environment>
   ```

3. **Verify wikis are working:**
   ```bash
   meza list-wikis <environment>
   ```

## Troubleshooting

If migration fails:
- Ensure wiki directories have proper `base.php` files
- Check file permissions on configuration directories
- Verify `$wgSitename` is properly set in `base.php` files
- Review backup files if rollback is needed

## See Also

- [`meza create`](create.md) - Create new wikis after migration
- [`meza delete`](delete.md) - Remove wikis after migration
- [`meza deploy`](deploy.md) - Apply migration changes
- [`meza list-wikis`](list-wikis.md) - Verify migrated wikis