# Playbook Diagrams

These graphs are interactive, and you can click nodes to open the relevant playbook or role file in VSCode.

## Roles Only

High-level view showing playbook structure and role dependencies:

- [backup.svg](backup.svg)
- [check-for-changes.svg](check-for-changes.svg)
- [cleanup-upload-stash.svg](cleanup-upload-stash.svg)
- [create-wiki.svg](create-wiki.svg)
- [create-wiki-promptless.svg](create-wiki-promptless.svg)
- [debug.svg](debug.svg)
- [delete-elasticsearch.svg](delete-elasticsearch.svg)
- [delete-wiki.svg](delete-wiki.svg)
- [delete-wiki-promptless.svg](delete-wiki-promptless.svg)
- [deploy-notify.svg](deploy-notify.svg)
- [getdocker.svg](getdocker.svg)
- [migrate-wikis.svg](migrate-wikis.svg)
- [push-backup.svg](push-backup.svg)
- [rebuild-smw-and-index.svg](rebuild-smw-and-index.svg)
- [run-maintenance.svg](run-maintenance.svg)
- [setbaseconfig.svg](setbaseconfig.svg)
- [setup-env.svg](setup-env.svg)
- [setup-meza-user.svg](setup-meza-user.svg)
- [site.svg](site.svg)
- [test-certbot.svg](test-certbot.svg)
- [verify-permissions.svg](verify-permissions.svg)

## Detailed with Tasks

Comprehensive view including individual tasks within each role:

- [backup-w-tasks.svg](backup-w-tasks.svg)
- [check-for-changes-w-tasks.svg](check-for-changes-w-tasks.svg)
- [cleanup-upload-stash-w-tasks.svg](cleanup-upload-stash-w-tasks.svg)
- [create-wiki-w-tasks.svg](create-wiki-w-tasks.svg)
- [create-wiki-promptless-w-tasks.svg](create-wiki-promptless-w-tasks.svg)
- [debug-w-tasks.svg](debug-w-tasks.svg)
- [delete-elasticsearch-w-tasks.svg](delete-elasticsearch-w-tasks.svg)
- [delete-wiki-w-tasks.svg](delete-wiki-w-tasks.svg)
- [delete-wiki-promptless-w-tasks.svg](delete-wiki-promptless-w-tasks.svg)
- [deploy-notify-w-tasks.svg](deploy-notify-w-tasks.svg)
- [getdocker-w-tasks.svg](getdocker-w-tasks.svg)
- [migrate-wikis-w-tasks.svg](migrate-wikis-w-tasks.svg)
- [push-backup-w-tasks.svg](push-backup-w-tasks.svg)
- [rebuild-smw-and-index-w-tasks.svg](rebuild-smw-and-index-w-tasks.svg)
- [run-maintenance-w-tasks.svg](run-maintenance-w-tasks.svg)
- [setbaseconfig-w-tasks.svg](setbaseconfig-w-tasks.svg)
- [setup-env-w-tasks.svg](setup-env-w-tasks.svg)
- [setup-meza-user-w-tasks.svg](setup-meza-user-w-tasks.svg)
- [site-w-tasks.svg](site-w-tasks.svg)
- [test-certbot-w-tasks.svg](test-certbot-w-tasks.svg)
- [verify-permissions-w-tasks.svg](verify-permissions-w-tasks.svg)

---

*These SVG files were generated using [ansible-playbook-grapher](https://wiki.freephile.org/wiki/Ansible_Playbook_Grapher). To update these graphs, run the script `../scripts/generate-playbook-graphs.sh` (or `../scripts/generate-playbook-graphs.sh --with-tasks` for the detailed versions).*
