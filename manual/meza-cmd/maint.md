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

**When it runs:**
- `meza maint rebuild <environment>` runs the dedicated rebuild playbook for the environment.
- With no extra Ansible tag filters, it runs both the search rebuild and the SMW rebuild.
- You can pass Ansible tags through to limit the run, for example:

```bash
meza maint rebuild <environment> --tags search-index
meza maint rebuild <environment> --tags smw-data
```

**Search rebuild behavior:**
- The search rebuild recreates the active CirrusSearch/Elasticsearch indices for each wiki.
- It runs `CirrusSearch:UpdateSearchIndexConfig --startOver` and then two `CirrusSearch:ForceSearchIndex` passes.
- In this rebuild path, `ForceSearchIndex` writes to Elasticsearch in-process by default. The rebuild is expected to populate the index before the command returns.
- After the search rebuild, Meza also runs `runJobs --type cirrusSearchElasticaWrite` for each wiki as a follow-up drain step so queued CirrusSearch writes do not lag behind the rebuild.

**What to expect from the job queue afterward:**
- It is normal for a later manual `runJobs` to still find other MediaWiki job types such as `refreshLinks`, `htmlCacheUpdate`, mail, or thumbnail jobs.
- It is not necessary for the general MediaWiki job queue to be completely empty for the search rebuild to be considered successful.
- The key post-rebuild check is that the Elasticsearch indices for the wiki have non-zero document counts when the wiki has indexable content.
- CirrusSearch may enqueue additional `cirrusSearchElasticaWrite` jobs while indexing is in progress, and those jobs can legitimately remain in the queue at command completion depending on queue backend and worker timing.
- Meza runs a targeted `runJobs --type cirrusSearchElasticaWrite` follow-up drain as a best-effort step, but an immediately empty queue is not guaranteed.

**Quick post-rebuild checks:**

```bash
curl -s 'localhost:9200/_cat/aliases/wiki_<wiki>_*?v'
curl -s 'localhost:9200/_cat/indices/wiki_<wiki>_*?v&h=index,docs.count,store.size'
WIKI=<wiki> /opt/htdocs/mediawiki/maintenance/run showJobs
```

**If it fails with** `Primary index was expected to be an alias`:
- The wiki's primary search index alias is missing or points at the wrong object.
- Repair the alias first, then rerun the rebuild.
- Quick check:

```bash
curl -s localhost:9200/_alias/wiki_<wiki>_general
curl -s localhost:9200/_cat/indices/wiki_<wiki>_general*?h=index
```
- If there is exactly one backing index, add the alias back with:

```bash
curl -s -XPOST 'localhost:9200/_aliases' -H 'Content-Type: application/json' -d '{"actions":[{"add":{"index":"<backing-index>","alias":"wiki_<wiki>_general"}}]}'
```

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
- ✅ When you want a full operator-driven search rebuild rather than waiting for incremental queue updates

**Upload Stash Cleanup (`cleanuploadstash`):**
- ✅ When disk space is running low
- ✅ As part of regular cleanup maintenance
- ✅ After failed bulk upload operations

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
- `meza maint rebuild` is the operator-facing command for full search/SMW rebuilds; routine `meza deploy` runs do not rebuild search unless you explicitly tag them

## Performance Considerations

- Large job queues may impact server performance
- Monitor system resources during job processing
- Consider breaking up large job runs across multiple sessions

## Advanced: Custom Maintenance Scripts

For advanced users, you can run any MediaWiki maintenance script using the general-purpose playbook:

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

### Examples
These commands are very long compared to direct invocation of a PHP script, but
they do work. Most importantly they work in the Ansible context where you can
change out the inventory etc for remote command and control across your infrastructure.

- `ansible-playbook /opt/meza/src/playbooks/run-maintenance.yml -e "maintenance_script=runJobs" -e "maintenance_args=--maxjobs=10" -i /opt/conf-meza/secret/monolith/hosts`
- `/opt/meza/src/playbooks/run-maintenance.yml -e "maintenance_script=runJobs" -e "maintenance_args=--maxjobs=10" -i /opt/conf-meza/secret/monolith/hosts -e "target_wiki=demo"`

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
