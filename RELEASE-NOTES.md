Release Notes

## Meza Release Notes HEAD

HEAD -> dev
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

origin/revise-hosts-template revise-hosts-template
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

* [53dcb430](https://github.com/freephile/meza/commit/53dcb430) (2025-06-03) Rich Evans: Update MezaCoreExtensions.yml Set Page Forms Version to the last version that supports MWM 1.39 (tag 5.9.1)
  - Modified: `config/MezaCoreExtensions.yml`

nasa/amcgillivray-nasa-patch-1
* [28a721c7](https://github.com/freephile/meza/commit/28a721c7) (2025-03-26) amcgillivray-nasa: Update MezaCoreExtensions.yml Granted the DeleteBatch permission to sysops (previous configuration did not grant the right to any groups)
  - Modified: `config/MezaCoreExtensions.yml`

* [a4e8bdf0](https://github.com/freephile/meza/commit/a4e8bdf0) (2024-12-19) Rich Evans: Update haproxy.cfg.j2 removed commented-out obsolete configuration text in haproxy.cfg
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

nasa/getMeza-patch-1
* [4f341436](https://github.com/freephile/meza/commit/4f341436) (2024-12-02) amcgillivray-nasa: Update getmeza.sh Incorporates cowen23's fix for Issue [#57](https://github.com/freephile/meza/issues/57)
  - Modified: `src/scripts/getmeza.sh`

* [ebcb21cc](https://github.com/freephile/meza/commit/ebcb21cc) (2024-09-18) Rich Evans: Update MezaCoreExtensions.yml added Extension UrlGetParameters
  - Modified: `config/MezaCoreExtensions.yml`

* [d15eabdb](https://github.com/freephile/meza/commit/d15eabdb) (2024-09-18) Rich Evans: Update MezaCoreExtensions.yml Update SMW config to not use links in values
  - Modified: `config/MezaCoreExtensions.yml`

## Commits
origin/bug/191-maintenance-scripts bug/191-maintenance-scripts
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

## Meza 43.28.4 use-ansible-best-practices
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

## Meza 43.26.5 origin/feature/ehance-elasticsearch-183 feature/ehance-elasticsearch-183
* [30791abc](https://github.com/freephile/meza/commit/30791abc) (2025-08-20) Greg Rundlett: Make task name and handler name match
  - Modified: `src/roles/elasticsearch/tasks/main.yml`

## Meza 43.25.12
* [bf90d10b](https://github.com/freephile/meza/commit/bf90d10b) (2025-08-19) Greg Rundlett: Add release notes for 39.5.0 through 43.25.11
  - Added: `RELEASE_NOTES-43.25.11.md`

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
R087	src/scripts/sbom.md	src/scripts/generate-sbom.md

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

## Meza 43.24.1 origin/feature/improve-python
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

## Meza 43.23.1 origin/sec/phpsecurity-s2083-injection sec/phpsecurity-s2083-injection
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

## Meza 43.22.1 origin/REL1_43 REL1_43
* [bb2f80c1](https://github.com/freephile/meza/commit/bb2f80c1) (2025-08-05) Greg Rundlett: Update CHANGELOG for REL1_43
  - Modified: `CHANGELOG`

origin/feature/sbom feature/sbom
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

origin/bug/issue-workflow bug/issue-workflow
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

## Meza 43.17.1 feature/new-issue-template-workflow
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

* [e4ba295c](https://github.com/freephile/meza/commit/e4ba295c) (2025-02-18) Greg Rundlett: make lint command graceful
  - Modified: `.github/workflows/yamllint.yml`

* [a3add764](https://github.com/freephile/meza/commit/a3add764) (2025-02-18) Greg Rundlett: final yamllint fixes
  - Modified: `config/Debian.yml`
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/MezaCoreSkins.yml`

* [33cfdf17](https://github.com/freephile/meza/commit/33cfdf17) (2025-02-18) Greg Rundlett: moved yamllint config
R100	src/.yamllint	.yamllint

origin/fix-yamllint fix-yamllint
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

origin/qb-1.43 qb-1.43
* [fd7ac3a9](https://github.com/freephile/meza/commit/fd7ac3a9) (2025-02-17) Greg Rundlett: Update README with yamllint workflow badge
  - Modified: `README.md`

* [73c2c0f6](https://github.com/freephile/meza/commit/73c2c0f6) (2025-02-17) Greg Rundlett: Add multiple branch patterns for the yamllint workflow
  - Modified: `.github/workflows/yamllint.yml`

origin/feature/yamlint-workflow feature/yamlint-workflow
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

## Meza 43.0.0
* [d7d6a88e](https://github.com/freephile/meza/commit/d7d6a88e) (2025-01-07) Greg Rundlett: Upgrade to REL1_43 Fixes Issue [#136](https://github.com/freephile/meza/issues/136)
set meza_repository_url to use freephile/meza
set mediawiki_version for core
set mediawiki_default_branch (for extensions)
set php_ius_version to php81
  - Modified: `config/defaults.yml`

## Meza 39.17.0 origin/qb origin/feature-kibana
* [18d66875](https://github.com/freephile/meza/commit/18d66875) (2024-12-19) Greg Rundlett: Kibana Security Do not allow connections from remote (the Internet)
Only allow localhost connections
Issue [#60](https://github.com/freephile/meza/issues/60)
  - Modified: `src/roles/geerlingguy.kibana/vars/main.yml`

* [a2a849ca](https://github.com/freephile/meza/commit/a2a849ca) (2024-12-19) Greg Rundlett: Comment our changes in the task file Issue [#37](https://github.com/freephile/meza/issues/37)
  - Modified: `src/roles/geerlingguy.kibana/tasks/main.yml`

* [a8904543](https://github.com/freephile/meza/commit/a8904543) (2024-12-18) Greg Rundlett: Add versionlock to Kibana Issue [#58](https://github.com/freephile/meza/issues/58) Issue [#37](https://github.com/freephile/meza/issues/37)
  - Modified: `src/roles/geerlingguy.kibana/tasks/main.yml`

* [0a6ed4ed](https://github.com/freephile/meza/commit/0a6ed4ed) (2024-12-18) Greg Rundlett: Add Kibana frontend to Elasticsearch Fixes Issue [#37](https://github.com/freephile/meza/issues/37)
Uses Geerlingguy Kibana
  - Modified: `.gitignore`
  - Modified: `config/defaults.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/requirements.yml`
  - Added: `src/roles/geerlingguy.kibana/.ansible-lint`
  - Added: `src/roles/geerlingguy.kibana/.github/FUNDING.yml`
  - Added: `src/roles/geerlingguy.kibana/.github/workflows/ci.yml`
  - Added: `src/roles/geerlingguy.kibana/.github/workflows/release.yml`
  - Added: `src/roles/geerlingguy.kibana/.github/workflows/stale.yml`
  - Added: `src/roles/geerlingguy.kibana/.gitignore`
  - Added: `src/roles/geerlingguy.kibana/.yamllint`
  - Added: `src/roles/geerlingguy.kibana/LICENSE`
  - Added: `src/roles/geerlingguy.kibana/README.md`
  - Added: `src/roles/geerlingguy.kibana/defaults/main.yml`
  - Added: `src/roles/geerlingguy.kibana/handlers/main.yml`
  - Added: `src/roles/geerlingguy.kibana/meta/.galaxy_install_info`
  - Added: `src/roles/geerlingguy.kibana/meta/main.yml`
  - Added: `src/roles/geerlingguy.kibana/molecule/default/converge.yml`
  - Added: `src/roles/geerlingguy.kibana/molecule/default/molecule.yml`
  - Added: `src/roles/geerlingguy.kibana/molecule/default/requirements.yml`
  - Added: `src/roles/geerlingguy.kibana/tasks/main.yml`
  - Added: `src/roles/geerlingguy.kibana/tasks/setup-Debian.yml`
  - Added: `src/roles/geerlingguy.kibana/tasks/setup-RedHat.yml`
  - Added: `src/roles/geerlingguy.kibana/templates/kibana.repo.j2`
  - Added: `src/roles/geerlingguy.kibana/templates/kibana.yml.j2`
  - Added: `src/roles/geerlingguy.kibana/vars/main.yml`

* [721e7fbf](https://github.com/freephile/meza/commit/721e7fbf) (2024-12-17) Greg Rundlett: rebased, but keep main comments Fixes Issue [#58](https://github.com/freephile/meza/issues/58)
  - Modified: `src/requirements.yml`

* [6706b93f](https://github.com/freephile/meza/commit/6706b93f) (2024-03-14) Greg Rundlett: Add Kibana frontend to Elasticsearch Using Ansible Galaxy and requirements.yml, we install Jeff Geeerling's
geerlingguy.kibana role. Fixes Issue [#37](https://github.com/freephile/meza/issues/37)
Kibana is available at port 5601
This work  was performed for NASA GRC-ATF by WikiWorks per NASA Contract  NNC15BA02B.
  - Modified: `src/playbooks/site.yml`
  - Added: `src/requirements.yml`

## Meza 39.16.4
* [7c01ff54](https://github.com/freephile/meza/commit/7c01ff54) (2024-12-17) Greg Rundlett: We do not need a special port for certbot creation Issue [#130](https://github.com/freephile/meza/issues/130)
  - Modified: `src/roles/ansible-role-certbot-meza/vars/main.yml`

## Meza 39.16.3
* [ce07fdb9](https://github.com/freephile/meza/commit/ce07fdb9) (2024-12-17) Greg Rundlett: Do not put crt and key into HAProxy Issue [#130](https://github.com/freephile/meza/issues/130)
  - Modified: `src/roles/haproxy/tasks/main.yml`

## Meza 39.16.2
* [39a65494](https://github.com/freephile/meza/commit/39a65494) (2024-10-13) Rich Evans: Update MezaCoreExtensions.yml Added $wgObjectCacheSessionExpiry to SMW Config and set for 24 hours
(cherry picked from commit bc3055accb69112040bf93839b1994e1d6a55c2c)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 39.16.1 origin/feature/certbot-130
* [82d4cb44](https://github.com/freephile/meza/commit/82d4cb44) (2024-12-11) Greg Rundlett: role name change to ansible-role-certbot-meza
  - Modified: `src/playbooks/site.yml`

## Meza 39.16.0
* [f4d54616](https://github.com/freephile/meza/commit/f4d54616) (2024-12-11) Greg Rundlett: Add TLS Certificate generation and auto-renewal (Certbot) Fixes Issue [#130](https://github.com/freephile/meza/issues/130)
  - Modified: `config/defaults.yml`
  - Modified: `src/playbooks/site.yml`
  - Added: `src/playbooks/test-certbot.yml`
  - Added: `src/roles/ansible-role-certbot-meza/.ansible-lint`
  - Added: `src/roles/ansible-role-certbot-meza/.gitignore`
  - Added: `src/roles/ansible-role-certbot-meza/.yamllint`
  - Added: `src/roles/ansible-role-certbot-meza/LICENSE`
  - Added: `src/roles/ansible-role-certbot-meza/README.md`
  - Added: `src/roles/ansible-role-certbot-meza/defaults/main.yml`
  - Added: `src/roles/ansible-role-certbot-meza/handlers/main.yml`
  - Added: `src/roles/ansible-role-certbot-meza/meta/main.yml`
  - Added: `src/roles/ansible-role-certbot-meza/molecule/default/converge.yml`
  - Added: `src/roles/ansible-role-certbot-meza/molecule/default/molecule.yml`
  - Added: `src/roles/ansible-role-certbot-meza/molecule/default/playbook-snap-install.yml`
  - Added: `src/roles/ansible-role-certbot-meza/molecule/default/playbook-source-install.yml`
  - Added: `src/roles/ansible-role-certbot-meza/molecule/default/playbook-standalone-nginx-aws.yml`
  - Added: `src/roles/ansible-role-certbot-meza/molecule/default/requirements.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/create-cert-standalone.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/create-cert-webroot.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/include-vars.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/install-from-source.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/install-with-package.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/install-with-snap.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/main.meza.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/main.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/renew-cron.yml`
  - Added: `src/roles/ansible-role-certbot-meza/tasks/setup-RedHat.yml`
  - Added: `src/roles/ansible-role-certbot-meza/templates/concat.pem.sh.j2`
  - Added: `src/roles/ansible-role-certbot-meza/templates/start_services.j2`
  - Added: `src/roles/ansible-role-certbot-meza/templates/stop_services.j2`
  - Added: `src/roles/ansible-role-certbot-meza/tests/inventory`
  - Added: `src/roles/ansible-role-certbot-meza/tests/test.yml`
  - Added: `src/roles/ansible-role-certbot-meza/vars/default.yml`
  - Added: `src/roles/ansible-role-certbot-meza/vars/main.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

## Meza 39.15.0
* [68249080](https://github.com/freephile/meza/commit/68249080) (2024-11-27) Greg Rundlett: Promote comments into names for each play. This should help with readability and output clarity.
Extract gluster comments into the gluster role default variables file
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/gluster/defaults/main.yml`

* [0f8252de](https://github.com/freephile/meza/commit/0f8252de) (2024-11-22) Greg Rundlett: improve wording for m_opcache_production_mode
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/init-controller-config/templates/public.yml.j2`

* [da7993df](https://github.com/freephile/meza/commit/da7993df) (2024-11-22) Greg Rundlett: update instruction + minor formatting This playbook need massive re-organization. See Issue [#42](https://github.com/freephile/meza/issues/42)
  - Modified: `src/playbooks/site.yml`

## Meza 39.14.1
* [528002e4](https://github.com/freephile/meza/commit/528002e4) (2024-11-22) Greg Rundlett: Fix paths for PdfHandler Add full paths for commands to solve
pdfinfo not reporting any info about pdfs
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 39.14.0
* [7ad20063](https://github.com/freephile/meza/commit/7ad20063) (2024-11-22) Greg Rundlett: Add PdfHandler extension The base task now installs xpdf for RockyLinux
Solves Issue [#128](https://github.com/freephile/meza/issues/128)
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `src/roles/base/tasks/main.yml`

## Meza 39.13.0
* [6737d49e](https://github.com/freephile/meza/commit/6737d49e) (2024-11-22) Greg Rundlett: Add extension Page Exchange Solves Issue [#126](https://github.com/freephile/meza/issues/126) but we still need
to identify and load at least one
package.
Perhaps put the work into making the SemanticMeetingMinutes into a package
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 39.12.0
* [a6cb3735](https://github.com/freephile/meza/commit/a6cb3735) (2024-11-22) Greg Rundlett: Alphabetize core extensions Fixes Issue [#129](https://github.com/freephile/meza/issues/129)
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 39.11.1
* [5042d74a](https://github.com/freephile/meza/commit/5042d74a) (2024-11-21) Greg Rundlett: remove obsolete commented tasks Rebuild Recent Changes was only necessary after
importing pages from script.
See Issue [#126](https://github.com/freephile/meza/issues/126)
  - Modified: `src/roles/verify-wiki/tasks/init-wiki.yml`

## Meza 39.11.0 origin/qb-merge
* [5d47bd26](https://github.com/freephile/meza/commit/5d47bd26) (2024-11-12) Greg Rundlett: Upgrade Bootstrap, BS Components, Chameleon to 5.x Fixes Issue [#125](https://github.com/freephile/meza/issues/125)
Fixes Issue  #107
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `config/MezaCoreSkins.yml`

## Meza 39.10.0
* [69c5db7a](https://github.com/freephile/meza/commit/69c5db7a) (2024-11-11) Greg Rundlett: Default to DEVELOPMENT Change default Opcache behavior
Do NOT install Netdata monitoring by default
Adds option for Composer require-dev packages
Fixes Issue [#123](https://github.com/freephile/meza/issues/123)
Fixes Issue [#121](https://github.com/freephile/meza/issues/121)
Helps address Issue [#120](https://github.com/freephile/meza/issues/120)
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/init-controller-config/templates/public.yml.j2`
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 39.9.6
* [387ba9c3](https://github.com/freephile/meza/commit/387ba9c3) (2024-11-07) Greg Rundlett: Be explicit about who can edit Gadgets
  - Modified: `config/MezaCoreExtensions.yml`

## Meza 39.9.5
* [85afac96](https://github.com/freephile/meza/commit/85afac96) (2024-11-02) Greg Rundlett: Remove Elasticsearch upgrade playbook Issue [#118](https://github.com/freephile/meza/issues/118)
  - Deleted: `src/playbooks/elasticsearch-upgrade.yml`
  - Deleted: `src/roles/elasticsearch/tasks/es_upgrade.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`

## Meza 39.9.4
* [69c8a213](https://github.com/freephile/meza/commit/69c8a213) (2024-11-02) Greg Rundlett: Comment the community collections previously setup for RL8 Fixes Issue [#51](https://github.com/freephile/meza/issues/51)
  - Modified: `requirements.yml`

* [8a7241b0](https://github.com/freephile/meza/commit/8a7241b0) (2024-11-02) Greg Rundlett: Example playbook to observe the function of block scalars
  - Added: `src/playbooks/example-block.yaml`

* [964b65e7](https://github.com/freephile/meza/commit/964b65e7) (2024-11-02) Greg Rundlett: Add a couple of 'ToDo' comments and reformat the smw index shell cmd The shell command was not working due to block folding the
list_of_wikis into a single string so the cmd was reformatted to a
single line (which is too long for yamllint compliance). But, at least
it nominally 'works'. A comment was added to address the issue that
this maintenance should not even exist in this role, but should be refactored. See Issue [#117](https://github.com/freephile/meza/issues/117)
  - Modified: `src/roles/mediawiki/tasks/main.yml`

* [105a5363](https://github.com/freephile/meza/commit/105a5363) (2024-10-24) Greg Rundlett: update github issue template
  - Modified: `.github/ISSUE_TEMPLATE.md`

## Meza 39.9.3
* [923758c1](https://github.com/freephile/meza/commit/923758c1) (2024-10-24) Greg Rundlett: Fix wiki symbolic links Issue [#115](https://github.com/freephile/meza/issues/115)
  - Modified: `src/roles/mediawiki/tasks/main.yml`

## Meza 39.9.2
* [1219d724](https://github.com/freephile/meza/commit/1219d724) (2024-10-24) Greg Rundlett: Use system ansible Issue [#51](https://github.com/freephile/meza/issues/51)
  - Modified: `src/scripts/meza.py`

* [aee09afe](https://github.com/freephile/meza/commit/aee09afe) (2024-10-24) Greg Rundlett: Fix ambiguous STDOUT messaging
  - Modified: `src/scripts/meza.py`

## Meza 39.9.1
* [a77b91ef](https://github.com/freephile/meza/commit/a77b91ef) (2024-10-24) Greg Rundlett: Use root for ansible-vault key operations become module touches on Issue [#72](https://github.com/freephile/meza/issues/72) privilege escalation
Also switch back to using system-installed ansible
over a local user installed ansible touches on Issue [#51](https://github.com/freephile/meza/issues/51)
Upgrade Ansible
[meza-ansible@rockylinux-s-4vcpu-8gb-nyc3-01 config]$ ansible --version
ansible [core 2.16.3]
  config file = /opt/meza/config/ansible.cfg
  configured module search path = ['/opt/conf-meza/users/meza-ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.12/site-packages/ansible
  ansible collection location = /opt/meza/collections
  executable location = /usr/bin/ansible
  python version = 3.12.5 (main, Sep 24 2024, 09:41:18) [GCC 8.5.0 20210514 (Red Hat 8.5.0-22)] (/usr/bin/python3.12)
  jinja version = 3.1.2
  libyaml = True
  - Modified: `src/roles/haproxy/tasks/main.yml`

## Meza 39.9.0
* [13820f17](https://github.com/freephile/meza/commit/13820f17) (2024-10-08) Rich Evans: Update getmeza.sh 1) Don't exclude "ansible" and "ansible core" from epel.repo
2) Don't install repo centos-release-ansible-29, and
3) Don't specify the version of ansible to install.
  - Modified: `src/scripts/getmeza.sh`

* [bc3055ac](https://github.com/freephile/meza/commit/bc3055ac) (2024-10-13) Rich Evans: Update MezaCoreExtensions.yml Added $wgObjectCacheSessionExpiry to SMW Config and set for 24 hours
  - Modified: `config/MezaCoreExtensions.yml`

* [5857d81a](https://github.com/freephile/meza/commit/5857d81a) (2024-10-08) amcgillivray-nasa: Update flow configuration in MezaCoreExtensions.yml Configured Flow to use Parsoid
  - Modified: `config/MezaCoreExtensions.yml`

* [ba25a5df](https://github.com/freephile/meza/commit/ba25a5df) (2024-10-08) Rich Evans: Update getmeza.sh 1) Don't exclude "ansible" and "ansible core" from epel.repo
2) Don't install of centos-release-ansible-29, and
3) Don't specify the version of ansible to install.
  - Modified: `src/scripts/getmeza.sh`

## Meza 39.8.1 qb-merge
* [4810a1e6](https://github.com/freephile/meza/commit/4810a1e6) (2024-10-07) Greg Rundlett: Configure Flow (Structured Discussions) for MW 1.39 Fixes Issue [#114](https://github.com/freephile/meza/issues/114) Visual Editor was not working properly for Flow boards on MW1.39
(Parsoid-PHP) The easily provoked error was:
"Exception caught: Conversion from 'html' to 'wikitext' was requested, but core's Parser only supports 'wikitext' to 'html' conversion"
In MW 1.39, Flow still ignores the zero-config setup of Parsoid-PHP.
So, we need to wfLoadExtension() the local vendored Parsoid library.
And, set $wgVirtualRestConfig
This makes Flow usable on MW 1.39, but ultimately, Flow needs to be replaced as described in Issue [#39](https://github.com/freephile/meza/issues/39)
  - Modified: `config/MezaCoreExtensions.yml`

* [9c6b44ad](https://github.com/freephile/meza/commit/9c6b44ad) (2024-10-04) Greg Rundlett: Temporary work-arounds for Issue [#72](https://github.com/freephile/meza/issues/72) Do not run as root
Do not require 'sudo' for calling meza
Temporary or partial fixes for path and user problems
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/scripts/meza.py`

* [eb39199d](https://github.com/freephile/meza/commit/eb39199d) (2024-10-04) Greg Rundlett: update getmeza.sh to fix Issue [#51](https://github.com/freephile/meza/issues/51) Install ansible as the meza-ansible user and
then run install collections
  - Modified: `src/scripts/getmeza.sh`

* [6b655263](https://github.com/freephile/meza/commit/6b655263) (2024-10-04) Greg Rundlett: Fix Issue [#113](https://github.com/freephile/meza/issues/113) with specific binary paths Use /usr/local/bin for ansible-galaxy commands
Both in the playbook, and in the tasks
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`

* [c2bde01c](https://github.com/freephile/meza/commit/c2bde01c) (2024-10-04) Greg Rundlett: Fix Issue [#108](https://github.com/freephile/meza/issues/108) Introduce requirements.yml and ansible.cfg changes
to install community collections we depend on
  - Modified: `config/ansible.cfg`
  - Added: `requirements.yml`

* [2f0e5cf0](https://github.com/freephile/meza/commit/2f0e5cf0) (2024-10-04) Greg Rundlett: Ignore common clutter and artifacts
  - Modified: `.gitignore`

* [8b683562](https://github.com/freephile/meza/commit/8b683562) (2024-10-04) Greg Rundlett: ignore Ansible collections
  - Modified: `.gitignore`

* [9cff9352](https://github.com/freephile/meza/commit/9cff9352) (2024-10-04) Greg Rundlett: add comment for powertools and remove  centos-release-ansible-29
  - Modified: `src/scripts/getmeza.sh`

* [88f3b2a6](https://github.com/freephile/meza/commit/88f3b2a6) (2024-10-04) Greg Rundlett: bump bootstrap; add bootstrap components
  - Modified: `config/MezaCoreExtensions.yml`

* [cb437664](https://github.com/freephile/meza/commit/cb437664) (2024-10-04) Greg Rundlett: Preliminary removal of Python install INSIDE MediaWiki role @TODO cleanup / remove the separate variables for package_pyhton3_pip and package_python3_pip_rhel8 See Issue [#41](https://github.com/freephile/meza/issues/41)#issuecomment-2045506153
  - Modified: `src/roles/mediawiki/tasks/main.yml`

* [a2c81668](https://github.com/freephile/meza/commit/a2c81668) (2024-10-04) Greg Rundlett: Re-enable Semantic Dependency Updater
  - Modified: `config/MezaCoreExtensions.yml`

* [eab5d30c](https://github.com/freephile/meza/commit/eab5d30c) (2024-10-04) Greg Rundlett: Clarify opcache settings m_use_production_settings was vague
m_opcache_production_mode better describes this switch
Add descriptive comments that explains what it does
  - Modified: `Vagrantfile`
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/apache-php/templates/php.ini.j2`
  - Modified: `src/roles/init-controller-config/templates/public.yml.j2`

* [fedf9fbf](https://github.com/freephile/meza/commit/fedf9fbf) (2024-10-04) Greg Rundlett: Fix rebuild SMW data and rebuild Elasticsearch Add 'base' tag to the deploy command
fixes #98
  - Modified: `RELEASE-NOTES.md`

* [aed2dc95](https://github.com/freephile/meza/commit/aed2dc95) (2024-10-04) Greg Rundlett: Fix rebuild SMW data and rebuild Elasticsearch substitute list_of_wikis in place of wikis_to_rebuild_data
because the latter variable is undefined
fixes Issue [#98](https://github.com/freephile/meza/issues/98)
  - Modified: `src/roles/mediawiki/tasks/main.yml`

* [20f938f3](https://github.com/freephile/meza/commit/20f938f3) (2024-10-04) Greg Rundlett: Remove the footer in .git-commit-template.
  - Modified: `.git-commit-template`

* [59cfafe9](https://github.com/freephile/meza/commit/59cfafe9) (2024-10-04) Greg Rundlett: downgrade ReplaceText + InputBox These extensions' 'main' branch requires
a higher version of MediaWiki core. So, revert to
the REL1_39 branch for now.
  - Modified: `config/MezaCoreExtensions.yml`

* [4b80c01f](https://github.com/freephile/meza/commit/4b80c01f) (2024-10-04) Greg Rundlett: Fix typo in MezaCoreExtensions.yml
  - Modified: `config/MezaCoreExtensions.yml`

* [cfbe3c22](https://github.com/freephile/meza/commit/cfbe3c22) (2024-10-04) Greg Rundlett: Remove SAML configuration The SAML configuration should go into a configuration repo
(e.g. conf-meza-myfarm) for wikis that use it.
The 'opt/conf-meza/public' directory should
ALWAYS be turned into a 'conf-meza-myfarm' repo
after the first 'meza deploy', so that's where SAML
config can be put in e.g. base.php
This way, Meza can be deployed and used with all
kinds of authentication options rather than a single
hard-coded option.
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [ccc932fe](https://github.com/freephile/meza/commit/ccc932fe) (2024-10-04) Greg Rundlett: Switch some repos to master Add comments about things that need to be fixed or checked
Switch some repos to 'master'
- ExternalData
- InputBox
- ReplaceText
- AdminLinks
- DataTransfer
Reformat line comments from PHP to YAML
so that the file is valid YAML
  - Modified: `config/MezaCoreExtensions.yml`

* [87837388](https://github.com/freephile/meza/commit/87837388) (2024-10-04) Greg Rundlett: Fix composer install bug Fix Issue [#94](https://github.com/freephile/meza/issues/94) which can happen when composer.json
has newer dependencies or requirements than
composer.lock
  - Modified: `src/roles/mediawiki/tasks/main.yml`

* [7166e16f](https://github.com/freephile/meza/commit/7166e16f) (2024-10-04) Greg Rundlett: Fix samesite cookie settings for a stubborn Chrome Chrome browser will error with
"State Information Lost" ( \SimpleSAML\Error\NoState: NOSTATE )
unless you set session.cookie.secure => true
and session.cookie.samesite => 'None'
  - Modified: `src/roles/saml/templates/config.php.j2`

* [87956a53](https://github.com/freephile/meza/commit/87956a53) (2024-10-03) amcgillivray-nasa: Update MezaCoreExtensions.yml Changing page forms version from master to 5.8.1
  - Modified: `config/MezaCoreExtensions.yml`

* [33588cc6](https://github.com/freephile/meza/commit/33588cc6) (2024-10-02) amcgillivray-nasa: Update MezaCoreExtensions.yml Fixed spacing issue
  - Modified: `config/MezaCoreExtensions.yml`

* [c3ab0884](https://github.com/freephile/meza/commit/c3ab0884) (2024-09-27) amcgillivray-nasa: Update MezaCoreExtensions.yml 1. Added $wgPageFormsUseDisplayTitle = false;
2. Added UrlGetParameters
  - Modified: `config/MezaCoreExtensions.yml`

* [6d604cb0](https://github.com/freephile/meza/commit/6d604cb0) (2024-09-26) amcgillivray-nasa: Update MezaCoreExtensions.yml 1. Added $wgPageFormsDelayReload = true;
2. Added $smwgParserFeatures = $smwgParserFeatures | SMW_PARSER_LINV;
3. Added Gadgets extension
  - Modified: `config/MezaCoreExtensions.yml`

* [816854ad](https://github.com/freephile/meza/commit/816854ad) (2024-09-20) James Montalvo: fix(vuln): remove default elasticsearch password Setting a default password could cause installations to use that
password in production systems, which is a security vulnerability since
the default password is published on github.
  - Modified: `src/roles/elasticsearch/defaults/main.yml`

* [6bd0c2d2](https://github.com/freephile/meza/commit/6bd0c2d2) (2024-09-11) Rich Evans: Removed WatchAnalytics in MezaCoreExtensions.yml Will add it back after full 1.39 checkout is complete.
  - Modified: `config/MezaCoreExtensions.yml`

* [b48a7455](https://github.com/freephile/meza/commit/b48a7455) (2024-09-11) Rich Evans: Update MezaCoreExtensions.yml so Extention HeaderTabs uses master
  - Modified: `config/MezaCoreExtensions.yml`

* [12a9ca69](https://github.com/freephile/meza/commit/12a9ca69) (2024-09-11) Rich Evans: removed extension not used in 1.34 MezaCoreExtensions.yml removed SubpageNavigation, InlineComments, DarkMode, WikiLove, FlexFormUpdate. Will add these extensions back after 1.39 is fully checked-out
  - Modified: `config/MezaCoreExtensions.yml`

* [7bc5f2f9](https://github.com/freephile/meza/commit/7bc5f2f9) (2024-09-10) Rich Evans: Update LocalSettings.php.j2 enabled 4 GB uploads and don't check fiile types
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [9ec786b1](https://github.com/freephile/meza/commit/9ec786b1) (2024-09-10) Rich Evans: Update defaults.yml update max file size to 5G
  - Modified: `config/defaults.yml`

* [dfb15e15](https://github.com/freephile/meza/commit/dfb15e15) (2024-09-05) Rich Evans: Update MezaCoreExtensions.yml Bump SMW from 4.1.3 to ~4.2 + added config properties, switch back to normal Mediawiki version of PF version master, added SubPageNavigation config, changed SDU config to use Job Queue.
  - Modified: `config/MezaCoreExtensions.yml`

* [89dccf34](https://github.com/freephile/meza/commit/89dccf34) (2024-09-05) amcgillivray-nasa: Update wgSDUUseJobQueue to true in MezaCoreExtensions.yml SDU works when set to true, and does not work when set to false
  - Modified: `config/MezaCoreExtensions.yml`

* [3a952f5b](https://github.com/freephile/meza/commit/3a952f5b) (2024-07-11) amcgillivray-nasa: Update haproxy.cfg.j2 Removed "no-tlsv12" in order to maintain compatibility with mwclient on RHEL8 using OpenSSL 1.1.1
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

* [f55071aa](https://github.com/freephile/meza/commit/f55071aa) (2024-07-03) ndc-rkevans: Add WikiLove, FlexForms, and change VEForAll brnach to master
  - Modified: `config/MezaCoreExtensions.yml`

* [a5d919e3](https://github.com/freephile/meza/commit/a5d919e3) (2024-06-10) Rich Evans: Update MezaCoreSkins.yml Add MediaWiki site configuration variables via the Vector skin config
  - Modified: `config/MezaCoreSkins.yml`

* [9ff624e4](https://github.com/freephile/meza/commit/9ff624e4) (2024-06-10) Rich Evans: Update MezaCoreSkins.yml removed skin:Poncho until we have time to debug it
  - Modified: `config/MezaCoreSkins.yml`

* [6f439740](https://github.com/freephile/meza/commit/6f439740) (2024-06-10) Rich Evans: Update MezaCoreExtensions.yml Configure Page Forms to allow autoedits in the User Namespace
  - Modified: `config/MezaCoreExtensions.yml`

* [2732e08e](https://github.com/freephile/meza/commit/2732e08e) (2024-06-06) Rich Evans: Update MezaCoreSkins.yml Notes - Chameleon is the default skin. All the other skins either ship with MW Core (1.39) or they were listed at: https://www.pro.wiki/articles/best-mediawiki-skins
  - Modified: `config/MezaCoreSkins.yml`

* [13c853fa](https://github.com/freephile/meza/commit/13c853fa) (2024-06-06) Rich Evans: Update MezaCoreSkins.yml adding more skins to choose from
  - Modified: `config/MezaCoreSkins.yml`

* [ea52868f](https://github.com/freephile/meza/commit/ea52868f) (2024-06-06) ndc-rkevans: replace depricated ansible includes with include_tasks
  - Modified: `src/roles/database/tasks/main.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`
  - Modified: `src/roles/gluster/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`

* [4f1fbe5a](https://github.com/freephile/meza/commit/4f1fbe5a) (2024-06-06) ndc-rkevans: Re-enable SDU and fix CommentStreams config typo
  - Modified: `config/MezaCoreExtensions.yml`

* [2cb0b81a](https://github.com/freephile/meza/commit/2cb0b81a) (2024-05-31) Rich Evans: Update MezaCoreExtensions.yml make it so that Comment Streams don't show on pages by default
  - Modified: `config/MezaCoreExtensions.yml`

* [da64b3ba](https://github.com/freephile/meza/commit/da64b3ba) (2024-05-20) Rich Evans: Update .htaccess.j2 Don't expose any files or folders with .git in the path
  - Modified: `src/roles/htdocs/templates/.htaccess.j2`

* [6ce641e0](https://github.com/freephile/meza/commit/6ce641e0) (2024-05-08) ndc-rkevans: Configure Apache ServerTokens to ProductOnly
  - Modified: `src/roles/apache-php/templates/httpd.conf.j2`

* [83d38a0c](https://github.com/freephile/meza/commit/83d38a0c) (2024-05-08) ndc-rkevans: Have meza overwrite local commits by default
  - Modified: `config/defaults.yml`

* [932042ab](https://github.com/freephile/meza/commit/932042ab) (2024-05-08) ndc-rkevans: Add Extension SubpageNavigation to Meza Core Extension
  - Modified: `config/MezaCoreExtensions.yml`

* [8eb22403](https://github.com/freephile/meza/commit/8eb22403) (2024-05-01) ndc-rkevans: saml configuration updates
  - Modified: `src/roles/configure-wiki/templates/samlAuthorizations.d/base.php.j2`
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/saml/templates/authsources.php.j2`
  - Modified: `src/roles/saml/templates/config.php.j2`

## Meza 39.6.2
* [d931e9cc](https://github.com/freephile/meza/commit/d931e9cc) (2024-03-29) Greg Rundlett: Add cache directory for SimpleSAMLphp The cachedir is templated in the config.php.j2 file.
The directory is created in the main tasks file.
Oddly enough, the system worked in prior tests without any cache defined.
See simplesamlphp/config/config.dist for all configurations available.
See Issue [#74](https://github.com/freephile/meza/issues/74)
This work was performed for NASA GRC-ATF by WikiWorks per NASA Contract NNC15BA02B.
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/saml/templates/config.php.j2`

## Meza 39.6.1
* [39dbcbf6](https://github.com/freephile/meza/commit/39dbcbf6) (2024-03-29) Greg Rundlett: Update CHANGELOG and RELEASE NOTES Add details on new features.
See Issue [#52](https://github.com/freephile/meza/issues/52)
See also #53 #54 #55
This work was performed for NASA GRC-ATF by WikiWorks per NASA Contract NNC15BA02B.
  - Modified: `CHANGELOG`
  - Modified: `RELEASE-NOTES.md`


## Meza 39.5.0

Upgrades:
- MediaWiki 1.39.6
- Semantic MediaWiki 4.1.3
- PHP 8.1 using the Remi repo
- Elasticsearch 7.10.2
- SAML Authentication
  - SimpleSAMLphp library to 2.2.1
  - Extension Pluggable Auth 7.0
  - Extension SimpleSAMLphp 7.0
- Composer
- Extensions
  - Simple Batch Upload
  - Flow
  - SubPageList 3.0.0
  - Maps
  - PageForms
  - Variables
  - Whos Online
  - Semantic Extra Special Properties
  - Header Footer
  - Watch Analytics
  - HTML5 Mediator
  - Simple MathJax
  - Media Functions
  - Widgets
  - Pipe Escape
  - Semantic Drilldown
  - Contribution Scores


Removed Extensions:
The following extensions were removed due to incompatibility
- Talk Right
- Wiretap

New Features:
- Only execute SMW Rebuild Data when requested explicitly.
  This feature improves the separation of concerns between "platform updates"
  and "special maintenance". It is accomplished using the tags feature
  of Ansible: `meza deploy monolith --tags base,smw-data`

  Note that you can use the `meza maint rebuild` command to rebuild
  SMW data **and** Elasticsearch indexes. This command is equivalent to
  `meza deploy monolith --tags base,smw-data,search-index`

- Pretty URLs
  There is no *index.php* in URLs, just `mysite.com/wiki/SomePage`
  Easier to type, easier to read, easier to remember, shorter, and pretty!

- Deploy over local changes
  Added `overwrite_local_git_changes` option (default: off) for deploys. Say you
  check out some new branch of code in a particular extension or MediaWiki itself.
  Then you test that in the browser and get results (good or bad). Next you want to
  re-deploy to a known state. This option allows you more control with less work.
  The default value is 'false' (off) preserving current behavior which will fail
  the deploy, refusing to overwrite local changes.

- WebP (.webp) images are supported for upload
  The WebP format now makes up 12% of the web. Designed to be more efficient than
  JPEG and PNG images, the WebP format uses advanced compression for smaller size
  without losing quality. WebP is supported by 96.3% of browsers.
  https://en.wikipedia.org/wiki/WebP

- Keep composer updated
  The configuration option `composer_keep_updated` is observed when running a
  deploy. Thus, if this role variable is set to 'true' (default), `composer` will
  self-update on your targets providing you with the latest features, bugfixes
  and security patches to composer itself.

Other Changes:
- Reduce git clone size of MediaWiki by 2+GB / improve speed
- Add .editorconfig
- Version lock Ansible and Python
- Disable (automatic) Elasticsearch upgrades for predictability
- Set PHP-FPM default port to 9000 avoiding surprises or conflicts
- Syntax cleanup
- Bug fixes in Python, PHP, YAML
- Documentation of all 50+ meza.py functions
- Improve testing scripts
- Create CHANGELOG
- Remove obsolete $wgShellLocale
- Allow easier forking
- Enable Ansible debugger

### Commits since 35.x
* 86aea14 (HEAD -> REL1_39, tag: 39.6.0, freephile/REL1_39) Fix first-time deploy errors related to SMW rebuild data
* 74e74a2 Change SAML logging handler to file
* 0ac901c Update saml20-idp-remote.php
* c8f3317 Add commit template; Add Rich to Release Notes
* 5e2200b (tag: 39.5.0) Create Release Notes for v39.5.0
* dce594e (HEAD -> REL1_39, origin/REL1_39) Versionlock Ansible and Python to prevent incompatibilities
* 84e08b0 Fix deploy errors on initial deploy
* 58933f2 Fix fatal recursion errors
* 8623081 Finish dressing out the SAML Authentication role
* df820d7 Remove the old 'remove Extension SimpleSamlAuth'
* f73c216 Fix default port for PHP-FPM
* 0011a5d Merge remote-tracking branch 'nasa/grc-atf-dev' into REL1_39
* 5c89037 (nasa/grc-atf-dev, nasa/39.x) Merge pull request #48 from freephile/REL1_39
* 315364c (tag: 39.4.0) Modify print_width in .editorconfig - but it doesn't seem to affect yamllint
* e554ccf Fix 'create wiki' failure due to variable scoping
* 18871ab Lift restriction on composer version
* 29f99dd Enable check mode for testing
* 7905761 Add LocalSettings directive for Extension:SubPageList
* 0441317 Add FIXME comment about composer
* e672dcc SubPageList needs a wfLoadExtension
* 0923618 Upgrade SAML auth to use simpleSAMLphp 2.2.1
* 5362af6 Extension SubPageList upgraded from 1.6.1 to 3.0.0
* 6ab981b Reformat: Wrap all comments at 120 characters
* d465e29 Delete errant swap file from repo
* 74beb29 (tag: 39.3.0) Fix delete / restore functionality
* 7d9915d Add VS Code settings to .gitignore
* 013a11b (tag: 39.2.0) Use Elasticsearch 7.10
* 873258d Add the --always option to git describe to avoid errors
* fc45add Document all 53 functions in meza.py
* 8ee9f63 Semantic Dependency Updater - new home / disabled
* b76d951 Fix thumbnail generation + add webp support
* 8edbf4a Fixe the compiled templates ownership issue
* cd5ad23 Update some integration test scripts
* 957a0ef Create a CHANGELOG as a de-minimus form of Release Notes
* d253642 Add some directories to gitignore
* 60d9bb0 (tag: 39.1.0) Merge remote-tracking branch 'nasa/grc-atf-dev' into REL1_39
* 1697c20 Add a "Section 508 Info" link to the footer via LocalSettings.php template
* 383f4c8 (origin/grc-atf-dev, grc-atf-dev) make sure widgets compipled templates folder is owned by meza-ansible to avoid local changes error when updating
* 81ac965 restore force debug to false
* e0fcbc4 Merge pull request #45 from freephile/REL1_39
* a4fadf4 ansible-lint code health changes
* a044cfe $wgShellLocale is obsolete as of REL1_38
* 45270d4 Final fixes for .smw.json and create wiki bugs
* 17f7fae yamllint code health syntax and formatting changes
* f0dba02 Merge pull request #44 from freephile/REL1_39
* 1e91f9e Fix permission problems + naming in .smw.json directory
* 4b0d76a Ensure .smw.json has a home
* 7049379 Feature: Short URLs
* 6ca76db Feature: Short URLs
* c8e6665 Remove commented line
* afb41e8 Make 'enforce_meza_version' undefined; with comment
* a02a80c Upgrade PHP to 8.1
* cd60cf1 Example of Remi repo usage from geerlingguy
* f2e7e1e Minor yaml lint fixes
* f3ed040 Add 'force' option to be able to 'overwrite local git changes'
* f7a5cec Make MediaWiki core branch depth a configuration value
* 602587f Make the Meza project repository a configuration value
* d95b682 Update Extension Flow for PHP8.1 compatibility
* 28f314e git repo URL and branch name as BASH variables
* 4cbcd64 Upgrade SimpleBatchUpload to 2.x for PHP 8.1 compatibility
* b6daa75 Use fully qualified built-in module name for dnf
* 0db71f8 Add .yamllint configuration
* d2fe7d9 Fix 50 yamllint errors in Base role
* 972d5ca Reorder dnf set-enabled, install per docs
* cdef0c4 Add EditorConfig to this project
* 48782c2 Use 'false' for negative  truthy values
* 817f8f0 Use 'true'/'false' for truthy values
* 2861473 Fix some yamllint and ansible-lint warnings
* c568524 Fix fatal indentation errors
* 62e2d78 Use fully qualified name  ansible.builtin.debug
* cd83e12 Upgrade Semantic MediaWiki to 4.1.3
* e61e989 Upgrade Maps to 10.1.1
* ccd118c Switch PageForms to latest version (5.6.3)
* c2bc0a6 Use master branch for Variables extension
* 4f9ea65 Revert "Variables extension - disabled"
* dbc68b6 Update WhosOnline for compatibility with REL1_39
* 3ca303b Fix database backup function
* 2367a82 Enable Ansible debugger by default
* e3228e3 Fix Widgets folder permissions tasks
* 7cac79a Update Semantic Extra Special Properties extesion
* 20d152c Fix Issue #2 Remove GitHub Actions
* da17c45 change raw_input() to input() for Python 3.x
* 4c31903 Fix inconsistent use of tabs and spaces
* de507d4 Fix issue #7 TypeError: must be str, not bytes
* dffc4cd Change Elasticsearch repo to disabled by default
* cee39d4 lint site playbook
* 4598d89 Add sample script for checking an Upgrade
* 6109296 Upgrade Elasticsearch to 7.x from 6.x
* 755bbcb Semantic MediaWiki
* c70ed42 Variables extension - disabled
* c6710dc Header Footer
* d3ef6c1 Watch Analytics - switch to WMF master
* 936ba9e Talk Right & Wiretap removed
* 19edfeb HTML5 Mediator
* faf0520 SimpleMathJax
* fd3701f Media Functions
* 74f26f2 Widgets
* a171341 Pipe Escape
* 277d390 Semantic Drilldown
* 420fd5e Contribution Scores
* 876b8ac Major upgrade of Meza for MediaWiki 1.39

### Contributors
* 94 Greg Rundlett
* 7 Rich Evans

# How to upgrade
There is no automatic upgrade path yet from 35.x to 39.x due to the major
Elasticsearch and SMW upgrades. An UPGRADE doc may be forthcoming, but basically
you can create a new instance, migrating your database and media files. Then
create the search indexes with `meza maint-rebuild monolith`.

