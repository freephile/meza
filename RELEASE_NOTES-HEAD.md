## Meza Release Notes 43.39.3 → HEAD

### Commits

HEAD -> dev
## Meza 43.54.3 origin/dev
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

origin/main origin/HEAD nasa/main main
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
