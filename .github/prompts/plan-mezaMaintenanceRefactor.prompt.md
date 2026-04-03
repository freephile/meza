# Plan: Modernize Meza Maintenance Interface

## TL;DR
Replace the narrow, positional-argument-based `meza maint` sub-commands with a flexible generic `meza maint run <env> <script>` command that is a thin wrapper over `run-maintenance.yml`. Fix the broken `run-jobs` command to take `env` + named args. Replace the PHP cron wrapper with direct `meza maint run-jobs` cron calls. Remove the redundant `cleanup-upload-stash.yml`. Update documentation.

**User decisions confirmed:**
- `run-jobs` will require `env` (breaking from broken behavior)
- Cron replaces `runAllJobs.php` with direct ansible-playbook calls via `meza maint run-jobs`
- `cleanup-upload-stash.yml` is removed as redundant

---

## Phase 1: Fix `run-maintenance.yml`

**File:** `src/playbooks/run-maintenance.yml`

1. Remove the `Set fact - maintenance script with extension` task that appends `.php`. The MediaWiki `maintenance/run` runner handles name resolution and the `.php` suffix is optional. The current logic also breaks `Extension:ScriptName` format scripts.
2. Change `script_name` fact to just be `{{ maintenance_script }}` directly.
3. Update the shell task to use `{{ maintenance_script | quote }}` directly (no `script_name` fact needed, or keep as simple alias without `.php` mangling).
4. Run linting: `./src/scripts/lint-files.sh src/playbooks/run-maintenance.yml`

## Phase 2: Add `meza_command_maint_run` — generic thin wrapper

**File:** `src/scripts/meza.py`

Add new function `meza_command_maint_run(argv)` using `argparse.ArgumentParser(add_help=False)` with `parse_known_args` so unknown args pass through to ansible-playbook:

```
meza maint run <env> <script> [--wiki=<wiki_id>] [--args="<script args>"] [<ansible-passthrough>]
```

- `argv[0]` = env (positional)
- `argv[1]` = script (positional, e.g. `runJobs`, `cleanupUploadStash`, `CirrusSearch:UpdateSearchIndexConfig`)
- `--wiki=<wiki_id>` → `target_wiki` extra var
- `--args="..."` → `maintenance_args` extra var (e.g. `--maxjobs=100 --maxtime=30`)
- remaining unknown args → appended to ansible-playbook command (e.g. `-vvv`, `--check`, `--tags`)

Build `more_extra_vars = {'maintenance_script': script}`, add `maintenance_args` and `target_wiki` when provided. Call `playbook_cmd('run-maintenance', env, more_extra_vars)` then append ansible passthrough args.

Run linting: `pylint src/scripts/meza.py`

## Phase 3: Rewrite `meza_command_maint_run_jobs`

**File:** `src/scripts/meza.py`

Replace the broken implementation with a thin wrapper over `meza_command_maint_run`:

```
meza maint run-jobs <env> [--wiki=<wiki>] [--maxjobs=N] [--maxtime=N] [--type=TYPE] [<ansible-passthrough>]
```

- Require `env` as first positional arg (validate with `check_environment`)
- Parse `--maxjobs`, `--maxtime`, `--type` locally; assemble into `maintenance_args` string
- Pass `--wiki` through to `target_wiki`
- Delegate to `run-maintenance.yml` with `maintenance_script=runJobs`
- Remove all filesystem/wiki-config.php discovery logic
- Remove `import re` (currently inside function body — should not be there anyway)
- Delete reference to `runAllJobs.php`

## Phase 4: Remove `cleanup-upload-stash.yml`

**File:** `src/playbooks/cleanup-upload-stash.yml` (and `.svg`, `-w-tasks.svg`)

- Remove `cleanup-upload-stash.yml` — fully redundant with `run-maintenance.yml`
- Remove associated SVG diagram files referenced in `src/playbooks/README.md`
- Update `src/playbooks/README.md` to remove references to this playbook
- The `meza maint cleanuploadstash <env>` CLI command continues to work (already calls `run-maintenance` playbook)

## Phase 5: Cron template — replace `runAllJobs.php`

**Files:**
- `src/roles/cron/templates/meza-ansible.crontab.j2`
- `src/roles/cron/templates/runAllJobs.php.j2` (delete)
- `config/defaults.yml` (update variables)

### Cron template changes

Replace the two `WIKI=... php ... runAllJobs.php ...` cron lines with `meza maint run-jobs` calls:

```jinja2
# Run jobs frequently with limits
{{ run_jobs_freq_crontime }} sudo meza maint run-jobs {{ env }} --maxtime={{ run_jobs_freq_maxtime }} --maxjobs={{ run_jobs_freq_maxjobs }} >> ...log

# Run all jobs (no limits)
{{ run_all_jobs_crontime }} sudo meza maint run-jobs {{ env }} >> ...log
```

- Drop `run_jobs_freq_totalmaxtime` and `run_jobs_freq_maxload` variables (PHP-only, no equivalent in runJobs.php)
- Rename the `run_jobs_freq_maxtime` / `run_jobs_freq_maxjobs` variables to reflect they become `--maxtime`/`--maxjobs` args to runJobs directly

### defaults.yml changes

- Remove `run_jobs_freq_totalmaxtime` and `run_jobs_freq_maxload` defaults
- Keep `run_jobs_freq_maxtime`, `run_jobs_freq_maxjobs`, `run_jobs_freq_crontime`, `run_all_jobs_crontime`
- Check these variables exist and have sensible defaults

### Delete `runAllJobs.php.j2`
- Also remove the corresponding deploy task in the cron role that writes `runAllJobs.php` to `.deploy-meza/`

## Phase 6: Documentation

**File:** `manual/meza-cmd/maint.md`

- Lead with `meza maint run <env> <script>` as the primary generic command
- Document `--wiki`, `--args`, and ansible passthrough
- Document all existing shortcut commands as convenience wrappers
- Add reference table of common maintenance scripts with example args
- Add section for extension maintenance scripts (`Extension:scriptname` format)
- Add note about cron integration variables (`run_jobs_freq_*`)
- Remove broken positional argument documentation for `run-jobs`

---

## Relevant Files

- `src/scripts/meza.py` — `meza_command_maint_run` (new), `meza_command_maint_run_jobs` (rewrite), lines ~1640–1810
- `src/playbooks/run-maintenance.yml` — remove `.php` appending from script_name fact
- `src/playbooks/cleanup-upload-stash.yml` — delete
- `src/roles/cron/templates/meza-ansible.crontab.j2` — replace runAllJobs.php cron lines
- `src/roles/cron/templates/runAllJobs.php.j2` — delete
- `config/defaults.yml` — remove PHP-only cron variables
- `manual/meza-cmd/maint.md` — rewrite

---

## Verification

1. `./src/scripts/lint-files.sh src/playbooks/run-maintenance.yml` — no new errors
2. `./src/scripts/lint-files.sh src/roles/cron/templates/meza-ansible.crontab.j2` — no errors
3. `pylint src/scripts/meza.py` — no new errors
4. Run `meza maint run <env> runJobs` — verify ansible-playbook executes on all wikis
5. Run `meza maint run <env> runJobs --wiki=demo` — verify single-wiki targeting
6. Run `meza maint run <env> runJobs --args="--maxjobs=5"` — verify arg passthrough
7. Run `meza maint run-jobs <env>` — verify runs on all wikis via run-maintenance.yml
8. Run `meza maint run-jobs <env> --maxjobs=10 --wiki=demo` — verify named args
9. Run `meza maint cleanuploadstash <env>` — verify still works (unchanged)
10. Verify cron template renders correctly: `ansible-playbook site.yml --tags cron --check`
11. Verify `meza maint run <env> CirrusSearch:UpdateSearchIndexConfig` — extension script format

---

## Decisions

- **Breaking change**: `meza maint run-jobs` now requires `<env>` as first arg
- **Dropped features**: `run_jobs_freq_totalmaxtime` (total max time across all wikis) and `run_jobs_freq_maxload` (PHP sys_getloadavg check) have no direct equivalent in runJobs.php; dropped from cron
- **Excluded**: `meza maint rebuild`, `meza maint encrypt-string`, `meza maint decrypt-string` — unchanged
- **Excluded**: `update.php` role — already well-designed, keep as-is
- **In scope**: `cleanup-upload-stash.yml` playbook deletion (user confirmed)

## Further Considerations

1. **Multi-server cron**: In a multi-server setup, `meza maint run-jobs` runs ansible from app_server nodes. This is consistent with `meza maint cleanuploadstash` already doing the same in cron — but confirm that `meza` is installed and runnable on app_servers in distributed setups.
2. **`run_jobs_freq_totalmaxtime` replacement**: If total-time limiting across all wikis is needed, a `--totalmaxtime` option could be added to `meza maint run-jobs` that wraps individual wiki runs in a time check. This is a future enhancement, not in scope.
