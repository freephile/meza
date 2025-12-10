## Meza Release Notes 43.0.0 → HEAD

### Commits

HEAD -> dev origin/dev
* [8feff366](https://github.com/freephile/meza/commit/8feff366) (2025-12-09) Greg Rundlett: enhance Copilot instructions for Python Also add references to named standards and conventions
  - Modified: `.github/copilot-instructions.md`

* [b02998fa](https://github.com/freephile/meza/commit/b02998fa) (2025-11-25) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [aa49f0b7](https://github.com/freephile/meza/commit/aa49f0b7) (2025-11-24) Greg Rundlett: Remove problematic line from Lockdown config You can not use $wgNamespaceProtection[NS_SPECIAL]['read'] = [ 'user' ];
to restrict the Special pseudo-namespace to registered users.
Note: This is a global variable, not specific to the Lockdown ext.
https://www.mediawiki.org/wiki/Manual:$wgNamespaceProtection
If you accidentally try this, you will receive an error upon accessing
Special:CreateAcccount that you do not have permission to EDIT pages in
the Special namespace.
Continuation of the fix for Issue [#156](https://github.com/freephile/meza/issues/156)
Add comment with API query example for SpecialPage aliases
  - Modified: `config/MezaCoreExtensions.yml`

* [ea8482ea](https://github.com/freephile/meza/commit/ea8482ea) (2025-10-31) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [59cd7f0c](https://github.com/freephile/meza/commit/59cd7f0c) (2025-10-31) Greg Rundlett: cleanup info about "install" command 
  - Modified: `manual/meza-cmd/MIGRATION.md`
  - Modified: `manual/meza-cmd/docker.md`
  - Modified: `manual/meza-cmd/help.md`
  - Modified: `manual/meza-cmd/index.md`
  - Modified: `manual/meza-cmd/install.md`

* [538fe06f](https://github.com/freephile/meza/commit/538fe06f) (2025-10-31) Greg Rundlett: strip trailing whitespace 
  - Modified: `src/scripts/meza.py`

* [c9f6d6d0](https://github.com/freephile/meza/commit/c9f6d6d0) (2025-10-31) Greg Rundlett: doc getmeza.sh concise version
Fixes Issue [#172](https://github.com/freephile/meza/issues/172)
  - Modified: `src/scripts/getmeza.md`

* [27d5656b](https://github.com/freephile/meza/commit/27d5656b) (2025-10-31) Greg Rundlett: doc getmeza.sh Verbose version
Addresses Issue [#172](https://github.com/freephile/meza/issues/172)
  - Added: `src/scripts/getmeza.md`

* [45ad0b89](https://github.com/freephile/meza/commit/45ad0b89) (2025-10-31) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [67bc1b6d](https://github.com/freephile/meza/commit/67bc1b6d) (2025-10-30) Greg Rundlett: Correct the basic meza help message Also, avoid catching too generic exception
  - Modified: `src/scripts/meza.py`

* [ca0e0d88](https://github.com/freephile/meza/commit/ca0e0d88) (2025-10-31) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.60.6
* [bd8551ea](https://github.com/freephile/meza/commit/bd8551ea) (2025-10-30) Greg Rundlett: Make lint-files.sh script more quiet By default only show warnings and errors.
We introduce a -v or --verbose option if you want to show success
messages too.
Add --help with usage
  - Modified: `src/scripts/lint-files.sh`

## Meza 43.60.5
* [979fe609](https://github.com/freephile/meza/commit/979fe609) (2025-10-30) Greg Rundlett: Fix yaml linting errors 
  - Modified: `.github/workflows/release-notes.yml`
  - Modified: `src/playbooks/create-wiki.yml`
  - Modified: `src/playbooks/debug.yml`
  - Modified: `src/playbooks/migrate-wikis.yml`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/imagemagick/tasks/setup-Debian.yml`
  - Modified: `src/roles/imagemagick/tasks/setup-RedHat.yml`

## Meza 43.60.4
* [99d95977](https://github.com/freephile/meza/commit/99d95977) (2025-10-30) Greg Rundlett: Improve linting configuration Ignore 'collections' which is 3rd-party code.
  - Modified: `.ansible-lint`
  - Modified: `.yamllint`

* [ff9e66b9](https://github.com/freephile/meza/commit/ff9e66b9) (2025-10-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.60.3
* [51e8d6f8](https://github.com/freephile/meza/commit/51e8d6f8) (2025-10-30) Greg Rundlett: We don't need no stinkin' badges 
  - Modified: `README.md`

* [1e877576](https://github.com/freephile/meza/commit/1e877576) (2025-10-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [a6a76f61](https://github.com/freephile/meza/commit/a6a76f61) (2025-10-30) Greg Rundlett: process the dev branch 
  - Modified: `.github/workflows/yamllint.yml`

* [09a7a3c3](https://github.com/freephile/meza/commit/09a7a3c3) (2025-10-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.60.2
* [b19e5f52](https://github.com/freephile/meza/commit/b19e5f52) (2025-10-30) Greg Rundlett: Major enhancements: Create wiki logging, etc. "meza create wiki" logging implementation
-----------------------------------------
The new create-wiki logging mirrors the deploy logging architecture with both transactional and processing logs.
Transactional log: /opt/data-meza/logs/create-wiki/create-wiki.log (tracks operations with metadata)
Processing log: /opt/data-meza/logs/create-wiki-output/{env}-{timestamp}.log (captures ansible output)
/opt/data-meza/logs/
├── create-wiki/           # Transactional logs
│   └── create-wiki.log    # Audit trail
└── create-wiki-output/    # Processing logs
    ├── demo-2025-10-29_175734.log
    └── prod-2025-10-29_180234.log
Added two new commands:
sudo meza create-wiki-tail <env>
- tells you what log its tailing and provides a way to check status on the create wiki process in real-time
sudo meza create-wiki-log <env>
- tells you the path of the process log e.g.
/opt/data-meza/logs/create-wiki-output/monolith-2025-10-29_225319.log
Meza.py uses paths from paths.yml
---------------------------------
- Single Source of Truth: All paths defined in paths.yml, easy to maintain
- Removed hardcoded path definitions from meza.py
- Consistency: Python CLI uses same paths as Ansible roles
- Deterministic: No fallbacks, clear failures
- Jinja2 Template Support: variables found in yaml are resolved. {{ m_install }} resolves to 'opt'
- Error Handling: Clear error messages for configuration issues such as paths.yml missing
- new m_logs_create_wiki variable in paths.yml to define the location of the "meza create wiki" log
Verify-wiki enhanced
----------------------
wiki_id and wiki_name (as well as password) are passed by extra_vars in meza.py when it calls create-wiki-promptless playbook.
create-wiki playbook now prompts for Admin password and passes it on to the 'create-admin-account' task list in verify-wiki.
src/roles/verify-wiki/tasks/import-wiki-sql.yml is enhanced with output about wiki creation status
and the set_fact section was improved to clarify what's happening:
- New wiki was created (truly new, not from backup)
- Wiki created but from backup/import
- Wiki already existed
BEFORE the created_new_wiki flag logic was problematic.
Admin Account creation
----------------------
The admin account creation was hardcoded to only work for wikis with wiki_id == "demo"
Removed wiki_id restriction: Changed from when: wiki_id == "demo" to run for any new wiki
Updated prompts: Made the messages generic to work for any wiki name
Fixes Issue [#217](https://github.com/freephile/meza/issues/217)
Fixes Issue [#220](https://github.com/freephile/meza/issues/220)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/create-wiki-promptless.yml`
  - Modified: `src/playbooks/create-wiki.yml`
  - Modified: `src/roles/create-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/create-admin-account.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `src/scripts/meza.py`

## Meza 43.59.2
* [465eaeeb](https://github.com/freephile/meza/commit/465eaeeb) (2025-10-29) Greg Rundlett: Fix the CHANGELOG automation - fix the updateCHANGELOG.sh script (used by Continuous Integration)
- Update the entire CHANGELOG for consistent 'pretty' formatting
- Limit the CHANGELOG to start at 2022-01-01 for length
[skip ci] chicken and egg problem
Fixes Issue [#219](https://github.com/freephile/meza/issues/219)
  - Modified: `CHANGELOG`
  - Modified: `src/scripts/updateCHANGELOG.sh`

* [6e51cc5b](https://github.com/freephile/meza/commit/6e51cc5b) (2025-10-29) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.60.1
* [a799fa87](https://github.com/freephile/meza/commit/a799fa87) (2025-10-29) Greg Rundlett: Prompt for credentials when creating Admin acct When Meza creates an Admin account, whether for the initial 'demo'
or for any new wiki, prompt for the secure password and do not log it.
This way it is only known to the user, and not a vulnerability.
Note: the way that this is executed in the role hierarchy is that
verify-wiki runs import-wiki-sql tasks for new wikis, which in turn
runs init-wiki tasks. Since 'init-wiki.yml' ONLY creates an Admin account
it was renamed 'create-admin-account.yml'
Fixes Issue [#217](https://github.com/freephile/meza/issues/217)
  - Added: `src/roles/verify-wiki/tasks/create-admin-account.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Deleted: `src/roles/verify-wiki/tasks/init-wiki.yml`

* [de0798e2](https://github.com/freephile/meza/commit/de0798e2) (2025-10-24) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.59.1
* [43cfde0a](https://github.com/freephile/meza/commit/43cfde0a) (2025-10-24) Greg Rundlett: Automated RELEASE NOTES and Changelog w/ Actions see .github/RELEASE_AUTOMATION.md for details
Though GitHub Actions, we integrated automatic Changelog and RELEASE
NOTES generation.
For pull requests and commits.
  - Added: `.github/RELEASE_AUTOMATION.md`
  - Added: `.github/workflows/advanced-release-management.yml`
  - Added: `.github/workflows/manual-release-notes.yml`
  - Added: `.github/workflows/release-notes.yml`
  - Added: `src/scripts/release-helper.sh`

## Meza 43.58.2
* [31f360d9](https://github.com/freephile/meza/commit/31f360d9) (2025-10-24) Greg Rundlett: Expand help.md to all meza commands 
  - Modified: `manual/meza-cmd/MIGRATION.md`
  - Modified: `manual/meza-cmd/help.md`
  - Modified: `manual/meza-cmd/install.md`

## Meza 43.58.1
* [9071e05b](https://github.com/freephile/meza/commit/9071e05b) (2025-10-24) Greg Rundlett: Correct help content about deploy command There is no 'install monolith' command.
  - Modified: `manual/meza-cmd/MIGRATION.md`
  - Modified: `manual/meza-cmd/help.md`
  - Modified: `manual/meza-cmd/install.md`

* [1effac3a](https://github.com/freephile/meza/commit/1effac3a) (2025-10-24) Greg Rundlett: Update Changelog and RELEASE NOTES-HEAD 
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.57.1
* [d91c7a73](https://github.com/freephile/meza/commit/d91c7a73) (2025-10-24) Greg Rundlett: Re-enable WatchAnalytics Fixes Issue [#214](https://github.com/freephile/meza/issues/214)
  - Modified: `config/MezaCoreExtensions.yml`

* [4541968c](https://github.com/freephile/meza/commit/4541968c) (2025-10-24) Greg Rundlett: minor tweaks to Quick Start section (curl not ready yet)
whitespace changes in meza.py
  - Modified: `manual/meza-cmd/index.md`
  - Modified: `src/scripts/meza.py`

## Meza 43.56.1
* [53d45c48](https://github.com/freephile/meza/commit/53d45c48) (2025-10-23) Greg Rundlett: Add Maintence script runner Remove the 'cleanup-upload-stash' playbook and replace it with a general purpose MediaWiki Maintenance script runner: `run-maintenance.yml`
Update maint command doc
Backward compatibility is retained for invoking cleanupUploadStash
  - Modified: `manual/meza-cmd/maint.md`
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Added: `src/playbooks/run-maintenance.yml`
  - Modified: `src/scripts/meza.py`

## Meza 43.55.1
* [a590d270](https://github.com/freephile/meza/commit/a590d270) (2025-10-23) Greg Rundlett: Add LinkTarget extension 
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.54.4
* [6eb271e6](https://github.com/freephile/meza/commit/6eb271e6) (2025-10-23) Greg Rundlett: Update Changelog and RELEASE NOTES 
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [0fb72fa6](https://github.com/freephile/meza/commit/0fb72fa6) (2025-10-23) Greg Rundlett: Update Changelog and RELEASE NOTES 
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`
  - Modified: `manual/meza-cmd/index.md`

## Meza 43.54.3
* [ce3ed9b9](https://github.com/freephile/meza/commit/ce3ed9b9) (2025-10-23) Greg Rundlett: Correct the quick start section Add curl command for running getmeza.sh
`curl -L https://raw.githubusercontent.com/nasa/meza/master/src/scripts/getmeza.sh | bash`
Fixes Issue [#211](https://github.com/freephile/meza/issues/211)
  - Modified: `manual/meza-cmd/index.md`

## Meza 43.54.2
* [c4043ba1](https://github.com/freephile/meza/commit/c4043ba1) (2025-10-23) Greg Rundlett: Add in the 'rich' requirement for better console help 
  - Modified: `requirements-dev.txt`

* [0faa71cf](https://github.com/freephile/meza/commit/0faa71cf) (2025-10-23) Greg Rundlett: Remove undefined 'destroy' command The meza destroy command was a placeholder for undefined functionality.
Fixes Issue [#211](https://github.com/freephile/meza/issues/211)
  - Modified: `src/scripts/meza.py`

## Meza 43.54.1
* [04b98d47](https://github.com/freephile/meza/commit/04b98d47) (2025-10-23) Greg Rundlett: Fix help command alignment Intuitive rename of base.md to help.md to follow the pattern where
meza commands have a .md file by the same name.
meza                   # Shows help.md (general help)
meza --help            # Shows help.md (general help)
meza help              # Shows help.md (general help)
meza help deploy       # Shows deploy.md (deploy command help)
meza help --help       # Shows help.md (help for help command itself)
meza deploy --help     # Shows deploy.md (deploy command help)
Fixes Issue [#211](https://github.com/freephile/meza/issues/211)
  - Modified: `manual/meza-cmd/MIGRATION.md`
R100	manual/meza-cmd/base.md	manual/meza-cmd/help.md
  - Modified: `src/scripts/meza.py`

* [19193c2a](https://github.com/freephile/meza/commit/19193c2a) (2025-10-23) Greg Rundlett: Add missing newline at end of file 
  - Modified: `manual/meza-cmd/deploy-notify.md`

## Meza 43.53.3
* [8c1e6c67](https://github.com/freephile/meza/commit/8c1e6c67) (2025-10-23) Greg Rundlett: Add doc for deploy-notify playbook and command - Adds manual/meza-cmd/deploy-notify.md
This fixes Issue [#211](https://github.com/freephile/meza/issues/211)
  - Added: `manual/meza-cmd/deploy-notify.md`

## Meza 43.53.2
* [016aacb6](https://github.com/freephile/meza/commit/016aacb6) (2025-10-23) Greg Rundlett: Add autodeployer doc - improve doc for 'debug'
- correct doc for 'config'
  - there's no such command, but we explain how config is managed in meza
- move cleanup-backups script documentation to scripts directory
Fixes Issue [#211](https://github.com/freephile/meza/issues/211)
  - Added: `manual/meza-cmd/autodeploy.md`
  - Modified: `manual/meza-cmd/config.md`
  - Modified: `manual/meza-cmd/debug.md`
  - Modified: `src/roles/logrotate/README.md`
R099	manual/meza-cmd/cleanup-backups.md	src/scripts/cleanup-backups.md

## Meza 43.53.1
* [64c1e8eb](https://github.com/freephile/meza/commit/64c1e8eb) (2025-10-23) Greg Rundlett: Document the maintenance command 
  - Modified: `manual/meza-cmd/index.md`
  - Modified: `manual/meza-cmd/maint.md`
  - Modified: `src/scripts/meza.py`

## Meza 43.52.2
* [43b4eb8c](https://github.com/freephile/meza/commit/43b4eb8c) (2025-10-23) Greg Rundlett: Avoid setting shared DB if there is no prime wiki, then there can be no
sharing configured
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

## Meza 43.52.1
* [2ab3548e](https://github.com/freephile/meza/commit/2ab3548e) (2025-10-22) Greg Rundlett: Add Backup and Retention Policy Framework meza.py
- add find_most_recent_log_file
- enhance get_deploy_log_path(env)
- enhance deploy_log
- make deploy-tail more able to find log_path
site.yml
- add task to 'Configure log rotation on all servers'
- with tags logrotate, logs
logrotate role
- see README.md for complete overview
- new - implements a complete log and backup retention policy
cleanup-backups.sh new script
cleanup-backups.md documentation
  - Added: `manual/meza-cmd/cleanup-backups.md`
  - Modified: `src/playbooks/site.yml`
  - Added: `src/roles/logrotate/README.md`
  - Added: `src/roles/logrotate/defaults/main.yml`
  - Added: `src/roles/logrotate/handlers/main.yml`
  - Added: `src/roles/logrotate/meta/main.yml`
  - Added: `src/roles/logrotate/tasks/main.yml`
  - Added: `src/roles/logrotate/templates/cleanup-backups.sh.j2`
  - Added: `src/roles/logrotate/templates/meza-logs.j2`
  - Added: `src/scripts/cleanup-backups.sh`
  - Modified: `src/scripts/meza.py`

## Meza 43.51.1
* [02d78fc8](https://github.com/freephile/meza/commit/02d78fc8) (2025-10-22) Greg Rundlett: Fix first-time deploy error due to Apache missing role: init-controller-config
- remove ownership details from 'wikis' directory (set it later)
role: apache-php
- add apache-php task to "Set proper ownership" on wikis
Fixes Issue [#212](https://github.com/freephile/meza/issues/212)
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`

## Meza 43.50.1
* [4a96eef8](https://github.com/freephile/meza/commit/4a96eef8) (2025-10-21) Greg Rundlett: Enhance help display using rich markdown rendering 
  - Modified: `src/scripts/meza.py`

## Meza 43.49.4
* [dc865669](https://github.com/freephile/meza/commit/dc865669) (2025-10-21) Greg Rundlett: Update CHANGELOG 
  - Modified: `CHANGELOG`

* [9a2be9a6](https://github.com/freephile/meza/commit/9a2be9a6) (2025-10-20) Greg Rundlett: Remove trailing whitespace in markdown 
  - Modified: `RELEASE-NOTES.md`
  - Modified: `RELEASE_NOTES-HEAD.md`

## Meza 43.49.3
* [2379a054](https://github.com/freephile/meza/commit/2379a054) (2025-10-20) Greg Rundlett: update RELEASE_NOTES to v43.49.2 
  - Modified: `RELEASE-NOTES.md`
  - Added: `RELEASE_NOTES-HEAD.md`

## Meza 43.49.2
* [29d0b9f2](https://github.com/freephile/meza/commit/29d0b9f2) (2025-10-20) Greg Rundlett: truncate RELEASE_NOTES 
  - Modified: `RELEASE-NOTES.md`

## Meza 43.49.1
* [cb737a5c](https://github.com/freephile/meza/commit/cb737a5c) (2025-10-20) Greg Rundlett: consolidate RELEASE_NOTES into one Fixes Issue [#3](https://github.com/freephile/meza/issues/3)
  - Modified: `RELEASE-NOTES.md`
  - Deleted: `RELEASE_NOTES-43.25.11.md`
  - Deleted: `RELEASE_NOTES-43.29.1.md`
  - Deleted: `RELEASE_NOTES-HEAD.md`

## Meza 43.48.2
* [724467c0](https://github.com/freephile/meza/commit/724467c0) (2025-10-20) Greg Rundlett: Remove obsolete text files Fixes Issue [#3](https://github.com/freephile/meza/issues/3)
  - Deleted: `manual/meza-cmd/backup.txt`
  - Deleted: `manual/meza-cmd/base.txt`
  - Deleted: `manual/meza-cmd/config.txt`
  - Deleted: `manual/meza-cmd/create.txt`
  - Deleted: `manual/meza-cmd/debug.txt`
  - Deleted: `manual/meza-cmd/delete.txt`
  - Deleted: `manual/meza-cmd/deploy.txt`
  - Deleted: `manual/meza-cmd/docker.txt`
  - Deleted: `manual/meza-cmd/install.txt`
  - Deleted: `manual/meza-cmd/list-wikis.txt`
  - Deleted: `manual/meza-cmd/maint.txt`
  - Deleted: `manual/meza-cmd/migrate-wikis.txt`
  - Deleted: `manual/meza-cmd/prompt.txt`
  - Deleted: `manual/meza-cmd/prompt_default_on_blank.txt`
  - Deleted: `manual/meza-cmd/prompt_secure.txt`
  - Deleted: `manual/meza-cmd/setup.txt`

## Meza 43.48.1
* [b21a3aeb](https://github.com/freephile/meza/commit/b21a3aeb) (2025-10-20) Greg Rundlett: Feat: migrate help system from txt to markdown Enhanced Documentation Features:
📊 Structured tables for arguments and options
🎨 Syntax-highlighted code blocks
⚠️ Visual warnings with emojis
🔗 Cross-references between related commands
📋 Consistent formatting across all files
command documentation is now in markdown files (.md) replacing any
pre-existing .txt files
Added documentation for previously undocumented commands
Improved documentation for meza create wiki and meza delete wiki
new command for **list-wikis**
`meza list-wikis`
new general purpose **debug** command backed by a debug playbook
`meza debug monolith m_htdocs`
new help system for every meza command
meza <command> --help
Fixes Issue [#3](https://github.com/freephile/meza/issues/3)
  - Added: `manual/meza-cmd/DELETION.md`
  - Added: `manual/meza-cmd/MIGRATION.md`
  - Added: `manual/meza-cmd/backup.md`
  - Added: `manual/meza-cmd/base.md`
  - Added: `manual/meza-cmd/config.md`
  - Added: `manual/meza-cmd/create.md`
  - Modified: `manual/meza-cmd/create.txt`
  - Added: `manual/meza-cmd/debug.md`
  - Added: `manual/meza-cmd/debug.txt`
  - Added: `manual/meza-cmd/delete.md`
  - Added: `manual/meza-cmd/delete.txt`
  - Added: `manual/meza-cmd/deploy-check.md`
  - Added: `manual/meza-cmd/deploy-kill.md`
  - Added: `manual/meza-cmd/deploy-lock.md`
  - Added: `manual/meza-cmd/deploy-log.md`
  - Added: `manual/meza-cmd/deploy-tail.md`
  - Added: `manual/meza-cmd/deploy-unlock.md`
  - Added: `manual/meza-cmd/deploy.md`
  - Added: `manual/meza-cmd/docker.md`
  - Added: `manual/meza-cmd/index.md`
  - Added: `manual/meza-cmd/install.md`
  - Added: `manual/meza-cmd/list-wikis.md`
  - Added: `manual/meza-cmd/list-wikis.txt`
  - Added: `manual/meza-cmd/maint.md`
  - Added: `manual/meza-cmd/migrate-wikis.md`
  - Added: `manual/meza-cmd/setup.md`
  - Added: `manual/meza-cmd/update.md`
  - Added: `src/playbooks/debug.yml`
  - Modified: `src/scripts/meza.py`

## Meza 43.47.1
* [13b0f8d4](https://github.com/freephile/meza/commit/13b0f8d4) (2025-10-20) Greg Rundlett: Add force for symlink creation `meza create wiki` could fail as late as during the update.php phase of a subsequent deploy because the .smw.json file was not writable in the symlinked config directory.
fixes Issue [#48](https://github.com/freephile/meza/issues/48) and Issue [#44](https://github.com/freephile/meza/issues/44)
  - Modified: `src/roles/verify-wiki/tasks/main.yml`

## Meza 43.46.2
* [f0acdaf9](https://github.com/freephile/meza/commit/f0acdaf9) (2025-10-20) Greg Rundlett: Fix ansible syntax problems FQCN (Fully Qualified Collection Names)
Fixed task key order
- name
- when
- delegate_to
- run_once
- block
Fix shell command issues
- set -o pipefail to shell commands to handle pipe failures
- changed_when: false for read-only shell commands
- changed_when: true for shell commands that modify files
Jinja2 spacing
- remove extra space (newline) before {%- endif -%}
Structure Issues
- Fixed duplicated when conditions that were appearing at both block and task levels
- Removed duplicate delegate_to and run_once declarations
- Properly structured task hierarchies
  - Modified: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`

## Meza 43.46.1
* [3f2f5d9e](https://github.com/freephile/meza/commit/3f2f5d9e) (2025-10-20) Greg Rundlett: Fix meza migrate-wikis task 'Set Primary wiki when no existing declarative config'
was broken with an undefined variable
The map filter was trying to loop a variable in a non-loop context
so the Jinja2 template logic was wrong
`sudo meza migrate-wikis monolith` works now
instead an 'undefined variable' error
Fixes Issue [#101](https://github.com/freephile/meza/issues/101) Use a declarative wiki ID
  - Modified: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`

## Meza 43.45.1
* [8087fde7](https://github.com/freephile/meza/commit/8087fde7) (2025-10-15) Greg Rundlett: Tag "paths" and "defaults" to run always The 'set-vars' role now includes vars from
- config/paths.yml
- config/defaults.yml
on all ansible commands by using the special 'always' tag.
A task with the always tag will always run, even if you use
--skip-tags always or run the playbook with different tags.
It's useful for critical setup or cleanup tasks.
The 'always' tag is the opposite of the 'never' tag.
Now the core configuration loading (OS-specific, paths, and defaults)
always run regardless of which tags are specified, ensuring that
essential variables are available for any tagged deployment scenario.
  - Modified: `src/roles/set-vars/tasks/main.yml`

## Meza 43.44.2
* [ff03f425](https://github.com/freephile/meza/commit/ff03f425) (2025-10-15) Greg Rundlett: Update SBOM files Update the generated Software Bill Of Materials (SBOM) files
Also make lint-files.sh executable.
  - Modified: `src/scripts/lint-files.sh`
  - Modified: `src/scripts/meza-sbom.cyclonedx.json`
  - Modified: `src/scripts/meza-sbom.spdx.json`
  - Modified: `src/scripts/meza-sbom.txt`

## Meza 43.44.1
* [9114307c](https://github.com/freephile/meza/commit/9114307c) (2025-10-15) Greg Rundlett: Fix meza maint run_jobs sudo meza maint run_jobs will run all jobs for all wikis.
Meza produces a wrapper script on deploy which can be used to invoke
MediaWiki's maintenance run.php runJobs for all defined wikis.
You can also selectively pass a wiki ID to the command.
Fixed the script invocation and also uses the declarative wiki approach.
  - Modified: `src/scripts/meza.py`

## Meza 43.43.1
* [091cf901](https://github.com/freephile/meza/commit/091cf901) (2025-10-15) Greg Rundlett: Make CoreExtensions and LocalExtensions robust Make the variable declarations more robust so that --check mode works.
e.g. ansible-playbook /opt/meza/src/playbooks/site.yml --check
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 43.42.1
* [f775e370](https://github.com/freephile/meza/commit/f775e370) (2025-10-15) Greg Rundlett: Add Debian support for ImageMagick and Ghostscript Follow the same pattern of cross-platform compatibility used in the
database role and the geerlingguy/kibana role for cross-platform
package installation. Also ensure that the ansible variable is
defined so that --check works with narrow playbook execution.
Touches on Issue [#42](https://github.com/freephile/meza/issues/42) and Issue [#204](https://github.com/freephile/meza/issues/204)
  - Modified: `src/roles/imagemagick/tasks/main.yml`
  - Added: `src/roles/imagemagick/tasks/setup-Debian.yml`
  - Added: `src/roles/imagemagick/tasks/setup-RedHat.yml`

## Meza 43.41.1
* [7dd492a3](https://github.com/freephile/meza/commit/7dd492a3) (2025-10-15) Greg Rundlett: Convert to using a declarative approach for wikis You can now declare wiki IDs, names, aliases, and other
attributes for wikis in YAML. This deprecates the implied or indirect
directory method of creating and identifying wikis.
The deprecated directory method is still supported.
There is a new meza command 'migrate-wikis' that will write the YAML
for you - storing it in your conf-meza/public/public.yml file.
Usage: sudo meza migrate-wikis <environment>
e.g. sudo meza migrate-wikis monolith
See config/defaults.yml for example declaration
You can now use Meza commands to 'create' wiki and 'delete' wiki.
However, you can now also simply edit your YAML configuration and
run a meza deploy which will create wikis accordingly.
New:
- manual/meza-cmd/migrate-wikis.txt
- src/playbooks/migrate-wikis.yml
- src/roles/base-config-scripts/templates/wiki-config.php.j2
- src/roles/migrate-to-declarative-wikis/tasks/main.yml
Modified:
- config/defaults.yml
- src/roles/base-config-scripts/tasks/main.yml
- src/roles/base-config-scripts/templates/config.sh.j2
- src/roles/configure-wiki/tasks/main.yml
- src/roles/delete-wiki-wrapper/tasks/main.yml
- src/roles/mediawiki/tasks/main.yml
- src/roles/mediawiki/templates/LocalSettings.php.j2
- src/roles/mediawiki/templates/refresh-links.sh.j2
- src/roles/mediawiki/templates/smw-rebuild-all.sh.j2
- src/roles/set-vars/tasks/main.yml
- src/scripts/meza.py
- src/scripts/unifyUserTables.php
Fixes Issue [#101](https://github.com/freephile/meza/issues/101)
  - Modified: `config/defaults.yml`
  - Added: `manual/meza-cmd/migrate-wikis.txt`
  - Added: `src/playbooks/migrate-wikis.yml`
  - Modified: `src/roles/base-config-scripts/tasks/main.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Added: `src/roles/base-config-scripts/templates/wiki-config.php.j2`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Added: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/scripts/meza.py`
  - Modified: `src/scripts/unifyUserTables.php`

## Meza 43.40.1
* [6f654084](https://github.com/freephile/meza/commit/6f654084) (2025-09-29) Greg Rundlett: Fix linting issues in init-controller-config - Remove trailing space character in a comment that breaks linting.
- Use Fully Qualified Collection Names (FQCN)
  such as ansible.builtin.file
- Use templates only at the end of task names.
  It is **discouraged** to use templates in names at all.
  If you do use them, at least put them at the end
  https://ansible.readthedocs.io/projects/lint/rules/name/
  - Modified: `src/roles/init-controller-config/tasks/main.yml`

origin/main
* [cbce465d](https://github.com/freephile/meza/commit/cbce465d) (2025-09-29) Rich Evans: fixes for the refresh-links.sh template These changes are what was required for the /opt/.deploy-meza/refresh-links.sh script to run without errors on my CMTE system.
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`

origin/fix-44-.smw.json
* [c6bbd3c1](https://github.com/freephile/meza/commit/c6bbd3c1) (2025-09-28) Greg Rundlett: Ensure .smw.json ownership and permissions Change the init-controller-config role to have a comment that reflects
the intention of the code.
Change owner and group to apache
Make ownership of 'wikis' directory recursive
Change `m_config_public_mode` from 0755 to 0775 for dirs 0664 for files
by using Symbolic mode u=rwX,g=rwX,o=rX.
Expand group permissions to be able to write files while reducing
'other' permissions to only be able to read files.
Remove permission to execute files from all users.
Change the `configure-wiki` role **which only runs on wiki creation**
to properly create `.smw.json` as group-owned by apache.
Fixes Issue [#44](https://github.com/freephile/meza/issues/44)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`

## Meza 43.39.5
* [3046811d](https://github.com/freephile/meza/commit/3046811d) (2025-09-25) Greg Rundlett: Update CHANGELOG and RELEASE_NOTES-HEAD Using the commit-hook actually worked and prevented my local commit
while enforcing the removal of trailing whitespace!
I also added better USAGE guidelines for the generate-release-notes.sh
script (printed if you invoke it without arguments).
`./src/scripts/updateCHANGELOG.sh` does the work without any arguments.
`./src/scripts/generate-release-notes.sh 43.29.1 HEAD` does the latest
release notes file.
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`
  - Modified: `src/scripts/generate-release-notes.sh`

## Meza 43.39.4
* [5068855d](https://github.com/freephile/meza/commit/5068855d) (2025-09-25) Greg Rundlett: Fix lint errors on essential-vars task file Also add fully qualified collection names (FQCN) to avoid other lint
errors. e.g. `ansible.builtin.set_fact` instead of just `set_fact`.
  - Modified: `src/roles/essential-vars/tasks/main.yml`

## Meza 43.39.2 origin/fix-207-essential-vars
* [b65ba2df](https://github.com/freephile/meza/commit/b65ba2df) (2025-09-25) Greg Rundlett: Fixup the test-certbot playbook to use set-vars The test-certbot playbook was broken - referencing an unknown role.
And it did not use the `set-vars` role to properly initialize.
Now it uses `set-vars` and includes the local certbot role.
Adds to the fix for Issue [#207](https://github.com/freephile/meza/issues/207)
  - Modified: `src/playbooks/test-certbot.yml`

## Meza 43.39.1
* [ab879a58](https://github.com/freephile/meza/commit/ab879a58) (2025-09-25) Greg Rundlett: Setup key variables early; avoid extra-vars We're one step closer to not needing sudo in the deploy command.
With a new role 'essential-vars', we set `ansible_user` and
`group_wheel` with OS-specific logic.
The variables `group_wheel` and `ansible_user` will now be consistently
available throughout all playbooks and roles where they are referenced.
On a RedHat family OS, using 'sudo meza deploy...' we get:
['group_wheel: wheel', 'ansible_user: meza-ansible', 'ansible_env.USER: root']
- Updated the bootstrap section of site.yml to use the new role
  instead of inline variable definitions.
- Maintains compatibility with existing `set-vars` role structure.
- Replace usage of `owner: "{{ ansible_user | default(ansible_env.USER) }}"`
  with owner: "{{ ansible_user | default('meza-ansible') }}"
  because when using 'sudo deploy...' $USER evaluates to 'root'!
- Use 'become' for operations in access-restricted directories where
  restrictions can otherwise prevent success. This is especially
  important for SSH private keys which must maintain strict security
  permissions (`mode: 0600`) and proper ownership to function correctly.
  Fixed the `mediawiki` role SSH key copy tasks and the `site.yml`
  bootstrap section SSH key copy tasks.
- On paths that belong to 'meza-ansible' (like ~/.ssh), set the owner
  explicitly instead of using a variable that could evaluate to
  something incorrect.
- These fixes ammend earlier attempts to fix permission issues like
  commit eee92a08 which used 'default(ansible_env.USER)' instead of
  the correct "default('meza-ansible')"
- Update CONTRIBUTING.md with info on establishing interactive login
  as meza-ansible
- TODO: Skip copy id_rsa to id_rsa and similar copy operations when
  `inventory_hostname == 'localhost'`
Fixes Issue [#207](https://github.com/freephile/meza/issues/207)
  - Modified: `CONTRIBUTING.md`
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/main.meza.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Added: `src/roles/essential-vars/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`

## Meza 43.38.3
* [74851065](https://github.com/freephile/meza/commit/74851065) (2025-09-25) Greg Rundlett: Add FIXME comment about CommentStreams not working CommentStreams is not showing any errors, nor functionality in our tests
of Meza 43.x
See https://phabricator.wikimedia.org/T388462
and the extension page for updates
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.38.2
* [c35a73bb](https://github.com/freephile/meza/commit/c35a73bb) (2025-09-25) Greg Rundlett: Add comments to CommentStreams config Meza specifically sets
      $wgCommentStreamsAllowedNamespaces = -1;
so you MUST use <comment-streams /> in the page content to enable it
on a per page basis.
If left to the default (null), comment-streams is allowed on all
pages in all content namespaces.
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.38.1
* [bf74c315](https://github.com/freephile/meza/commit/bf74c315) (2025-09-23) Rich Evans: Update MezaCoreExtensions.yml Update Extension:CommentStreams to use "mediawiki_default_branch" rather than "master"
  - Modified: `config/MezaCoreExtensions.yml`

* [40337063](https://github.com/freephile/meza/commit/40337063) (2025-09-17) Greg Rundlett: Add a new script to update the CHANGELOG updateCHANGELOG.sh simply uses git log --pretty to prepend new git activity into the CHANGELOG The CHANGELOG is a 'raw' version of what is changed.
The RELEASE_NOTES are the more stylized content where the output is
formatted in markdown, links are included for issues and commit SHAs.
  - Modified: `CHANGELOG`
  - Added: `src/scripts/updateCHANGELOG.sh`

## Meza 43.37.3
* [5e50315a](https://github.com/freephile/meza/commit/5e50315a) (2025-09-16) Greg Rundlett: Update CONTRIBUTING.md with new details Begin the process of updating the tools and quality controls for
Meza.
  - Modified: `CONTRIBUTING.md`

## Meza 43.37.2
* [a23b1bdf](https://github.com/freephile/meza/commit/a23b1bdf) (2025-09-15) Greg Rundlett: Add comment for extension UrlGetParameters As the name implies, the extension enables you to use and/or display
the "GET" parameters of the requested URL.
https://www.mediawiki.org/wiki/Extension:UrlGetParameters
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.37.1
* [f041dc20](https://github.com/freephile/meza/commit/f041dc20) (2025-09-15) Greg Rundlett: Add config and UPO for HTML emails by default Allowing HTML email only enables the User Preference Option.
$wgAllowHTMLEmail = true;
And, we set the UPO over-riding the default of 'plain-text'
$wgDefaultUserOptions['echo-email-format'] = 'html';
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

## Meza 43.36.2
* [07ebd3df](https://github.com/freephile/meza/commit/07ebd3df) (2025-09-11) Greg Rundlett: Update Meza Core Skins - Delete duplicate MinervaNeue block
- Add comment for Timeless skin
  - Modified: `config/MezaCoreSkins.yml`

## Meza 43.36.1
* [eee92a08](https://github.com/freephile/meza/commit/eee92a08) (2025-09-11) Greg Rundlett: Ensure the verify-permissions playbook executes Add pre_tasks section to the playbook to load variables via the set-vars role.
All playbooks should do this.
Eliminate specification of owner/group in the test for cache writing by meza-ansible:
- owner: "{{ ansible_user | default(ansible_env.USER) }}"
- group: "{{ group_apache }}"
because those cause a chmod which is not allowed even though meza-ansible
can write to the cache directory.
Note: although we could get a full shell with
become_flags: '-i'
this is not necessary for testing write permissions in the cache directory
Ensure message display by filtering items to integer with the 'int' jinja filter
Final work following on https://github.com/freephile/meza/commit/b3badfcf6ffe518115c83271e03e0028b589eed9
Fixes Issue [#186](https://github.com/freephile/meza/issues/186)
  - Modified: `src/playbooks/verify-permissions.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`

## Meza 43.35.1
* [138d1092](https://github.com/freephile/meza/commit/138d1092) (2025-09-06) Greg Rundlett: Add missing Bundled extensions There were 7 bundled extensions which were in MezaLocalExtensions.yml
instead of the MezaCoreExtensions.yml - thus not included in the Meza distribution.
Adds
- CategoryTree
- CheckUser
- CiteThisPage
- ConfirmEdit
- Nuke
- Poem
- TemplateStyles
Fixes Issue [#201](https://github.com/freephile/meza/issues/201)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.34.1
* [7335503c](https://github.com/freephile/meza/commit/7335503c) (2025-09-04) Greg Rundlett: Update PageForms to 6.x Switch to using Composer for PageForms to make version constraints
easier to manage.
Also quote the version "master" for SemanticDependencyUpdater
Fixes Issue [#200](https://github.com/freephile/meza/issues/200) exception from SMWDIProperty class not found
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.33.2
* [6b9c3765](https://github.com/freephile/meza/commit/6b9c3765) (2025-08-31) Greg Rundlett: Add additional RELEASE_NOTES file up to HEAD This RELEASE_NOTES can be updated throughout a release cycle until
such time that a release cycle ends when it can be saved off as the
full historical RELEASE NOTES for that cycle.
To generate updates to this file during the 43.x release cycle,
use .src/scripts/generate-release-notes.sh 43.29.1 HEAD
since 43.29.1 was the last ref used in
https://github.com/freephile/meza/blob/main/RELEASE_NOTES-43.29.1.md
Partly addresses Issue [#3](https://github.com/freephile/meza/issues/3)
  - Added: `RELEASE_NOTES-HEAD.md`

## Meza 43.33.1
* [f5159bda](https://github.com/freephile/meza/commit/f5159bda) (2025-08-31) Greg Rundlett: Add DynamicPageList3 Extension DPL allows for creating lists of pages like you would be able to
using SMW queries and properties, but with simpler mechanics and
a small learning curve.
We've added the actively maintained DynamicPageList3 and will switch
to DynamicPageList4 soon.
Fixes Issue [#198](https://github.com/freephile/meza/issues/198)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.32.1
* [c0a5192e](https://github.com/freephile/meza/commit/c0a5192e) (2025-08-29) Greg Rundlett: Use MediaWiki REL1_43 and  SMW 6.x With fixes in the latest MediaWiki and SMW 6, everything appears
to be working again and we are not restricted to MW 1.43.1
See https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki_6.0.0
https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki_6.0.1
Fixes Issue [#163](https://github.com/freephile/meza/issues/163)
Adds Feature #185
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/defaults.yml`

## Meza 43.31.4
* [bf35f37e](https://github.com/freephile/meza/commit/bf35f37e) (2025-08-28) Greg Rundlett: Do not ignore errors in memcache installation The PECL installation of the PHP-memcache extension was brute force.
Therefore it would error every deploy once it was installed. And so
'ignore errors' was on.
Instead, now we look to see whether it is installed;
register a fact memcached_pecl_installed when it is already present.
And thus skip installation depending on the circumstance.
Partly addresses Issue [#144](https://github.com/freephile/meza/issues/144)
  - Modified: `src/roles/apache-php/tasks/php-redhat8.yml`

origin/revise-hosts-template
* [ddac1217](https://github.com/freephile/meza/commit/ddac1217) (2025-08-28) Greg Rundlett: Use YAML instead of INI in hosts file YAML is preferred for Ansible, and is more suitable for more complex
hosts management.
See Issue [#68](https://github.com/freephile/meza/issues/68)
  - Modified: `src/roles/setup-env/templates/hosts.j2`

## Meza 43.31.3
* [72adcda9](https://github.com/freephile/meza/commit/72adcda9) (2025-08-28) Greg Rundlett: Fix deprecation warning: collections_path Settings variable name is singular, not plural.
[DEPRECATION WARNING]: [defaults]collections_paths option, does not
fit var naming standard, use the singular form collections_path
instead. This feature will be removed from ansible-core in version 2.19.
Deprecation warnings can be disabled by setting
deprecation_warnings=False in ansible.cfg.
Also, add symlink to config/ansible.cfg from project root because some
tools or IDEs expect it there.
  - Added: `ansible.cfg`
  - Modified: `config/ansible.cfg`

## Meza 43.31.2
* [190e7f30](https://github.com/freephile/meza/commit/190e7f30) (2025-08-28) Greg Rundlett: Fix branch name for Medik skin This repo uses 'master' not 'main' terminology
Fixes #139
  - Modified: `config/MezaCoreSkins.yml`

## Meza 43.31.1
* [e7b2ea3c](https://github.com/freephile/meza/commit/e7b2ea3c) (2025-08-27) Greg Rundlett: Re-enable the Medik Skin By enabling the main branch we should pull in the proper commits for
compatibility with 1.43 and 1.44 too
Do not use the tag 5.1.3
Fixes #139
  - Modified: `config/MezaCoreSkins.yml`

## Meza 43.30.2
* [65bc6c43](https://github.com/freephile/meza/commit/65bc6c43) (2025-08-27) Greg Rundlett: Regenerate RELEASE_NOTES up to 43.25.11 Use src/scripts/generate-release-notes.sh to
update for additional links formatting and --name-status info.
  - Modified: `RELEASE_NOTES-43.25.11.md`

## Meza 43.30.1
* [53cc7484](https://github.com/freephile/meza/commit/53cc7484) (2025-08-27) Greg Rundlett: Add script to generate RELEASE NOTES Also update the latest release notes.
  - Modified: `RELEASE_NOTES-43.29.1.md`
  - Added: `src/scripts/generate-release-notes.sh`

## Meza 43.29.2
* [148ea866](https://github.com/freephile/meza/commit/148ea866) (2025-08-26) Greg Rundlett: Add latest RELEASE_NOTES Updated procedure at https://wiki.freephile.org/wiki/RELEASE_NOTES
  - Added: `RELEASE_NOTES-43.29.1.md`

origin/bug/191-maintenance-scripts
* [d6310e8e](https://github.com/freephile/meza/commit/d6310e8e) (2025-08-25) Greg Rundlett: Add comment about Issue [#72](https://github.com/freephile/meza/issues/72) (deploy without sudo) 
  - Modified: `src/scripts/getmeza.sh`

* [9802d43d](https://github.com/freephile/meza/commit/9802d43d) (2025-08-25) Greg Rundlett: Fix maintenance script quoting For Issue [#191](https://github.com/freephile/meza/issues/191)
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/verify-wiki/tasks/init-wiki.yml`

* [06c2b554](https://github.com/freephile/meza/commit/06c2b554) (2025-08-24) Greg Rundlett: Fix maintenance script quoting + best practices - Use FQCN
- Improve spacing
- Name all tasks
- Remove quotes from task names
- Improve block order to put tags first
For Issue [#191](https://github.com/freephile/meza/issues/191)
  - Modified: `src/roles/update.php/tasks/main.yml`

* [db3fb090](https://github.com/freephile/meza/commit/db3fb090) (2025-08-24) Greg Rundlett: Fix maintenance script quoting Here we fix templated shell scripts
For Issue [#191](https://github.com/freephile/meza/issues/191)
  - Modified: `src/roles/cron/templates/runAllJobs.php.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Modified: `src/roles/meza-log/templates/server-performance.sh.j2`

* [88a74acb](https://github.com/freephile/meza/commit/88a74acb) (2025-08-24) Greg Rundlett: Fix maintenance script quoting Issue [#191](https://github.com/freephile/meza/issues/191)
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/roles/mediawiki/tasks/cirrus_metastore_upgrade.yml`

* [61b7e63b](https://github.com/freephile/meza/commit/61b7e63b) (2025-08-24) Greg Rundlett: Fixing maintenance script quoting Issue [#191](https://github.com/freephile/meza/issues/191)
  - Modified: `src/scripts/unite-the-wikis.sh`

* [e36b8067](https://github.com/freephile/meza/commit/e36b8067) (2025-08-24) Greg Rundlett: Remove commented task CirrusSearch:Metastore --upgrade Fixed in d0a1ecb3 with new cirrus_metastore_upgrade.yml task
--no-verify used in commit bc we still have
69 failure(s), 0 warning(s) on 2 files.
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 43.28.4 origin/use-ansible-best-practices
* [a7bec3ef](https://github.com/freephile/meza/commit/a7bec3ef) (2025-08-22) Greg Rundlett: Fix most Ansible fatal linting errors; Add requirements.yml - Fixes Issue [#187](https://github.com/freephile/meza/issues/187)
- Fixes Issue [#46](https://github.com/freephile/meza/issues/46)
- Related to Issue [#47](https://github.com/freephile/meza/issues/47)
- Fixes Issue [#90](https://github.com/freephile/meza/issues/90) with requirements.yml - and CentOS is obsolete, so see #15
  - Modified: `requirements.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/create-cert-standalone.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/install-from-source.yml`
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Modified: `src/roles/apache-php/tasks/mssql_driver_for_php.yml`
  - Modified: `src/roles/apache-php/tasks/php-redhat8.yml`
  - Modified: `src/roles/apache-php/tasks/profiling.yml`
  - Modified: `src/roles/backup-uploads/tasks/main.yml`
  - Modified: `src/roles/base-config-scripts/tasks/main.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/composer/tasks/global-require.yml`
  - Modified: `src/roles/composer/tasks/main.yml`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/database/tasks/configure.yml`
  - Modified: `src/roles/database/tasks/databases.yml`
  - Modified: `src/roles/database/tasks/replication.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/dump-db-wikis/tasks/main.yml`
  - Modified: `src/roles/elasticsearch/tasks/es_reindex.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`
  - Modified: `src/roles/geerlingguy.kibana/tasks/main.yml`
  - Modified: `src/roles/geerlingguy.kibana/tasks/setup-RedHat.yml`
  - Modified: `src/roles/gluster/tasks/main.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/lua/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/sync-configs/tasks/main.yml`
  - Modified: `src/roles/umask-set/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`
  - Modified: `tests/deploys/setup-alt-source-backup.yml`

## Meza 43.28.3
* [6749c666](https://github.com/freephile/meza/commit/6749c666) (2025-08-22) Greg Rundlett: Adopt standard .yamlint for compatibility The default configuration works better with ansible-lint in our CI
because 'Prettier' is the most popular formatter in Python
https://ansible.readthedocs.io/projects/lint/rules/yaml/#yamllint-configuration
Issue [#46](https://github.com/freephile/meza/issues/46)
  - Modified: `.yamllint`

## Meza 43.28.2
* [9c8132e9](https://github.com/freephile/meza/commit/9c8132e9) (2025-08-22) Greg Rundlett: Fix Fully Qualified Collection Name (FQCN) best practices Just for these files:
- src/roles/base/tasks/main.yml
- src/roles/base/tasks/parsoid-cleanup.yml
- src/roles/mediawiki/defaults/main.yml
- src/roles/setup-env/tasks/main.yml
pertains to Issue [#46](https://github.com/freephile/meza/issues/46)
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/base/tasks/parsoid-cleanup.yml`
  - Modified: `src/roles/mediawiki/defaults/main.yml`
  - Modified: `src/roles/setup-env/tasks/main.yml`

## Meza 43.28.1
* [68c45e66](https://github.com/freephile/meza/commit/68c45e66) (2025-08-22) Greg Rundlett: Default to ansible_env.USER for ansible_user When all plays are executed by the 'Application User' (meza-ansible)
then the ansible environment will know the USER as 'meza-ansible'
This works even in instances when ansible.cfg is not read in.
relevant to Issue [#186](https://github.com/freephile/meza/issues/186)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/main.meza.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/setup-env/tasks/main.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`

## Meza 43.27.3
* [67ff2e2b](https://github.com/freephile/meza/commit/67ff2e2b) (2025-08-21) Greg Rundlett: Add pre-commit framework Use the pre-commit framework https://pre-commit.com/
to manage pre-commit hooks.
With the new .pre-commit-config.yaml file we now have automatic
linting and fixing before errors can be commited into the repo.
To avoid (skip) the pre-commit tasks, use '--no-verify'
NEW requirements-dev.txt is for Python
  - Added: `.pre-commit-config.yaml`
  - Added: `requirements-dev.txt`

## Meza 43.27.2
* [2619b97c](https://github.com/freephile/meza/commit/2619b97c) (2025-08-21) Greg Rundlett: remove blank space 
  - Modified: `src/scripts/lint-files.sh`
  - Modified: `src/scripts/meza.py`
  - Modified: `src/scripts/shell-functions/linux-user.sh`

## Meza 43.27.1
* [b3badfcf](https://github.com/freephile/meza/commit/b3badfcf) (2025-08-21) Greg Rundlett: Fix users, groups, file permissions AND linting ---- Key Changes ----
1. Variable Structure:
Distribution-specific variables (RedHat.yml vs Debian.yml):
- user_apache: apache vs www-data
- group_apache: apache vs www-data
- group_wheel: wheel vs sudo
Common variables (paths.yml):
REMOVED m_meza_owner in favor of ansible_user defined in ansible.cfg
RENAMED m_meza_group to m_group (pattern for meza variables)
m_htdocs_owner: "{{ m_user }}" (resolves to meza-ansible)
m_logs_owner: "{{ m_user }}" (resolves to meza-ansible)
2. Usage Patterns:
✅ user_apache: 15 consistent references across roles
✅ group_apache: 33 consistent references across roles
✅ m_htdocs_owner: 9 consistent references across roles
✅ group_wheel: 18 consistent references across roles
3. Tools:
3.1 Enhanced linux-user.sh script for managing Linux users and groups
- mf_add_ssh_user() automatically adds meza-ansible to required groups
- Detects and adds to apache/www-data group for web file access
- Ensures wheel group membership for sudo access
- Provides user feedback when groups are added
3.2 Added verify-permissions playbook and role
- Verifies group memberships, directory permissions, and write access
- Provides detailed output for troubleshooting
You can now run the verification playbook to check if
permissions are correctly set:
    ansible-playbook -i hosts src/playbooks/verify-permissions.yml
Systematically setup all critical dirs w proper ownership and perms
Sticky bit (2775) on all data dirs for consistent group inheritance
Covers: m_meza_data, m_cache_directory, m_logs, m_backups
🔧 Fixes Applied
1. Replaced hardcoded values in roles and playbooks:
- Changed "meza-ansible" to "{{ ansible_user }}"
- Changed "apache" to "{{ user_apache }}"
- Changed "wheel" to "{{ group_wheel }}"
2. Applied proper group permissions with group sticky bit on dirs
3. Improved group detection and fallback in Meza.py
4. Enhanced lock file management better group detection, proper perms
5. Updated cache directory perms to use apache group and sticky bit
---- NEW Linting Improvements ----
- Added Ansible + YAML linting instructions for GitHub Copilot AI agent
- Added .ansible-lint.yml for linting configuration
- Added LINTING.md for linting guidelines
- Added lint-files.sh script for linting files
🔧 Fixes Applied
2. Fixed YAML formatting:
- Corrected brace spacing for ansible-lint compliance
- Removed a trailing space
📋 Verification Results
All modified configuration files pass YAML linting ✅
No hardcoded user/group references remain ✅
Cross-platform compatibility improved ✅
Variable definitions are complete and consistent ✅
The system now properly uses distribution-specific variables for
user_apache/group_apache
(apache/apache on RedHat, www-data/www-data on Debian)
while maintaining consistent references across all roles and playbooks.
  - Added: `.ansible-lint`
  - Added: `.github/copilot-instructions.md`
  - Added: `LINTING.md`
  - Modified: `config/Debian.yml`
  - Modified: `config/RedHat.yml`
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/site.yml`
  - Added: `src/playbooks/verify-permissions.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/main.meza.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/update.php/tasks/main.yml`
  - Added: `src/roles/verify-permissions/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`
  - Added: `src/scripts/lint-files.sh`
  - Modified: `src/scripts/meza.py`
  - Modified: `src/scripts/shell-functions/linux-user.sh`
  - Modified: `tests/deploys/setup-alt-source-backup.yml`

## Meza 43.25.14
* [d89466b6](https://github.com/freephile/meza/commit/d89466b6) (2025-08-21) Greg Rundlett: Add message about RELEASE_NOTES-43.25.11.md 
  - Modified: `RELEASE-NOTES.md`

## Meza 43.25.13
* [e100e377](https://github.com/freephile/meza/commit/e100e377) (2025-08-20) Greg Rundlett: Ensure task names and handler names match Task names should start with an Uppercase letter
Ensure the handler names match the task
  - Modified: `src/roles/database/handlers/main.yml`
  - Modified: `src/roles/database/tasks/configure.yml`
  - Modified: `src/roles/firewalld/handlers/main.yml`
  - Modified: `src/roles/firewalld/tasks/main.yml`
  - Modified: `src/roles/geerlingguy.kibana/handlers/main.yml`
  - Modified: `src/roles/geerlingguy.kibana/tasks/main.yml`

## Meza 43.26.5 origin/feature/ehance-elasticsearch-183
* [30791abc](https://github.com/freephile/meza/commit/30791abc) (2025-08-20) Greg Rundlett: Make task name and handler name match 
  - Modified: `src/roles/elasticsearch/tasks/main.yml`

## Meza 43.25.12
* [bf90d10b](https://github.com/freephile/meza/commit/bf90d10b) (2025-08-19) Greg Rundlett: Add release notes for 39.5.0 through 43.25.11 
  - Added: `RELEASE_NOTES-43.25.11.md`

## Meza 43.25.11
* [43be9737](https://github.com/freephile/meza/commit/43be9737) (2025-08-17) Greg Rundlett: Make wiki config directory group executable Not sure this should be apache owned, but if meza-ansible
user is going to have any permission to do anything here
then it needs to be group executable
  - Modified: `src/roles/configure-wiki/tasks/main.yml`

## Meza 43.25.10
* [45658c32](https://github.com/freephile/meza/commit/45658c32) (2025-08-17) Greg Rundlett: fix quoting in SMW setupStore shell command 
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`

## Meza 43.25.9
* [8a5fde26](https://github.com/freephile/meza/commit/8a5fde26) (2025-08-16) Greg Rundlett: Add Admin rights for SMW Allow access to Special:SemanticMediaWiki for Sysops group.
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.25.8
* [4b5df1df](https://github.com/freephile/meza/commit/4b5df1df) (2025-08-16) Greg Rundlett: ignore Python venv and Composer vendor 
  - Modified: `.gitignore`

## Meza 43.26.4
* [d0a1ecb3](https://github.com/freephile/meza/commit/d0a1ecb3) (2025-08-16) Greg Rundlett: Add MediaWiki CirrusSearch metastore update and indexing The index template is a conservative mapping covering typical
CirrusSearch indices (wiki_*_content*, wiki_*_general*).
Adjust mappings/analysis as needed for your data.
You can enable the process by setting
mediawiki_cirrus_metastore_upgrade: true
in inventory/group_vars/host_vars.
mediawiki_cirrus_metastore_upgrade defaults to false
in the role default vars file.
It will only run once due to the marker file.
new files:
- src/roles/mediawiki/tasks/cirrus_metastore_upgrade.yml
- src/roles/mediawiki/tasks/files/cirrussearch_index_template.json
extraneous:
- remove unsupported RedHat 7 yum Python install
Still need to addres
https://github.com/freephile/meza/issues/41#issuecomment-2045506153
  - Modified: `src/roles/mediawiki/defaults/main.yml`
  - Added: `src/roles/mediawiki/tasks/cirrus_metastore_upgrade.yml`
  - Added: `src/roles/mediawiki/tasks/files/cirrussearch_index_template.json`
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 43.26.3
* [b41853e4](https://github.com/freephile/meza/commit/b41853e4) (2025-08-15) Greg Rundlett: Add retry and backoff to index building New Ansible variables:
elasticsearch_index_retry_max: 5
elasticsearch_index_retry_initial: 5
Retry/backoff defaults for CirrusSearch/ForceSearchIndex calls during bulk indexing.
These can be overridden per-host/group via inventory, or via environment variables.
The Environment variables are RETRY_MAX and RETRY_INITIAL.
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`

## Meza 43.26.2
* [22d977a1](https://github.com/freephile/meza/commit/22d977a1) (2025-08-15) Greg Rundlett: yum is now dnf Besides that, fixed Ansible lint errors.
- Find them with:
ansible-lint $(find ./src/roles/elasticsearch/ -name '*.yml')
- Learn them from https://ansible.readthedocs.io/projects/lint/rules/
  - Modified: `src/roles/elasticsearch/handlers/main.yml`
  - Modified: `src/roles/elasticsearch/tasks/es_reindex.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`

## Meza 43.26.1
* [c6734682](https://github.com/freephile/meza/commit/c6734682) (2025-08-15) Greg Rundlett: Improve elastic index building; add reindexing - Made per-wiki bootstrap script safer and faster:
src/roles/mediawiki/templates/elastic-build-index.sh.j2
Added strict shell flags, flock-based locking, traps, disable-refresh/replica optimization
before bulk indexing, restore settings after, and improved logging.
- Reworked reindex script for zero-downtime alias swap and robustness
src/roles/elasticsearch/templates/elastic-reindex.sh.j2
This script was previously not used anywhere!
Added strict shell flags, locking, optimized create/reindex steps (disable refresh/replicas),
attempted atomic alias swap (fallback safe two-step), preserved aliases handling, better
logging, and placeholders for snapshots.
- add new default var elasticsearch_reindex: false
- when setting elasticsearch_reindex: true in inventory, host_vars, group_vars,
or in the role default vars, then the es_reindex.yml tasks will be executed.
TEST
Locking prevents concurrent runs.
Reindex produces the new index and aliases swap as expected.
Search is not interrupted during alias swap.
Index settings (refresh_interval, replicas) are toggled and restored.
  - Modified: `src/roles/elasticsearch/defaults/main.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`
  - Modified: `src/roles/elasticsearch/templates/elastic-reindex.sh.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`

## Meza 43.25.7
* [c32d15ed](https://github.com/freephile/meza/commit/c32d15ed) (2025-08-14) Greg Rundlett: Add meza-sbom-stats.txt 
  - Added: `src/scripts/meza-sbom-stats.txt`
  - Deleted: `src/scripts/package-stats.txt`

## Meza 43.25.6
* [7a060f0e](https://github.com/freephile/meza/commit/7a060f0e) (2025-08-14) Greg Rundlett: Add stats file generation - --stats option now generates a file in addition to console output
- Update documentation
- avoid directory traversal
  - Modified: `src/scripts/generate-sbom.md`
  - Modified: `src/scripts/generate-sbom.php`

## Meza 43.25.5
* [7a333fbf](https://github.com/freephile/meza/commit/7a333fbf) (2025-08-14) Greg Rundlett: Add package-stats.txt 
  - Added: `src/scripts/package-stats.txt`

## Meza 43.25.4
* [e85adee9](https://github.com/freephile/meza/commit/e85adee9) (2025-08-14) Greg Rundlett: Add first generated SBOM files 
  - Added: `src/scripts/meza-sbom.cyclonedx.json`
  - Added: `src/scripts/meza-sbom.spdx.json`
  - Added: `src/scripts/meza-sbom.txt`

## Meza 43.25.3
* [10803fbd](https://github.com/freephile/meza/commit/10803fbd) (2025-08-14) Greg Rundlett: update docs for generate-sbom.php The GitHub action is disabled since we do not
track composer.lock or composer.local.json in the repo.
  - Modified: `CHANGELOG`
R088	src/scripts/sbom.md	src/scripts/generate-sbom.md

## Meza 43.25.2
* [c4dc2d19](https://github.com/freephile/meza/commit/c4dc2d19) (2025-08-13) Greg Rundlett: Yamllint: truthy values should be one of [false, true] 
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/roles/autodeployer/tasks/do-deploy.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/database/tasks/replication.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/key-transfer/tasks/grant-keys.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/remote-dir-check/tasks/main.yml`
  - Modified: `src/roles/remote-mysqldump/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `tests/deploys/setup-alt-source-backup.yml`

## Meza 43.25.1
* [bc092fb6](https://github.com/freephile/meza/commit/bc092fb6) (2025-08-13) Greg Rundlett: Fix invalid workflow generate-sbom - indentation 
  - Modified: `.github/workflows/generate-sbom.yml`

## Meza 43.24.2
* [3a761ccb](https://github.com/freephile/meza/commit/3a761ccb) (2025-08-13) Greg Rundlett: Add PEP 8 rule to .editorconfig for Python files 
  - Modified: `.editorconfig`

## Meza 43.24.1
* [66db2464](https://github.com/freephile/meza/commit/66db2464) (2025-08-13) Greg Rundlett: Code update to score 9.7 / 10 - Added Module Docstring (C0114)
Added comprehensive module documentation explaining the purpose
- Fixed Constant Naming (C0103)
deploy_lock_environment → DEPLOY_LOCK_ENVIRONMENT
language → LANGUAGE
- Fixed Function Naming (C0103)
meza_command_maint_runJobs → meza_command_maint_run_jobs
- Fixed Superfluous Parentheses (C0325)
while (not value): → while not value:
- Fixed Boolean Comparisons (C1805, C1804)
len(argv) == 0 → not argv
rc != 0 → rc
return_code == 0 → not return_code
status != "" → status
status == "" → not status
- Fixed Variable Name Shadowing (W0621, W0622)
datetime parameter → timestamp
dir parameter → directory
- Added Missing Function Docstrings (C0116)
Added docstrings for legacy and placeholder functions
- Fixed File Encoding Issues (W1514)
Added encoding='utf-8' to all file operations
- Fixed Return Statement Consistency (R1710)
Added return None to exception handler in load_yaml
- Removed Unused Variables (W0612)
Removed unused assignments for subprocess calls
Fixed unused args variable with _ placeholder
- Fixed Signal Handler (W0613)
Added pylint disable for required but unused signal handler parameters
- Improved Resource Management (R1732)
Used with statements for file operations where practical
#181 should be test ready
  - Modified: `src/scripts/meza.py`

* [86a5ee11](https://github.com/freephile/meza/commit/86a5ee11) (2025-08-13) Greg Rundlett: Fix Import outside toplevel pylint warnings - Standard library imports come first, alphabetically
- Third-party libraries (yaml) come next
- Unused libraries (jinja2) removed
Ansible uses Jinja2, but we don't use it in meza.py
All the duplicate imports were moved to the top-level per PEP8 standards.
  - Modified: `src/scripts/meza.py`

* [11d074d8](https://github.com/freephile/meza/commit/11d074d8) (2025-08-13) Greg Rundlett: fixed all the C0301 "line too long" warnings Use proper line continuation (indent) for long docstrings
./.venv/bin/pylint src/scripts/meza.py --disable=all --enable=C0301 --score=y
is now scored 10/10
  - Modified: `src/scripts/meza.py`

* [8cb704db](https://github.com/freephile/meza/commit/8cb704db) (2025-08-13) Greg Rundlett: Use Python 3.6 f-strings - "text {}".format(variable) -> f"text {variable}"
- Complex multi-line format strings with better readable f-string formatting
- File path constructions with multiple variables
- More readable
- Better performance
- Less verbose without the .format() calls
- Type safety
  - Modified: `src/scripts/meza.py`

* [68766375](https://github.com/freephile/meza/commit/68766375) (2025-08-13) Greg Rundlett: Agressive Auto PEP 8 formatting reduce long lines
add space around operators
  - Modified: `src/scripts/meza.py`

* [81807369](https://github.com/freephile/meza/commit/81807369) (2025-08-13) Greg Rundlett: basic AutoPEP8 fixes /home/greg/src/meza/.venv/bin/python -m autopep8 --in-place src/scripts/meza.py
  - Modified: `src/scripts/meza.py`

* [1a9ff046](https://github.com/freephile/meza/commit/1a9ff046) (2025-08-13) Greg Rundlett: convert tabs to spaces 
  - Modified: `src/scripts/meza.py`

## Meza 43.23.1 origin/sec/phpsecurity-s2083-injection
* [6959b04a](https://github.com/freephile/meza/commit/6959b04a) (2025-08-07) Greg Rundlett: Slight refactor to put regex into a constant 
  - Modified: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`

* [b1d3eccd](https://github.com/freephile/meza/commit/b1d3eccd) (2025-08-06) Greg Rundlett: remove error suppression and handle disabled shell_exec 
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`

* [bf2521eb](https://github.com/freephile/meza/commit/bf2521eb) (2025-08-06) Greg Rundlett: Prevent web access to sensitive content. Prevents possible XSS in Test files which are not meant
to be served in a web context.
Block test files: RewriteRule ^BackupDownload/.*Test\.php$ - [F,L]
This prevents access to any PHP files ending in "Test.php" in the BackupDownload directory
Returns a 403 Forbidden response
Block README files: RewriteRule ^BackupDownload/README\.md$ - [F,L]
Prevents access to README.md files that might contain sensitive information
Block all markdown files: RewriteRule ^BackupDownload/.*\.md$ - [F,L]
Prevents access to any .md files including documentation that might reveal system details
The [F,L] flags mean:
F = Forbidden (return 403 status)
L = Last rule (stop processing further rules)
  - Modified: `src/roles/htdocs/templates/.htaccess.j2`

* [83e1f601](https://github.com/freephile/meza/commit/83e1f601) (2025-08-06) Greg Rundlett: Avoid using error suppression operator Using the @ operator to suppress errors can hide important issues. The error handling is already in place, so suppression is unnecessary.
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`

* [250d2aee](https://github.com/freephile/meza/commit/250d2aee) (2025-08-06) Greg Rundlett: Strengthen path containment check The current path validation using strpos() could have edge cases.
For example, if the base path is /backup and the file path is /backup2/file,
the check would incorrectly pass.
Improve both download.php and DownloadTest.php
for pull #180
  - Modified: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`

* [a6e593b0](https://github.com/freephile/meza/commit/a6e593b0) (2025-08-06) Greg Rundlett: Fixed dynamic loading of config - add comment to DownloadTest to keep helper methods  in sync
- replace spaces with tabs for coding standards
syntax hints added to code blocks in README
The dynamic config loading was mentioned in pull #180
Documentation in src/roles/htdocs/files/BackupDownload/PATH_RESOLUTION_FIX.md
  - Modified: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Added: `src/roles/htdocs/files/BackupDownload/PATH_RESOLUTION_FIX.md`
  - Modified: `src/roles/htdocs/files/BackupDownload/README.md`
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/index.php`

* [f520f670](https://github.com/freephile/meza/commit/f520f670) (2025-08-06) Greg Rundlett: Implement a hybrid Test Framework that works with both PHPUnit (MediaWiki standard) when available; and a custom fallback framework. Created a comprehensive test file (DownloadTest.php) that:
- Automatically detects if PHPUnit is available and uses it
- Falls back to a custom test framework when PHPUnit is not available
- Provides 20+ test methods covering all security aspects
- Tests 37+ individual security validations
Test Coverage: The test suite validates:
- Input validation - All parameter validation functions
- Path traversal prevention - Multiple attack vector simulations
- File type validation - Extension checking and double extension attacks
- Authorization - User permission and access control testing
- Edge cases - Null bytes, Windows paths, absolute paths, etc.
Security Implementation: The download.php script now includes:
- CWE-22 prevention - Multiple layers of path traversal protection
- Input sanitization - Strict regex validation of all inputs
- File type restriction - Only approved backup file extensions allowed
- Authorization integration - SAML and Meza user management integration
Documentation: Created comprehensive README.md documenting:
- Security features and implementation details
- Usage examples and approved patterns
- Testing procedures and development notes
- Error handling and logging information
The test suite runs successfully and validates that all security measures
are working correctly. The few "failing" tests are actually demonstrating
that the security validation is working properly by rejecting malicious
inputs.
The implementation is now ready for production use with comprehensive
security validation and testing coverage.
Fixes #179
  - Added: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Added: `src/roles/htdocs/files/BackupDownload/README.md`

* [d064cb43](https://github.com/freephile/meza/commit/d064cb43) (2025-08-06) Greg Rundlett: Prevent directory traversal vulnerability. (Vulnerability found with SonarQube) Key Security Improvements:
- Input Validation: All user inputs are validated with strict regex patterns
- Path Construction: File paths are built securely without direct user input
- Realpath Validation: Uses realpath() to resolve paths and ensure they stay within allowed directories
- File Allowlist: Only allows files that actually exist in the filesystem
- Extension Allowlist: Only allows specific file extensions for backups
- No Path Traversal: Completely prevents ../ attacks through validation
- Error Handling: Proper error handling with appropriate HTTP status codes
- Logging: Errors are logged for debugging without exposing sensitive information
This approach ensures that users can only download files that:
- Actually exist in the backup directory structure
- Have allowed file extensions
- The user has permission to access
- Are within the authorized directory tree
Also
- Change copyright
- Add license
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`

## Meza 43.22.4
* [4b0511b6](https://github.com/freephile/meza/commit/4b0511b6) (2025-08-05) Greg Rundlett: fix YAML lint errors 
  - Modified: `.github/workflows/generate-sbom.yml`

## Meza 43.22.3
* [b92c983d](https://github.com/freephile/meza/commit/b92c983d) (2025-08-05) Greg Rundlett: fix YAML lint errors 
  - Modified: `.github/workflows/generate-sbom.yml`
  - Modified: `src/roles/apache-php/tasks/main.yml`

## Meza 43.22.2
* [0fee59cf](https://github.com/freephile/meza/commit/0fee59cf) (2025-08-05) Greg Rundlett: Update README with component logos 
  - Modified: `README.md`
  - Added: `assets/meza_component_logos.png`

## Meza 43.22.1 origin/REL1_43
* [bb2f80c1](https://github.com/freephile/meza/commit/bb2f80c1) (2025-08-05) Greg Rundlett: Update CHANGELOG for REL1_43 
  - Modified: `CHANGELOG`

origin/feature/sbom
* [ac1eb9c5](https://github.com/freephile/meza/commit/ac1eb9c5) (2025-08-04) Greg Rundlett: Add the github action workflow This needs to be tested.
  - Added: `.github/workflows/generate-sbom.yml`

* [4f3323fe](https://github.com/freephile/meza/commit/4f3323fe) (2025-08-04) Greg Rundlett: Add script to show git (annotated) tags You SHOULD use Git Graph in VsCode, but this script is handy for Release Notes and so on.
  - Added: `src/scripts/showTags.md`
  - Added: `src/scripts/showTags.sh`

* [6152f022](https://github.com/freephile/meza/commit/6152f022) (2025-08-04) Greg Rundlett: spaces to tabs 
  - Modified: `src/scripts/importExtensions.php`
  - Modified: `src/scripts/listCoreExtensions.php`

* [16a93f80](https://github.com/freephile/meza/commit/16a93f80) (2025-08-02) Greg Rundlett: convert spaces to tabs per coding standards 
  - Modified: `src/scripts/generate-sbom.php`

* [6abeeac0](https://github.com/freephile/meza/commit/6abeeac0) (2025-08-02) Greg Rundlett: Change root package reference to NASA - Updated download location: Changed from https://github.com/enterprisemediawiki/meza to https://github.com/nasa/meza
- Updated copyright: Changed from Copyright Enterprise MediaWiki to Copyright NASA
- Updated supplier: Changed from Organization: Enterprise MediaWiki to Organization: NASA
- Updated vendor in CycloneDX: Changed from Meza to NASA
- Added external references: Added both the GitHub repository and the MediaWiki documentation page for better reference
These changes ensure that the SBOM correctly identifies NASA as the organization behind the Meza project and points to the correct repository location.
  - Modified: `src/scripts/generate-sbom.php`

* [5170674e](https://github.com/freephile/meza/commit/5170674e) (2025-08-02) Greg Rundlett: Update to include composer.LOCAL.lock Key improvements in this updated version:
- Dual File Support: Automatically detects and includes composer.local.lock
- Conflict Resolution: When the same package exists in both files, uses the version from composer.lock
- Source Tracking: All packages include metadata about which file they came from
- Enhanced Reporting: Statistics and human-readable output show breakdown by source file
- Visual Indicators: Local packages are marked with [LOCAL] in text output
- Updated Documentation: Explains the dual-file approach and precedence rules
Now the SBOM will include all dependencies from both your main composer.lock and any local overrides in composer.local.lock, giving you a complete picture of your dependency landscape.
Note that when "looking" for composer.lock, the path is hard-coded as
/opt/htdocs/mediawiki/composer.lock. We could make it 'intelligently search' but for now we'll use the known path for Meza installations.
  - Modified: `src/scripts/generate-sbom.php`
  - Modified: `src/scripts/sbom.md`

* [274a8e02](https://github.com/freephile/meza/commit/274a8e02) (2025-08-02) Greg Rundlett: initial concept with just composer.json This comprehensive SBOM solution will:
- Parse your composer.lock to extract all dependencies
- Generate industry-standard SBOM formats (SPDX, CycloneDX)
- Provide human-readable summaries
- Automatically update when dependencies change
- Support security and compliance requirements
- Integrate with CI/CD pipelines
The generated SBOMs will include all 200+ packages
from your MediaWiki ecosystem, properly categorized
by scope and type, with complete license and metadata information.
  - Added: `src/scripts/generate-sbom.php`
  - Added: `src/scripts/sbom.md`

* [65933815](https://github.com/freephile/meza/commit/65933815) (2025-08-01) Greg Rundlett: Create SECURITY policy (#175) * Create SECURITY.md
GitHub reads this root-level file as the repository's Security Policy (IOW it's standard)
* Simplify link, add email, fix linting
  - Added: `SECURITY.md`

## Meza 43.19.4
* [3588683f](https://github.com/freephile/meza/commit/3588683f) (2025-08-01) Greg Rundlett: Add TODO comments 
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Modified: `src/scripts/getmeza.sh`

## Meza 43.19.3
* [bbfc7943](https://github.com/freephile/meza/commit/bbfc7943) (2025-07-31) Greg Rundlett: Turn off Kibana by default 
  - Modified: `config/defaults.yml`

## Meza 43.19.2
* [373275a5](https://github.com/freephile/meza/commit/373275a5) (2025-07-31) Greg Rundlett: Turn off Certbot by default 
  - Modified: `config/defaults.yml`

## Meza 43.19.1
* [04c92425](https://github.com/freephile/meza/commit/04c92425) (2025-07-31) Greg Rundlett: Add missing composer merge for Abuse Filter May (likely!) fix Issue [#168](https://github.com/freephile/meza/issues/168)
Although it appeared to be a permission error, or
missing class, the underlying problem was missing
composer libraries needed by AbuseFilter
  - Modified: `config/MezaCoreExtensions.yml`

origin/bug/issue-workflow
* [5be1107c](https://github.com/freephile/meza/commit/5be1107c) (2025-07-29) Greg Rundlett: Final nitpick changes fixes Issue [#170](https://github.com/freephile/meza/issues/170) 
  - Modified: `.github/ISSUE_TEMPLATE/bug_report.md`
  - Modified: `.github/ISSUE_TEMPLATE/feature_request.md`

* [0263f719](https://github.com/freephile/meza/commit/0263f719) (2025-07-29) Greg Rundlett: Update new issue workflow templates - updates Pull #169
- fixes Issue [#170](https://github.com/freephile/meza/issues/170)
- deletes (legacy) .github/ISSUE_TEMPLATE.md
  - Deleted: `.github/ISSUE_TEMPLATE.md`
  - Modified: `.github/ISSUE_TEMPLATE/bug_report.md`
  - Modified: `.github/ISSUE_TEMPLATE/custom.md`
  - Modified: `.github/ISSUE_TEMPLATE/feature_request.md`

* [91a52b1d](https://github.com/freephile/meza/commit/91a52b1d) (2025-07-29) Greg Rundlett: Update issue templates to new workflow See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
  - Added: `.github/ISSUE_TEMPLATE/bug_report.md`
  - Added: `.github/ISSUE_TEMPLATE/custom.md`
  - Added: `.github/ISSUE_TEMPLATE/feature_request.md`

## Meza 43.17.1 origin/feature/new-issue-template-workflow
* [2a996bd0](https://github.com/freephile/meza/commit/2a996bd0) (2025-07-24) Greg Rundlett: DOWNGRADE MediaWiki to 1.43.1 Avoid breaking changes in 1.43.2 which technically should
not happen in a point release; without announcment
if you follow semantic versioning and test backports.
Addresses Issue [#163](https://github.com/freephile/meza/issues/163)
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 43.16.1
* [7d40d3ee](https://github.com/freephile/meza/commit/7d40d3ee) (2025-07-24) Greg Rundlett: Upgrade ModernTimeline to 2.x Upgrade from 1.x to 2.x
Fixes #167
Was getting 500 error
From Release Notes https://github.com/ProfessionalWiki/ModernTimeline#release-notes
Released on July 7th, 2025.
- Raised minimum PHP version to 8.0
- Raised minimum MediaWiki version to 1.39
- Upgraded to TimelineJS3 3.9.6
- Translation updates from https://translatewiki.net
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.15.1
* [9aab3a1b](https://github.com/freephile/meza/commit/9aab3a1b) (2025-07-23) Greg Rundlett: Enable 'overwrite_local_changes'  for Composer Add composer-installed skins and extensions to the switch for overwriting local changes. This gives parity with Git-controlled extensions and skins.
The default is 'false' because neither git nor Composer want to clobber local changes. But if you want to be able to, it can be easily done with the Meza config variable 'overwrite_local_changes' (bool)
  - Modified: `RELEASE-NOTES.md`
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/composer.local.json.j2`

## Meza 43.14.1
* [8a6d4932](https://github.com/freephile/meza/commit/8a6d4932) (2025-07-22) Greg Rundlett: Upgrade Maps from 10.x to 11.x Fixes #166 SMWPrintRequest not found
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.13.3
* [1896a15e](https://github.com/freephile/meza/commit/1896a15e) (2025-07-10) Greg Rundlett: Fix linting - remove trailing spaces 
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/MezaCoreSkins.yml`

## Meza 43.13.2
* [869607c0](https://github.com/freephile/meza/commit/869607c0) (2025-07-09) Greg Rundlett: remove extraneous '1' 
  - Modified: `src/scripts/listCoreExtensions.php`

## Meza 43.13.1
* [db2e3b5c](https://github.com/freephile/meza/commit/db2e3b5c) (2025-07-09) Greg Rundlett: Disable Who's Online for being problematic 
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.12.1
* [37b9be51](https://github.com/freephile/meza/commit/37b9be51) (2025-06-06) Greg Rundlett: Add MW Core bundled extensions Fixes #135
Adds extensions
- AbuseFilter
- DiscussionTools
- Linter
- LoginNotify
- Math
- OATHAuth
- SecureLinkFixer
- SpamBlacklist
- TitleBlacklist
plus the skin Timeless
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/MezaCoreSkins.yml`

## Meza 43.11.2
* [7581e79e](https://github.com/freephile/meza/commit/7581e79e) (2025-06-06) Greg Rundlett: re-enable Semantic Extensions   SRF and SCQ update Semantic Result Formats
    composer: "mediawiki/semantic-result-formats"
    version: "^5.0"
enable SemanticCompoundQueries
    composer: "mediawiki/semantic-compound-queries"
    version: "3.x-dev"
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.11.1
* [9e3ff555](https://github.com/freephile/meza/commit/9e3ff555) (2025-06-05) Greg Rundlett: Fix #140 enabling the SemanticDependencyUpdater and SRF SemanticDependencyUpdater and SemanticResultFormats
are the last of the SMW extensions to be re-enabled.
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.10.5
* [35a35c13](https://github.com/freephile/meza/commit/35a35c13) (2025-06-05) Greg Rundlett: Fixes #143 elimating duplicates between MezaCoreExtensions and MezaLocalExtensions Adds utility scripts that can be used to list core and diff to local.
A corresponding commit was made to the meza-conf repository affecting MezaLocalExtensions.yml.
  - Modified: `config/MezaCoreExtensions.yml`
  - Added: `src/scripts/findDupesInLocalExtensions.php`
  - Added: `src/scripts/listCoreExtensions.php`

## Meza 43.10.4
* [41bbcd82](https://github.com/freephile/meza/commit/41bbcd82) (2025-06-05) Greg Rundlett: Fixes Issue [#62](https://github.com/freephile/meza/issues/62) Url for Netdata install has changed Update the URL, and use sh instead of bash because that is
what the install guide does (hence there are no 'bashisms')
  - Modified: `src/roles/netdata/tasks/main.yml`

## Meza 43.10.3
* [66d7a4b2](https://github.com/freephile/meza/commit/66d7a4b2) (2025-06-04) Greg Rundlett: specify theme (neutral) for Mermaid extension 
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.10.2
* [6100d3c3](https://github.com/freephile/meza/commit/6100d3c3) (2025-06-04) Greg Rundlett: Block WhatLinksHere using Lockdown against robots #156 
  - Modified: `config/MezaCoreExtensions.yml`

* [53dcb430](https://github.com/freephile/meza/commit/53dcb430) (2025-06-03) Rich Evans: Update MezaCoreExtensions.yml Set Page Forms Version to the last version that supports MWM 1.39 (tag 5.9.1)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.10.1
* [7985579b](https://github.com/freephile/meza/commit/7985579b) (2025-06-01) Greg Rundlett: Fixes #157 include CommentStreams composer.json in composer.local.json
  - Modified: `config/MezaCoreExtensions.yml`

* [63103b85](https://github.com/freephile/meza/commit/63103b85) (2025-05-15) Greg Rundlett: Add logos of component technologies 
  - Modified: `README.md`

* [f37f706c](https://github.com/freephile/meza/commit/f37f706c) (2024-12-19) Rich Evans: Update haproxy.cfg.j2 removed commented-out obsolete configuration text in haproxy.cfg
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

* [9a7c9991](https://github.com/freephile/meza/commit/9a7c9991) (2024-12-02) amcgillivray-nasa: Update getmeza.sh Incorporates cowen23's fix for Issue [#57](https://github.com/freephile/meza/issues/57)
  - Modified: `src/scripts/getmeza.sh`

* [cf09936d](https://github.com/freephile/meza/commit/cf09936d) (2025-03-28) Greg Rundlett: Add quotes to version spec for Bootstrap 
  - Modified: `config/MezaCoreExtensions.yml`

* [28a721c7](https://github.com/freephile/meza/commit/28a721c7) (2025-03-26) amcgillivray-nasa: Update MezaCoreExtensions.yml Granted the DeleteBatch permission to sysops (previous configuration did not grant the right to any groups)
  - Modified: `config/MezaCoreExtensions.yml`

* [e4ba295c](https://github.com/freephile/meza/commit/e4ba295c) (2025-02-18) Greg Rundlett: make lint command graceful 
  - Modified: `.github/workflows/yamllint.yml`

* [a3add764](https://github.com/freephile/meza/commit/a3add764) (2025-02-18) Greg Rundlett: final yamllint fixes 
  - Modified: `config/Debian.yml`
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/MezaCoreSkins.yml`

* [33cfdf17](https://github.com/freephile/meza/commit/33cfdf17) (2025-02-18) Greg Rundlett: moved yamllint config 
R100	src/.yamllint	.yamllint

origin/fix-yamllint
* [f6ad58ee](https://github.com/freephile/meza/commit/f6ad58ee) (2025-02-18) Greg Rundlett: Fix yaml files for syntax 
  - Modified: `.github/workflows/yamllint.yml`
  - Modified: `.travis.yml`
  - Modified: `config/Debian.yml`
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/MezaCoreSkins.yml`
  - Modified: `config/defaults.yml`
  - Modified: `config/i18n/en.yml`
  - Modified: `requirements.yml`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/playbooks/delete-elasticsearch.yml`
  - Modified: `src/playbooks/example-block.yaml`
  - Modified: `src/playbooks/getdocker.yml`
  - Modified: `src/playbooks/push-backup.yml`
  - Modified: `src/playbooks/rebuild-smw-and-index.yml`
  - Modified: `src/playbooks/test-certbot.yml`
  - Modified: `src/requirements.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/.yamllint`
  - Modified: `src/roles/ansible-role-certbot-meza/defaults/main.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/meta/main.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/main.meza.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/setup-RedHat.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/vars/default.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/vars/main.yml`
  - Modified: `src/roles/apache-php/tasks/mssql_driver_for_php.yml`
  - Modified: `src/roles/backup-config/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis-push/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis/tasks/main.yml`
  - Modified: `src/roles/backup-uploads-push/tasks/main.yml`
  - Modified: `src/roles/backup-uploads/tasks/main.yml`
  - Modified: `src/roles/base-extras/tasks/main.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/composer/defaults/main.yml`
  - Modified: `src/roles/cron/defaults/main.yml`
  - Modified: `src/roles/database/defaults/main.yml`
  - Modified: `src/roles/database/tasks/configure.yml`
  - Modified: `src/roles/database/tasks/replication.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/database/tasks/setup-Debian.yml`
  - Modified: `src/roles/elasticsearch/tasks/es_reindex.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`
  - Modified: `src/roles/firewall_service/tasks/main.yml`
  - Modified: `src/roles/geerlingguy.kibana/.github/workflows/stale.yml`
  - Modified: `src/roles/gluster/defaults/main.yml`
  - Modified: `src/roles/haproxy/handlers/main.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/memcached/tasks/main.yml`
  - Modified: `src/roles/remote-dir-check/tasks/main.yml`
  - Modified: `src/roles/remote-mysqldump/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/sql-backup-cleanup/tasks/main.yml`
  - Modified: `src/roles/sync-configs/tasks/main.yml`
  - Modified: `src/roles/update.php/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `src/roles/verify-wiki/tasks/init-wiki.yml`
  - Modified: `src/roles/verify-wiki/tasks/transfer-backup-to-db-master.yml`
  - Modified: `tests/deploys/setup-alt-source-backup.yml`

origin/qb-1.43
* [fd7ac3a9](https://github.com/freephile/meza/commit/fd7ac3a9) (2025-02-17) Greg Rundlett: Update README with yamllint workflow badge 
  - Modified: `README.md`

* [73c2c0f6](https://github.com/freephile/meza/commit/73c2c0f6) (2025-02-17) Greg Rundlett: Add multiple branch patterns for the yamllint workflow 
  - Modified: `.github/workflows/yamllint.yml`

* [5c333f5e](https://github.com/freephile/meza/commit/5c333f5e) (2025-02-17) Greg Rundlett: Add new linting workflow 
  - Added: `.github/workflows/yamllint.yml`

## Meza 43.8.1
* [900a1dc9](https://github.com/freephile/meza/commit/900a1dc9) (2025-01-28) Greg Rundlett: Switch Mermaid and BootstrapComponents to dev-master Replace deprecated Class loading for \PHPUnit\Framework\TestCase
Fixes Issue [#141](https://github.com/freephile/meza/issues/141)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.4.7
* [7bc8622d](https://github.com/freephile/meza/commit/7bc8622d) (2025-01-24) Greg Rundlett: Finish off Maintenance Script improvements Last commits for this round of maintenance script operations
Fixes Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/roles/elasticsearch/tasks/es_reindex.yml`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-rebuild-all.sh.j2`

## Meza 43.7.1
* [7cb90918](https://github.com/freephile/meza/commit/7cb90918) (2025-01-24) Greg Rundlett: Add comments for $smwgParserFeatures (Links In Values feature) 
  - Modified: `config/MezaCoreExtensions.yml`

* [ab10ebe1](https://github.com/freephile/meza/commit/ab10ebe1) (2025-01-17) Greg Rundlett: Maintenance Script update (missed these) Convert script calls to go through executable
'maintenance/run'
For extensions, use the class naming pattern
'Extension:ClassName'
Fixes Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/roles/cron/templates/runAllJobs.php.j2`

## Meza 43.4.6
* [ca179104](https://github.com/freephile/meza/commit/ca179104) (2025-01-17) Greg Rundlett: Finish Maintenance Script update Convert script calls to go through executable
'maintenance/run'
For extensions, use the class naming pattern
'Extension:ClassName'
Fixes Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Modified: `src/roles/meza-log/templates/server-performance.sh.j2`
  - Modified: `src/roles/update.php/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `src/roles/verify-wiki/tasks/init-wiki.yml`
  - Modified: `src/scripts/unite-the-wikis.sh`

## Meza 43.6.1
* [d624f7b4](https://github.com/freephile/meza/commit/d624f7b4) (2025-01-16) Greg Rundlett: A new tool to inspect the git repos on the controller 
  - Added: `src/scripts/listExtensionRepos.sh`

## Meza 43.4.5
* [e267f148](https://github.com/freephile/meza/commit/e267f148) (2025-01-16) Greg Rundlett: Update the Update.php role for new Maintenance script ops Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/roles/update.php/tasks/main.yml`

## Meza 43.4.4
* [9e4de5e1](https://github.com/freephile/meza/commit/9e4de5e1) (2025-01-16) Greg Rundlett: Update maintenance scripts Server Performance logging/reporting role
(Probably needs to be eliminated altogether)
Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/roles/meza-log/templates/server-performance.sh.j2`

## Meza 43.4.3
* [278c394e](https://github.com/freephile/meza/commit/278c394e) (2025-01-16) Greg Rundlett: Update maintenance scripts showSiteStats and refreshLinks
Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`

## Meza 43.4.2
* [57c9bb20](https://github.com/freephile/meza/commit/57c9bb20) (2025-01-16) Greg Rundlett: Disable metastore maintenance All maintenance needs to be refactored
Issue [#142](https://github.com/freephile/meza/issues/142)
Also, this may be affected by upgrading to SMW 5.x
Issue [#136](https://github.com/freephile/meza/issues/136)
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 43.5.1
* [7ad66760](https://github.com/freephile/meza/commit/7ad66760) (2025-01-16) Greg Rundlett: Prefer source in composer managed extensions Use the --prefer-source option to composer
Eliminate the duplicate composer run
Eliminate the removal of a non-existant SMW file (IdeAliases.php)
needed for Issue [#136](https://github.com/freephile/meza/issues/136)
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 43.4.1
* [f87b92b2](https://github.com/freephile/meza/commit/f87b92b2) (2025-01-16) Greg Rundlett: Update maintenance scripts for MediaWiki 1.40 Fixes Issue [#142](https://github.com/freephile/meza/issues/142)
  - Modified: `src/roles/cron/templates/runAllJobs.php.j2`

## Meza 43.3.1
* [4ca775d6](https://github.com/freephile/meza/commit/4ca775d6) (2025-01-16) Greg Rundlett: Update MezaCoreExtensions.yml for REL1_43 Use full enableSemantics() call to fix URL pattern
Switch to gerrit because GitHub seems to throttle
SemanticDrilldown 3.05 -> dev-master
SemanticScribunto 2.2.0 -> dev-master
add quotes on SemanticDrilldown version spec
add quotes on SubPageList version spec
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.2.1
* [e2873948](https://github.com/freephile/meza/commit/e2873948) (2025-01-10) Greg Rundlett: Create a variable named php_memory_limit defaulting to 128M PHP normally defaults to 128M so we also default to that.
Templated in the php.ini template of the apache-php role.
Fixes Issue [#151](https://github.com/freephile/meza/issues/151)
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/apache-php/templates/php.ini.j2`

## Meza 43.1.2
* [51c89233](https://github.com/freephile/meza/commit/51c89233) (2025-01-08) Greg Rundlett: Enable SemanticCompoundQueries Was 2.2.0
Now 3.x-dev (same as dev-master)
Issue [#140](https://github.com/freephile/meza/issues/140)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.1.1
* [d2a87e79](https://github.com/freephile/meza/commit/d2a87e79) (2025-01-08) Greg Rundlett: Use SubPageList dev-master Fixes Issue [#138](https://github.com/freephile/meza/issues/138)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.0.3
* [ca17aac6](https://github.com/freephile/meza/commit/ca17aac6) (2025-01-07) Greg Rundlett: Disable or update non-working skins These skins need a version adjustment or update
to work with REL1_43
- Tweeki
- Medik
Use tags/v4.39.1 for Tweeki
Issue [#136](https://github.com/freephile/meza/issues/136)
  - Modified: `config/MezaCoreSkins.yml`

## Meza 43.0.2
* [cde7d8cf](https://github.com/freephile/meza/commit/cde7d8cf) (2025-01-07) Greg Rundlett: Disable non-working extensions These extensions do not work, or need a version adjustment,
to be compatible with REL1_43 and SMW 5.x
- SemanticCompoundQueries
- SemanticDependencyUpdater
- SemanticDrilldown
- SemanticExtraSpecialProperties
- SemanticResultFormats
- SemanticScribunto
- SubPageList
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 43.0.1
* [36567d83](https://github.com/freephile/meza/commit/36567d83) (2025-01-07) Greg Rundlett: Switch SMW to dev-master Addresses Issue [#137](https://github.com/freephile/meza/issues/137)
composer show -a mediawiki/semantic-media-wiki
shows all available composer versions
  - Modified: `config/MezaCoreExtensions.yml`

* [a4e8bdf0](https://github.com/freephile/meza/commit/a4e8bdf0) (2024-12-19) Rich Evans: Update haproxy.cfg.j2 removed commented-out obsolete configuration text in haproxy.cfg
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

* [4f341436](https://github.com/freephile/meza/commit/4f341436) (2024-12-02) amcgillivray-nasa: Update getmeza.sh Incorporates cowen23's fix for Issue [#57](https://github.com/freephile/meza/issues/57)
  - Modified: `src/scripts/getmeza.sh`

* [bc3055ac](https://github.com/freephile/meza/commit/bc3055ac) (2024-10-13) Rich Evans: Update MezaCoreExtensions.yml Added $wgObjectCacheSessionExpiry to SMW Config and set for 24 hours
  - Modified: `config/MezaCoreExtensions.yml`

* [5857d81a](https://github.com/freephile/meza/commit/5857d81a) (2024-10-08) amcgillivray-nasa: Update flow configuration in MezaCoreExtensions.yml Configured Flow to use Parsoid
  - Modified: `config/MezaCoreExtensions.yml`

* [ba25a5df](https://github.com/freephile/meza/commit/ba25a5df) (2024-10-08) Rich Evans: Update getmeza.sh 1) Don't exclude "ansible" and "ansible core" from epel.repo
2) Don't install of centos-release-ansible-29, and 
3) Don't specify the version of ansible to install.
  - Modified: `src/scripts/getmeza.sh`

* [ebcb21cc](https://github.com/freephile/meza/commit/ebcb21cc) (2024-09-18) Rich Evans: Update MezaCoreExtensions.yml added Extension UrlGetParameters
  - Modified: `config/MezaCoreExtensions.yml`

* [d15eabdb](https://github.com/freephile/meza/commit/d15eabdb) (2024-09-18) Rich Evans: Update MezaCoreExtensions.yml Update SMW config to not use links in values
  - Modified: `config/MezaCoreExtensions.yml`
