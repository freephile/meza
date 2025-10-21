# Meza Command: `delete`

## Description

Delete wikis or other components in the Meza environment.

## Usage

```bash
meza delete wiki <environment>
meza delete wiki-promptless <environment> <wiki_id>
meza delete elasticsearch <environment>
```

## Examples

```bash
# Interactive wiki deletion (shows list to choose from)
meza delete wiki monolith
meza delete wiki production

# Delete specific wiki without prompts
meza delete wiki-promptless monolith testwiki
meza delete wiki-promptless production oldwiki

# Delete elasticsearch data (search indexes)
meza delete elasticsearch monolith
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<environment>` | Environment name | ✓ |
| `<wiki_id>` | Wiki identifier to delete | ✓ (wiki-promptless only) |

## Sub-commands

- **`wiki`** - Interactive wiki deletion with confirmation prompts
- **`wiki-promptless`** - Non-interactive wiki deletion (automation-friendly)
- **`elasticsearch`** - Delete search index data (does not affect wikis)

## ⚠️ WARNING

**Wiki deletion is IRREVERSIBLE** and will permanently remove:

- ❌ All wiki content and pages
- ❌ Database tables and data
- ❌ Uploaded files and media
- ❌ Wiki-specific configuration

## Safety Recommendations

1. **Create a backup before deletion:**
   ```bash
   meza backup <environment>
   ```

2. **Verify wiki list first:**
   ```bash
   meza list-wikis <environment>
   ```

3. **Use interactive mode for safety:**
   ```bash
   meza delete wiki <environment>
   ```

## Notes

- Interactive mode shows available wikis and requires confirmation
- Non-interactive mode is useful for scripting but **use with caution**
- Elasticsearch deletion only removes search indexes, not wiki content
- Deleted wikis are automatically removed from environment configuration
- Recovery requires restoring from backup

## See Also

- [`meza create`](create.md) - Create new wikis
- [`meza backup`](backup.md) - Create backups
- [`meza list-wikis`](list-wikis.md) - List existing wikis