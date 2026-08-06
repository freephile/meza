# Developing With Vagrant

This note documents a Vagrant-based workflow for running development tools inside the Rocky Linux VM, where the system
Python is 3.6.8 to match the supported target OS for `meza deploy` and everything else in Meza.

## Repo Mount Location

The source repo you clone with `git` into your preferred local directory on your host workstation/laptop (e.g.
`~/src/meza`) is mounted inside the VM at `/opt/meza` making it easy to use a live working copy for both host-level
tools and vm operations.

## Port-forwarding

You can also forward ports between the host and VM for easily using graphical tools (e.g. DBeaver for DB admin).

## First-time Vagrant Setup

These steps assume you have Vagrant installed on your workstation.

### Linux pre-requisites
If your host is Linux, you will want to ensure you have libvirt
(unless you want to use VirtualBox provisioner - but that can conflict with DockerDesktop)

```
sudo apt install libvirt-dev libvirt-daemon-system qemu-kvm  # Debian/Ubuntu
vagrant plugin install vagrant-libvirt
# Make your user a member of the libvirt group
sudo usermod -aG libvirt $(whoami)
# Either log out and back in again, or use newgrp
newgrp libvirt
# Verify that you are a member
groups # should show 'libvirt' in the output
```
And also nfs-kernel-server for the persistent bi-directional automatic mount avoiding `vagrant rsync`
```
# Debian/Ubuntu
sudo apt install nfs-kernel-server

# RHEL/Rocky/Alma
sudo dnf install nfs-utils
```

### All OSes
```
# get the code
git clone https://github.com/freephile/meza.git
# switch to the local repo
cd meza
# invoke the Vagrantfile
vagrant up
# ssh into the local VM
vagrant ssh
# switch user to the service account
sudo su - meza-ansible
# switch to the mounted project directory
cd /opt/meza
# Create a Python virtual environment so you can install pre-commit, and linters
# Note that this venv must have a different name than any venv created from
# the host in the same source directory. So '.venv' on the host and .mvvenv
# on the VM
python -m venv .vmvenv
# activate it
source .vmvenv/bin/activate
# upgrade pip in your Python virtual environment
python -m pip install --upgrade pip
# install the 'pre-commit' Python package
python -m pip install pre-commit
# use pre-commit to install the project's commit hooks
pre-commit install
# change to the project's ansible config dir to pickup ansible.cfg
cd /opt/meza/config
# create a demo wiki on the VM
sudo meza deploy vagrant -vvv
# browse the site
(visit https://192.168.56.56/demo in your browser from your host desktop)
```

## Host vs VM Virtualenvs

"[pre-commit](.pre-commit-config.yaml)" is a tool we use to manage and run git pre-commit hooks on your local developer
repository to enforce quality and standards prior to allowing git commits to succeed. It relies on Python, so you should
create a Python virtual environment (so-called 'venv') on _both_ your host and the Vagrant VM.

To avoid conflicts, use distinct names:

- Host workstation: `.venv`
- Vagrant VM: `.vmvenv`

This keeps both environments stable and avoids PATH confusion when switching between host and VM.

## Git Configuration

`meza setup dev` has been removed, so setup your git configuration manually for the user you use to commit to GitHub

Typically you do this from your workstation, and you can either configure git 'globally', or for the specific repository
that you are working on.
```
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
git config --global color.ui true
```

## Using VSCode
With the vagrant VM mounting your code you can work in VSCode (or other IDE) right in your source checkout on your workstation (the 'host'). This works great if all you want to modify is Meza source. However, in order to
modify other files - say MediaWiki core, or a Meza config repo, or live .deploy-meza files to try debugging,
then you will want to use VSCode Remote Explorer to SSH to the VM.
Use `vagrant ssh-config` from the source directory, and copy the output into your local ~/.ssh/config file.
For example, you will see something like
```
Host app1
  HostName 192.168.121.145
  User vagrant
  Port 22
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/greg/src/meza/.vagrant/machines/app1/libvirt/private_key
  IdentitiesOnly yes
  LogLevel FATAL
  PubkeyAcceptedKeyTypes +ssh-rsa
  HostKeyAlgorithms +ssh-rsa
```
Once that is in your SSH config file, you'll see 'app1' as a menu option in the Remote Explorer.

## PATH, permissions, groups For The meza-ansible User

When you deploy meza, it will automatically ensure that the service account 'meza-ansible' is setup appropriately.
Always use the meza-ansible user account when operating on the Vagrant Virtual Machine or other controller host. meza-ansible is
a password-less sudoer so the account is fully privileged. The main 'deploy' command should be invoked with sudo. That said, most commands do not require sudo, and we are working to [remove 'sudo' from all meza commands](https://github.com/freephile/meza/issues/72).

## Finding your way around

Here's the basic structure of the source files:
```
meza/
├── src/
│   ├── playbooks/          # Ansible playbooks (30+ yml files)
│   ├── roles/              # Ansible roles (58+ directories)
│   └── scripts/            # Python and shell scripts
├── config/                 # Configuration files
├── manual/                 # Documentation including meza-cmd help files
├── tests/                  # Test suite
└── [root files]            # README, CHANGELOG, LICENSE, etc.
```
