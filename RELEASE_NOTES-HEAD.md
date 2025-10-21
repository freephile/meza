## Meza Release Notes 43.39.2 → HEAD

### Commits

HEAD -> dev 
## Meza 43.49.2
* [29d0b9f2](https://github.com/freephile/meza/commit/29d0b9f2) (2025-10-20) Greg Rundlett: truncate RELEASE_NOTES 
  - Modified: `RELEASE-NOTES.md`

## Meza 43.49.1 origin/dev
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
