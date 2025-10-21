# Meza Command: `maint`

## Description

Perform maintenance operations on Meza environments and wikis.

## Usage

```bash
meza maint [directive]
```

## Directives

### `jobs` - Run Wiki Jobs

Run all pending jobs on all wikis in the environment.

```bash
meza maint jobs
```

**What it does:**
- Executes MediaWiki's job queue for all wikis
- Processes background tasks like:
  - Page link updates
  - Search index updates
  - Email notifications
  - Image thumbnail generation
  - Cache invalidation

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `[directive]` | Maintenance operation to perform | No |

## Job Queue Operations

The job queue processes various MediaWiki background tasks:

| Job Type | Description |
|----------|-------------|
| **RefreshLinks** | Update internal link tables |
| **HTMLCacheUpdate** | Update page cache |
| **SearchUpdate** | Update search indexes |
| **SendMail** | Send pending email notifications |
| **ThumbnailRender** | Generate image thumbnails |
| **CategoryMembershipChange** | Update category memberships |

## When to Run Jobs

Run maintenance jobs when:
- ✅ After bulk content imports
- ✅ After extension installations
- ✅ When search results seem outdated
- ✅ When page links appear broken
- ✅ As part of regular maintenance schedule

## Notes

- Job processing may take time for large wikis
- Jobs run automatically during normal wiki operation
- Manual job runs are useful after bulk operations
- Jobs process in background without affecting wiki availability
- Consider running during low-traffic periods for large job queues

## Performance Considerations

- Large job queues may impact server performance
- Monitor system resources during job processing
- Consider breaking up large job runs across multiple sessions

## See Also

- [`meza deploy`](deploy.md) - Deploy environment updates
- [`meza backup`](backup.md) - Backup before major maintenance
- [`meza debug`](debug.md) - Debug job queue issues