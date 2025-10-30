## Meza Release Notes 43.58.2 → HEAD

### Commits

HEAD -> dev origin/dev
* a6a76f6 (2025-10-30) Greg Rundlett: process the dev branch 
  - Modified: `.github/workflows/yamllint.yml`

* 09a7a3c (2025-10-30) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* b19e5f5 (2025-10-30) Greg Rundlett: Major enhancements: Create wiki logging, etc. "meza create wiki" logging implementation
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

* 465eaee (2025-10-29) Greg Rundlett: Fix the CHANGELOG automation - fix the updateCHANGELOG.sh script (used by Continuous Integration)
- Update the entire CHANGELOG for consistent 'pretty' formatting
- Limit the CHANGELOG to start at 2022-01-01 for length
[skip ci] chicken and egg problem
Fixes Issue [#219](https://github.com/freephile/meza/issues/219)
  - Modified: `CHANGELOG`
  - Modified: `src/scripts/updateCHANGELOG.sh`

* 6e51cc5 (2025-10-29) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* a799fa8 (2025-10-29) Greg Rundlett: Prompt for credentials when creating Admin acct When Meza creates an Admin account, whether for the initial 'demo'
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

* de0798e (2025-10-24) GitHub Action: Auto-update CHANGELOG and release notes - Updated CHANGELOG with latest commits
- Generated RELEASE_NOTES-HEAD.md
- Automated by GitHub Actions
  - Modified: `CHANGELOG`
  - Modified: `RELEASE_NOTES-HEAD.md`

* 43cfde0 (2025-10-24) Greg Rundlett: Automated RELEASE NOTES and Changelog w/ Actions see .github/RELEASE_AUTOMATION.md for details
Though GitHub Actions, we integrated automatic Changelog and RELEASE
NOTES generation.
For pull requests and commits.
  - Added: `.github/RELEASE_AUTOMATION.md`
  - Added: `.github/workflows/advanced-release-management.yml`
  - Added: `.github/workflows/manual-release-notes.yml`
  - Added: `.github/workflows/release-notes.yml`
  - Added: `src/scripts/release-helper.sh`
