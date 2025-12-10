## Meza Release Notes 43.60.6 → HEAD

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
