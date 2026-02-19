# update.php role

Runs MediaWiki database updates for a wiki, with a backup and logging flow.

## Purpose

This role performs the following steps:

- Logs that it is running for the given wiki.
- Creates a timestamped SQL backup of the wiki database on the backup server.
- Optionally prunes old SQL backups.
- Ensures an update.php log directory exists and writes output to a per-wiki log.
- Runs MediaWiki `maintenance/run update`.
- On failure, captures logs and applies a targeted workaround for the
  "Main slot of revision not found in database" error, then retries.

## Usage of the string "update.php" in this project

The string "update.php" appears in three distinct contexts in the Meza
codebase. This README calls them out explicitly to support future refactoring
so that these contexts use distinct identifiers.

### 1) Ansible role name

Role name: `update.php`

Referenced from:

- src/roles/mediawiki/tasks/main.yml
- src/roles/verify-wiki/tasks/import-wiki-sql.yml

### 2) Ansible tag

Tag name: `update.php`

Used in:

- src/roles/update.php/tasks/main.yml
- src/roles/mediawiki/tasks/main.yml
- src/roles/verify-wiki/tasks/import-wiki-sql.yml

Also referenced in documentation as a tag to skip:

- CONTRIBUTING.md
- manual/meza-cmd/config.md
- .github/copilot-instructions.md

### 3) MediaWiki maintenance script invocation

The actual PHP script is invoked via MediaWiki's maintenance runner:

- src/roles/update.php/tasks/main.yml uses:
  `maintenance/run update --quick --doshared`

Mentions in docs or comments:

- src/playbooks/run-maintenance.yml (commented example)
- CHANGELOG, RELEASE-NOTES.md, RELEASE_NOTES-HEAD.md (release notes)

## Notes for refactoring

To disambiguate these contexts, consider:

- Renaming the role to something like `app-maintenance-update` or `mediawiki-maintenance-update`.
- Renaming tags to `mw-db-update` (or similar).
- Leaving the actual script name as-is, since it is upstream MediaWiki.
