# Meza Command: `maint`

## Description

Perform maintenance operations on Meza environments and wikis.

## Usage

```bash
meza maint [directive]
```

## Directives

### `run-jobs` - Run Wiki Jobs

Run all pending jobs on all wikis in the environment.

```bash
meza maint run-jobs
```

**What it does:**
- Executes MediaWiki's job queue for all wikis
- Processes background tasks like:
  - Page link updates
  - Search index updates
  - Email notifications
  - Image thumbnail generation
  - Cache invalidation

### `rebuild <env>` - Rebuild Search and SMW

Rebuild Semantic MediaWiki data and search indexes for an environment.

```bash
meza maint rebuild <environment>
```

**What it does:**
- Rebuilds Semantic MediaWiki (SMW) data structures
- Recreates search indexes for all wikis
- Updates CirrusSearch/Elasticsearch indexes

### `run <env> <script>` - Run Any Maintenance Script

Run any MediaWiki maintenance script on an environment's wikis. This is the
general-purpose command for ad-hoc maintenance operations.

```bash
meza maint run <environment> <script>
meza maint run <environment> <script> --wiki <wiki_id>
meza maint run <environment> <script> --args '<script_args>'
meza maint run <environment> <script> --wiki <wiki_id> --args '<script_args>'
```

**Options:**

| Option | Description |
|--------|-------------|
| `--wiki <wiki_id>` | Run script on a specific wiki only (defaults to all wikis) |
| `--args '<script_args>'` | Arguments to pass to the maintenance script |

**Examples:**

```bash
# Run update.php on all wikis
meza maint run monolith update

# Run refreshLinks.php on a specific wiki
meza maint run monolith refreshLinks --wiki demo

# Run runJobs.php with a maximum job count
meza maint run monolith runJobs --args '--maxjobs=50'

# Run refreshLinks.php with verbose output on a specific wiki
meza maint run monolith refreshLinks --wiki demo --args '--verbose'
```

**What it does:**
- Runs any MediaWiki maintenance script via the `run-maintenance.yml` playbook
- Targets all wikis by default, or a specific wiki with `--wiki`
- Passes optional arguments to the script with `--args`
- Reports per-wiki output, exit code, and any errors

### `cleanuploadstash <env>` - Clean Upload Stash

Clean up temporary upload files from the upload stash directory.

```bash
meza maint cleanuploadstash <environment>
```

**What it does:**
- Removes stale temporary upload files
- Frees up disk space from incomplete uploads
- Cleans upload stash directory

### `encrypt-string <env> <value> [var_name]` - Encrypt String

Encrypt a string value using Ansible Vault for secure storage.

```bash
meza maint encrypt-string <environment> <secret_value>
meza maint encrypt-string <environment> <secret_value> variable_name
```

**What it does:**
- Encrypts sensitive values using Ansible Vault
- Optionally assigns a variable name to the encrypted string
- Returns encrypted string for use in configuration files

### `decrypt-string <env> <encrypted_value>` - Decrypt String

Decrypt a previously encrypted string using Ansible Vault.

```bash
meza maint decrypt-string <environment> '$ANSIBLE_VAULT;1.1;AES256...'
```

**What it does:**
- Decrypts Ansible Vault encrypted strings
- Shows the original plaintext value
- Useful for retrieving forgotten encrypted values

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `[directive]` | Maintenance operation to perform | No |
| `<environment>` | Environment name (for env-specific commands) | Yes (for some directives) |
| `<script>` | Maintenance script name (with or without .php) | Yes (for `run`) |
| `--wiki <wiki_id>` | Target a specific wiki (for `run`) | No |
| `--args '<script_args>'` | Arguments to pass to script (for `run`) | No |
| `<value>` | Value to encrypt/decrypt | Yes (for encrypt/decrypt) |
| `[var_name]` | Variable name for encrypted string | No |

## Job Queue Operations

The job queue processes various MediaWiki background tasks:

| Job Type | Description |
|----------|-------------|
| **RefreshLinks** | Update internal link tables |
| **HTMLCacheUpdate** | Update page cache |
| **SearchUpdate** | Update search indexes |
| **SendMail** | Send pending email notifications |
| **ThumbnailRender** | Generate image thumbnails |
| **CategoryMembershipChange** | Update category memberships |

## When to Run Maintenance

Run various maintenance operations when:

**Job Queue (`run-jobs`):**
- ✅ After bulk content imports
- ✅ After extension installations
- ✅ When search results seem outdated
- ✅ When page links appear broken
- ✅ As part of regular maintenance schedule

**Rebuild (`rebuild`):**
- ✅ After Semantic MediaWiki updates
- ✅ When search functionality is broken
- ✅ After major content restructuring
- ✅ When CirrusSearch indexes are corrupted

**Upload Stash Cleanup (`cleanuploadstash`):**
- ✅ When disk space is running low
- ✅ As part of regular cleanup maintenance
- ✅ After failed bulk upload operations

**Ad-hoc Script Execution (`run`):**
- ✅ For any one-off maintenance task
- ✅ After debugging specific MediaWiki issues
- ✅ When a specific script needs to be run on one or all wikis

**String Encryption/Decryption:**
- ✅ When storing sensitive configuration values
- ✅ For secure password management
- ✅ When troubleshooting encrypted values

## Notes

- Job processing may take time for large wikis
- Jobs run automatically during normal wiki operation
- Manual job runs are useful after bulk operations
- Jobs process in background without affecting wiki availability
- Consider running during low-traffic periods for large job queues

## Performance Considerations

- Large job queues may impact server performance
- Monitor system resources during job processing
- Consider breaking up large job runs across multiple sessions

## Advanced: Custom Maintenance Scripts

The `meza maint run` command provides the simplest way to run any MediaWiki
maintenance script. For cases where you need more control over the Ansible
invocation, you can also call the underlying playbook directly.

### Using `meza maint run` (Recommended)

```bash
# Run any MediaWiki maintenance script on all wikis
meza maint run <env> <script>

# Run with arguments
meza maint run <env> runJobs --args '--maxjobs=10'

# Run on a specific wiki
meza maint run <env> update --wiki demo
```

### Direct Ansible Playbook Usage

```bash
# Run any MediaWiki maintenance script on all wikis
ansible-playbook /opt/meza/src/playbooks/run-maintenance.yml \
  -e "maintenance_script=scriptname" \
  -i /opt/conf-meza/secret/<env>/hosts

# Run script with arguments on all wikis
ansible-playbook /opt/meza/src/playbooks/run-maintenance.yml \
  -e "maintenance_script=runJobs" \
  -e "maintenance_args=--maxjobs=10" \
  -i /opt/conf-meza/secret/<env>/hosts

# Run script on specific wiki only
ansible-playbook /opt/meza/src/playbooks/run-maintenance.yml \
  -e "maintenance_script=update" \
  -e "target_wiki=demo" \
  -i /opt/conf-meza/secret/<env>/hosts
```

### Common Maintenance Scripts

| Script | Purpose | Example Arguments |
|--------|---------|-------------------|
| `runJobs` | Process job queue | `--maxjobs=50 --type=refreshLinks` |
| `update` | Update database schema | `--quick` |
| `refreshLinks` | Refresh page links | `--verbose` |
| `rebuildall` | Rebuild all indexes | ` ` |
| `cleanupUploadStash` | Clean upload stash | `--delete-after=7` |
| `importDump` | Import XML dump | `--username-prefix=import` |
| `dumpBackup` | Create XML backup | `--full --uploads` |

### Script Parameters

- **`maintenance_script`** (required): Name of the maintenance script (with or without .php extension)
- **`maintenance_args`** (optional): Command-line arguments to pass to the script
- **`target_wiki`** (optional): Run on specific wiki only (defaults to all wikis)

## See Also

- [`meza deploy`](deploy.md) - Deploy environment updates
- [`meza backup`](backup.md) - Backup before major maintenance
- [`meza debug`](debug.md) - Debug maintenance issues
- [`meza create`](create.md) - Create new wikis
- [`meza delete`](delete.md) - Delete wikis or components
