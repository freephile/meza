#!/usr/bin/env python
"""
Meza command-line interface.

This module provides the main command-line interface for the Meza MediaWiki
Enterprise application platform. It handles deployment, backup, maintenance,
and configuration tasks for MediaWiki environments.
"""

import datetime
import errno
import getopt
import getpass
import grp
import hashlib
import json
import os
import pwd
import random
import shutil
import signal
import string
import subprocess
import sys
import time
import yaml

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import webbrowser
    WEBBROWSER_AVAILABLE = True
except ImportError:
    WEBBROWSER_AVAILABLE = False

# Get installation directory, typically /opt, but configurable elsewhere
install_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


def resolve_jinja_templates(data, context, max_iterations=10):
    """
    Recursively resolve Jinja2-style template variables in a dictionary.

    Args:
        data: Dictionary or string containing template variables
        context: Dictionary of variables to substitute
        max_iterations: Maximum number of resolution passes to prevent infinite loops

    Returns:
        Resolved data with template variables substituted
    """
    import re

    def substitute_string(text, ctx):
        """Substitute {{ variable }} patterns in a string."""
        if not isinstance(text, str):
            return text

        # Pattern to match {{ variable_name }}
        pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'

        def replacer(match):
            var_name = match.group(1)
            if var_name in ctx:
                return str(ctx[var_name])
            else:
                # Leave unresolved variables as-is for now
                return match.group(0)

        return re.sub(pattern, replacer, text)

    def resolve_recursive(obj, ctx):
        """Recursively resolve templates in nested data structures."""
        if isinstance(obj, dict):
            return {k: resolve_recursive(v, ctx) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_recursive(item, ctx) for item in obj]
        elif isinstance(obj, str):
            return substitute_string(obj, ctx)
        else:
            return obj

    # Make multiple passes to resolve interdependent variables
    current_data = data
    current_context = dict(context)  # Copy to avoid modifying original

    for iteration in range(max_iterations):
        previous_data = current_data

        # Resolve templates using current context
        current_data = resolve_recursive(current_data, current_context)

        # Update context with newly resolved values (if data is a dict)
        if isinstance(current_data, dict):
            current_context.update(current_data)

        # Check if we've converged (no more changes)
        if current_data == previous_data:
            break
    else:
        print(f"Warning: Template resolution did not converge after {max_iterations} iterations")

    return current_data


def load_defaults_from_paths_yml():
    """
    Load default paths from config/paths.yml with template resolution.

    Returns:
        dict: Resolved configuration dictionary

    Raises:
        SystemExit: If paths.yml cannot be loaded or parsed
    """
    paths_yml_file = os.path.join(install_dir, "meza", "config", "paths.yml")

    if not os.path.isfile(paths_yml_file):
        print(f"ERROR: Required configuration file not found: {paths_yml_file}")
        print("Meza requires a properly configured paths.yml file to operate.")
        sys.exit(1)

    try:
        # Load the raw YAML content
        with open(paths_yml_file, 'r', encoding='utf-8') as f:
            raw_config = yaml.load(f, Loader=yaml.Loader)

        if not isinstance(raw_config, dict):
            raise ValueError("paths.yml must contain a YAML dictionary")

        # Set up initial context with m_install_dir
        initial_context = {
            "m_install_dir": install_dir
        }

        # Resolve all template variables
        resolved_config = resolve_jinja_templates(raw_config, initial_context)

        # Extract the specific variables meza.py needs
        required_vars = [
            "m_config_i18n_dir", "m_data_dir", "m_data_deploy_log_file", "m_data_create_wiki_log_file", "m_data_logs_dir",
            "m_conf_secret_dir", "m_conf_users_dir", "m_conf_vault_dir"
        ]

        defaults = {}
        missing_vars = []

        for var in required_vars:
            if var in resolved_config:
                defaults[var] = resolved_config[var]
            else:
                missing_vars.append(var)

        if missing_vars:
            print(f"ERROR: Required variables missing from paths.yml: {', '.join(missing_vars)}")
            print(f"Please ensure paths.yml contains all required path definitions.")
            sys.exit(1)

        return defaults

    except yaml.YAMLError as e:
        print(f"ERROR: Failed to parse paths.yml: {e}")
        print(f"Please check the YAML syntax in: {paths_yml_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to load configuration from paths.yml: {e}")
        print(f"Configuration file: {paths_yml_file}")
        sys.exit(1)


# Load defaults from paths.yml - no fallbacks, fail fast if not available
defaults = load_defaults_from_paths_yml()

# Handle pressing of ctrl-c. Make sure to remove lock file when deploying.
DEPLOY_LOCK_ENVIRONMENT = False


def sigint_handler(sig, frame):  # pylint: disable=unused-argument
    """
    Signal handler for SIGINT (Ctrl+C) interrupt.

    Args:
        sig (int): The signal number.
        frame (frame): The current stack frame.
    """
    print('Cancelling...')
    if DEPLOY_LOCK_ENVIRONMENT:
        print('Deploy underway...removing lock file')
        unlock_deploy(DEPLOY_LOCK_ENVIRONMENT)
    sys.exit(1)


signal.signal(signal.SIGINT, sigint_handler)


def load_yaml(filepath):
    """
    Load YAML data from a file.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        dict: The parsed YAML data.

    Raises:
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    with open(filepath, encoding='utf-8') as stream:
        try:
            return yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
            return None


# Hard-coded for now, because I'm not sure where to set it yet
LANGUAGE = "en"
i18n = load_yaml(os.path.join(defaults['m_config_i18n_dir'], LANGUAGE + ".yml"))


def main(argv):
    """
    The main function of the script.

    Parameters:
    - argv (list): The list of command-line arguments passed to the script.

    Returns:
    None
    """

    # meza requires a command parameter. No first param, no command. Display
    # help. Also display help if explicitly specifying help.
    if not argv:
        display_docs('help')
        sys.exit(1)
    elif argv[0] in ('-h', '--help'):
        display_docs('help')
        sys.exit(0)  # asking for help doesn't give error code
    elif argv[0] in ('-v', '--version'):
        version = subprocess.check_output(
            ["git", f"--git-dir={install_dir}/meza/.git", "describe", "--tags", "--always"])
        commit = subprocess.check_output(
            ["git", f"--git-dir={install_dir}/meza/.git", "rev-parse", "HEAD"])
        print("Meza " + version.strip().decode())
        print("Commit " + commit.strip().decode())
        print("Mediawiki EZ Admin")
        print("")
        sys.exit(0)

    # Every command has a sub-command. No second param, no sub-command. Display
    # help for that specific sub-command.
    # sub-command "update" and "list-wikis" do not require additional directives
    if len(argv) == 1 and argv[0] not in ("update", "list-wikis"):
        display_docs(argv[0])
        sys.exit(1)
    elif len(argv) == 2 and argv[1] in ('--help', '-h'):
        display_docs(argv[0])
        sys.exit(0)

    command = argv[0]
    command_fn = f"meza_command_{argv[0]}".replace("-", "_")

    # if command_fn is a valid Python function, pass it all remaining args
    if command_fn in globals() and callable(globals()[command_fn]):
        globals()[command_fn](argv[1:])
    else:
        print()
        print(f"{command} is not a valid command")
        sys.exit(1)


def meza_command_deploy(argv):
    """
    Deploy the environment specified by the given argv.

    Args:
        argv (list): A list of command-line arguments.

    Returns:
        None
    """
    env = argv[0]

    rc = check_environment(env)

    lock_success = request_lock_for_deploy(env)

    if not lock_success:
        print(f"Deploy for environment {env} in progress. Exiting")
        sys.exit(1)

    # return code != 0 means failure
    if rc:
        if env == "monolith":
            meza_command_setup_env(env, True)
        else:
            sys.exit(rc)

    more_extra_vars = {}

    # strip environment off of it
    argv = argv[1:]

    # save state of args before stripping -o and --overwrite
    args_string = ' '.join(argv)

    # if argv[1:] includes -o or --overwrite
    if len(set(argv).intersection({"-o", "--overwrite"})) > 0:
        # remove -o and --overwrite from args;
        argv = [value for value in argv[:]
                if value not in ["-o", "--overwrite"]]

        more_extra_vars['force_overwrite_from_backup'] = True

    if len(set(argv).intersection({"--no-firewall"})) > 0:
        # remove --no-firewall from args:
        argv = [value for value in argv[:] if value not in ["--no-firewall"]]

        more_extra_vars['firewall_skip_tasks'] = True

    if not more_extra_vars:
        more_extra_vars = False

    start = get_datetime_string()
    unique = hashlib.sha1((start + env).encode('utf-8')).hexdigest()[:8]

    write_deploy_log(start, env, unique, 'start', args_string)

    shell_cmd = playbook_cmd('site', env, more_extra_vars)
    if len(argv) > 0:
        shell_cmd = shell_cmd + argv

    deploy_log = get_deploy_log_path(env)

    return_code = meza_shell_exec(shell_cmd, True, deploy_log)

    unlock_deploy(env)
    if not return_code:
        condition = 'complete'
    else:
        condition = 'failed'

    end = get_datetime_string()
    write_deploy_log(end, env, unique, condition, args_string)

    meza_shell_exec_exit(return_code)

#
# Intended to be used by cron job to check for changes to config and meza. Can
# also be called with `meza autodeploy <env>`
#


def meza_command_autodeploy(argv):
    """
    Perform an autodeploy for the specified environment.

    Args:
        argv (list): List of command line arguments.

    Returns:
        None
    """
    env = argv[0]

    rc = check_environment(env)

    lock_success = request_lock_for_deploy(env)

    if not lock_success:
        print(f"Deploy for environment {env} in progress. Exiting")
        sys.exit(1)

    # return code != 0 means failure
    if rc:
        sys.exit(rc)

    more_extra_vars = False

    # strip environment off of it
    argv = argv[1:]

    if len(argv) > 0:
        more_extra_vars = {
            'deploy_type': argv[0]
        }
        argv = argv[1:]  # strip deploy type off

    if len(argv) > 0:
        more_extra_vars['deploy_args'] = argv[0]
        argv = argv[1:]  # strip deploy args off

    shell_cmd = playbook_cmd('check-for-changes', env, more_extra_vars)
    if len(argv) > 0:
        shell_cmd = shell_cmd + argv

    return_code = meza_shell_exec(shell_cmd)

    unlock_deploy(env)  # double check

    meza_shell_exec_exit(return_code)

# Just a wrapper on deploy that does some notifications. This needs some
# improvement. FIXME. Lots of duplication between this and meza_command_deploy
# and meza_command_autodeploy


def meza_command_deploy_notify(argv):
    """
    Deploy the environment and notify the deployment status.

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None
    """
    env = argv[0]

    rc = check_environment(env)

    lock_success = request_lock_for_deploy(env)

    if not lock_success:
        print(f"Deploy for environment {env} in progress. Exiting")
        sys.exit(1)

    # return code != 0 means failure
    if rc:
        sys.exit(rc)

    more_extra_vars = False

    # strip environment off of it
    argv = argv[1:]

    if len(argv) > 0:
        more_extra_vars = {
            'deploy_type': argv[0]
        }
        argv = argv[1:]  # strip deploy type off

    if len(argv) > 0:
        more_extra_vars['deploy_args'] = argv[0]
        argv = argv[1:]  # strip deploy args off

    shell_cmd = playbook_cmd('deploy-notify', env, more_extra_vars)
    if len(argv) > 0:
        shell_cmd = shell_cmd + argv

    return_code = meza_shell_exec(shell_cmd)

    unlock_deploy(env)  # double check

    meza_shell_exec_exit(return_code)


def request_lock_for_deploy(env):
    """
    Requests a lock for deployment.

    Args:
        env (str): The environment for which the lock is requested.

    Returns:
        dict or bool: If the lock is successfully created, returns a dictionary
        containing the process ID (pid) and timestamp of the lock creation.
        Otherwise, returns False.

    Raises:
        None

    """
    lock_file = get_lock_file_path(env)

    if os.path.isfile(lock_file):
        print(f"Deploy lock file already exists at {lock_file}")
        return False

    print(f"Create deploy lock file at {lock_file}")
    pid = str(os.getpid())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Before creating lock file, this global must be set in order for ctrl-c
    # interrupts (SIGINT) to be properly managed (SIGINT will call
    # sigint_handler function)
    global DEPLOY_LOCK_ENVIRONMENT
    DEPLOY_LOCK_ENVIRONMENT = env

    with open(lock_file, 'w', encoding='utf-8') as f:
        f.write(f"{pid}\n{timestamp}")
        f.close()

    # Apache guaranteed to exist due to bootstrap sequencing (Issue #287)
    # If neither apache nor www-data group exists, system is not properly set up
    try:
        grp.getgrnam('apache')
        meza_chown(lock_file, 'meza-ansible', 'apache')
        os.chmod(lock_file, 0o664)
    except KeyError:
        try:
            grp.getgrnam('www-data')  # Debian/Ubuntu
            meza_chown(lock_file, 'meza-ansible', 'www-data')
            os.chmod(lock_file, 0o664)
        except KeyError:
            print("\nERROR: Neither 'apache' nor 'www-data' group exists on this system.")
            print("This indicates that Meza has not been properly set up on this control host.")
            print("Apache must be installed before running meza commands.")
            print("\nPlease follow the installation instructions at:")
            print("https://www.mediawiki.org/wiki/Meza")
            sys.exit(1)

    return {"pid": pid, "timestamp": timestamp}


def unlock_deploy(env):
    """
    Removes the lock file for the specified environment.

    Args:
        env (str): The environment for which to unlock the deployment.

    Returns:
        bool: True if the lock file was successfully removed, False otherwise.
    """
    lock_file = get_lock_file_path(env)
    if os.path.exists(lock_file):
        os.remove(lock_file)
        return True
    else:
        return False


def get_lock_file_path(env):
    """
    Get the path of the lock file for the given environment.

    Args:
        env (str): The environment name.

    Returns:
        str: The path of the lock file.
    """
    lock_file = os.path.join(
        defaults['m_data_dir'], f"env-{env}-deploy.lock")
    return lock_file


def write_deploy_log(timestamp, env, unique, condition, args_string):
    """
    Write deployment log to a file.

    Args:
        timestamp (str): The timestamp of the deployment.
        env (str): The environment in which the deployment is performed.
        unique (str): A unique identifier for the deployment.
        condition (str): The condition of the deployment.
        args_string (str): A string representation of the deployment arguments.

    Returns:
        None
    """
    deploy_log = defaults['m_data_deploy_log_file']

    line = (f"{timestamp}\t{env}\t{unique}\t{condition}\t"
            f"{get_git_describe_tags(f'{install_dir}/meza')}\t"
            f"{get_git_hash(f'{install_dir}/meza')}\t"
            f"{get_git_hash(f'{install_dir}/conf-meza/secret')}\t"
            f"{get_git_hash(f'{install_dir}/conf-meza/public')}\t"
            f"{args_string}\n")

    log_dir = os.path.dirname(os.path.realpath(deploy_log))

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    with open(deploy_log, "a", encoding='utf-8') as myfile:
        myfile.write(line)


def write_create_wiki_log(timestamp, env, unique, condition, wiki_id, wiki_name, args_string):
    """
    Write create-wiki log to a file.

    Args:
        timestamp (str): The timestamp of the wiki creation.
        env (str): The environment in which the wiki is created.
        unique (str): A unique identifier for the operation.
        condition (str): The condition of the operation.
        wiki_id (str): The ID of the wiki being created.
        wiki_name (str): The display name of the wiki being created.
        args_string (str): A string representation of the arguments.

    Returns:
        None
    """
    create_wiki_log = defaults['m_data_create_wiki_log_file']

    line = (f"{timestamp}\t{env}\t{unique}\t{condition}\t"
            f"{wiki_id}\t{wiki_name}\t"
            f"{get_git_describe_tags(f'{install_dir}/meza')}\t"
            f"{get_git_hash(f'{install_dir}/meza')}\t"
            f"{get_git_hash(f'{install_dir}/conf-meza/secret')}\t"
            f"{get_git_hash(f'{install_dir}/conf-meza/public')}\t"
            f"{args_string}\n")

    log_dir = os.path.dirname(os.path.realpath(create_wiki_log))

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    with open(create_wiki_log, "a", encoding='utf-8') as myfile:
        myfile.write(line)


def get_create_wiki_log_path(env):
    """
    Get the path to the create-wiki processing log file for a given environment.

    Args:
        env (str): The environment name.

    Returns:
        str: The path to the create-wiki processing log file, or the most recent log file if no operation is active.

    """
    log_dir = os.path.join(defaults['m_data_logs_dir'], 'create-wiki-output')

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    try:
        # Try to get timestamp from active create-wiki operation (not implemented yet, but future-ready)
        # For now, find the most recent log file for this environment
        log_path = find_most_recent_log_file(env, log_dir)
    except:
        # Find the most recent log file for this environment
        log_path = find_most_recent_log_file(env, log_dir)

    return log_path

# "meza deploy-check <ENV>" to return 0 on no deploy, 1 on deploy is active


def meza_command_deploy_check(argv):
    """
    Check if a Meza environment is currently deploying.

    Args:
        argv (list): A list of command-line arguments. The first argument should be the
            environment name.

    Returns:
        None

    Raises:
        SystemExit: If the lock file exists, indicating that the environment is currently deploying.

    """
    env = argv[0]
    lock_file = get_lock_file_path(env)
    if os.path.isfile(lock_file):
        print(f"Meza environment '{env}' deploying; {lock_file} exists")
        sys.exit(1)
    else:
        print(f"Meza environment '{env}' not deploying")
        sys.exit(0)


def meza_command_deploy_lock(argv):
    """
    Locks the specified environment for deployment.

    Args:
        argv (list): A list containing the command-line arguments. The first element should be
            the environment name.

    Returns:
        None
    """
    env = argv[0]
    success = request_lock_for_deploy(env)
    if success:
        print(f"Environment '{env}' locked for deploy")
        sys.exit(0)
    else:
        print(f"Environment '{env}' could not be locked")
        sys.exit(1)


def meza_command_deploy_unlock(argv):
    """
    Unlocks the deploy lock for the specified environment.

    Args:
        argv (list): A list containing the command-line arguments. The first element should be
            the environment name.

    Returns:
        None

    Raises:
        None
    """
    env = argv[0]
    success = unlock_deploy(env)
    if success:
        print(f"Environment '{env}' deploy lock removed")
        sys.exit(0)
    else:
        print(f"Environment '{env}' is not deploying")
        sys.exit(1)


def meza_command_deploy_kill(argv):
    """
    Terminate a Meza deployment process for the specified environment.

    Args:
        argv (list): A list of command-line arguments. The first argument should be the environment.

    Returns:
        None

    Raises:
        None
    """
    env = argv[0]
    lock_file = get_lock_file_path(env)
    if os.path.isfile(lock_file):
        print(f"Meza environment {env} deploying; killing...")
        di = get_deploy_info(env)
        os.system(f"kill $(ps -o pid= --ppid {di['pid']})")
        time.sleep(2)
        os.system(
            'wall "Meza deploy terminated using \'meza deploy-kill\' command."')
        sys.exit(0)
    else:
        print(f"Meza environment '{env}' not deploying")
        sys.exit(1)


def get_deploy_info(env):
    """
    Retrieves deployment information for a given environment.

    Args:
        env (str): The name of the environment.

    Returns:
        dict: A dictionary containing the deployment information, including the process ID (pid)
            and timestamp.

    Raises:
        FileNotFoundError: If the lock file for the environment does not exist.

    """
    lock_file = get_lock_file_path(env)
    if not os.path.isfile(lock_file):
        raise FileNotFoundError(f"Environment '{env}' not deploying")
    with open(lock_file, encoding='utf-8') as f:
        pid = f.readline()
        timestamp = f.readline()
        f.close()
        return {"pid": pid, "timestamp": timestamp}


def get_deploy_log_path(env):
    """
    Get the path to the deploy log file for a given environment.

    Args:
        env (str): The environment name.

    Returns:
        str: The path to the deploy log file, or the most recent log file if no deployment is active.

    """
    log_dir = os.path.join(defaults['m_data_logs_dir'], 'deploy-output')

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    try:
        # Try to get timestamp from active deployment
        timestamp = get_deploy_info(env)["timestamp"]
        filename = f"{env}-{timestamp}.log"
        log_path = os.path.join(log_dir, filename)
    except FileNotFoundError:
        # No active deployment, find the most recent log file for this environment
        log_path = find_most_recent_log_file(env, log_dir)

    return log_path


def find_most_recent_log_file(env, log_dir):
    """
    Find the most recent log file for a given environment.

    Args:
        env (str): The environment name.
        log_dir (str): The directory containing log files.

    Returns:
        str: The path to the most recent log file, or None if no logs found.

    """
    import glob

    # Look for log files matching the pattern: env-*.log
    pattern = os.path.join(log_dir, f"{env}-*.log")
    log_files = glob.glob(pattern)

    if not log_files:
        return None

    # Sort by modification time, most recent first
    log_files.sort(key=os.path.getmtime, reverse=True)

    return log_files[0]


def meza_command_deploy_log(argv):
    """
    Get the deploy log path for the specified environment.

    Args:
        argv (list): A list containing the environment name.

    Returns:
        str: The path to the deploy log file.

    """
    env = argv[0]
    log_path = get_deploy_log_path(env)

    if log_path is None:
        print(f"No deployment log files found for environment '{env}'")
        sys.exit(1)
    else:
        print(log_path)


def meza_command_deploy_tail(argv):
    """
    Display the tail of the deploy log for the specified environment.

    Args:
        argv (list): A list of command-line arguments. The first element should be the environment.

    Returns:
        None
    """
    env = argv[0]
    log_path = get_deploy_log_path(env)

    if log_path is None:
        print(f"No deployment log files found for environment '{env}'")
        print("Try running a deployment first with:")
        print(f"  sudo meza deploy {env}")
        sys.exit(1)
    elif not os.path.isfile(log_path):
        print(f"Log file not found: {log_path}")
        print("The deployment may not have started yet or the log file was removed.")
        sys.exit(1)
    else:
        print(f"Following deployment log: {log_path}")
        os.system(" ".join(["tail", "-f", log_path]))


def meza_command_create_wiki_log(argv):
    """
    Get the create-wiki processing log path for the specified environment.

    Args:
        argv (list): A list containing the environment name.

    Returns:
        str: The path to the create-wiki processing log file.

    """
    env = argv[0]
    log_path = get_create_wiki_log_path(env)

    if log_path is None:
        print(f"No create-wiki log files found for environment '{env}'")
        sys.exit(1)
    else:
        print(log_path)


def meza_command_create_wiki_tail(argv):
    """
    Display the tail of the create-wiki processing log for the specified environment.

    Args:
        argv (list): A list of command-line arguments. The first element should be the environment.

    Returns:
        None
    """
    env = argv[0]
    log_path = get_create_wiki_log_path(env)

    if log_path is None:
        print(f"No create-wiki log files found for environment '{env}'")
        print("Try running a wiki creation first with:")
        print(f"  sudo meza create wiki {env}")
        sys.exit(1)
    elif not os.path.isfile(log_path):
        print(f"Log file not found: {log_path}")
        print("The create-wiki operation may not have started yet or the log file was removed.")
        sys.exit(1)
    else:
        print(f"Following create-wiki log: {log_path}")
        os.system(" ".join(["tail", "-f", log_path]))


def get_git_hash(directory):
    """
    Get the git hash of a directory.

    Args:
        directory (str): The directory path.

    Returns:
        str: The git hash of the directory if it is a git repository, otherwise returns
            "not-a-git-repo".
    """
    git_dir = f"{directory}/.git"

    if os.path.isdir(git_dir):
        try:
            commit = subprocess.check_output(
                ["git", f"--git-dir={git_dir}", "rev-parse", "HEAD"]).strip()
        except BaseException:
            commit = "git-error"
        return commit
    else:
        return "not-a-git-repo"


def get_git_describe_tags(directory):
    """
    Get the description of the latest Git tag in the specified directory.

    Args:
        directory (str): The directory path.

    Returns:
        str: The description of the latest Git tag if the directory is a Git repository,
             "git-error" if there was an error executing the Git command,
             or "not-a-git-repo" if the directory is not a Git repository.
    """
    git_dir = f"{directory}/.git"

    if os.path.isdir(git_dir):
        try:
            tags = subprocess.check_output(
                ["git", f"--git-dir={git_dir}", "describe", "--tags", "--always"]).strip()
        except BaseException:
            tags = "git-error"
        return tags
    else:
        return "not-a-git-repo"

# env
# docker

def meza_command_setup(argv):
    """
    Sets up the command for the Meza script.

    Args:
        argv (list): The list of command line arguments.

    Returns:
        None
    """
    sub_command = argv[0]
    if sub_command == "dev":
        print("setup dev is removed; configure developer tools manually")
        sys.exit(1)
    command_fn = "meza_command_setup_" + sub_command

    # if command_fn is a valid Python function, pass it all remaining args
    if command_fn in globals() and callable(globals()[command_fn]):
        globals()[command_fn](argv[1:])
    else:
        print()
        print(sub_command + " is not a valid sub-command for setup")
        sys.exit(1)


def meza_command_update(argv):
    """
    Update the Meza repository to a specific version or branch.

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None

    Raises:
        None

    """
    # This function executes many Git commands that need to be from /otp/meza
    os.chdir("/opt/meza")

    # Define a special git remote repository so we can control its settings
    # Else, a user using Vagrant may have their origin remote setup for SSH
    # but these commands need HTTPS.
    meza_remote = "mezaremote"

    check_remotes = subprocess.check_output(
        ["git", "remote"]).decode().strip().split("\n")
    if meza_remote not in check_remotes:
        subprocess.check_output(
            ["git", "remote", "add", meza_remote,
                "https://github.com/nasa/meza.git"]
        )

    # Get latest commits and tags from mezaremote
    subprocess.check_output(["git", "fetch", meza_remote])
    try:
        subprocess.check_output(["git", "fetch", meza_remote, "--tags"])
    except subprocess.CalledProcessError:
        # If tag fetch fails due to conflicts, try with --force
        subprocess.check_output(
            ["git", "fetch", meza_remote, "--tags", "--force"])
    tags_text = subprocess.check_output(["git", "tag", "-l"]).decode()

    if not argv:
        # print fetch.strip()
        print("The following versions are available:")

        # Filter tags to only show those starting with "43" and sort numerically
        all_tags = [tag.strip()
                    for tag in tags_text.strip().split("\n") if tag.strip()]
        version_43_tags = [tag for tag in all_tags if tag.startswith("43.")]

        # Sort numerically by parsing version components
        def version_sort_key(version):
            try:
                # Split version string like "43.25.11" into [43, 25, 11]
                parts = version.split(".")
                return [int(part) for part in parts]
            except (ValueError, IndexError):
                # If parsing fails, put at end
                return [999, 999, 999]

        version_43_tags.sort(key=version_sort_key)

        for tag in version_43_tags:
            print(tag)

        print("")
        closest_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--always"]).decode()
        print(f"You are currently on version {closest_tag.strip()}")
        print("To change versions, do 'sudo meza update <version>'")
    elif len(argv) > 1:
        print(f"Unknown argument {argv[1]}")
    else:
        # Needed else 'git status' gives bad response
        status = subprocess.check_output(
            ["git", "status", "--untracked-files=no", "--porcelain"]).decode()
        status = status.strip()
        if status:
            print(f"'git status' not empty:\n{status}")

        version = argv[0]
        if not status:
            tags = tags_text.split("\n")
            branches = subprocess.check_output(
                ["git", "branch", "-a"]).decode().strip().split("\n")
            branches = map(str.strip, branches)
            if version in tags:
                version_type = "at version"
                tag_version = f"tags/{version}"
                subprocess.check_output(
                    ["git", "checkout", tag_version], stderr=subprocess.STDOUT)
            elif version in branches or f"* {version}" in branches:
                version_type = "on branch"
                subprocess.check_output(
                    ["git", "checkout", version], stderr=subprocess.STDOUT)
                subprocess.check_output(
                    ["git", "reset", "--hard", f"mezaremote/{version}"])
            elif f"remotes/{meza_remote}/{version}" in branches:
                version_type = "on branch"
                subprocess.check_output(
                    ["git", "checkout", "-b", version, '-t',
                        f"{meza_remote}/{version}"],
                    stderr=subprocess.STDOUT,
                )
            else:
                print(f"{version} is not a valid version or branch")
                sys.exit(1)
            print("")
            print("")
            print(f"Meza now {version_type} {version}")
            print("Now deploy changes with 'sudo meza deploy <environment>'")
        else:
            print(
                "Files have been modified in /opt/meza. Clean them up before proceeding.")
            print(f"MSG: {status}")

# FIXME #824: This function is big.


def meza_command_setup_env(argv, return_not_exit=False):
    """
    Sets up the environment for the Meza deployment.

    Args:
        argv (str or list): The command line arguments passed to the function.
            If a string is provided, it is treated as the environment name.
            If a list is provided, the first element is treated as the environment name.
        return_not_exit (bool, optional): If True, the function returns the exit code instead of
            exiting the program. Defaults to False.

    Returns:
        int or None: The exit code if `return_not_exit` is True, otherwise None.

    Raises:
        Exception: If an error occurs while parsing the command line arguments.

    """

    if isinstance(argv, str):
        env = argv
    else:
        env = argv[0]

    if not os.path.isdir("/opt/conf-meza"):
        os.mkdir("/opt/conf-meza")

    if not os.path.isdir("/opt/conf-meza/secret"):
        os.mkdir("/opt/conf-meza/secret")

    if os.path.isdir("/opt/conf-meza/secret/" + env):
        print("")
        print(f"Environment {env} already exists")
        sys.exit(1)

    fqdn = db_pass = private_net_zone = False
    try:
        opts, _ = getopt.getopt(
            argv[1:], "", ["fqdn=", "db_pass=", "private_net_zone="])
    except Exception as e:
        print(str(e))
        print('meza setup env <env> [options]')
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--fqdn":
            fqdn = arg
        elif opt == "--db_pass":
            # This will put the DB password on the command line, so should
            # only be done in testing cases
            db_pass = arg
        elif opt == "--private_net_zone":
            private_net_zone = arg
        else:
            print("Unrecognized option " + opt)
            sys.exit(1)

    if not fqdn:
        fqdn = prompt("fqdn")

    if not db_pass:
        db_pass = prompt_secure("db_pass")

    # No need for private networking. Set to public.
    if env == "monolith":
        private_net_zone = "public"
    elif not private_net_zone:
        private_net_zone = prompt("private_net_zone")

    # Ansible environment variables
    env_vars = {
        'env': env,

        'fqdn': fqdn,
        'private_net_zone': private_net_zone,

        # Set all db passwords the same
        'mysql_root_pass': db_pass,
        'wiki_app_db_pass': db_pass,
        'db_slave_pass': db_pass,

        # Generate a random secret key
        'wg_secret_key': random_string(
            num_chars=64, valid_chars=string.ascii_letters + string.digits)

    }

    server_types = [
        'load_balancers',
        'app_servers',
        'memcached_servers',
        'db_slaves',
        'elastic_servers',
        'backup_servers',
        'logging_servers']

    for stype in server_types:
        if stype in os.environ:
            env_vars[stype] = [x.strip() for x in os.environ[stype].split(',')]
        elif stype == "db_slaves":
            # unless db_slaves are explicitly set, don't configure any
            env_vars["db_slaves"] = []
        elif "default_servers" in os.environ:
            env_vars[stype] = [x.strip()
                               for x in os.environ["default_servers"].split(',')]
        else:
            env_vars[stype] = ['localhost']

    if "db_master" in os.environ:
        env_vars["db_master"] = os.environ["db_master"].strip()
    elif "default_servers" in os.environ:
        env_vars["db_master"] = os.environ["default_servers"].strip()
    else:
        env_vars["db_master"] = 'localhost'

    json_env_vars = json.dumps(env_vars)

    # Create temporary extra vars file in secret directory so passwords
    # are not written to command line. Putting in secret should make
    # permissions acceptable since this dir will hold secret info, though it's
    # sort of an odd place for a temporary file. Perhaps /root instead?
    extra_vars_file = os.path.join(
        defaults['m_conf_secret_dir'], "temp_vars.json")
    if os.path.isfile(extra_vars_file):
        os.remove(extra_vars_file)
    with open(extra_vars_file, 'w', encoding='utf-8') as f:
        f.write(json_env_vars)
        f.close()

    # Make sure temp_vars.json is accessible. On the first run of deploy it is
    # possible that user meza-ansible will not be able to reach this file,
    # specifically if the system has a restrictive umask set (e.g 077).
    meza_chown(defaults['m_conf_secret_dir'], 'meza-ansible', 'wheel')
    meza_chown(extra_vars_file, 'meza-ansible', 'wheel')
    os.chmod(extra_vars_file, 0o664)

    shell_cmd = playbook_cmd("setup-env") + \
        ["--extra-vars", '@' + extra_vars_file]
    rc = meza_shell_exec(shell_cmd)

    os.remove(extra_vars_file)

    print("")
    print("Please review your host file. Run command:")
    print(f"  sudo vi /opt/conf-meza/secret/{env}/hosts")
    print("Please review your secret config. Run command:")
    print(f"  sudo vi /opt/conf-meza/secret/{env}/secret.yml")
    if return_not_exit:
        return rc
    else:
        sys.exit(rc)

# @FIXME this is obsolete (because it's for CentOS) but should be updated

def meza_command_setup_docker(argv):  # pylint: disable=unused-argument
    """
    Set up Docker for the Meza command.

    Args:
        argv (list): The command line arguments.

    Returns:
        None
    """
    shell_cmd = playbook_cmd("getdocker")
    meza_shell_exec(shell_cmd)
    sys.exit(0)


def meza_command_migrate_wikis(argv):
    """
    Migrate existing directory-based wikis to declarative configuration.

    Scans existing wiki directories and extracts wiki names from base.php files
    to populate the wikis: section in public.yml.

    Args:
        argv (list): The command line arguments. First argument should be environment name.

    Returns:
        None

    Raises:
        SystemExit: If the environment is not provided or invalid.

    """
    if len(argv) < 1:
        print("You must specify an environment: 'meza migrate-wikis ENV'")
        sys.exit(1)

    env = argv[0]

    rc = check_environment(env)
    if rc > 0:
        meza_shell_exec_exit(rc)

    print("Migrating existing wikis to declarative configuration...")
    shell_cmd = playbook_cmd("migrate-wikis", env)
    rc = meza_shell_exec(shell_cmd)
    meza_shell_exec_exit(rc)


def meza_command_debug(argv):
    """
    Debug Ansible variables and facts for an environment.

    General-purpose debug command that can output any Ansible variable or fact.
    Default variable is 'list_of_wikis' if not specified.

    Args:
        argv (list): [environment, variable_name (optional)]

    Returns:
        None

    Raises:
        SystemExit: If the environment is invalid.

    """
    if len(argv) < 1:
        print("You must specify an environment: 'meza debug ENV [variable]'")
        sys.exit(1)

    env = argv[0]
    debug_var = argv[1] if len(argv) >= 2 else 'list_of_wikis'

    rc = check_environment(env)
    if rc > 0:
        meza_shell_exec_exit(rc)

    # Use general-purpose debug playbook
    shell_cmd = playbook_cmd('debug', env, {'debug_var': debug_var})
    rc = meza_shell_exec(shell_cmd, False)
    meza_shell_exec_exit(rc)


def meza_command_list_wikis(argv):
    """
    List all wikis configured for an environment.

    Uses the general-purpose debug.yml playbook to display list_of_wikis.
    Default environment is 'monolith' if not specified.

    Args:
        argv (list): The command line arguments. First argument should be environment name (optional).

    Returns:
        None

    Raises:
        SystemExit: If the environment is invalid.

    """
    # Default environment is monolith if not specified
    env = argv[0] if len(argv) >= 1 else "monolith"

    rc = check_environment(env)
    if rc > 0:
        meza_shell_exec_exit(rc)

    # Use general-purpose debug playbook
    shell_cmd = playbook_cmd('debug', env, {'debug_var': 'list_of_wikis'})
    rc = meza_shell_exec(shell_cmd, False)
    meza_shell_exec_exit(rc)


def meza_command_create(argv):
    """
    Create a new wiki in the specified environment.

    This command supports two modes:
    1. Interactive mode (wiki) - Prompts user for wiki details
    2. Non-interactive mode (wiki-promptless) - Uses command-line arguments

    Usage:
        Interactive:    meza create wiki <environment>
        Non-interactive: meza create wiki-promptless <environment> <wiki_id> <wiki_name> [admin_password]

    Examples:
        # Interactive wiki creation (will prompt for details)
        meza create wiki monolith
        meza create wiki production

        # Non-interactive wiki creation
        meza create wiki-promptless monolith testwiki "Test Wiki" "SecureP@ssw0rd123!"
        meza create wiki-promptless production blogwiki "Company Blog" "MyS3cur3P@ss!"

    Args:
        argv (list): Command line arguments:
            [0] - Sub-command: 'wiki' or 'wiki-promptless'
            [1] - Environment name (required)
            [2] - Wiki ID (required for wiki-promptless only)
            [3] - Wiki display name (required for wiki-promptless only)
            [4] - Admin password (optional for wiki-promptless; if not provided, generates secure random password)

    Returns:
        None

    Raises:
        SystemExit: If required arguments are missing or environment is invalid.

    Notes:
        - Wiki IDs must be unique within the environment
        - Wiki IDs should be lowercase, alphanumeric (no spaces or special chars)
        - Uses create-wiki.yml or create-wiki-promptless.yml Ansible playbooks
        - All operations are logged to create-wiki.log for audit purposes
    """
    sub_command = argv[0]

    if sub_command in ("wiki", "wiki-promptless"):

        if len(argv) < 2:
            print("You must specify an environment: 'meza create wiki ENV'")
            sys.exit(1)

        env = argv[1]

        rc = check_environment(env)
        if rc > 0:
            meza_shell_exec_exit(rc)

        # Set up logging
        start = get_datetime_string()
        unique = hashlib.sha1((start + env).encode('utf-8')).hexdigest()[:8]
        args_string = ' '.join(argv)

        # Get wiki details for logging
        if sub_command == "wiki-promptless":
            if len(argv) < 4:
                print("create wiki-promptless requires wiki_id and wiki_name arguments")
                print("Usage: meza create wiki-promptless <env> <wiki_id> <wiki_name> [admin_password]")
                sys.exit(1)
            wiki_id = argv[2]
            wiki_name = argv[3]
            # Optional admin password; generate secure random if not provided
            if len(argv) >= 5:
                admin_password = argv[4]
            else:
                # Generate a secure random password meeting MediaWiki requirements
                import secrets
                import string
                # Ensure password has all required character types
                chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
                admin_password = ''.join(secrets.choice(chars) for _ in range(16))
                # Ensure it contains at least one of each required type
                admin_password = (
                    secrets.choice(string.ascii_uppercase) +
                    secrets.choice(string.ascii_lowercase) +
                    secrets.choice(string.digits) +
                    secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?") +
                    admin_password[4:]
                )
                print(f"Generated secure admin password: {admin_password}")
                print("Please save this password - it will not be displayed again!")
        else:
            # For interactive mode, we don't know the wiki details yet
            wiki_id = "interactive"
            wiki_name = "interactive"

        # Write start log
        write_create_wiki_log(start, env, unique, 'start', wiki_id, wiki_name, args_string)

        playbook = "create-" + sub_command

        if sub_command == "wiki-promptless":
            shell_cmd = playbook_cmd(
                playbook, env, {'wiki_id': wiki_id, 'wiki_name': wiki_name, 'admin_password': admin_password})
        else:
            shell_cmd = playbook_cmd(playbook, env)

        # Execute with processing log (similar to deploy-output)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        log_file = f"{defaults['m_data_logs_dir']}/create-wiki-output/{env}-{timestamp}.log"
        log_dir = os.path.dirname(log_file)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        rc = meza_shell_exec(shell_cmd, True, log_file)

        # Write completion log
        end = get_datetime_string()
        if not rc:
            condition = 'complete'
        else:
            condition = 'failed'

        write_create_wiki_log(end, env, unique, condition, wiki_id, wiki_name, args_string)
        meza_shell_exec_exit(rc)


def meza_command_delete(argv):
    """
    Delete wikis or other components in the Meza environment.

    This command supports deletion of different components with three modes:
    1. Interactive wiki deletion (wiki) - Prompts user to select wiki to delete
    2. Non-interactive wiki deletion (wiki-promptless) - Deletes specified wiki
    3. Elasticsearch data deletion (elasticsearch) - Removes search index data

    Usage:
        Interactive wiki:     meza delete wiki <environment>
        Non-interactive wiki: meza delete wiki-promptless <environment> <wiki_id>
        Elasticsearch:        meza delete elasticsearch <environment>

    Examples:
        # Interactive wiki deletion (will show list to choose from)
        meza delete wiki monolith
        meza delete wiki production

        # Delete specific wiki without prompts
        meza delete wiki-promptless monolith testwiki
        meza delete wiki-promptless production oldwiki

        # Delete elasticsearch data
        meza delete elasticsearch monolith

    Args:
        argv (list): Command line arguments:
            [0] - Sub-command: 'wiki', 'wiki-promptless', or 'elasticsearch'
            [1] - Environment name (required)
            [2] - Wiki ID (required for wiki-promptless only)

    Returns:
        None

    Raises:
        SystemExit: If sub-command is invalid, required arguments are missing,
                   or environment is invalid.

    Warning:
        Wiki deletion is irreversible. Ensure you have backups before proceeding.
        Use 'meza backup <env>' to create backups before deletion.

    Notes:
        - Uses delete-wiki.yml, delete-wiki-promptless.yml, or delete-elasticsearch.yml playbooks
        - Interactive mode shows available wikis and prompts for confirmation
        - Wiki deletion removes database, files, and configuration
    """

    sub_command = argv[0]

    if sub_command not in ("wiki", "wiki-promptless", "elasticsearch"):
        print(f"{sub_command} is not a valid sub-command for delete")
        sys.exit(1)

    if len(argv) < 2:
        print(
            f"You must specify an environment: 'meza delete {sub_command} ENV'")
        sys.exit(1)

    env = argv[1]

    rc = check_environment(env)
    if rc > 0:
        meza_shell_exec_exit(rc)

    playbook = "delete-" + sub_command

    if sub_command == "wiki-promptless":
        if len(argv) < 3:
            print("delete wiki-promptless requires wiki_id")
            sys.exit(1)
        shell_cmd = playbook_cmd(playbook, env, {'wiki_id': argv[2]})
    else:
        shell_cmd = playbook_cmd(playbook, env)

    rc = meza_shell_exec(shell_cmd)
    meza_shell_exec_exit(rc)


def meza_command_backup(argv):
    """
    Perform a backup operation for the specified environment.

    Args:
        argv (list): A list of command-line arguments.

    Returns:
        None
    """

    env = argv[0]

    rc = check_environment(env)
    if rc != 0:
        meza_shell_exec_exit(rc)

    shell_cmd = playbook_cmd('backup', env) + argv[1:]
    rc = meza_shell_exec(shell_cmd)

    meza_shell_exec_exit(rc)


def meza_command_setbaseconfig(argv):
    """
    Executes the 'setbaseconfig' playbook command for the specified environment.

    Args:
        argv (list): A list of command-line arguments passed to the function. The first element
            should be the environment.

    Returns:
        None
    """
    env = argv[0]

    rc = check_environment(env)
    if rc != 0:
        meza_shell_exec_exit(rc)

    shell_cmd = playbook_cmd('setbaseconfig', env) + argv[1:]
    rc = meza_shell_exec(shell_cmd)

    meza_shell_exec_exit(rc)


# General-purpose maintenance script runner implemented.
# The run-maintenance.yml playbook can now run any MediaWiki
# maintenance script on all wikis or specific wikis. Examples:
#   $ ansible-playbook run-maintenance.yml -e "maintenance_script=runJobs"
#   $ ansible-playbook run-maintenance.yml -e "maintenance_script=createAndPromote" -e "maintenance_args=--bureaucrat"
#
# The meza maint command provides pre-configured shortcuts for common operations:
#   $ meza maint cleanuploadstash <env>    --> run cleanupUploadStash.php on all wikis
#   $ meza maint rebuild <env>             --> rebuild search index and SMW
#   $ meza maint run-jobs                  --> run jobs on all wikis
#
# For custom scripts, use the playbook directly with maintenance_script parameter.
def meza_command_maint(argv):
    """
    Executes the specified maintenance sub-command.

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None

    Raises:
        SystemExit: If the specified sub-command is not valid.

    """
    # FIXME #711: This has no notion of environments and won't work in polylith

    sub_command = argv[0]
    command_fn = "meza_command_maint_" + sub_command.replace("-", "_")

    # if command_fn is a valid Python function, pass it all remaining args
    if command_fn in globals() and callable(globals()[command_fn]):
        globals()[command_fn](argv[1:])
    else:
        print("")
        print(sub_command + " is not a valid sub-command for maint")
        sys.exit(1)


def meza_command_maint_run_jobs(argv):
    """
    Run maintenance jobs (mediawiki/maintenance/runJobs.php) for available wikis.

    This function executes the meza `runAllJobs.php` script.

    By default, it will run jobs for ALL wikis. The wiki id used is just to get
        meza to run. If a specific wiki is provided as a command-line argument,
    the function runs maintenance jobs only for that wiki.

    Usage:
    Run jobs for all wikis:
        sudo meza maint run_jobs

    Run jobs for a specific wiki (e.g., 'demo'):
    sudo meza maint run_jobs -- demo

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None
    """
    # FIXME This has not been made to work on a distributed app-server setup.

    # Get wiki list from declarative configuration
    anywiki = None
    try:
        with open(f"{install_dir}/.deploy-meza/wiki-config.php", 'r') as config_file:
            # Parse PHP config file to extract wiki list
            # This is a simple approach - a more robust solution would use a proper PHP parser
            # The wiki-config.php file is created during deploy and contains the
            # list of wikis as the only quoted strings, so the simple regex works.
            content = config_file.read()
            import re
            matches = re.findall(r"'([^']+)',", content)
            if matches:
                anywiki = matches[0]  # Use first configured wiki
    except (FileNotFoundError, IndexError):
        # Fallback to directory-based discovery (legacy)
        wikis_dir = f"{install_dir}/htdocs/wikis"
        wikis = os.listdir(wikis_dir)
        for i in wikis:
            if os.path.isdir(os.path.join(wikis_dir, i)):
                anywiki = i
                break

    if not anywiki:
        print("No wikis available to run jobs")
        sys.exit(1)

    shell_cmd = ["WIKI=" + anywiki, "php",
                 f"{install_dir}/.deploy-meza/runAllJobs.php"]
    if len(argv) > 0:
        shell_cmd = shell_cmd + ["--wikis=" + argv[1]]
    rc = meza_shell_exec(shell_cmd)

    meza_shell_exec_exit(rc)


def meza_command_maint_rebuild(argv):
    """
    Rebuilds the specified environment and executes the 'rebuild-smw-and-index' playbook command.

    Args:
        argv (list): A list of command-line arguments passed to the function. The first argument
            is the environment.

    Returns:
        None
    """
    env = argv[0]

    rc = check_environment(env)

    # return code != 0 means failure
    if rc != 0:
        meza_shell_exec_exit(rc)

    more_extra_vars = False

    # strip environment off of it
    argv = argv[1:]

    shell_cmd = playbook_cmd('rebuild-smw-and-index', env, more_extra_vars)
    if len(argv) > 0:
        shell_cmd = shell_cmd + argv

    rc = meza_shell_exec(shell_cmd)

    # exit with same return code as ansible command
    meza_shell_exec_exit(rc)


def meza_command_maint_cleanuploadstash(argv):
    """
    Clean up the upload stash directory for a given environment.

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None
    """

    env = argv[0]

    rc = check_environment(env)

    # return code != 0 means failure
    if rc != 0:
        meza_shell_exec_exit(rc)

    more_extra_vars = False

    # strip environment off of it
    argv = argv[1:]

    more_extra_vars = {'maintenance_script': 'cleanupUploadStash'}

    shell_cmd = playbook_cmd('run-maintenance', env, more_extra_vars)
    if len(argv) > 0:
        shell_cmd = shell_cmd + argv

    rc = meza_shell_exec(shell_cmd)

    # exit with same return code as ansible command
    meza_shell_exec_exit(rc)


def meza_command_maint_encrypt_string(argv):
    """
    Encrypts a string using Ansible Vault.

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None

    Raises:
        SystemExit: If the function is called without the required arguments.

    Example:
        encrypt_string requires value to encrypt. Ex:
          sudo meza maint encrypt_string <env> somesecretvalue
        Additionally, you can supply the variable name. Ex:
          sudo meza maint encrypt_string <env> somesecretvalue var_name
    """
    env = argv[0]

    rc = check_environment(env)

    # return code != 0 means failure
    if rc != 0:
        meza_shell_exec_exit(rc)

    # strip environment off of it
    argv = argv[1:]

    if len(argv) == 0:
        print("encrypt_string requires value to encrypt. Ex:")
        print("  sudo meza maint encrypt_string <env> somesecretvalue")
        print("Additionally, you can supply the variable name. Ex:")
        print("  sudo meza maint encrypt_string <env> somesecretvalue var_name")
        sys.exit(1)

    varvalue = argv[0]
    vault_pass_file = get_vault_pass_file(env)

    shell_cmd = ["ansible-vault", "encrypt_string",
                 "--vault-id", vault_pass_file, varvalue]

    # If name argument passed in, use it
    if len(argv) == 2:
        shell_cmd = shell_cmd + ["--name", argv[1]]

    # false = don't print command prior to running
    rc = meza_shell_exec(shell_cmd, False)

    # exit with same return code as ansible command
    meza_shell_exec_exit(rc)


# sudo meza maint decrypt_string <env> <encrypted_string>
def meza_command_maint_decrypt_string(argv):
    """
    Decrypts an encrypted string using Ansible Vault.

    Args:
        argv (list): List of command-line arguments.

    Returns:
        None

    Raises:
        SystemExit: If no encrypted string is provided as an argument.

    Example:
        To decrypt a string, run the following command:
        sudo meza maint decrypt_string <env> '$ANSIBLE_VAULT;1.1;AES256
        31386561343430626435373766393066373464656262383063303630623032616238383838346132
        6162313461666439346337616166396133616466363935360a373333313165343535373761333634
        62636634306632633539306436363866323639363332613363346663613235653138373837303337
        6133383864613430370a623661653462336565376565346638646238643132636663383761613966
        6566'
    """
    env = argv[0]

    rc = check_environment(env)

    # return code != 0 means failure
    if rc != 0:
        meza_shell_exec_exit(rc)

    # strip environment off of it
    argv = argv[1:]

    if len(argv) == 0:
        print("decrypt_string requires you to supply encrypted string. Ex:")
        print("""
        sudo meza maint decrypt_string <env> '$ANSIBLE_VAULT;1.1;AES256
        31386561343430626435373766393066373464656262383063303630623032616238383838346132
        6162313461666439346337616166396133616466363935360a373333313165343535373761333634
        62636634306632633539306436363866323639363332613363346663613235653138373837303337
        6133383864613430370a623661653462336565376565346638646238643132636663383761613966
        6566'
        """)
        sys.exit(1)

    encrypted_string = argv[0]
    vault_pass_file = get_vault_pass_file(env)

    tmp_file = write_vault_decryption_tmp_file(env, encrypted_string)

    shell_cmd = ["ansible-vault", "decrypt", tmp_file,
                 "--vault-password-file", vault_pass_file]

    # false = don't print command prior to running
    rc = meza_shell_exec(shell_cmd, False)

    decrypted_value = read_vault_decryption_tmp_file(env)

    print("")
    print("Decrypted value:")
    print(decrypted_value)

    # exit with same return code as ansible command
    meza_shell_exec_exit(rc)

# @FIXME this is obsolete (because all Docker functionality is untested)
# Should be updated or removed - especially the hard-link to
# enterprisemediawiki


def meza_command_docker(argv):
    """
    Executes Docker commands based on the provided arguments.

    Args:
        argv (list): A list of command-line arguments.

    Raises:
        SystemExit: If the provided command is not valid or if required arguments are missing.

    Returns:
        None
    """

    if argv[0] == "run":

        if len(argv) == 1:
            docker_repo = "enterprisemediawiki/meza:max"
        else:
            docker_repo = argv[1]

        rc = meza_shell_exec(
            ["bash", f"{install_dir}/meza/src/scripts/build-docker-container.sh", docker_repo])
        meza_shell_exec_exit(rc)

    elif argv[0] == "exec":

        if len(argv) < 2:
            print("Please provide docker container id")
            meza_shell_exec(["docker", "ps"])
            sys.exit(1)
        else:
            container_id = argv[1]

        if len(argv) < 3:
            print("Please supply a command for your container")
            sys.exit(1)

        shell_cmd = ["docker", "exec", "--tty",
                     container_id, "env", "TERM=xterm"] + argv[2:]
        rc = meza_shell_exec(shell_cmd)

    else:
        print(argv[0] + " is not a valid command")
        sys.exit(1)


def meza_command_push_backup(argv):
    """
    Pushes the backup for the specified environment.

    Args:
        argv (list): A list of command-line arguments.

    Returns:
        None
    """
    env = argv[0]

    rc = check_environment(env)
    if rc != 0:
        meza_shell_exec_exit(rc)

    shell_cmd = playbook_cmd('push-backup', env) + argv[1:]
    rc = meza_shell_exec(shell_cmd)

    meza_shell_exec_exit(rc)


def playbook_cmd(playbook, env=False, more_extra_vars=False):
    """
    Constructs the command to execute an Ansible playbook.

    Args:
        playbook (str): The name of the playbook to execute.
        env (str, optional): The environment for the playbook execution. Defaults to False.
        more_extra_vars (dict, optional): Additional extra variables to pass to the playbook.
            Defaults to False.

    Returns:
        list: The constructed command as a list of strings.
    """
    command = ['sudo', '-u', 'meza-ansible', 'ansible-playbook',
               f'{install_dir}/meza/src/playbooks/{playbook}.yml']
    if env:
        host_file = f"{install_dir}/conf-meza/secret/{env}/hosts"

        # Meza _needs_ to be able to load this file. Be perhaps a little
        # overzealous and chown/chmod it everytime
        secret_file = f'{install_dir}/conf-meza/secret/{env}/secret.yml'
        meza_chown(secret_file, 'meza-ansible', 'wheel')
        os.chmod(secret_file, 0o660)

        # Setup password file if not exists (environment info is potentially
        # encrypted)
        vault_pass_file = get_vault_pass_file(env)

        command = command + ['-i', host_file,
                             '--vault-password-file', vault_pass_file]
        extra_vars = {'env': env}

    else:
        extra_vars = {}

    if more_extra_vars:
        for varname, value in more_extra_vars.items():
            extra_vars[varname] = value

    if len(extra_vars) > 0:
        command = command + \
            ["--extra-vars",
                f"'{json.dumps(extra_vars)}'".replace('"', '\\"')]

    return command


def meza_shell_exec(shell_cmd, print_command=True, log_file=False):
    """
    Executes a shell command and returns the return code.

    Args:
        shell_cmd (list): The shell command to execute, as a list of strings.
        print_command (bool, optional): Whether to print the command before executing it.
            Defaults to True.
        log_file (str, optional): The path to the log file to write the command output to.
            Defaults to False.

    Returns:
        int: The return code of the executed shell command.
    """
    # Get errors with user meza-ansible trying to write to the calling-user's
    # home directory if don't cd to a neutral location. By cd'ing to this
    # location you can pick up ansible.cfg and use vars there.
    starting_wd = os.getcwd()
    os.chdir(f"{install_dir}/meza/config")

    #
    # FIXME #874: For some reason `sudo -u meza-ansible ...` started failing in
    #             fall 2017. Using `su meza-ansible -c "..."` works. It is not
    #             known why this started happening, but a fix was needed. This,
    #             despite being somewhat of a hack, seemed like the best way to
    #             address the issue at the time.
    #
    firstargs = ' '.join(shell_cmd[0:3])
    if firstargs == "sudo -u meza-ansible":
        cmd = f"su meza-ansible -c \"{' '.join(shell_cmd[3:])}\""
    else:
        cmd = ' '.join(shell_cmd)

    if print_command:
        print(cmd)

    if log_file:
        log = open(log_file, 'ab')
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(proc.stdout.readline, b''):
        print(line.rstrip().decode())
        if log_file:
            log.write(line)
    proc.wait()

    rc = proc.returncode

    # Move back to original working directory
    os.chdir(starting_wd)

    return rc

# Return codes from function meza_shell_exec may either not be numbers or they
# may be out of the range accepted by sys.exit(). For example, return codes in
# the 30000 range were not being interpretted as failures. This function will
# instead take any non-zero return code and make it return the integer 1.


def meza_shell_exec_exit(return_code=0):
    """
    Exits the script with the given return code.

    Args:
        return_code (int): The return code to exit with.

    Returns:
        None
    """
    if int(return_code) > 0:
        print(f"Exiting with return code {return_code}")
        sys.exit(1)
    else:
        sys.exit(0)


def get_vault_pass_file(env):
    """
    Get the path to the vault password file for the given environment.

    Args:
        env (str): The environment for which the vault password file is needed.

    Returns:
        str: The path to the vault password file.

    Raises:
        None

    """
    home_dir = defaults['m_conf_users_dir']
    legacy_file = f'{home_dir}/meza-ansible/.vault-pass-{env}.txt'

    vault_dir = defaults['m_conf_vault_dir']
    vault_pass_file = f'{vault_dir}/vault-pass-{env}.txt'

    if not os.path.isfile(vault_pass_file):
        if not os.path.exists(vault_dir):
            os.mkdir(vault_dir)
            meza_chown(vault_dir, 'meza-ansible', 'wheel')
            os.chmod(vault_dir, 0o700)

        # If legacy vault password file exists copy that into new location.
        # Otherwise, create one in the new location
        if os.path.isfile(legacy_file):
            shutil.copyfile(legacy_file, vault_pass_file)
        else:
            with open(vault_pass_file, 'w', encoding='utf-8') as f:
                f.write(random_string(num_chars=64))
                f.close()

    # Run this everytime, since it should be fast and if meza-ansible can't
    # read this then you're stuck!
    meza_chown(vault_pass_file, 'meza-ansible', 'wheel')
    os.chmod(vault_pass_file, 0o600)

    return vault_pass_file


def write_vault_decryption_tmp_file(env, value):
    """
    Write the given value to a temporary file for vault decryption.

    Args:
        env (str): The environment name.
        value (str): The value to be written to the file.

    Returns:
        str: The path of the temporary file.

    """
    home_dir = defaults['m_conf_users_dir']
    temp_decrypt_file = f'{home_dir}/meza-ansible/.vault-temp-decrypt-{env}.txt'

    with open(temp_decrypt_file, 'w', encoding='utf-8') as filetowrite:
        filetowrite.write(value)

    return temp_decrypt_file


def read_vault_decryption_tmp_file(env):
    """
    Read the contents of a temporary decryption file.

    Args:
        env (str): The environment name.

    Returns:
        str: The contents of the temporary decryption file, or "[decryption error]" if an error
            occurs.
    """
    home_dir = defaults['m_conf_users_dir']
    temp_decrypt_file = f'{home_dir}/meza-ansible/.vault-temp-decrypt-{env}.txt'

    with open(temp_decrypt_file, encoding='utf-8') as f:
        if f.mode == 'r':
            contents = f.read()
            f.close()
            os.remove(temp_decrypt_file)
        else:
            contents = "[decryption error]"

    return contents


def meza_chown(path, username, groupname):
    """
    Change the ownership of a file or directory to the specified user and group.

    Args:
        path (str): The path to the file or directory.
        username (str): The name of the user.
        groupname (str): The name of the group.

    Returns:
        None
    """
    uid = pwd.getpwnam(username).pw_uid
    gid = grp.getgrnam(groupname).gr_gid
    os.chown(path, uid, gid)


def _get_github_help_url(filename):
    """
    Generate GitHub URL for help documentation with automatic branch detection.

    Args:
        filename (str): The name of the help file (e.g., 'base.md')

    Returns:
        str: GitHub URL for the help file
    """
    # Try to detect current git branch
    try:
        branch = subprocess.check_output(
            ["git", f"--git-dir={install_dir}/meza/.git",
                "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to dev branch if git command fails
        branch = "dev"

    # Use dev branch for most common case, but allow for other branches
    if branch in ["main", "master", "dev"]:
        return f"https://github.com/freephile/meza/blob/{branch}/manual/meza-cmd/{filename}"
    else:
        # For feature branches or unknown branches, default to dev
        return f"https://github.com/freephile/meza/blob/dev/manual/meza-cmd/{filename}"


def display_docs(name):
    """
    Display the contents of a help file with the given name.
    Prefers Markdown (.md) files over text (.txt) files.
    Provides multiple rendering strategies for optimal display.

    Args:
        name (str): The name of the help file to display.

    Returns:
        None

    Notes:
        - Prioritizes .md files over .txt files for enhanced formatting
        - Uses multiple rendering strategies: rich (with fallbacks), plain text, and browser links
        - Provides fallback to legacy .txt files if .md files don't exist
        - Shows helpful update instructions if no help file is found
        - Guides users to update their project sources for latest documentation
    """
    # Try .md file first, fallback to .txt
    # Use install_dir to work both in development and production
    md_file = f'{install_dir}/meza/manual/meza-cmd/{name}.md'
    txt_file = f'{install_dir}/meza/manual/meza-cmd/{name}.txt'

    if os.path.exists(md_file):
        with open(md_file, encoding='utf-8') as f:
            content = f.read()

        # Strategy 1: Try rich markdown rendering
        if RICH_AVAILABLE:
            try:
                console = Console()
                markdown = Markdown(content)
                console.print(markdown)

                # Check if content has tables and rich version might have issues
                if '|' in content and 'Command' in content:
                    console.print(
                        "\n[dim]Note: For best table formatting, view the full documentation at:[/dim]")
                    github_url = _get_github_help_url(f"{name}.md")
                    console.print(f"[link]{github_url}[/link]")

                return
            except (ImportError, AttributeError, UnicodeError, OSError):
                # Rich failed, fall through to other strategies
                pass

        # Strategy 2: Enhanced plain text with basic table formatting
        _display_enhanced_plain_text(content, md_file)

    elif os.path.exists(txt_file):
        with open(txt_file, encoding='utf-8') as f:
            print(f.read())
    else:
        print(f"Help file not found: {name}")
        print("")
        print("This may indicate that your Meza installation is outdated.")
        print("Please update your project sources to get the latest help documentation:")
        print("")
        print("  git fetch --all")
        print("  # then")
        print("  git status")
        print("")
        print("For a complete list of available commands, try:")
        print("  meza --help")
        return


def _display_enhanced_plain_text(content, file_path):
    """
    Display markdown content with enhanced plain text formatting.

    Args:
        content (str): The markdown content to display
        file_path (str): Path to the original file for reference
    """
    lines = content.split('\n')
    in_code_block = False
    in_table = False

    print()  # Start with a blank line

    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                print("┌" + "─" * 78 + "┐")
                continue
            else:
                print("└" + "─" * 78 + "┘")
                continue

        if in_code_block:
            print(f"│ {line:<76} │")
            continue

        # Handle headers
        if line.startswith('# '):
            print("=" * 80)
            print(f" {line[2:].strip().upper()}")
            print("=" * 80)
            continue
        elif line.startswith('## '):
            print("\n" + "─" * 60)
            print(f" {line[3:].strip()}")
            print("─" * 60)
            continue
        elif line.startswith('### '):
            print(f"\n▶ {line[4:].strip()}")
            print("─" * 40)
            continue

        # Handle tables
        if '|' in line and ('Command' in line or 'Description' in line or line.count('|') >= 2):
            if not in_table:
                in_table = True
                print()

            # Simple table formatting
            if '━' in line or '─' in line:
                print("─" * 80)
            else:
                # Clean up table cells and format
                cells = [cell.strip()
                         for cell in line.split('|') if cell.strip()]
                if cells:
                    # Limit to 4 columns
                    formatted = "  ".join(f"{cell:<20}" for cell in cells[:4])
                    print(formatted)
            continue
        else:
            if in_table:
                in_table = False
                print()

        # Handle bullet points
        if line.strip().startswith('• ') or line.strip().startswith('- '):
            print(f"  • {line.strip()[2:]}")
            continue
        elif line.strip().startswith('* '):
            print(f"  • {line.strip()[2:]}")
            continue

        # Handle numbered lists
        import re
        if re.match(r'^\d+\.\s', line.strip()):
            print(f"  {line.strip()}")
            continue

        # Regular text
        if line.strip():
            print(line)
        else:
            print()

    # Add footer with link to full documentation
    print("\n" + "─" * 60)
    print("📖 For full formatting and latest updates, view the complete documentation:")

    # Extract just the filename from the full path for GitHub URL
    filename = os.path.basename(file_path)
    github_url = _get_github_help_url(filename)
    print(f"   {github_url}")
    print("   Or open in your browser for best markdown rendering.")
    print("─" * 60)


def meza_command_help(argv):
    """
    Enhanced help command with multiple viewing options.

    Usage:
        meza help <command>           # Display help in terminal
        meza help <command> --browser # Open help in default browser
        meza help <command> --editor  # Open help in default editor
        meza help <command> --path    # Show path to help file

    Args:
        argv (list): Command line arguments
    """
    if len(argv) < 1:
        display_docs('help')
        return

    command = argv[0]
    options = argv[1:] if len(argv) > 1 else []

    # Find the help file
    md_file = f'{install_dir}/meza/manual/meza-cmd/{command}.md'
    txt_file = f'{install_dir}/meza/manual/meza-cmd/{command}.txt'

    help_file = md_file if os.path.exists(md_file) else (
        txt_file if os.path.exists(txt_file) else None)

    if not help_file:
        print(f"Help file not found for command: {command}")
        return

    # Handle different viewing options
    if '--browser' in options:
        # Generate GitHub URL for better markdown rendering
        filename = os.path.basename(help_file)
        github_url = _get_github_help_url(filename)

        if WEBBROWSER_AVAILABLE:
            print(f"Opening {command} help in browser (GitHub)...")
            webbrowser.open(github_url)
        else:
            print("Browser opening not available. GitHub URL:")
            print(github_url)
    elif '--editor' in options:
        editor = os.environ.get('EDITOR', 'vi')
        print(f"Opening {command} help in {editor}...")
        os.system(f'{editor} "{help_file}"')
    elif '--path' in options:
        filename = os.path.basename(help_file)
        github_url = _get_github_help_url(filename)
        print(f"Local file: {os.path.abspath(help_file)}")
        print(f"GitHub URL: {github_url}")
    else:
        # Default: display in terminal
        display_docs(command)


def prompt(varname, default=False):
    """
    Prompts the user for input and returns the value entered.

    Args:
        varname (str): The name of the variable being prompted for.
        default (bool, optional): The default value to use if the user does not provide any input.
            Defaults to False.

    Returns:
        str: The value entered by the user.

    """
    # Pretext message is prior to the actual line the user types on. Input msg
    # is on the same line and will be repeated if the user does not give good
    # input
    pretext_msg = i18n["MSG_prompt_pretext_" + varname]
    input_msg = i18n["MSG_prompt_input_" + varname]

    print("")
    print(pretext_msg)

    value = input(input_msg)
    if default:
        value = value or default
    else:
        while not value:
            value = input(input_msg)

    return value


def prompt_secure(varname):
    """
    Prompts the user to enter a secure value for the given variable name.

    Args:
        varname (str): The name of the variable for which the user is prompted.

    Returns:
        str: The secure value entered by the user.

    """
    # See prompt() for more info
    pretext_msg = i18n["MSG_prompt_pretext_" + varname]
    input_msg = i18n["MSG_prompt_input_" + varname]

    print()
    print(pretext_msg)

    value = getpass.getpass(input_msg)
    if not value:
        value = random_string()

    return value


def random_string(**params):
    """
    Generate a random string.

    Args:
        params (dict): Optional parameters for generating the random string.
            - num_chars (int): The length of the random string. Default is 32.
            - valid_chars (str): The characters to choose from when generating the random string.
              Default is all uppercase and lowercase letters, digits, and the special characters
              '!@$%^*'.

    Returns:
        str: The randomly generated string.

    """
    if 'num_chars' in params:
        num_chars = params['num_chars']
    else:
        num_chars = 32

    if 'valid_chars' in params:
        valid_chars = params['valid_chars']
    else:
        valid_chars = string.ascii_letters + string.digits + '!@$%^*'

    return ''.join(random.SystemRandom().choice(valid_chars)
                   for _ in range(num_chars))


# return code 0 success, 1+ failure
def check_environment(env):
    """
    Check if the specified environment exists and is valid.

    Args:
        env (str): The name of the environment to check.

    Returns:
        int: Returns 0 if the environment is valid, 1 otherwise.
    """
    conf_dir = f"{install_dir}/conf-meza/secret"

    env_dir = os.path.join(conf_dir, env)
    if not os.path.isdir(env_dir):

        if env == "monolith":
            return 1

        print()
        print(f'"{env}" is not a valid environment.')
        print("Please choose one of the following:")

        conf_dir_stuff = os.listdir(conf_dir)
        valid_envs = []
        for x in conf_dir_stuff:
            if os.path.isdir(os.path.join(conf_dir, x)):
                valid_envs.append(x)

        if len(valid_envs) > 0:
            for x in valid_envs:
                print("  " + x)
        else:
            print("  No environments configured")
            print("  Run command: meza setup env <environment name>")

        return 1

    host_file = os.path.join(env_dir, "hosts")
    if not os.path.isfile(host_file):
        print()
        print(f"{host_file} not a valid file")
        return 1

    return 0

# http://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python


def copy(src, dst):
    """
    Copy a file or directory from source to destination.

    Args:
        src (str): The path of the source file or directory.
        dst (str): The path of the destination directory.

    Raises:
        OSError: If an error occurs while copying the file or directory.

    Returns:
        None
    """
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def get_datetime_string():
    """
    Returns the current date and time as a formatted string.

    Returns:
        str: The current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st


if __name__ == "__main__":
    main(sys.argv[1:])
