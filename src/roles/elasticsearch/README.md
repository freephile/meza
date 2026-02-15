# Elasticsearch role

This role installs and configures Elasticsearch for MediaWiki (CirrusSearch/Elastica) in Meza.
It pins Elasticsearch to the configured version, handles config and directories, and ensures
the service is running.

## What this role does

- Installs Java and configures `JAVA_HOME`.
- Adds the Elasticsearch yum repository (disabled by default) and installs a pinned version.
- Detects and downgrades Elasticsearch if a host has advanced past the pinned version.
- Optionally applies a DNF versionlock to prevent future upgrades.
- Lays down the Elasticsearch configuration, prepares data/log directories, and starts the service.

## Why it does it this way

MediaWiki and its search extensions are sensitive to Elasticsearch versions. Meza pins
Elasticsearch to the version defined in role defaults to keep deployments stable and
avoid unplanned upgrades that break CirrusSearch or Elastica.

## Key variables

Set these in your inventory or environment config when needed.

- `elasticsearch_version` (default: `7.10.2`): Target Elasticsearch version to install.
- `elasticsearch_major_version` (default: `7.x` in [config/defaults.yml](../../../config/defaults.yml)):
  Repo channel to use when fetching packages.
- `elasticsearch_versionlock_enabled` (default: `true`): When `true`, applies a DNF
  versionlock for the pinned version. Set to `false` in dev/test or when planning
  controlled upgrades (for example, a MediaWiki 1.44+ upgrade path).

## Example overrides

```yaml
elasticsearch_version: "7.10.2"
elasticsearch_versionlock_enabled: false
```
