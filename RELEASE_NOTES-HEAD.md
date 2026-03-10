## Meza Release Notes 43.60.6 → HEAD

### Commits

HEAD -> dev origin/dev
* [6b1dccb9](https://github.com/freephile/meza/commit/6b1dccb9) (2026-03-10) Greg Rundlett: Add Vagrant pre-requisites for Linux Issue [#268](https://github.com/freephile/meza/issues/268) 
  - Modified: `manual/DEVELOPING.md`

* [fa93b3bc](https://github.com/freephile/meza/commit/fa93b3bc) (2026-03-10) Greg Rundlett: Add comments and documentation for ARA ARA Records Ansible was shown to be extremely useful, but also requires
some thought about how to integrate it.
Add comments for easy integration in a test lab.
Address Issue [#85](https://github.com/freephile/meza/issues/85)
  - Modified: `config/ansible.cfg`
  - Added: `manual/ARA_NIST_800-53_Compliance.md`

* [3b0dd737](https://github.com/freephile/meza/commit/3b0dd737) (2026-03-10) Greg Rundlett: Improve development environment Make Vagrantfile 'multi-provider' for cross-platform support of
Windows and Linux
Using Vagrant's `VAGRANT_DEFAULT_PROVIDER` override and conditional
provider blocks. Linux users get libvirt, others stay on VirtualBox.
On Linux, DockerDesktop collides with Virtualbox, so to avoid any
problems we just use libvirt for Virtualbox on Linux.
Move post-up message so it displays AFTER you do `vagrant up` - so
it's not lost in the provisioner window.
Adopt some good practices from MediaWiki-vagrant project
Avoid adding meza-ansible to group vboxsf under libvirt bc it doesn't exist.
Address Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `Vagrantfile`

* [e563c965](https://github.com/freephile/meza/commit/e563c965) (2026-03-09) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [5d41d318](https://github.com/freephile/meza/commit/5d41d318) (2026-03-09) Greg Rundlett: Add info about using InstantCommons With new rate limits imposed by WMF for api requests and
their policies to thwart AI scrapers, it is important to implement
InstantCommons with the proper class, UA identifier, and configuration.
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [7b5762bd](https://github.com/freephile/meza/commit/7b5762bd) (2026-03-09) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [af64c0fd](https://github.com/freephile/meza/commit/af64c0fd) (2026-03-09) Greg Rundlett: Block AI bots and scrapers Issue [#323](https://github.com/freephile/meza/issues/323) Add calculation for memory consumption for HAProxy connections
Add calculation for memory consumption for stick tables
Fix warnings in haproxy.cfg Issue [#327](https://github.com/freephile/meza/issues/327)
Restrict access to HAProxy stats to local/private networks
Fixes original Issue [#234](https://github.com/freephile/meza/issues/234)
  - Modified: `config/defaults.yml`
  - Modified: `manual/meza-cmd/config.md`
  - Modified: `src/roles/haproxy/README.md`
  - Added: `src/roles/haproxy/defaults/main.yml`
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

* [0f899f7e](https://github.com/freephile/meza/commit/0f899f7e) (2026-03-08) Greg Rundlett: Add back the bind for port 80 Fixes #327 
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

* [9777616b](https://github.com/freephile/meza/commit/9777616b) (2026-03-05) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [03e2d999](https://github.com/freephile/meza/commit/03e2d999) (2026-03-05) Greg Rundlett: remove trailing space 
  - Modified: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`

* [8613f218](https://github.com/freephile/meza/commit/8613f218) (2026-03-05) Greg Rundlett: add a README for the HAProxy role 
  - Added: `src/roles/haproxy/README.md`

* [0e0aa034](https://github.com/freephile/meza/commit/0e0aa034) (2026-03-05) Greg Rundlett: update declarative wiki migration deglitter migrate-wikis help
make references to 'primary_wiki' singular because there should only
ever be ONE primary wiki
fail if there is more than one primary wiki
update the pattern regex to replace declarative wiki stanza but note
that it is still problematic for handling comments when you manually
comment your wiki declaration, and then try to use the manual
"edit public.yml to create a wiki" process.
  - Modified: `manual/meza-cmd/migrate-wikis.md`
  - Modified: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`

* [27f06827](https://github.com/freephile/meza/commit/27f06827) (2026-03-05) Greg Rundlett: update yaml and linter configs update ansible-lint config with Issue links and comments
update yamllint with proper list
update LINTING.md with link to Ansible docs
yaml strings do not need quotes;
unless the value is at risk of being interpreted as an integer;
so quote "128M" and "127.0.0.1"
add new variable for memcached listen port to defaults.yml
add new variable for the 'listen' port for memcached in its config file
add documentation about meza's config file hierarchy
- in manual/meza-cmd/config.md
- in public.yml template
Addresses Issue [#83](https://github.com/freephile/meza/issues/83) and Issue [#144](https://github.com/freephile/meza/issues/144)
  - Modified: `.ansible-lint`
  - Modified: `.yamllint`
  - Modified: `LINTING.md`
  - Modified: `config/defaults.yml`
  - Modified: `manual/meza-cmd/config.md`
  - Modified: `src/roles/htdocs/defaults/main.yml`
  - Modified: `src/roles/init-controller-config/templates/public.yml.j2`
  - Modified: `src/roles/memcached/templates/memcached.j2`

* [7fac5158](https://github.com/freephile/meza/commit/7fac5158) (2026-03-05) Greg Rundlett: update SBOM 
  - Modified: `src/scripts/meza-sbom.cyclonedx.json`
  - Modified: `src/scripts/meza-sbom.spdx.json`
  - Modified: `src/scripts/meza-sbom.txt`

* [b944f271](https://github.com/freephile/meza/commit/b944f271) (2026-02-19) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [21e45c2e](https://github.com/freephile/meza/commit/21e45c2e) (2026-02-19) Greg Rundlett: Doc each role #321 in preparation for #42 Adds a brief explanation for each of the 56 roles
Categorized as follows:
- Third-party / vendor roles
- Infrastructure / system roles
- Meza orchestration roles
- Wiki lifecycle roles
- Backup roles
- Utility / library roles
  - Added: `src/roles/README.md`

* [22bf91c9](https://github.com/freephile/meza/commit/22bf91c9) (2026-02-19) Greg Rundlett: Add README for update.php role #320 
  - Added: `src/roles/update.php/README.md`

* [1f5f0d37](https://github.com/freephile/meza/commit/1f5f0d37) (2026-02-18) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [fe95d559](https://github.com/freephile/meza/commit/fe95d559) (2026-02-18) Greg Rundlett: Comment about the logo used in Chameleon Chameleon skin uses the 1x 'meza-logo-135.png' file.
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [99b8f074](https://github.com/freephile/meza/commit/99b8f074) (2026-02-18) Greg Rundlett: Adjust logrotate to actual elasticsearch logs Elasticsearch logs are in the m_data_dir/elasticsearch/log directory
They are NOT in the m_data_log_dir/elasticsearch directory
  - Modified: `src/roles/logrotate/README.md`
  - Modified: `src/roles/logrotate/tasks/main.yml`

* [b9643cf9](https://github.com/freephile/meza/commit/b9643cf9) (2026-02-18) Greg Rundlett: These variables do not belong to this role #42 These variables are used in the init-controller and htdocs roles. The verify-wiki role needs to be factored into component parts because what it does is not exactly clear.
  - Deleted: `src/roles/verify-wiki/defaults/main.yml`

* [d0c4b9b9](https://github.com/freephile/meza/commit/d0c4b9b9) (2026-02-15) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [c46a2932](https://github.com/freephile/meza/commit/c46a2932) (2026-02-14) Greg Rundlett: Fix regression bug: Elasticsearch advanced #311 improve the elastic-build-index.sh script
It was possibly contributing to failed indexing because the throwaway
`jq` pipe was just putting errors in the log instead of giving good
information on whether setting were successfully set.
Now we retrieve and report the HTTP status code on the interaction
with elasticsearch.
Fixes Issue [#311](https://github.com/freephile/meza/issues/311)
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`

* [575fab5c](https://github.com/freephile/meza/commit/575fab5c) (2026-02-15) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [17b64402](https://github.com/freephile/meza/commit/17b64402) (2026-02-14) Greg Rundlett: Fix regression bug: Elasticsearch advanced #311 MediaWiki 1.43 requires Elasticsearch to be at 7.10.2
fixed the elasticsearch install task
Apparently it broke due to the 'name' of the package being a version test:
   ` name: "elasticsearch <= {{ elasticsearch_version }}"`
Added downgrade if system has advanced beyone pinned package version
added `elasticsearch_versionlock_enabled: true` to role defaults
created role README.md
Fixes Issue [#311](https://github.com/freephile/meza/issues/311)
  - Added: `src/roles/elasticsearch/README.md`
  - Modified: `src/roles/elasticsearch/defaults/main.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`

* [9c4a615a](https://github.com/freephile/meza/commit/9c4a615a) (2026-02-14) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [382f5b5c](https://github.com/freephile/meza/commit/382f5b5c) (2026-02-13) Greg Rundlett: Remove `meza setup dev-networking` and ref. #304 setup dev-networking was obsolete
Fixes Issue [#304](https://github.com/freephile/meza/issues/304)
  - Modified: `manual/meza-cmd/help.md`
  - Modified: `manual/meza-cmd/install.md`
  - Modified: `manual/meza-cmd/setup.md`
  - Deleted: `src/scripts/dev-networking.sh`
  - Modified: `src/scripts/meza.py`

* [f931e4d3](https://github.com/freephile/meza/commit/f931e4d3) (2026-02-14) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [5df4eb80](https://github.com/freephile/meza/commit/5df4eb80) (2026-02-13) Greg Rundlett: Add pre-commit badge to README We use pre-commit, so might as well advertise it.
Part of Issue [#304](https://github.com/freephile/meza/issues/304)
  - Modified: `README.md`

* [19ec6aa5](https://github.com/freephile/meza/commit/19ec6aa5) (2026-02-13) Greg Rundlett: Remove meza setup dev command and ref Issue [#304](https://github.com/freephile/meza/issues/304)
  - Modified: `config/i18n/en.yml`
  - Modified: `manual/meza-cmd/help.md`
  - Modified: `manual/meza-cmd/index.md`
  - Modified: `manual/meza-cmd/setup.md`
  - Modified: `src/scripts/meza.py`

* [6c278c8e](https://github.com/freephile/meza/commit/6c278c8e) (2026-02-13) Greg Rundlett: update CONTRIBUTING.md with link to DEVELOPING.md new DEVELOPING.md focused on development workflow.
part of Issue [#304](https://github.com/freephile/meza/issues/304)
  - Modified: `CONTRIBUTING.md`
  - Added: `manual/DEVELOPING.md`

* [34164620](https://github.com/freephile/meza/commit/34164620) (2026-02-13) Greg Rundlett: update git pre-commit hook to match lint-files.sh using pre-commit: https://pre-commit.com
exclude svg from 'trailing-whitespace' rule
exclude svg from 'end-of-file-fixer' rule
check that non-binary executables have shebangs
update/install with (.venv) `pre-commit install` when making changes
NOTE: Although I tried valiantly, I could not enable the check-ast
hook for Python files with the specification that language_version
be 3.6.8 which is what we need on RockyLinux 8 because I could not
intall it with pyenv on Ubuntu 24.04 no matter what I tried. So,
skipping any check-ast commit hook for now.
See
- https://github.com/pre-commit/pre-commit
- https://github.com/pre-commit/pre-commit-hooks
part of Issue [#304](https://github.com/freephile/meza/issues/304)
  - Modified: `.pre-commit-config.yaml`

* [598a8980](https://github.com/freephile/meza/commit/598a8980) (2026-02-13) Greg Rundlett: Add README and detailed set of graphs #306 See README.md in the playbooks directory
Fixes Issue [#306](https://github.com/freephile/meza/issues/306)
  - Added: `src/playbooks/README.md`
  - Added: `src/playbooks/backup-w-tasks.svg`
  - Added: `src/playbooks/check-for-changes-w-tasks.svg`
  - Added: `src/playbooks/cleanup-upload-stash-w-tasks.svg`
  - Added: `src/playbooks/create-wiki-promptless-w-tasks.svg`
  - Added: `src/playbooks/create-wiki-w-tasks.svg`
  - Added: `src/playbooks/debug-w-tasks.svg`
  - Added: `src/playbooks/delete-elasticsearch-w-tasks.svg`
  - Added: `src/playbooks/delete-wiki-promptless-w-tasks.svg`
  - Added: `src/playbooks/delete-wiki-w-tasks.svg`
  - Added: `src/playbooks/deploy-notify-w-tasks.svg`
  - Added: `src/playbooks/getdocker-w-tasks.svg`
  - Added: `src/playbooks/migrate-wikis-w-tasks.svg`
  - Added: `src/playbooks/push-backup-w-tasks.svg`
  - Added: `src/playbooks/rebuild-smw-and-index-w-tasks.svg`
  - Added: `src/playbooks/run-maintenance-w-tasks.svg`
  - Added: `src/playbooks/setbaseconfig-w-tasks.svg`
  - Added: `src/playbooks/setup-env-w-tasks.svg`
  - Added: `src/playbooks/setup-meza-user-w-tasks.svg`
  - Added: `src/playbooks/site-w-tasks.svg`
  - Added: `src/playbooks/test-certbot-w-tasks.svg`
  - Added: `src/playbooks/verify-permissions-w-tasks.svg`
  - Modified: `src/scripts/generate-playbook-graphs.sh`

* [f27e66b0](https://github.com/freephile/meza/commit/f27e66b0) (2026-02-13) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [452ea649](https://github.com/freephile/meza/commit/452ea649) (2026-02-13) Greg Rundlett: Try to give spaced out CoPilot more brains 
  - Modified: `.github/copilot-instructions.md`

* [5cfa18a4](https://github.com/freephile/meza/commit/5cfa18a4) (2026-02-13) Greg Rundlett: improve lint-files.sh to respect .gitignore The lint-files.sh script tries to detect directory entries in .gitignore
and adds them to the base set of directories that it already skips:
.venv
vendor
.cache
.git
tests/docker
collections
node_modules
Also avoid linting SVG (and common binaries)
SVGs are technically text files and so were being modified.
For Issue [#306](https://github.com/freephile/meza/issues/306)
  - Modified: `src/scripts/lint-files.sh`

* [a85c9982](https://github.com/freephile/meza/commit/a85c9982) (2026-02-13) Greg Rundlett: minor correction to the `meza setup dev` doc #304 Currently, you can either:
`meza setup dev`
or
`meza setup env <env>`
In the first form (special case) no extra arg is required.
In the second form, 'env' directive, an environment name is required.
Special handling occurs for the environment names
'monolith', or 'vagrant'.
`meza setup env vagrant` and
`meza setup env monolith` are normally handled for you by bootstrapping
from the Vagrantfile and/or 'getmeza.sh' so users only ever need to
`meza setup env staging` for example
For Issue [#304](https://github.com/freephile/meza/issues/304)
  - Modified: `manual/meza-cmd/setup.md`

* [2493f4de](https://github.com/freephile/meza/commit/2493f4de) (2026-02-13) Greg Rundlett: Improve script to document playbooks #306 Add option `--with-tasks` to invoke `ansible-playbook-grapher --include-role-tasks`
This will change the SVG title and the output filename accordingly
For Issue [#306](https://github.com/freephile/meza/issues/306)
  - Modified: `src/scripts/generate-playbook-graphs.sh`

* [69eff908](https://github.com/freephile/meza/commit/69eff908) (2026-02-13) Greg Rundlett: Add svg files to document playbooks #306 Add script to generate (update) the SVGs on-demand for easy
periodic updating.
For Issue [#306](https://github.com/freephile/meza/issues/306)
  - Added: `src/playbooks/backup.svg`
  - Added: `src/playbooks/check-for-changes.svg`
  - Added: `src/playbooks/cleanup-upload-stash.svg`
  - Added: `src/playbooks/create-wiki-promptless.svg`
  - Added: `src/playbooks/create-wiki.svg`
  - Added: `src/playbooks/debug.svg`
  - Added: `src/playbooks/delete-elasticsearch.svg`
  - Added: `src/playbooks/delete-wiki-promptless.svg`
  - Added: `src/playbooks/delete-wiki.svg`
  - Added: `src/playbooks/deploy-notify.svg`
  - Added: `src/playbooks/getdocker.svg`
  - Added: `src/playbooks/migrate-wikis.svg`
  - Added: `src/playbooks/push-backup.svg`
  - Added: `src/playbooks/rebuild-smw-and-index.svg`
  - Added: `src/playbooks/run-maintenance.svg`
  - Added: `src/playbooks/setbaseconfig.svg`
  - Added: `src/playbooks/setup-env.svg`
  - Added: `src/playbooks/setup-meza-user.svg`
  - Added: `src/playbooks/site.svg`
  - Added: `src/playbooks/test-certbot.svg`
  - Added: `src/playbooks/verify-permissions.svg`
  - Added: `src/scripts/generate-playbook-graphs.sh`

* [34eae490](https://github.com/freephile/meza/commit/34eae490) (2026-02-12) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [090f72e4](https://github.com/freephile/meza/commit/090f72e4) (2026-02-11) Greg Rundlett: remove the "Last 500 edits" label `rclimit=500` means the query can only return 500 maximum,
and we need rclimit so we don't get the default 10;
but most times the API will return fewer than 500 results -
even when there are more than 500 edits
Polish Issue [#206](https://github.com/freephile/meza/issues/206)
  - Modified: `src/roles/htdocs/templates/meza-landing-page.php.j2`

* [aa55f5ea](https://github.com/freephile/meza/commit/aa55f5ea) (2026-02-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [607fea55](https://github.com/freephile/meza/commit/607fea55) (2026-02-11) Greg Rundlett: Correct the tooltip label - tally the last 500 edits Fixes Issue [#206](https://github.com/freephile/meza/issues/206)
  - Modified: `src/roles/htdocs/templates/meza-landing-page.php.j2`

* [4a709eb1](https://github.com/freephile/meza/commit/4a709eb1) (2026-02-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [3f76e403](https://github.com/freephile/meza/commit/3f76e403) (2026-02-11) Greg Rundlett: Replace WikiBlender fix excess margin and padding in footer
remove fake "legacy location" lookup for wgSitename
fix api query to get correct editor counts
Fixes Issue [#206](https://github.com/freephile/meza/issues/206)
  - Modified: `src/roles/htdocs/templates/meza-landing-page.php.j2`

* [3e97cc2c](https://github.com/freephile/meza/commit/3e97cc2c) (2026-02-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [2ad3b611](https://github.com/freephile/meza/commit/2ad3b611) (2026-02-11) Greg Rundlett: Deletes symlink for Issue [#50](https://github.com/freephile/meza/issues/50) 
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`

* [5719dfbd](https://github.com/freephile/meza/commit/5719dfbd) (2026-02-11) Greg Rundlett: clarify some config command in docs 
  - Modified: `manual/meza-cmd/config.md`

* [fb96617a](https://github.com/freephile/meza/commit/fb96617a) (2026-02-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [677c3572](https://github.com/freephile/meza/commit/677c3572) (2026-02-11) Greg Rundlett: Replace WikiBlender with simple htdocs task remove Blender from .htaccess
remove Blender variables from MediaWiki role defaults
remove Blender tasks from `mediawiki` role
remove BlenderSettings.php from `mediawiki` role
create new meza-landing-page.php that replaces the functionality of
WikiBlender in the `htdocs` role
use favicon from primary wiki, or default to project favicon
add meza-landing-page.php to htdocs templating task
`require` meza-landing-page.php from index.php (instead of WikiBlender)
add default vars for htdocs role that should be overridden in public.yml
add blender vars in the public.yml template for new controllers
Fixes Issue [#206](https://github.com/freephile/meza/issues/206)
  - Added: `src/roles/htdocs/defaults/main.yml`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/htdocs/templates/.htaccess.j2`
  - Modified: `src/roles/htdocs/templates/index.php.j2`
  - Added: `src/roles/htdocs/templates/meza-landing-page.php.j2`
  - Modified: `src/roles/init-controller-config/templates/public.yml.j2`
  - Modified: `src/roles/mediawiki/defaults/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Deleted: `src/roles/mediawiki/templates/BlenderSettings.php.j2`

* [46e8238a](https://github.com/freephile/meza/commit/46e8238a) (2026-02-10) Greg Rundlett: Update logo - add to task Follow-up commit 5d355f9 by actually adding the logo file to the
'distribution' task "Ensure base files are in place (but do not
overwrite)"
Remember: usage of 'logo.png' is deprecated, but at least it's there
for use and override in conf-meza/public/wikis/<wiki>/
Fixes Issue [#270](https://github.com/freephile/meza/issues/270)
  - Modified: `src/roles/configure-wiki/tasks/main.yml`

* [0f56e190](https://github.com/freephile/meza/commit/0f56e190) (2026-02-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [a4c8a14c](https://github.com/freephile/meza/commit/a4c8a14c) (2026-02-10) Greg Rundlett: Remove obsolete Parsoid code This just removes the obsolete ansible variables and the
'cleanup-parsoid' role that was coupled into 'base'.
Other 'cleanup' would involve the ServerPerformance and cron roles.
See Issue [#19](https://github.com/freephile/meza/issues/19)
Fixes Issue [#45](https://github.com/freephile/meza/issues/45)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Deleted: `src/roles/base/tasks/parsoid-cleanup.yml`

* [a725e5b9](https://github.com/freephile/meza/commit/a725e5b9) (2026-02-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [f938ab2c](https://github.com/freephile/meza/commit/f938ab2c) (2026-02-10) Greg Rundlett: Fix remaining Ansible Lint issues == Config ==
paths.yml - fix long comment lines
REMOVE .travis.yml - we don't use Travis CI
== Playbooks ==
check-for-changes.yml - reorder keys for blocks; add noqa comments for git operations; FQCN
== Roles ==
autodeployer - Fixed FQCN, add missing 'name:'; jinja spacing
umask-set - Fixed FQCN
umask-unset - Fixed FQCN
yamllint comments for exceptions
use [true, false] for truthy values
Fixes Issue [#16](https://github.com/freephile/meza/issues/16)
  - Deleted: `.travis.yml`
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/playbooks/example-block.yaml`
  - Modified: `src/playbooks/push-backup.yml`
  - Modified: `src/roles/autodeployer/tasks/do-deploy.yml`
  - Modified: `src/roles/autodeployer/tasks/main.yml`
  - Modified: `src/roles/database/defaults/main.yml`
  - Modified: `src/roles/database/tasks/main.yml`
  - Modified: `src/roles/database/tasks/replication.yml`
  - Modified: `src/roles/gluster/defaults/main.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/netdata/tasks/main.yml`
  - Modified: `src/roles/umask-set/tasks/main.yml`
  - Modified: `src/roles/umask-unset/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/create-admin-account.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`

* [b7035d54](https://github.com/freephile/meza/commit/b7035d54) (2026-02-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [31d0dbff](https://github.com/freephile/meza/commit/31d0dbff) (2026-02-10) Greg Rundlett: Fix remaining Ansible Lint issues Add `var-naming[no-role-prefix]` to 'skip_list' in .ansible-lint
configuration
== Playbooks ==
backup.yml - Fixed FQCN for set_fact, jinja spacing
migrate-wikis.yml - Fixed FQCN for debug
rebuild-smw-and-index.yml - Fixed FQCN, no-changed-when, added noqa
when intentionally using shell module
== Roles ==
backup-db-wikis - Fixed FQCN
dump-db-wikis - Fixed FQCN
backup-uploads - Fixed FQCN
delete-wiki-wrapper - Fixed FQCN; re-order keys in block;
use uri module rather than shell for curl commands
Fixes Issue [#16](https://github.com/freephile/meza/issues/16)
  - Modified: `.ansible-lint`
  - Modified: `src/playbooks/backup.yml`
  - Modified: `src/playbooks/migrate-wikis.yml`
  - Modified: `src/playbooks/rebuild-smw-and-index.yml`
  - Modified: `src/roles/backup-db-wikis/tasks/main.yml`
  - Modified: `src/roles/backup-uploads/tasks/main.yml`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/dump-db-wikis/tasks/main.yml`

* [3fb8a2f5](https://github.com/freephile/meza/commit/3fb8a2f5) (2026-02-10) Greg Rundlett: Cleanup with Ansible Lint Fix indentation of msg block
Add ignore for .github/workflows to .yamllint config
GitHub Actions workflow files use `on:` as a required top-level keyword
(not a boolean value), which triggers yamllint's truthy rule.
Since these are GitHub-specific YAML files (not Ansible), excluding
them from yamllint checks is appropriate. The workflows will still be
validated by GitHub's own workflow syntax checker.
Fixes Issue [#16](https://github.com/freephile/meza/issues/16)
  - Modified: `.yamllint`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`

* [69cf237e](https://github.com/freephile/meza/commit/69cf237e) (2026-02-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [aada3bec](https://github.com/freephile/meza/commit/aada3bec) (2026-02-10) Greg Rundlett: Cleanup with Ansible Lint Fix FQCN and Jinja spacing in import-wiki-sql.yml
Addresses Issue [#16](https://github.com/freephile/meza/issues/16)
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`

* [e485c4d3](https://github.com/freephile/meza/commit/e485c4d3) (2026-02-10) Greg Rundlett: Fix Admin password logic in create wiki create-wiki.yml playbook for User interaction
create-wiki-wrapper role = presentation of Admin password at the end of workflow (fixed FQCN)
ensure-admin-password.yml = verify wiki business logic
import-wiki-sql.yml = verify wiki orchestration
Fixes Issue [#269](https://github.com/freephile/meza/issues/269)
  - Modified: `src/playbooks/create-wiki.yml`
  - Modified: `src/roles/create-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/create-admin-account.yml`
  - Added: `src/roles/verify-wiki/tasks/ensure-admin-password.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`

* [1fe0e7bb](https://github.com/freephile/meza/commit/1fe0e7bb) (2026-02-10) Greg Rundlett: Normalize meza variables replace path_alias.yml with definitions in paths.yml
Closes Issue [#286](https://github.com/freephile/meza/issues/286)
  - Deleted: `config/path_alias.yml`
  - Modified: `config/paths.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`

* [54578f39](https://github.com/freephile/meza/commit/54578f39) (2026-02-09) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [4d0fc94a](https://github.com/freephile/meza/commit/4d0fc94a) (2026-02-08) Greg Rundlett: Normalize meza variables update paths.yml and path_alias.yml
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/path_alias.yml`
  - Modified: `config/paths.yml`

* [dde5c1f8](https://github.com/freephile/meza/commit/dde5c1f8) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_config_secret_dir with m_conf_secret_dir
replaced m_config_public_dir with m_conf_public_dir
replaced m_config_vault with m_conf_vault_dir
replaced m_home with m_conf_users_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `.github/copilot-instructions.md`
  - Modified: `Vagrantfile`
  - Modified: `config/paths.yml`
  - Modified: `manual/MEZA_USER_ROLE.md`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/playbooks/migrate-wikis.yml`
  - Modified: `src/playbooks/run-maintenance.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/renew-cron.yml`
  - Modified: `src/roles/apache-php/tasks/profiling.yml`
  - Modified: `src/roles/backup-config/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis-push/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis/tasks/main.yml`
  - Modified: `src/roles/backup-uploads-push/tasks/main.yml`
  - Modified: `src/roles/backup-uploads/tasks/main.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/configure-wiki/README.md`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/configure-wiki/templates/preLocalSettings.d/base.php.dist.j2`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/dump-db-wikis/tasks/main.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/key-transfer/tasks/grant-keys.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/meza-user/README.md`
  - Modified: `src/roles/meza-user/defaults/main.yml`
  - Modified: `src/roles/meza-user/tasks/main.yml`
  - Modified: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`
  - Modified: `src/roles/php/tasks/profiling.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/setup-env/tasks/main.yml`
  - Modified: `src/roles/sync-configs/tasks/main.yml`
  - Modified: `src/scripts/meza.py`
  - Modified: `tests/deploys/setup-alt-source-backup.yml`

* [442a78d3](https://github.com/freephile/meza/commit/442a78d3) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_mediawiki with m_mediawiki_install_path
variable name is consistent with MediaWiki's own $IP and MW_INSTALL_PATH
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/path_alias.yml`
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/playbooks/run-maintenance.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/configure-wiki/templates/preLocalSettings.d/base.php.dist.j2`
  - Modified: `src/roles/create-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/cron/templates/runAllJobs.php.j2`
  - Modified: `src/roles/mediawiki/tasks/cirrus_metastore_upgrade.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Modified: `src/roles/meza-log/templates/server-performance.sh.j2`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/update.php/tasks/main.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/create-admin-account.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `src/scripts/unite-the-wikis.sh`
  - Modified: `src/scripts/uniteTheWikis.php`

* [dc21db81](https://github.com/freephile/meza/commit/dc21db81) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_apache with m_web_conf_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`

* [d6e4c2f1](https://github.com/freephile/meza/commit/d6e4c2f1) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_htdocs with m_web_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/debug.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/README.md`
  - Modified: `src/roles/ansible-role-certbot-meza/vars/main.yml`
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Modified: `src/roles/apache-php/templates/httpd.conf.j2`
  - Modified: `src/roles/apache-php/templates/php-fpm-httpd.conf.j2`
  - Modified: `src/roles/apache/tasks/main.yml`
  - Modified: `src/roles/apache/templates/httpd.conf.j2`
  - Modified: `src/roles/apache/templates/php-fpm-httpd.conf.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/create-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/htdocs/README.md`
  - Modified: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/index.php`
  - Modified: `src/roles/htdocs/meta/main.yml`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/BlenderSettings.php.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-rebuild-all.sh.j2`
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`
  - Modified: `src/scripts/unifyUserTables.php`

* [58b07019](https://github.com/freephile/meza/commit/58b07019) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_logs_deploy with m_data_deploy_log_file
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/scripts/meza.py`

* [9e651e69](https://github.com/freephile/meza/commit/9e651e69) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_tmp with m_data_tmp_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/roles/autodeployer/templates/git-fetch.sh.j2`
  - Modified: `src/roles/backup-db-wikis-push/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis/tasks/main.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/database/tasks/replication.yml`
  - Modified: `src/roles/dump-db-wikis/tasks/main.yml`
  - Modified: `src/roles/enforce-meza-version/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/import-wiki-sql.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/transfer-backup-to-db-master.yml`
  - Modified: `tests/deploys/setup-alt-source-backup.yml`

* [280f2578](https://github.com/freephile/meza/commit/280f2578) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_logs with m_data_logs_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/defaults.yml`
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/rebuild-smw-and-index.yml`
  - Modified: `src/roles/apache-php/templates/php.ini.j2`
  - Modified: `src/roles/autodeployer/templates/meza-autodeployer-cron.j2`
  - Modified: `src/roles/backups-cleanup/templates/meza-cron-backups-cleanup.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/cron/templates/meza-ansible.crontab.j2`
  - Modified: `src/roles/elasticsearch/tasks/es_reindex.yml`
  - Modified: `src/roles/logrotate/tasks/main.yml`
  - Modified: `src/roles/logrotate/templates/cleanup-backups.sh.j2`
  - Modified: `src/roles/logrotate/templates/meza-logs.j2`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-rebuild-all.sh.j2`
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Modified: `src/roles/php/templates/php.ini.j2`
  - Modified: `src/roles/update.php/tasks/main.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`
  - Modified: `src/scripts/meza.py`

* [4b099b3d](https://github.com/freephile/meza/commit/4b099b3d) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_cache_directory with m_data_cache_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`

* [153f5fca](https://github.com/freephile/meza/commit/153f5fca) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_backups with m_data_backups_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/backup-config/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis-push/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis/tasks/main.yml`
  - Modified: `src/roles/backup-uploads-push/tasks/main.yml`
  - Modified: `src/roles/backup-uploads/tasks/main.yml`
  - Modified: `src/roles/backups-cleanup/templates/backups-cleanup.sh.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/index.php`
  - Modified: `src/roles/logrotate/tasks/main.yml`
  - Modified: `src/roles/logrotate/templates/cleanup-backups.sh.j2`
  - Modified: `src/roles/sql-backup-cleanup/tasks/main.yml`
  - Modified: `src/roles/update.php/tasks/main.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`

* [dd62a84a](https://github.com/freephile/meza/commit/dd62a84a) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_logs_create_wiki with m_data_create_wiki_log_file
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/scripts/meza.py`

* [397298ae](https://github.com/freephile/meza/commit/397298ae) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_meza_data with m_data_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/delete-elasticsearch.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`
  - Modified: `src/roles/elasticsearch/templates/elasticsearch.yml.j2`
  - Modified: `src/roles/mediawiki/tasks/cirrus_metastore_upgrade.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`
  - Modified: `src/scripts/meza.py`
  - Modified: `src/scripts/unifyUserTables.php`

* [669d68e2](https://github.com/freephile/meza/commit/669d68e2) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_local_secret with m_config_secret_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `.github/copilot-instructions.md`
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/setup-env/tasks/main.yml`
  - Modified: `src/scripts/meza.py`

* [f6325884](https://github.com/freephile/meza/commit/f6325884) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_local_public with m_config_public_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/playbooks/cleanup-upload-stash.yml`
  - Modified: `src/playbooks/migrate-wikis.yml`
  - Modified: `src/playbooks/run-maintenance.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/apache-php/tasks/profiling.yml`
  - Modified: `src/roles/backup-config/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis-push/tasks/main.yml`
  - Modified: `src/roles/backup-db-wikis/tasks/main.yml`
  - Modified: `src/roles/backup-uploads-push/tasks/main.yml`
  - Modified: `src/roles/backup-uploads/tasks/main.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/configure-wiki/README.md`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Modified: `src/roles/configure-wiki/templates/preLocalSettings.d/base.php.dist.j2`
  - Modified: `src/roles/delete-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/dump-db-wikis/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/migrate-to-declarative-wikis/tasks/main.yml`
  - Modified: `src/roles/php/tasks/profiling.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/sync-configs/tasks/main.yml`

* [d4e0b410](https://github.com/freephile/meza/commit/d4e0b410) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_i18n with m_config_i18n_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/scripts/meza.py`
  - Modified: `src/scripts/ssh-users/setup-minion-user.sh`

* [2e250f24](https://github.com/freephile/meza/commit/2e250f24) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_deploy with m_config_deploy_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/rebuild-smw-and-index.yml`
  - Modified: `src/roles/backups-cleanup/tasks/main.yml`
  - Modified: `src/roles/backups-cleanup/templates/meza-cron-backups-cleanup.j2`
  - Modified: `src/roles/base-config-scripts/tasks/main.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/create-wiki-wrapper/tasks/main.yml`
  - Modified: `src/roles/cron/templates/meza-ansible.crontab.j2`
  - Modified: `src/roles/elasticsearch/tasks/es_reindex.yml`
  - Modified: `src/roles/htdocs/files/BackupDownload/DownloadTest.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/download.php`
  - Modified: `src/roles/htdocs/files/BackupDownload/index.php`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-build-index.sh.j2`
  - Modified: `src/roles/mediawiki/templates/elastic-rebuild-all.sh.j2`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/saml/templates/NonMediaWikiSimpleSamlAuth.php.j2`
  - Modified: `src/roles/saml/templates/samlLocalSettings.php.j2`
  - Modified: `src/roles/sync-configs/tasks/main.yml`
  - Modified: `src/roles/verify-wiki/tasks/main.yml`
  - Modified: `src/scripts/unifyUserTables.php`

* [50dbfa3a](https://github.com/freephile/meza/commit/50dbfa3a) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_config_core with m_config_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`

* [81c26718](https://github.com/freephile/meza/commit/81c26718) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_test with m_app_tests_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/path_alias.yml`
  - Modified: `config/paths.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`

* [db561daf](https://github.com/freephile/meza/commit/db561daf) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_scripts with m_app_scripts_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/logrotate/tasks/main.yml`
  - Modified: `src/scripts/getmeza.sh`
  - Modified: `src/scripts/ssh-users/setup-master-user.sh`
  - Modified: `src/scripts/ssh-users/transfer-master-key.sh`
  - Modified: `src/scripts/unite-the-wikis.sh`

* [bbc151ca](https://github.com/freephile/meza/commit/bbc151ca) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_meza with m_app_dir
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `config/paths.yml`
  - Modified: `manual/APACHE_PHP_SPLIT_IMPLEMENTATION.md`
  - Modified: `manual/MEZA_USER_ROLE.md`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/roles/autodeployer/templates/git-fetch.sh.j2`
  - Modified: `src/roles/autodeployer/templates/slack-notify.sh.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/enforce-meza-version/tasks/main.yml`
  - Modified: `src/roles/htdocs/README.md`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/scripts/unifyUserTables.php`

* [ed048685](https://github.com/freephile/meza/commit/ed048685) (2026-02-08) Greg Rundlett: Normalize meza variables replaced m_install with m_install_dir
removed TODO comments from paths.yml
created path_alias.yml with variable map
Addresses Issue [#286](https://github.com/freephile/meza/issues/286)
  - Modified: `.github/copilot-instructions.md`
  - Added: `config/path_alias.yml`
  - Modified: `config/paths.yml`
  - Modified: `manual/MEZA_USER_ROLE.md`
  - Modified: `manual/meza-cmd/debug.md`
  - Modified: `src/roles/autodeployer/templates/git-fetch.sh.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.php.j2`
  - Modified: `src/roles/base-config-scripts/templates/config.sh.j2`
  - Modified: `src/roles/configure-wiki/templates/preLocalSettings.d/base.php.dist.j2`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/htdocs/templates/index.php.j2`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/mediawiki/templates/refresh-links.sh.j2`
  - Modified: `src/roles/mediawiki/templates/smw-rebuild-all.sh.j2`
  - Modified: `src/roles/meza-log/templates/disk-space-usage.sh.j2`
  - Modified: `src/roles/meza-log/templates/server-performance.sh.j2`
  - Modified: `src/roles/netdata/tasks/main.yml`
  - Modified: `src/roles/saml/templates/SAMLConfig.php.j2`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/setup-env/templates/secret.yml.j2`
  - Modified: `src/scripts/getmeza.sh`
  - Modified: `src/scripts/meza.py`

* [e39ddc92](https://github.com/freephile/meza/commit/e39ddc92) (2026-02-08) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [c54bb580](https://github.com/freephile/meza/commit/c54bb580) (2026-02-07) Greg Rundlett: Add new 'reminder' provisioner to Vagrantfile Echo instructions so it's very easy to get the first deploy done.
Addresses Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `Vagrantfile`

* [ddfe42b4](https://github.com/freephile/meza/commit/ddfe42b4) (2026-02-06) Greg Rundlett: Set `check_mode: false` (meaning always run) The pattern:
For tasks that DO NOT HAVE SIDE-EFFECTS, such as read-only tasks, that
register a variable or set a fact, which is then used to DO something
and possibly FAIL, be sure to use `check_mode: false` on the read-only
task. This way the task runs always; even when you test a playbook by
using `--check` mode (aka **`--dry-run`** in other software)
Without this pattern, trying to test your playbooks in `--check` mode
can cause them to fail for no good reason since the read-only task
would be skipped and the registered variable would be empty.
For example: "check if user is in group_apache"
Also, Format verify-permissions role
Place the user/group checks first
Use variable `{{ m_user }}` instead of hard-coded 'meza-ansible'
Use variable `{{ user_apache }}` and `{{ group_apache }}` instead of
hard-coded 'apache'
Comment/disable `{{ m_uploads_dir }}` in permission fix because it can
be huge, should not fail, and is not a routine operation.
It should be handled separately.
Remove extraneous 'when: RedHat'
Add USAGE instructions at the top of the verify-permissions playbook,
just like the role, for quick reference.
  - Modified: `src/playbooks/verify-permissions.yml`
  - Modified: `src/roles/apache-php/tasks/php-redhat8.yml`
  - Modified: `src/roles/apache-php/tasks/profiling.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/elasticsearch/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/meza-user/tasks/main.yml`
  - Modified: `src/roles/php/tasks/profiling.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`

* [b0792e05](https://github.com/freephile/meza/commit/b0792e05) (2026-02-06) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

origin/issue287-separate-apache
* [a55e46d3](https://github.com/freephile/meza/commit/a55e46d3) (2026-02-05) Greg Rundlett: Fix linting issues with netdata role Added proper names to the debug tasks instead of 'free-form'
Added `set -o pipefail` and `executable: /bin/bash` to shell that uses
pipes.
Added `change_when` false to integrity-check (read-only) and true to
install task (it actually installs)
Switched to the command module for the installer because no shell
features are actually needed **in the task** and we can still invoke
the shell (`sh foo.sh`) as the command.
Fixes Issue [#16](https://github.com/freephile/meza/issues/16)
  - Modified: `src/roles/netdata/tasks/main.yml`

* [23fdc901](https://github.com/freephile/meza/commit/23fdc901) (2026-02-05) Greg Rundlett: Improve logrotate role based on separate apache In the logrotate configuration file template for
`/etc/logrotate.d/meza-logs`, remove defensive fallback logic based on
complicated 'getent_group' since apache is guaranteed to be installed.
Formerly the 'if' conditions were complicated and the fallbacks would
introduce permission problems by using 'root' instead of intentional
variables such as `logrotate_deploy_logs.create_owner`.
Remove whole duplicate "Fix directory permissions after apache installation"
because apache is guaranteed to be installed.
Remove 'ignore errors' flag so we're not silently failing.
Add whole section in the role README.md on Testing and Deployment
Fixes Issue [#287](https://github.com/freephile/meza/issues/287)
  - Modified: `src/roles/logrotate/README.md`
  - Modified: `src/roles/logrotate/tasks/main.yml`
  - Modified: `src/roles/logrotate/templates/meza-logs.j2`

* [d0971019](https://github.com/freephile/meza/commit/d0971019) (2026-02-05) Greg Rundlett: Fix deploy with separate apache, php roles Fix profiling per-wiki override logic while also fixing deploys on
fresh Vagrant infrastructure where `wikis` isn't defined yet. This
fixes an issue with Vagrant where you used to need to
- 'deploy'->
- 'create wiki'->
- 'deploy' (again)
to get started.
Now, the demo wiki is created on first deploy in Vagrant the same as
before with 'monolith' environments.
- Add new play "Ensure demo wiki exists if no wikis configured" to site
playbook which runs **before** app server configuration (before the PHP
role). This ensures that the `wikis` variable is available when the PHP
role runs (and invokes the profiling tasks).
- Remove the same play from the `mediawiki` role; and leave a comment
in its place.
Fixes Issue [#287](https://github.com/freephile/meza/issues/287)
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/php/templates/postLocalSettings.d/profiling.php.j2`

* [5edb1811](https://github.com/freephile/meza/commit/5edb1811) (2026-02-05) Greg Rundlett: Split apache-php into separate roles - make note in Vagrantfile that getmeza.sh installs Apache
- add apache installation into getmeza.sh
- add doc in 'manual' for Apache-PHP split implementation
- split old role in site.yml
- change deploy lock file ownership in meza.py to enforce the architectural
guarantee that Apache is installed during bootstrap. Fail fast with helpful
guidance if the system isn't properly configured.
- Add FIXME for removing RedHat 7 Issue [#290](https://github.com/freephile/meza/issues/290)
- no need for defaults and fallbacks in paths.yml when group_apache is a
pre-requisite
- the apache task no longer attempts to create or fix m_public/wikis started in
init-controller because that is not apache's concern
- replace complex getent module with simple getent command and return code in
init-controller-config to fail fast if the prerequisite apache is not present
then use proper group variable for setting ownership instead of silent fallbacks
- add new meta file for apache-php role to describe it as deprecated
- copy prior httpd.conf and php-fpm conf templates into new apache role
- copy `etc-sysconfig-httpd` template into new apache role
- add large deprecation notice at the top of the apache-php task file
- add meta file for apache-php that invokes the separate roles as pre-requisites
- add README.md for the apache-php role that explains the deprecation
- add README.md for the meza-user role explaining boostrap sequence
- fix the  PHP profiling logic for per-wiki overrides
- copy README_PROFILING.md into new php role
and the rest of the php role files
- README.md
- meta/main.yml
- README_PROFILING.md
- handlers/main.yml
- templates/php.ini.j2
- templates/10-opcache.ini.j2
- templates/www.conf.j2
- templates/postLocalSettings.d/profiling.php.j2
- templates/20-xhprof.ini.j2
- templates/20-sqlsrv.ini.j2
- templates/freetds.conf.j2
- templates/40-memcached.ini.j2
- templates/php.conf
- templates/30-pdo_sqlsrv.ini.j2
- templates/logrotate-profiler.j2
- defaults/main.yml
- tasks/php-redhat8.yml
- tasks/main.yml
- tasks/mssql_driver_for_php.yml
- tasks/php-debian.yml
- tasks/php-redhat7.yml
- tasks/profiling.yml
- tasks/php.yml
Issue [#287](https://github.com/freephile/meza/issues/287) is ready for testing
  - Modified: `Vagrantfile`
  - Modified: `config/RedHat.yml`
  - Modified: `config/paths.yml`
  - Added: `manual/APACHE_PHP_SPLIT_IMPLEMENTATION.md`
  - Modified: `src/playbooks/site.yml`
  - Added: `src/roles/apache-php/README.md`
  - Added: `src/roles/apache-php/meta/main.yml`
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Added: `src/roles/apache/README.md`
  - Added: `src/roles/apache/defaults/main.yml`
  - Added: `src/roles/apache/handlers/main.yml`
  - Added: `src/roles/apache/meta/main.yml`
  - Added: `src/roles/apache/tasks/main.yml`
  - Added: `src/roles/apache/templates/etc-sysconfig-httpd.j2`
  - Added: `src/roles/apache/templates/httpd.conf.j2`
  - Added: `src/roles/apache/templates/php-fpm-httpd.conf.j2`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Added: `src/roles/meza-user/README.md`
  - Added: `src/roles/php/README.md`
  - Added: `src/roles/php/README_PROFILING.md`
  - Added: `src/roles/php/defaults/main.yml`
  - Added: `src/roles/php/handlers/main.yml`
  - Added: `src/roles/php/meta/main.yml`
  - Added: `src/roles/php/tasks/main.yml`
  - Added: `src/roles/php/tasks/mssql_driver_for_php.yml`
  - Added: `src/roles/php/tasks/php-debian.yml`
  - Added: `src/roles/php/tasks/php-redhat7.yml`
  - Added: `src/roles/php/tasks/php-redhat8.yml`
  - Added: `src/roles/php/tasks/php.yml`
  - Added: `src/roles/php/tasks/profiling.yml`
  - Added: `src/roles/php/templates/10-opcache.ini.j2`
  - Added: `src/roles/php/templates/20-sqlsrv.ini.j2`
  - Added: `src/roles/php/templates/20-xhprof.ini.j2`
  - Added: `src/roles/php/templates/30-pdo_sqlsrv.ini.j2`
  - Added: `src/roles/php/templates/40-memcached.ini.j2`
  - Added: `src/roles/php/templates/freetds.conf.j2`
  - Added: `src/roles/php/templates/logrotate-profiler.j2`
  - Added: `src/roles/php/templates/php.conf`
  - Added: `src/roles/php/templates/php.ini.j2`
  - Added: `src/roles/php/templates/postLocalSettings.d/profiling.php.j2`
  - Added: `src/roles/php/templates/www.conf.j2`
  - Modified: `src/scripts/getmeza.sh`
  - Modified: `src/scripts/meza.py`

* [9effcfd5](https://github.com/freephile/meza/commit/9effcfd5) (2026-02-04) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [50657c90](https://github.com/freephile/meza/commit/50657c90) (2026-02-04) Greg Rundlett: use set-vars in setup-meza-user playbook - Prepare for Issue [#287](https://github.com/freephile/meza/issues/287) - splitting the apache-php role
- Comment paths.yml for Issue [#286](https://github.com/freephile/meza/issues/286) - normalize variable names
- Simplify group detection in the meza-user role
- Make FQCN edits to pass linting on set-vars role for Issue [#16](https://github.com/freephile/meza/issues/16)
  - Modified: `config/paths.yml`
  - Modified: `src/playbooks/setup-meza-user.yml`
  - Modified: `src/roles/meza-user/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`

* [9bd4e14f](https://github.com/freephile/meza/commit/9bd4e14f) (2026-02-03) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [482739a0](https://github.com/freephile/meza/commit/482739a0) (2026-02-03) Greg Rundlett: distribute 'dist' files for configuration Since the file names are new, pre-existing customizations will be
safe.
- Needed to rename the template files, not just the target files
Also fix linting with FQCN and
improve the task key order to: name, delegate_to, run_once, block
Fixes Issue [#270](https://github.com/freephile/meza/issues/270)
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
R100	src/roles/configure-wiki/templates/preLocalSettings.d/base.php.j2	src/roles/configure-wiki/templates/preLocalSettings.d/base.php.dist.j2
R099	src/roles/configure-wiki/templates/samlAuthorizations.d/base.php.j2	src/roles/configure-wiki/templates/samlAuthorizations.d/base.php.dist.j2

* [461a8b10](https://github.com/freephile/meza/commit/461a8b10) (2026-02-03) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [72833be2](https://github.com/freephile/meza/commit/72833be2) (2026-02-03) Greg Rundlett: switch to 'dist' files for configuration Since the file names are new, pre-existing customizations will be
safe.
Since the distributed 'base.php.dist' file is now propagated, users
will receive new instructions and content for replication in 'config'
repos.
Also fix linting with FQCN and
improve the task key order to: name, delegate_to, run_once, block
Fixes Issue [#270](https://github.com/freephile/meza/issues/270)
  - Modified: `src/roles/configure-wiki/tasks/main.yml`

* [e537e1be](https://github.com/freephile/meza/commit/e537e1be) (2026-02-03) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [c54781e2](https://github.com/freephile/meza/commit/c54781e2) (2026-02-03) Greg Rundlett: Add audit permissions script for Issue [#272](https://github.com/freephile/meza/issues/272) 
  - Added: `src/scripts/audit-permissions.sh`

* [992b77f2](https://github.com/freephile/meza/commit/992b77f2) (2026-02-03) Greg Rundlett: add exports to the lint-files.sh script Adding exports for meza's local Config and Roles path allows linters
to find the right sources.
  - Modified: `src/scripts/lint-files.sh`

* [a8649f3d](https://github.com/freephile/meza/commit/a8649f3d) (2026-02-03) Greg Rundlett: Update Medik skin repo source and version The Medik skin is now on GitHub and the version is a commit SHA
The former bitbucket URL no longer exists.
  - Modified: `config/MezaCoreSkins.yml`

origin/issue270-logo
* [5d355f9d](https://github.com/freephile/meza/commit/5d355f9d) (2026-02-03) Greg Rundlett: Add back logo.png for legacy references logo.png usage is DEPRECATED however it is being added back for old
references that may exist in the wild. Do not rely on this file being
present.
Fix-up (temporarily) internal project references to 'logo.png'.
These playbooks and roles still need to be reviewed and modernized.
- check-for-changes
- push-backups
- autodeployer and slack-notify
Fixes Issue [#270](https://github.com/freephile/meza/issues/270)
  - Modified: `config/defaults.yml`
  - Modified: `src/playbooks/check-for-changes.yml`
  - Modified: `src/playbooks/push-backup.yml`
  - Modified: `src/roles/autodeployer/tasks/do-deploy.yml`
  - Modified: `src/roles/autodeployer/templates/slack-notify.sh.j2`
  - Added: `src/roles/configure-wiki/files/logo.png`

* [19a969fc](https://github.com/freephile/meza/commit/19a969fc) (2026-02-03) Greg Rundlett: New Feature: custom branding Integrate the htdocs role with the configure-wiki and mediawiki roles
so that there is a three-tier override for branding assets:
3. Per-wiki customization via upload
2. Per-wiki customization version-controlled and distributed fron config
file system on the controller.
1. Project-wide default set by htdocs role
Fixes Issue [#270](https://github.com/freephile/meza/issues/270)
  - Modified: `src/roles/configure-wiki/templates/preLocalSettings.d/base.php.j2`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [0796267d](https://github.com/freephile/meza/commit/0796267d) (2026-02-02) Greg Rundlett: correct co-pilot instructions 
  - Modified: `.github/copilot-instructions.md`

* [bc313c66](https://github.com/freephile/meza/commit/bc313c66) (2026-02-02) Greg Rundlett: Improve branding w configure-wiki and htdocs roles - Improve  `configure-wiki` role that sets up wiki configuration
scaffolding with wgLogos files.
  - Added metadata and task header comments improving documentation
  - Add group write permission for created files and directories.
- Add task header comments in `htdocs` role which manages web-accessible
content in Apache's document root.
- Use FQCN to pass linting
- Update `LocalSettings.php` template to use $wgLogos multiple logo sizes.
- Add $wgFavicon
- Add $wgAppleTouchIcon
- Added README documentation for both roles detailing their purpose,
usage, and configuration.
- Remove deprecated single 'logo.png'
Fixes Issue [#270](https://github.com/freephile/meza/issues/270)
  - Modified: `config/defaults.yml`
  - Added: `src/roles/configure-wiki/README.md`
  - Added: `src/roles/configure-wiki/files/apple-touch-icon.png`
  - Modified: `src/roles/configure-wiki/files/favicon.ico`
  - Deleted: `src/roles/configure-wiki/files/logo.png`
  - Added: `src/roles/configure-wiki/files/meza-icon-50.svg`
  - Added: `src/roles/configure-wiki/files/meza-logo-1.5x.png`
  - Added: `src/roles/configure-wiki/files/meza-logo-135.png`
  - Added: `src/roles/configure-wiki/files/meza-logo-2x.png`
  - Added: `src/roles/configure-wiki/files/meza-logo-inkscape.svg`
  - Added: `src/roles/configure-wiki/meta/main.yml`
  - Modified: `src/roles/configure-wiki/tasks/main.yml`
  - Added: `src/roles/htdocs/README.md`
  - Added: `src/roles/htdocs/meta/main.yml`
  - Modified: `src/roles/htdocs/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/scripts/lint-files.sh`

* [06dad963](https://github.com/freephile/meza/commit/06dad963) (2026-01-29) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [fc1a74d8](https://github.com/freephile/meza/commit/fc1a74d8) (2026-01-29) Greg Rundlett: Use MediaWiki REL1_43 branch v 1.43.6 tag This updates critical issue with PHPUnit
  - Modified: `config/defaults.yml`

origin/issue279-netdata
* [d454a1b8](https://github.com/freephile/meza/commit/d454a1b8) (2026-01-29) Greg Rundlett: Fix netdata installation Use POSIX shell, avoid bashism like process substitution
Add integrity check on the installer before using it.
Fixes Issue [#279](https://github.com/freephile/meza/issues/279)
  - Modified: `src/roles/netdata/tasks/main.yml`

origin/issue272-fix-permissions
* [d8377bf4](https://github.com/freephile/meza/commit/d8377bf4) (2026-01-27) Greg Rundlett: Fix permissions and extract user creation Performance benchmarks on Vagrant:
- 3 min for vagrant up (first time)
- 21:24 for meza deploy (first time)
- 43 sec for create wiki (mw-debug perm error on page view)
- 4 min for verify-permissions (fixes 'mediawiki' dir)
- 3:42 for meza deploy (second time)
The `meza-user` Ansible role replaces the previous bash scripts
(`linux-user.sh`, `setup-master-user.sh`) for managing the meza-ansible
user.
This provides better idempotency, testability, and integration with the
Ansible deployment workflow.
== Specific changes ==
src/scripts/getmeza.sh
- add setup-meza-user playbook with fallback on
setup-master-user.sh script
src/scripts/shell-functions/linux-user.sh
- enhance by sourcing shell initialization files
- also replace tabs with spaces for formatting
MEZA_USER_ROLE.md documents the new approach for creating the
meza-ansible user.
PATH_FIX.md documents how the typical user path is setup on Linux.
Vagrantfile
print out the 'groups' and home directory configuration of the
meza-ansible user
paths.yml
- use literal meza-ansible in places
- use group_apache instead of group_wheel for m_htdocs_group
src/playbooks/setup-meza-user.yml
- new playbook to setup the meza-ansible service account instead of
doing it with shell scripts.
src/playbooks/site.yml
- Add set-vars to umask-set so that it can use the m_umask variable.
- The whole umask-set and umask-unset roles should be avoidable.
src/roles/apache-php/tasks/main.yml
- use meza-ansible owner of htdocs
src/roles/ansible-role-certbot-meza/tasks/main.meza.yml
src/roles/base/tasks/main.yml
src/roles/cron/tasks/main.yml
src/roles/database/tasks/secure-installation.yml
src/roles/essential-vars/tasks/main.yml
src/roles/saml/tasks/main.yml
src/roles/meza-log/tasks/main.yml
- use meza-ansible explicitly
src/roles/enforce-meza-version/tasks/main.yml
src/roles/mediawiki/tasks/main.yml
src/roles/saml/tasks/main.yml
src/roles/umask-set/templates/umask.profile.sh.j2
- use m_umask variable instead of hard-coding it
After create wiki, a deploy fails on dubious ownership of 'mediawiki'
To correct it, you can run the verify-permissions playbook in 4 minutes,
and then deploy but WHY is it failing? The ownership needs to be ironed
out.
These 4 files were incorrect:
and thus later git ops would fail with dubious ownership
'mediawiki' dir owned by apache instead of meza-ansible
"Changed files: [
'/opt/htdocs/mediawiki',
'/opt/htdocs/mediawiki/extensions/Widgets/compiled_templates',
'/opt/htdocs/mediawiki/extensions/Widgets/compiled_templates/.htaccess',
'/opt/htdocs/mediawiki/vendor/microsoft/tolerant-php-parser/php-langspec/spec/php-spec-draft.md']
src/roles/init-controller-config/tasks/main.yml
- make group_apache group ownership conditional for cases where apache
doesn't even exist yet.
- Add note that the role needs to be part of a refactor
src/roles/mediawiki/templates/LocalSettings.php.j2
- move the mw-debug.log file into the logs/mediawiki directory where it
can be properly written by apache
src/roles/set-vars/tasks/main.yml
- make the set-vars role not fail when public.yml does not yet exist
Fixes Issue [#272](https://github.com/freephile/meza/issues/272)
  - Modified: `Vagrantfile`
  - Modified: `config/paths.yml`
  - Added: `manual/MEZA_USER_ROLE.md`
  - Modified: `manual/PATH_FIX.md`
  - Added: `src/playbooks/setup-meza-user.yml`
  - Modified: `src/playbooks/site.yml`
  - Modified: `src/roles/ansible-role-certbot-meza/tasks/main.meza.yml`
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Modified: `src/roles/base/tasks/main.yml`
  - Modified: `src/roles/cron/tasks/main.yml`
  - Modified: `src/roles/database/tasks/secure-installation.yml`
  - Modified: `src/roles/enforce-meza-version/tasks/main.yml`
  - Modified: `src/roles/essential-vars/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`
  - Modified: `src/roles/meza-log/tasks/main.yml`
  - Added: `src/roles/meza-user/defaults/main.yml`
  - Added: `src/roles/meza-user/tasks/main.yml`
  - Added: `src/roles/meza-user/templates/bash_profile.j2`
  - Added: `src/roles/meza-user/templates/bashrc.j2`
  - Modified: `src/roles/saml/tasks/main.yml`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/roles/umask-set/templates/umask.profile.sh.j2`
  - Modified: `src/scripts/getmeza.sh`
  - Modified: `src/scripts/shell-functions/linux-user.sh`

* [4f3152bb](https://github.com/freephile/meza/commit/4f3152bb) (2026-01-20) Greg Rundlett: Add better vagrant deploy instructions in comments 
  - Modified: `vagrantconf.default.yml`

* [92636735](https://github.com/freephile/meza/commit/92636735) (2026-01-20) Greg Rundlett: public.yml is neccessary Remove the 'failed_when: false" for public.yml
public/public.yml is required.
Remove include_vars for 'secret/secret.yml' There is no such thing.
Addresses Issue [#272](https://github.com/freephile/meza/issues/272)
  - Modified: `src/roles/set-vars/tasks/main.yml`

* [b5a4fbfd](https://github.com/freephile/meza/commit/b5a4fbfd) (2026-01-20) Greg Rundlett: Extract directory and permissions into role - remove 'ignore submodules' before MediaWiki is installed
ignore is repeated on line 88
- remove 'failed_when: false' in mediawiki clone
- extract directory setup and permission checking for 'data-meza'
into the verify-permissions role.
- add easy-to-read output for directory setup
Addresses Issue [#272](https://github.com/freephile/meza/issues/272)
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`

* [3e9dda34](https://github.com/freephile/meza/commit/3e9dda34) (2026-01-20) Greg Rundlett: Fix up paths.yml for permissions mgmt - use 4-digit mode settings
- add leading 2 for group sticky bit
- avoids problems with leading zero
- add missing group `m_cache_directory_group`
- add missing `m_logs_group`
Addresses Issue [#272](https://github.com/freephile/meza/issues/272)
  - Modified: `config/paths.yml`

* [b0d9ddff](https://github.com/freephile/meza/commit/b0d9ddff) (2026-01-20) Greg Rundlett: create new variable m_umask Also, fix up examples of profiling
Remove erroneous namespaced public.yml references
Addresses Issue [#272](https://github.com/freephile/meza/issues/272)
  - Modified: `config/defaults.yml`

* [1d5f8657](https://github.com/freephile/meza/commit/1d5f8657) (2026-01-20) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [d5fa3e62](https://github.com/freephile/meza/commit/d5fa3e62) (2026-01-20) Greg Rundlett: Correct erroneous mentions of namespaced public.yml The 'public.yml' file is shared by ALL wikis in a Meza instance.
PHP directory structures in 'conf-meza' still allow for customization
of each wiki.
The 'secret.yml' files are namespaced by <env> within the Meza instance
so that you can have separate values or configurations as needed.
  - Modified: `.github/copilot-instructions.md`
  - Modified: `manual/meza-cmd/config.md`
  - Modified: `manual/meza-cmd/deploy-notify.md`
  - Modified: `manual/meza-cmd/migrate-wikis.md`
  - Modified: `src/roles/apache-php/README_PROFILING.md`
  - Modified: `src/roles/logrotate/README.md`
  - Modified: `src/roles/set-vars/tasks/main.yml`
  - Modified: `src/scripts/cleanup-backups.md`

* [3415e45a](https://github.com/freephile/meza/commit/3415e45a) (2026-01-20) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [49e7c39e](https://github.com/freephile/meza/commit/49e7c39e) (2026-01-20) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

origin/issue268-better-dev
* [a610b5f7](https://github.com/freephile/meza/commit/a610b5f7) (2026-01-19) Greg Rundlett: Add blank known_hosts file to avoid error in dev Probably a code smell. Investigate later. known_hosts is created in
multiple other roles that seem loosely organized and definitely not
documented.
Final fix for Issue [#268](https://github.com/freephile/meza/issues/268) Better Dev Environments with Vagrant
  - Modified: `Vagrantfile`

* [94efecef](https://github.com/freephile/meza/commit/94efecef) (2026-01-17) Greg Rundlett: remove problematic initialization The 'sophisticated' conditioning of the Vagrant box during
initialization caused problems with the vagrant-vbguest plugin
detecting completion - resulting in a "hung" `vagrant up` because the
terminal prompt would not return. The box got created, but the prompt
was never released.
Fixes Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `Vagrantfile`

* [158abdf8](https://github.com/freephile/meza/commit/158abdf8) (2026-01-17) Greg Rundlett: Add comments to Vagrant configuration 
  - Modified: `vagrantconf.default.yml`

* [d2395cf4](https://github.com/freephile/meza/commit/d2395cf4) (2026-01-17) Greg Rundlett: rebuild Vagrant infrastructure In the Vagrantfile...
Used generic/rocky8 for baseBox for VirtualBox compatibility.
Increased boot time to 10 min for slower systems.
Add VBGuest installer hooks before install:
- Wait up to 60 seconds for network connectivity (ping 8.8.8.8)
- Install build dependencies (with retry)
- Pause briefly so system settles and to avoid RockyLinux boot issues.
- VirtualBox Guest Additions installer runs (automatic, configured by
vbguest plugin)
Without these dependencies, VirtualBox Guest Additions compilation fails,
causing:
- No shared folder support (/opt/meza mount fails)
- Poor VM performance (no graphics acceleration)
- Time sync issues between host and guest
The retry logic specifically addresses Rocky Linux's occasional slow
network initialization on first boot.
Add graphics controller for VirtualBox compatibility
Missing SSH Keys Fix:
Modified the Vagrantfile getmeza provisioner to:
- Check if files exist before trying to move them
- Create .ssh directory before attempting file operations
- Show warning messages if keys aren't found (helps debug the issue)
- Removed rm -rf commands that were pointlessly trying to remove files
that don't exist yet
Fix Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `Vagrantfile`

* [b65cb79e](https://github.com/freephile/meza/commit/b65cb79e) (2026-01-16) Greg Rundlett: improve getmeza.sh (setup-env) The setup-env role would pollute the output of `vagrant up` by
dumping the entire Ansible 'vars'
Now gate it on the value of `m_force_debug`
related to Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `src/roles/setup-env/tasks/main.yml`

* [d80b6e21](https://github.com/freephile/meza/commit/d80b6e21) (2026-01-16) Greg Rundlett: improve getmeza.sh The script is now ~40% shorter, easier to maintain, and only supports
platforms that are actively maintained and relevant for modern MediaWiki.
Complete refactor removing EOL distros CentOS, RHEL 7.x
Note: more work to remove related code
Remove sed workarounds for old incompatible packages.
Modern Rocky/RHEL 8 repos don't have conflicting ansible packages.
We install ansible via pip explicitly (not dnf)
Add `--root-user-action=ignore` to intentional system-wide pip commands
Python 3.6 is the base, python38 conflicts are no longer relevant.
The exclusions were workarounds for old repo states.
Ansible is now installed system-wide vs. user
Simplified Repository Setup
- Single code path for Rocky 8 and RHEL 8
- Clear error messages for unsupported versions
- Better diagnostic output for PowerTools/CRB repository
- `libmemcached-devel` is in the PowerTools repository.
Consolidated package installation into one `dnf install`
Better Error Handling
- Version checking with clear error messages
- Repository verification with diagnostic output
Cleaner Structure
- Removed nested case statements
- Consolidated duplicate code
- Better comments explaining each section
- More consistent echo statements for progress tracking every time, not
just when EPEL is missing
- Made PowerTools enablement idempotent - Checks if already enabled
before trying to enable it
- Added verification after enabling - Confirms PowerTools is actually
in the enabled repos list
- Removed the EPEL check wrapper - Repository configuration now runs
- Separated EPEL installation - EPEL check is now independent of
PowerTools enablement
Developer note: you can update your VM while it's running to reflect
changes made to the Vagrantfile.
E.g. from your host, invoke
`vagrant provision app1 --provision-with getmeza`
Fix for Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `src/scripts/getmeza.sh`

* [edb16345](https://github.com/freephile/meza/commit/edb16345) (2026-01-15) Greg Rundlett: improve Vagrant for better local development - make the same fix in the 'base' role:
  when creating users do not move_home
- add scripts and documentation about fixing permission bits, umask,
  and shares in Vagrant
Fixes Issue [#268](https://github.com/freephile/meza/issues/268)
  - Added: `manual/PATH_FIX.md`
  - Added: `manual/VBOX_755_MIGRATION_COMPLETE.md`
  - Added: `manual/VBOX_MANUAL_VM.md`
  - Added: `manual/VBOX_PERMISSIONS.md`
  - Modified: `src/roles/base/tasks/main.yml`
  - Added: `src/scripts/fix-meza-command.sh`
  - Added: `src/scripts/fix-vbox-permissions.sh`
  - Added: `src/scripts/setup-manual-vbox-mount.sh`
  - Modified: `vagrantconf.default.yml`

* [b8d583df](https://github.com/freephile/meza/commit/b8d583df) (2026-01-15) Greg Rundlett: fix Vagrantfile for permissions, UID, GID Enable it so that you can work and commit from your host while files in the guest also appear correctly.
For Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `Vagrantfile`

* [b1e9840b](https://github.com/freephile/meza/commit/b1e9840b) (2026-01-15) Greg Rundlett: prevent alt-meza-ansible from blocking deploy Remove the 'move_home' option - it is wrong to include it here.
Current code will properly "Ensure controller has user alt-meza-ansible
- If the user doesn't exist: Ansible creates it and sets up the home directory
- If the user exists: Ansible updates the home path if needed
- If the directory already exists: Ansible will use it
(no need to "move" it)
When the alt-meza-ansible user exists, but you change something about
the user (like their login config to include traditional system paths
such as /usr/bin) then a subsequent deploy can block on
'Ensure controller has user alt-meza-ansible user' due to the 'move_home'
option which should not be used.
The move_home parameter is only meaningful when modifying an existing
user's home directory location.
For Issue [#268](https://github.com/freephile/meza/issues/268)
  - Modified: `src/playbooks/site.yml`

origin/issue267-faster-deploy
* [3d05a705](https://github.com/freephile/meza/commit/3d05a705) (2026-01-15) Greg Rundlett: Make meza deploy faster - remove unneccessary and duplicative file mode and ownership conditioning
- extract file mode and ownership conditioning into 'verify-permissions' role which is then included; and can be run independently
Handles
-- Widgets
-- cache
-- images
-- uploads
as well as other project-wide folders and permissions (@TODO split)
- use ansible shell module to invoke composer commands with the proper umask so that pesky file permission problems are avoided in restrictive umask environments.
Example of running verify-permissions playbook:
ansible-playbook -i localhost, --connection=local  /opt/meza/src/playbooks/verify-permissions.yml -e env=monolith
For Issue [#267](https://github.com/freephile/meza/issues/267)
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/verify-permissions/tasks/main.yml`

* [f28d3067](https://github.com/freephile/meza/commit/f28d3067) (2026-01-15) Greg Rundlett: enable ansible profiling in ansible.cfg - fix spelling error in callbacks_enabled configuration to regain ansible profiling
- add commented section with defaults showing how to change profiling report
- convert comment style to use modern '#' instead of legacy ini-style ';'
for Issue [#267](https://github.com/freephile/meza/issues/267)
  - Modified: `config/ansible.cfg`

* [69b12928](https://github.com/freephile/meza/commit/69b12928) (2026-01-13) Greg Rundlett: add link to PROFILING README Ansible profiling is available by default.
Timings are in the deploy output and logs
Add link to additional information about profiling Ansible plays
see Issue [#267](https://github.com/freephile/meza/issues/267)
  - Modified: `src/roles/apache-php/README_PROFILING.md`

* [4b14ee15](https://github.com/freephile/meza/commit/4b14ee15) (2026-01-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [745068b1](https://github.com/freephile/meza/commit/745068b1) (2026-01-11) Greg Rundlett: fix documentation - fix paths
- explain how to 'turn off'
- you do NOT have to 'view source'
output is at the bottom of the page
for Issue [#262](https://github.com/freephile/meza/issues/262)
  - Modified: `src/roles/apache-php/README_PROFILING.md`

* [3c87f2e0](https://github.com/freephile/meza/commit/3c87f2e0) (2026-01-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [9197e025](https://github.com/freephile/meza/commit/9197e025) (2026-01-11) Greg Rundlett: fix destination and ownership of profiling.php for Issue [#262](https://github.com/freephile/meza/issues/262)
  - Modified: `src/roles/apache-php/tasks/profiling.yml`

* [311a8d17](https://github.com/freephile/meza/commit/311a8d17) (2026-01-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [62791b9a](https://github.com/freephile/meza/commit/62791b9a) (2026-01-11) Greg Rundlett: modernized Meza PHP profiling Replace XHGui+MongoDB with lightweight xhprof-based profiling
which integrates with MediaWiki.
Changes Made
== NEW files ==
- 20-xhprof.ini.j2 - PHP extension configuration
- profiling.php.j2 - MediaWiki profiler configuration with hierarchical control
- logrotate-profiler.j2 - Log rotation for file-based output
- README_PROFILING.md - Comprehensive documentation
== Changed files ==
- profiling.yml - Replaced MongoDB/XHGui with xhprof-only installation
- php.yml - Added conditional xhprof extension deployment
- main.yml - Uncommented profiling task include
- defaults.yml - Added profiling configuration with detailed comments
- php.ini.j2 - Removed obsolete profiling references
- httpd.conf.j2 - Removed port 8089 VirtualHost
- php-fpm-httpd.conf.j2 - Removed port 8089 VirtualHost
- main.yml - Removed port 8088 firewall rules
== DELETED files ==
mongod.conf.j2 - Obsolete MongoDB configuration
mongo.repo.j2 - Obsolete MongoDB repository
xhgui.config.php.j2 - Obsolete XHGui configuration
== Features ==
- Hierarchical profiling control - Environment-level, per-wiki, and output format
- Two output modes - Footer display (ProfilerOutputText) or file logging
- Automatic log rotation - Daily cleanup with configurable retention
- Security considerations - Documented risks and best practices
- Comprehensive documentation - Usage guide with common scenarios
- Backward compatibility - Legacy deployments handled gracefully
== Configuration Example ==
```yaml
m_setup_php_profiling: true
m_profiling_output_type: footer
m_profiling_file_retention_days: 1
wikis:
  - id: demo
    name: Demo Wiki
    enable_profiling: true
```
All YAML files validated successfully. Ready for testing and deployment.
Fixes Issue [#262](https://github.com/freephile/meza/issues/262)
  - Modified: `config/defaults.yml`
  - Added: `src/roles/apache-php/README_PROFILING.md`
  - Modified: `src/roles/apache-php/tasks/main.yml`
  - Modified: `src/roles/apache-php/tasks/php.yml`
  - Modified: `src/roles/apache-php/tasks/profiling.yml`
  - Added: `src/roles/apache-php/templates/20-xhprof.ini.j2`
  - Modified: `src/roles/apache-php/templates/httpd.conf.j2`
  - Added: `src/roles/apache-php/templates/logrotate-profiler.j2`
  - Deleted: `src/roles/apache-php/templates/mongo.repo.j2`
  - Deleted: `src/roles/apache-php/templates/mongod.conf.j2`
  - Modified: `src/roles/apache-php/templates/php-fpm-httpd.conf.j2`
  - Modified: `src/roles/apache-php/templates/php.ini.j2`
  - Added: `src/roles/apache-php/templates/postLocalSettings.d/profiling.php.j2`
  - Deleted: `src/roles/apache-php/templates/xhgui.config.php.j2`
  - Modified: `src/roles/haproxy/tasks/main.yml`
  - Modified: `src/roles/haproxy/templates/haproxy.cfg.j2`

* [fa7d5861](https://github.com/freephile/meza/commit/fa7d5861) (2026-01-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [180c02e1](https://github.com/freephile/meza/commit/180c02e1) (2026-01-10) Greg Rundlett: property parseable is not allowed in ansible-lint config The -p (or --parseable) command-line option and the corresponding
parseable configuration file property were used in older versions of
ansible-lint to produce output in a pep8 compatible format. These
options were removed as part of a breaking change in favor of the
current, more structured output formats. The schema validation in
newer versions of ansible-lint now flags this deprecated property as
an error.
You may wish to upgrade your ansible-lint with
pip install --upgrade ansible-lint
  - Modified: `.ansible-lint`

* [127c494a](https://github.com/freephile/meza/commit/127c494a) (2026-01-10) Greg Rundlett: make Parser Cache Type into a configurable setting Historically Meza used $wgParserCacheType = CACHE_NONE so that is the
default configuration. Users who wish to enable caching can now set
this to CACHE_ANYTHING OR CACHE_MEMCACHED by overriding it in
their public.yml.
See https://www.mediawiki.org/wiki/Meza/Variables
fixes Issue [#111](https://github.com/freephile/meza/issues/111)
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/mediawiki/defaults/main.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [696531ec](https://github.com/freephile/meza/commit/696531ec) (2026-01-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [fe969fc1](https://github.com/freephile/meza/commit/fe969fc1) (2026-01-10) Greg Rundlett: set parser cache Performance improved 50%
$wgParserCacheType = CACHE_MEMCACHED;
fixes Issue [#111](https://github.com/freephile/meza/issues/111)
Also, last commit standardized PHP comment syntax
in MezaCoreExtensions.yml config blocks
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [4311c054](https://github.com/freephile/meza/commit/4311c054) (2026-01-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [680a9de7](https://github.com/freephile/meza/commit/680a9de7) (2026-01-10) Greg Rundlett: add cache for SemanticMediaWiki set `$smwgQueryResultCacheType=CACHE_MEMCACHED;` for SMW
Memcached is already configured for other caches in LocalSettings.php
fixes Issue [#111](https://github.com/freephile/meza/issues/111)
  - Modified: `config/MezaCoreExtensions.yml`

* [858a6d5a](https://github.com/freephile/meza/commit/858a6d5a) (2026-01-10) Greg Rundlett: add helpful prompt about missing WIKI=foo The new failure message for a missing wikiId now includes a line to say
"Perhaps you forgot to specify WIKI=foo in your script command?"
[skip ci]
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [d653d469](https://github.com/freephile/meza/commit/d653d469) (2026-01-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [fa83a80a](https://github.com/freephile/meza/commit/fa83a80a) (2026-01-10) Greg Rundlett: format PHP templates for quality / conformance fix up LocalSettings.php and Extensions.php files
- PHPDoc header - Added proper file documentation with @package Meza
- Section headers - Changed from SECTION X) to SECTION X: format with proper PHPDoc blocks /** */
- Comment style - Changed # and ## to // for inline comments, PHPDoc /** */ for blocks
- Array syntax - Changed all array() to short syntax []
- Quote consistency - Fixed inconsistent quote usage (single quotes for string literals)
- Spacing - Added spaces around parentheses: if ( condition ) not if( condition )
- elseif - Changed else if to elseif (PHP best practice)
- Capitalization - Consistent comment capitalization
- Indentation - Tabs inside conditionals, proper formatting throughout
- @see tags - Changed reference comments to proper @see PHPDoc tags
- removed old $wgDisableCookieCheck setting
  - Modified: `src/roles/mediawiki/templates/Extensions.php.j2`
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [e6f73eff](https://github.com/freephile/meza/commit/e6f73eff) (2026-01-09) Greg Rundlett: clean up LocalSettings.php template shrink excess vertical whitespace by adding SECTION labels in all caps
This makes it like Extensions.php and is easy to search / visually scan
Also added a minor failsafe die() for any invalid auth-type
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [e7d6a6e6](https://github.com/freephile/meza/commit/e7d6a6e6) (2026-01-09) Greg Rundlett: add new feature to exclude core extensions reenable Wiretap extension; switching to freephile repo
introduce new variable `m_excluded_extension_names` that can be used
in `public.yml` to exclude extensions which otherwise are installed
as 'core' by MezaCoreExtensions.yml.
Excluded extensions *can* be re-enabled at the same time in
LocalExtensions.yml
(where they can also be configured to only install on a per-wiki basis).
Deploy output contains a message about excluded extensions for visibility
src/roles/init-controller-config/templates/public.yml.j2 contains
example exclude content to guide new admins
add `--public-config` option to `src/scripts/render_extensions_php.py`
helper script so that the tool mimics the extension excludes
revert interim solution from src/roles/init-controller-config/tasks/main.yml
fixes Issue [#256](https://github.com/freephile/meza/issues/256)
  - Modified: `config/MezaCoreExtensions.yml`
  - Modified: `src/roles/init-controller-config/tasks/main.yml`
  - Modified: `src/roles/init-controller-config/templates/public.yml.j2`
  - Modified: `src/roles/mediawiki/tasks/main.yml`
  - Modified: `src/roles/mediawiki/templates/Extensions.php.j2`
  - Modified: `src/scripts/render_extensions_php.py`

* [b0f0b6d7](https://github.com/freephile/meza/commit/b0f0b6d7) (2026-01-08) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [b2785e3d](https://github.com/freephile/meza/commit/b2785e3d) (2026-01-08) Greg Rundlett: remove archived Graph extension Graph should not be used on a public wiki and the code is archived.
Fixes Issue [#251](https://github.com/freephile/meza/issues/251)
For more, see the discussion "Improve Chartinging capabilities of
Meza" https://github.com/freephile/meza/discussions/252
  - Modified: `config/MezaCoreExtensions.yml`

* [7e016a91](https://github.com/freephile/meza/commit/7e016a91) (2026-01-06) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [f602c7b0](https://github.com/freephile/meza/commit/f602c7b0) (2026-01-06) Greg Rundlett: remove inadvertent setting for CategoryTree ext CategoryTree can have $wgCategoryTreeSidebarRoot, but it would be a
local choice and is not valid in some skins.
The setting has been disabled by comment in CoreExtensions
  - Modified: `config/MezaCoreExtensions.yml`

* [e5221464](https://github.com/freephile/meza/commit/e5221464) (2026-01-03) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [3a30ea25](https://github.com/freephile/meza/commit/3a30ea25) (2026-01-03) Greg Rundlett: add SVG native client-side rendering Using `$wgSVGNativeRendering=true;` MediaWiki will serve SVG files
to the client browser instead of converting them to rasterized formats.
Fixes Issue [#248](https://github.com/freephile/meza/issues/248)
  - Modified: `src/roles/mediawiki/templates/LocalSettings.php.j2`

* [7bdd76d9](https://github.com/freephile/meza/commit/7bdd76d9) (2025-12-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [3a48d02d](https://github.com/freephile/meza/commit/3a48d02d) (2025-12-30) Greg Rundlett: fix typo skip-ci 
  - Modified: `src/scripts/render_extensions_php.py`

* [b58b1a11](https://github.com/freephile/meza/commit/b58b1a11) (2025-12-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [7ba28a1e](https://github.com/freephile/meza/commit/7ba28a1e) (2025-12-30) Greg Rundlett: add comment about the helper script for Extensions.php 
  - Modified: `src/roles/mediawiki/templates/Extensions.php.j2`

* [ab35d350](https://github.com/freephile/meza/commit/ab35d350) (2025-12-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [2ca5454a](https://github.com/freephile/meza/commit/2ca5454a) (2025-12-30) Greg Rundlett: add script for developing the jinja template for Extensions.php Jinja templating is hard, confusing, and unpredictable.
Toss in differences between Python 3.6.8 and modern Python and you're soon pulling your hair out.
This script allows you to iterate on src/roles/mediawiki/templates/Extensions.php.j2
without needing to do deploys just to see the results.
  - Added: `src/scripts/render_extensions_php.py`

* [def1caba](https://github.com/freephile/meza/commit/def1caba) (2025-12-30) Greg Rundlett: replace tabs with spaces in Jinja templates 
  - Modified: `src/roles/mediawiki/templates/Extensions.php.j2`

* [353dc13c](https://github.com/freephile/meza/commit/353dc13c) (2025-12-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [9882079d](https://github.com/freephile/meza/commit/9882079d) (2025-12-29) Greg Rundlett: Improve templating of Extensions Add better examples and reference link to MezaLocalExtensions.yml
Include the -wikis conditional gate for Local Extensions described on-wiki
Improve the wording, and remove excess whitespace from the 'Extensions.php' deploy file
Add Jinja comments to improve the readability of control structures
  - Modified: `src/roles/init-controller-config/templates/MezaLocalExtensions.yml.j2`
  - Modified: `src/roles/mediawiki/templates/Extensions.php.j2`

* [386986b1](https://github.com/freephile/meza/commit/386986b1) (2025-12-19) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [1494ef61](https://github.com/freephile/meza/commit/1494ef61) (2025-12-18) Greg Rundlett: Re-enable WhosOnline After fixing the extension for MW compatibility
and removing logging of anonymous users, we can re-enable the extension
Fixes Issue [#177](https://github.com/freephile/meza/issues/177)
  - Modified: `config/MezaCoreExtensions.yml`

* [94e7c884](https://github.com/freephile/meza/commit/94e7c884) (2025-12-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [78f9f5e8](https://github.com/freephile/meza/commit/78f9f5e8) (2025-12-11) Greg Rundlett: disable ParserMigration extension requires MediaWiki 1.46+
fixes Issue [#239](https://github.com/freephile/meza/issues/239)
  - Modified: `config/MezaCoreExtensions.yml`

* [745e90b9](https://github.com/freephile/meza/commit/745e90b9) (2025-12-11) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [4b24c258](https://github.com/freephile/meza/commit/4b24c258) (2025-12-11) Greg Rundlett: add ParserMigration for Parsoid reads There should be new User preferences to opt in
Fixes Issue [#239](https://github.com/freephile/meza/issues/239)
  - Modified: `config/MezaCoreExtensions.yml`

* [eba1f494](https://github.com/freephile/meza/commit/eba1f494) (2025-12-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [ef9a927e](https://github.com/freephile/meza/commit/ef9a927e) (2025-12-10) Greg Rundlett: Security and Maintenance release update to 1.43.6
also fix typo for sudoers
  - Modified: `config/defaults.yml`
  - Modified: `src/roles/base/tasks/main.yml`

* [427747c6](https://github.com/freephile/meza/commit/427747c6) (2025-12-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [06545e1c](https://github.com/freephile/meza/commit/06545e1c) (2025-12-10) Greg Rundlett: add examples and reference for PyWikiBot 
  - Added: `scripts/README_PYWIKIBOT.md`
  - Added: `scripts/create_extension_features.py`
  - Added: `scripts/pywikibot-user-config.py`

* [c6d00a97](https://github.com/freephile/meza/commit/c6d00a97) (2025-12-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* [123f4378](https://github.com/freephile/meza/commit/123f4378) (2025-12-09) Greg Rundlett: add CrawlerProtection extension Block bots with CrawlerProtection
Lockdown extension is left installed, but the configuration is
removed since currently it is not doing anything out of the box.
  - Modified: `config/MezaCoreExtensions.yml`

* [f9d4e87a](https://github.com/freephile/meza/commit/f9d4e87a) (2025-12-10) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

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
