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

These steps assume you have Vagrant installed on your workstation:

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

## PATH, permissions, groups For The meza-ansible User

When you deploy meza, it will automatically ensure that the service account 'meza-ansible' is setup appropriately.
Always use the meza-ansible user account when operating on the Vagrant Virtual Machine or other controller host. meza-ansible is
a password-less sudoer so the account is fully privileged. The main 'deploy' command should be invoked with sudo. That said, most commands do not require sudo, and we are working to remove 'sudo' from all meza commands.
