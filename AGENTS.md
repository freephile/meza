# AGENTS.md

Meza is a MediaWiki deployment automation platform built with Ansible and a
Python CLI. It manages multi-server MediaWiki environments including
VisualEditor, CirrusSearch, and 40+ curated extensions.

## Project structure

```
src/scripts/meza.py          # Primary CLI entry point
src/playbooks/site.yml       # Main Ansible deployment playbook
src/roles/                   # 40+ Ansible roles
config/defaults.yml          # Core configuration defaults
config/paths.yml             # Path definitions
config/MezaCoreExtensions.yml
```

## Setup commands

```bash
# Install dev environment (Vagrant-based)
meza setup-dev

# Deploy to local monolith environment
meza deploy monolith -vvv

# Create a new wiki in an environment
meza create wiki <wikiname>
```

## Build & deploy commands

```bash
# Full deploy
meza deploy <env>

# Targeted deploy (skip slow tasks)
meza deploy <env> --tags mediawiki --skip-tags latest,update.php,verify-wiki

# Syntax-check playbook without running it
ANSIBLE_CONFIG=/opt/meza/config/ansible.cfg \
  ansible-playbook /opt/meza/src/playbooks/site.yml --syntax-check

# Dry-run a playbook
ansible-playbook src/playbooks/site.yml --check
```

## Testing & linting

**Always lint YAML/Ansible files before and after edits.**

```bash
# Lint one or more specific files
./src/scripts/lint-files.sh src/roles/mediawiki/tasks/main.yml
./src/scripts/lint-files.sh src/playbooks/verify-permissions.yml

# Lint all YAML files in the project
./src/scripts/lint-files.sh

# Manual linting
yamllint <file.yml>
ansible-lint <playbook.yml>
pylint <script.py>

# Docker integration test (experimental)
tests/docker/run-tests.sh monolith-from-scratch
```

Linting config:
- `.yamllint` — 140-char line limit, relaxed rules
- `.ansible-lint` — production profile, FQCN enforcement
- Excluded: `.venv/`, `vendor/`, `tests/docker/`, external roles

## Code style — YAML & Ansible

- 2-space indentation, no trailing whitespace, no lines with only spaces/tabs
- Max line length: 140 characters
- Use FQCN for all modules: `ansible.builtin.file`, not `file`
- Use absolute paths in all Ansible tasks (never relative)
- Test with `--check` before applying changes
- Follow `set-vars` → role dependency pattern; always set-vars first

**Blank lines inside YAML blocks must be completely empty (zero characters).**

## Code style — Python

- Follow PEP 8; validate with `pylint`
- All modules need a docstring with Requirements/Usage sections
- Non-trivial functions need docstrings (Args, Returns, Raises)
- Use specific exception types — never bare `except Exception:`
- Prefix intentionally unused variables with `_`
- Only use f-strings when interpolating variables
- Naming: `UPPER_CASE` constants, `lower_case` functions/variables, `PascalCase` classes
- Group imports: stdlib → third-party → local
- Escape braces for `.format()` templates: `{{{{` generates `{{` in output
- Executable scripts: `#!/usr/bin/env python3` shebang + `chmod +x`

## Code style — PHP (MediaWiki)

- Follow MediaWiki PSR-2 coding conventions
- Always use MediaWiki's database abstraction layer — never raw SQL
- Use MediaWiki's built-in escaping functions for all user input
- Include PHPDoc comments on all functions and classes

## Configuration hierarchy (highest → lowest precedence)

1. `/opt/conf-meza/secret/<env>/secret.yml`
2. `/opt/conf-meza/public/public.yml`
3. `config/RedHat.yml` or `config/Debian.yml`
4. `config/defaults.yml`
5. `config/paths.yml`

## Deployment lock management

```bash
meza deploy-check <env>   # 0 = not deploying, 1 = deploying
meza deploy-unlock <env>  # manually clear a stuck lock
meza deploy-kill <env>    # kill a running deployment
meza deploy-tail <env>    # stream live deployment logs
meza deploy-log <env>     # view deployment log
```

## Security & common pitfalls

- Never commit secrets — use `/opt/conf-meza/secret/<env>/` paths
- Never modify files under `/opt/meza/` during a live deployment
- Always use absolute paths in Ansible tasks
- Clean up lock files (`/opt/data-meza/env-{env}-deploy.lock`) if a deploy is interrupted
- Multi-server setups require SSH key management between nodes
- Test image/file access with anonymous users after any permission change

## Debugging

```bash
# Force debug mode (dev environments only — set in public.yml)
# m_force_debug: true

# Or use ?requestDebug=true query param in the web interface

# List all tasks a playbook will run
ansible-playbook src/playbooks/site.yml --list-tasks

# Run only a specific role
ansible-playbook src/playbooks/site.yml --tags <role-name> --check
```

## Adding a new CLI command

Add a function to `src/scripts/meza.py` following the naming convention:

```python
def meza_command_<name>(argv):
    """Short description."""
    # validate len(argv), then implement
```

## References

- [LINTING.md](LINTING.md) — full linting documentation
- [MediaWiki coding conventions](https://www.mediawiki.org/wiki/Manual:Coding_conventions)
- [Ansible best practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)
- [yamllint docs](https://yamllint.readthedocs.io/)
- [ansible-lint docs](https://ansible-lint.readthedocs.io/)
- [PEP 8](https://pep8.org/) · [PEP 257](https://www.python.org/dev/peps/pep-0257/)
