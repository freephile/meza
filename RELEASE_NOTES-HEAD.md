## Meza Release Notes 43.60.6 → HEAD

### Commits

HEAD -> dev origin/dev
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
