## Meza Release Notes 43.58.2 → HEAD

### Commits

HEAD -> dev origin/dev
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
