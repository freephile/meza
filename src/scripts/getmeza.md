
## getmeza.sh
The getmeza.sh script is a bootstrap installer for the Meza platform. Here’s what it does, step by step:

1. **Root Check**: Ensures it is run as root (or with sudo).
2. **Environment Setup**: Determines script and install directories, sets umask for group write permissions.
3. **Internet Connection Check**: Optionally checks for internet connectivity by pinging `cdn.redhat.com`.
4. **OS Detection**: Detects if the system is Rocky, or RedHat, and determines the version.
5. **Repository Setup**: Installs the EPEL repository and other required repositories depending on the OS and version.
6. **Package Installation**: Installs required packages like `git`, `ansible`, and Python libraries, using the appropriate package manager (`yum` or `dnf`).
7. **Meza Source Clone**: Clones the Meza repository from GitHub into the install directory if it doesn’t already exist.
8. **Permissions**: Sets appropriate permissions on Meza directories and files.
9. **Symlink Creation**: Creates a symlink for the `meza` command in bin.
10. **Basic Config**: Creates a basic `.deploy-meza/config.sh` if it doesn’t exist.
11. **User Setup**: Ensures the `meza-ansible` user exists and has the correct home directory, creating or moving it as needed.
12. **Sudoers Tweaks**: Modifies sudoers to comment out `requiretty` and `!visiblepw` for smoother automation.
13. **Ansible Setup**: Switches to the `meza-ansible` user, installs Ansible in their environment, and installs required Ansible collections.
14. **Final Message**: Prints instructions for running the `meza` command.

**Summary:**  
This script prepares a Linux server (Rocky, or RedHat) for Meza by installing dependencies, configuring users and permissions, cloning the Meza codebase, and setting up Ansible. It is intended to be run as root and automates all the setup steps needed before using Meza.
