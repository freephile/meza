# Meza Command: `create`

## Description

Create new wikis in the specified environment.

## Usage

```bash
meza create wiki <environment>
meza create wiki-promptless <environment> <wiki_id> <wiki_name>
```

## Examples

```bash
# Interactive wiki creation (prompts for details)
meza create wiki monolith
meza create wiki production

# Non-interactive wiki creation
meza create wiki-promptless monolith testwiki "Test Wiki"
meza create wiki-promptless production blogwiki "Company Blog"
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<environment>` | Environment name | ✓ |
| `<wiki_id>` | Unique wiki identifier | ✓ (wiki-promptless only) |
| `<wiki_name>` | Display name for the wiki | ✓ (wiki-promptless only) |

## Sub-commands

- **`wiki`** - Interactive wiki creation with prompts
- **`wiki-promptless`** - Non-interactive wiki creation (automation-friendly)

## Notes

- Wiki IDs must be unique within the environment
- Wiki IDs should be lowercase, alphanumeric (no spaces or special chars)
- Interactive mode will prompt for wiki ID, name, and other settings
- Non-interactive mode is useful for scripting and automation
- New wikis are automatically added to the environment configuration

## See Also

- [`meza delete`](delete.md) - Delete wikis
- [`meza list-wikis`](list-wikis.md) - List existing wikis
- [`meza deploy`](deploy.md) - Deploy environment