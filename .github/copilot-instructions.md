# Meza AI Coding Agent Instructions

## ⚠️ CRITICAL: MANDATORY LINTING REQUIREMENT ⚠️

**BEFORE making ANY changes to YAML files, Ansible playbooks, or roles, you MUST:**

1. **Run linting**: `./src/scripts/lint-files.sh <file>` to check current state
2. **After changes**: Run linting again to verify no new errors introduced
3. **Fix all errors**: Before proceeding or suggesting changes to the user
4. **See**: `LINTING.md` for complete linting documentation

**Example Workflow:**
```bash
# Check before editing
./src/scripts/lint-files.sh src/roles/mediawiki/tasks/main.yml
# Make changes
# Check after editing
./src/scripts/lint-files.sh src/roles/mediawiki/tasks/main.yml
```

## Project Overview
Meza is the leading MediaWiki deployment automation platform built with Ansible. It provides a single `meza` command-line interface to deploy, manage, and maintain complex MediaWiki environments across multiple servers with features like VisualEditor, CirrusSearch, and many other carefully selected extensions.

## Architecture & Key Components

### Core Structure
- **Primary CLI**: `src/scripts/meza.py` - Main Python CLI with commands like `deploy`, `backup`, `create`, `setup-env`
- **Ansible Core**: `src/playbooks/site.yml` - Main deployment playbook that orchestrates all roles
- **Configuration Layer**: `config/` directory with `defaults.yml`, `paths.yml`, and OS-specific configs
- **Role-Based Architecture**: `src/roles/` contains 40+ specialized Ansible roles for different components

### Key Architectural Patterns

#### Path Resolution System
All paths are dynamically resolved from the meza binary location:
```python
# In meza.py and set-vars role
install_dir = dirname(dirname(dirname(dirname(realpath(which meza)))))
# Typically resolves to /opt, but configurable
```

#### Multi-Environment Support
- Environments defined in `/opt/conf-meza/secret/<env>/` and `/opt/conf-meza/public/<env>/`
- Each environment has separate inventory files, secrets, and configuration
- Deploy locks prevent concurrent deployments: `/opt/data-meza/env-{env}-deploy.lock`

#### Command Dispatch Pattern
```python
# meza.py uses function naming convention
def meza_command_deploy(argv):     # maps to: meza deploy
def meza_command_setup_env(argv):  # maps to: meza setup-env
def meza_command_backup(argv):     # maps to: meza backup
```

## Critical Development Workflows

### Local Development
```bash
# Setup development environment
meza setup-dev
# Deploy to local environment (first run creates the 'demo' wiki)
meza deploy monolith -vvv
# Create test wiki
meza create wiki testwiki
```

### Testing Commands (Not Obvious from Files)
```bash
# Test Ansible syntax before deployment
ANSIBLE_CONFIG=/opt/meza/config/ansible.cfg ansible-playbook /opt/meza/src/playbooks/site.yml --syntax-check

# Quick config-only deploy (skip slow tasks)
meza deploy <env> --tags mediawiki --skip-tags latest,update.php,verify-wiki

# Force debug mode for troubleshooting
# Set in /opt/conf-meza/public/public.yml:
m_force_debug: true
```

### Deployment Lock Management
```bash
# Check if environment is deploying
meza deploy-check <env>  # returns 0=not deploying, 1=deploying
# Manually unlock stuck deployments
meza deploy-unlock <env>
# Kill running deployment
meza deploy-kill <env>
```

## Project-Specific Conventions

### Configuration Hierarchy (Order of Precedence)
1. Environment-specific: `/opt/conf-meza/secret/<env>/secret.yml`
2. Public environment: `/opt/conf-meza/public/public.yml`
3. OS-specific: `config/RedHat.yml` or `config/Debian.yml`
4. Core defaults: `config/defaults.yml`
5. Path definitions: `config/paths.yml`

### Ansible Role Patterns
- **set-vars role**: Always runs first to establish all path variables and config hierarchy
- **sync-configs role**: Synchronizes configuration between controller and target servers
- **Role dependencies**: Many roles depend on `set-vars` being run first
- **Jinja2 templating**: Extensive use of `{{ m_variable }}` pattern for paths and configs

### MediaWiki Integration Points
- **Wiki creation**: `configure-wiki` role generates LocalSettings.php override scaffolding
- **Extension management**: `config/MezaCoreExtensions.yml` defines default extension set
- **Local Extension management**: `conf-meza/public/MezaLocalExtensions.yml` defines default *additional* extension set managed by the local instance
- **Update workflows**: `update.php` role handles MediaWiki database updates
- **File uploads**: GlusterFS used for multi-server setups (`m_uploads_dir` override)

## Development Guidelines

### When Modifying meza.py
- Add new commands using `meza_command_<name>` function pattern
- Always validate argv length before accessing arguments
- Use `defaults` dictionary for consistent path handling
- Implement proper lock file management for deployment-related commands

### When Creating Ansible Roles
- Always include `set-vars` as dependency or include it in main playbook
- Use `{{ m_install_dir }}/meza/` prefix for all Meza-related paths
- Follow the sync-configs pattern for multi-server deployments
- Test with both single server and multi-server inventories

### PHP Code Standards (MediaWiki Integration)
- **Follow MediaWiki coding conventions**: Use MediaWiki's PSR-2 based coding standards
- **Security practices**: Always sanitize user input, use MediaWiki's built-in escaping functions
- **Database interactions**: Use MediaWiki's database abstraction layer, never raw SQL
- **Namespace usage**: Use proper MediaWiki namespaces and avoid global scope pollution
- **Documentation**: Include PHPDoc comments for all functions and classes
- **Error handling**: Use MediaWiki's logging and error handling mechanisms

### Configuration Changes
- Test changes with `--check` mode first
- Use `--tags` and `--skip-tags` for targeted deployments
- Remember config hierarchy: secret.yml overrides public.yml overrides defaults.yml
- Validate YAML syntax with yamllint (CI requirement)

### Testing Requirements
- All changes must pass YAML linting (`yamllint`)
- Manual testing should include: wiki creation, VisualEditor, search, file uploads
- For security changes: test image access permissions with anonymous users
- Use Docker test framework: `tests/docker/run-tests.sh monolith-from-scratch` (NOTE: this is experimental)

## External Dependencies & Integration
- **MediaWiki Core**: Git SEMVER, submodules, and composer dependencies for version management
- **Composer**: PHP dependency management for MediaWiki extensions
- **Elasticsearch**: Search backend requiring specific Java/memory configuration
- **GlusterFS**: Distributed file system for multi-server uploads
- **HAProxy**: Load balancing for multi-server deployments
- **Certbot/Let's Encrypt**: SSL certificate automation

## Common Pitfalls
- Don't modify files in `/opt/meza/` during deployment (use `m_conf_secret_dir` paths)
- Always use absolute paths in Ansible (relative paths cause issues)
- Lock files must be cleaned up on deployment interruption
- Environment-specific secrets should never be committed to git
- Multi-server deployments require careful SSH key management between nodes

## Mandatory Code Quality Requirements

### **CRITICAL: Always Run Linting Before Suggesting Changes**
Before making ANY changes to YAML files, Python files, or Ansible playbooks/roles, you MUST:

1. **Run linting tools** to check for syntax and style errors
2. **Verify changes don't introduce new linting errors**
3. **Use the project's linting script**: `./src/scripts/lint-files.sh [files...]`

#### Linting Commands
```bash
# Lint specific files
./src/scripts/lint-files.sh src/roles/mediawiki/tasks/main.yml
./src/scripts/lint-files.sh src/playbooks/verify-permissions.yml

# Lint all YAML files in project
./src/scripts/lint-files.sh

# Manual linting commands
yamllint <file.yml>                    # For YAML syntax/style
ansible-lint <playbook.yml>            # For Ansible best practices
```

#### Pre-Edit Workflow
1. **BEFORE editing any file**: Run `./src/scripts/lint-files.sh <file>` to check current state
2. **AFTER making changes**: Run linting again to verify no new errors introduced
3. **If linting fails**: Fix all errors before proceeding or suggesting the changes to user

#### Pre-Commit Checklist

**For Python Files:**
- [ ] Remove unused imports and variables (or prefix unused with `_`)
- [ ] Use specific exception types, not bare `Exception`
- [ ] Add module docstring with Requirements and Usage
- [ ] Add function docstrings for non-trivial functions
- [ ] Remove unnecessary f-strings (static strings)
- [ ] Check line length (aim for <100 chars)
- [ ] Follow naming conventions (UPPER_CASE, lower_case, PascalCase)
- [ ] Escape template braces for `.format()`: `{{{{` → `{{`
- [ ] Run: `pylint yourfile.py`

**For YAML/Ansible Files:**
- [ ] Use 2-space indentation consistently
- [ ] Use FQCN for all Ansible modules
- [ ] No trailing whitespace
- [ ] Line length under 140 chars
- [ ] Run: `./src/scripts/lint-files.sh <file>`

**For All Files:**
- [ ] Executable scripts have `#!/usr/bin/env python3` and `chmod +x`
- [ ] No secrets or passwords committed
- [ ] Absolute paths used in Ansible (not relative)
- [ ] Test changes with `--check` or `--dry-run` mode first

#### Linting Configuration
- **yamllint config**: `.yamllint` (140 char line length, relaxed rules)
- **ansible-lint config**: `.ansible-lint` (production profile, FQCN enforcement)
- **Excluded paths**: `.venv/`, `vendor/`, `tests/docker/`, external roles

### Code Quality Standards

#### YAML
- Follow yamllint rules, use consistent indentation (2 spaces)
- No trailing whitespace
- Maximum line length: 140 characters

#### Ansible
- Use FQCN for modules (`ansible.builtin.file` not `file`)
- Follow ansible-lint production profile rules
- Test with `--check` mode before applying changes

#### Python
All Python code must follow **PEP 8** (Python Enhancement Proposal 8 - Style Guide for Python Code) and pass pylint validation:

**Import Management:**
- Only import what you use - remove unused imports
- Group imports per **PEP 8**: stdlib, third-party, local modules
```python
# ✅ Good
import argparse
import sys
import pywikibot

# ❌ Bad - unused import
from pywikibot import pagegenerators  # If not used elsewhere
```

**Exception Handling:**
- Use specific exceptions, never bare `except Exception:`
```python
# ✅ Good
try:
    page.save()
except (pywikibot.exceptions.Error, OSError) as e:
    print(f"Error: {e}")

# ❌ Bad - too broad
except Exception as e:
    pass
```

**Variable Naming:**
- Prefix intentionally unused variables with underscore
```python
# ✅ Good
_created, _skipped, error_count = create_pages()
# Only error_count is used later

# ❌ Bad - pylint will complain about unused variables
created, skipped, errors = create_pages()
```

**String Formatting:**
- Only use f-strings when interpolating variables
```python
# ✅ Good
print(f"Processing: {page_title}")
print("Static message")

# ❌ Bad - unnecessary f-string
print(f"Static message")
```

**Docstrings:**
- All modules must have docstrings explaining purpose and usage
- Non-trivial functions need docstrings with Args, Returns, Raises sections
```python
#!/usr/bin/env python3
"""
Module description.

Requirements:
    pip install package

Usage:
    python script.py [options]
"""

def process_data(input_file, verbose=False):
    """
    Process the input file.

    Args:
        input_file: Path to file to process
        verbose: Enable verbose output

    Returns:
        int: Number of items processed

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    pass
```

**Naming Conventions:**
- Follow **PEP 8** naming standards:
- `UPPER_CASE` for constants: `MAX_RETRIES = 3`
- `lower_case_with_underscores` for variables/functions: `page_title`, `create_feature_page()`
- `PascalCase` for classes: `WikiPageCreator`

**Template String Escaping:**
- When generating content with braces, escape for `.format()`:
```python
# ✅ Good - generates {{Feature}} in output
template = "{{{{Feature\n|title={title}\n}}}}"

# ❌ Bad - generates {Feature} in output
template = "{{Feature\n|title={title}\n}}"
```

**Special Config Files:**
- Use `# pylint: skip-file` for PyWikibot/special config files that use runtime variables
```python
# pylint: skip-file
# flake8: noqa
# This file uses PyWikibot's configuration format

family = 'freephile'
usernames['freephile']['en'] = 'BotName'  # Defined at runtime
```

**File Permissions:**
- Executable scripts must have `chmod +x` and shebang: `#!/usr/bin/env python3`
- No trailing whitespace in any files

## Debugging Commands
```bash
# View deployment logs
meza deploy-tail <env>
# Check deployment status
meza deploy-log <env>
# Verify configuration loading
ansible-playbook site.yml --list-tasks
# Test specific role in isolation
ansible-playbook site.yml --tags <role-name> --check
```

## Standards and References

### Python
- **PEP 8** – Style Guide for Python Code: https://pep8.org/
- **PEP 257** – Docstring Conventions: https://www.python.org/dev/peps/pep-0257/
- **Pylint Documentation**: https://pylint.pycqa.org/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html

### YAML & Ansible
- **yamllint**: https://yamllint.readthedocs.io/
- **ansible-lint**: https://ansible-lint.readthedocs.io/
- **Ansible Best Practices**: https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html

### MediaWiki
- **MediaWiki Coding Conventions**: https://www.mediawiki.org/wiki/Manual:Coding_conventions
- **PyWikibot Documentation**: https://www.mediawiki.org/wiki/Manual:Pywikibot
- **MediaWiki API**: https://www.mediawiki.org/wiki/API:Main_page
