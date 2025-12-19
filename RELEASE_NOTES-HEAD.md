## Meza Release Notes 43.60.6 → HEAD

### Commits

HEAD -> dev origin/dev
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
