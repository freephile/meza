# ARA Records Ansible – NIST 800-53 Compliance Mapping

## Overview

ARA Records Ansible (ARA) automatically records Ansible playbook execution history,
capturing timestamps, executing users, target hosts, task results, and changed state.
In a NIST 800-53 based System Security Plan (SSP), ARA functions as a supporting
tool that provides an automated audit trail for all infrastructure configuration
activity performed via Ansible.

---

## Primary Control Family: AU – Audit and Accountability

| Control | Title | How ARA Helps |
|---|---|---|
| **AU-2** | Event Logging | Records every Ansible task execution as a loggable event with configurable verbosity |
| **AU-3** | Content of Audit Records | Captures: who ran the playbook (user + controller hostname), what ran (playbook path, task name), when (timestamp), where (target hosts), and outcome (ok/changed/failed/skipped) |
| **AU-6** | Audit Review, Analysis, and Reporting | ARA's web UI and REST API enable search, filtering, and analysis of all execution records across time |
| **AU-9** | Protection of Audit Information | Records are stored in a dedicated database (SQLite or PostgreSQL/MySQL) separate from the systems being configured |
| **AU-11** | Audit Record Retention | Retention period is configurable; ARA database can be backed up and archived per organizational policy |
| **AU-12** | Audit Record Generation | Every `ansible-playbook` invocation automatically generates structured records via the callback plugin without requiring manual action |

---

## Secondary Control Families

### CM – Configuration Management

| Control | Title | How ARA Helps |
|---|---|---|
| **CM-3** | Configuration Change Control | Provides a timestamped, attributable record of every configuration change applied via Ansible, including task-level diffs |
| **CM-6** | Configuration Settings | Provides evidence that approved configuration baselines (playbooks/roles) were applied to target systems |
| **CM-8** | System Component Inventory | Records which hosts were targeted in each playbook execution, supporting inventory reconciliation |

### CA – Assessment, Authorization, and Monitoring

| Control | Title | How ARA Helps |
|---|---|---|
| **CA-7** | Continuous Monitoring | ARA's historical record and API support integration into dashboards for ongoing monitoring of infrastructure change activity |

### SI – System and Information Integrity

| Control | Title | How ARA Helps |
|---|---|---|
| **SI-12** | Information Management and Retention | ARA retains structured execution history for the retention period configured per AU-11 requirements |

---

## Limitations – What ARA Does NOT Cover

- Records **Ansible activity only** — manual changes, interactive logins, package
  installs outside Ansible, and other tools are not captured
- Is **not** a substitute for OS-level audit logging (`auditd`), which satisfies
  AU controls for system calls, file access, and privileged user actions
- Provides **no integrity verification** of playbooks themselves — that is a
  CM/SA concern addressed by version control (git) and code signing
- Does **not** record the content of Ansible Vault-encrypted variables, protecting
  secrets from appearing in audit logs

---

## Suggested SSP Language

For use in the AU-2, AU-3, or AU-12 control implementation statements:

> *Configuration automation is performed exclusively via Ansible. ARA Records
> Ansible (ARA) is deployed as an Ansible callback plugin that automatically
> records all playbook executions without requiring operator action. Each record
> captures: timestamp, executing user, controller hostname, target hosts, playbook
> path, individual task names, task results (ok/changed/failed/skipped), and
> Ansible version. These records constitute the audit trail for all automated
> configuration management activity and are retained for [X days] in accordance
> with AU-11. Records are accessible via the ARA REST API and web interface for
> review and analysis per AU-6.*

---

## ARA Architecture in Meza

In the Meza deployment platform:

- **Callback plugin**: Configured in `/opt/meza/config/ansible.cfg` via
  `callbacks_enabled = ara_default`
- **Plugin paths**: `/usr/local/lib/python3.12/site-packages/ara/plugins/`
- **Database**: `/opt/conf-meza/users/meza-ansible/.ara/server/ansible.sqlite`
- **Settings**: `/opt/conf-meza/users/meza-ansible/.ara/server/settings.yaml`
- **Triggering user**: `meza-ansible` (the Ansible service account)

All `meza deploy` invocations are automatically recorded without requiring
any additional operator steps.

---

## References

- [ARA Records Ansible documentation](https://ara.recordsansible.org/)
- [NIST SP 800-53 Rev 5 – AU Family](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [NIST SP 800-53 Rev 5 – CM Family](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
