# Fix: "meza: command not found"

## Problem

The `meza-ansible` user's PATH doesn't include `/usr/bin`:

```bash
$ meza deploy monolith
bash: meza: command not found
```

## Quick Fix

```bash
sudo bash /opt/meza/src/scripts/fix-vbox-permissions.sh
exit  # Log out
sudo su - meza-ansible  # Log back in
which meza  # Should show /usr/bin/meza
```

## Manual Fix

Add PATH to `.bashrc`:

```bash
sudo su - meza-ansible
cat >> ~/.bashrc <<'EOF'

# Ensure standard paths
for dir in /usr/local/bin /usr/bin /usr/local/sbin /usr/sbin; do
    [[ ":$PATH:" != *":$dir:"* ]] && PATH="$dir:$PATH"
done
export PATH
EOF
exit
sudo su - meza-ansible
```

## Verify

```bash
sudo su - meza-ansible

# Check PATH includes standard directories
echo $PATH
# Should show: /usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:...

# Verify meza command is found
which meza
# Should show: /usr/bin/meza

# Test meza command
meza help
# Should display meza help
```

## Why This Happens

The `meza-ansible` user has a non-standard home directory (`/opt/conf-meza/users/meza-ansible`) and may not have shell initialization files created during user creation. The system's default `/etc/profile` and `/etc/bashrc` set up PATH for standard users, but when those files aren't sourced properly, the meza-ansible user ends up with a minimal PATH.

## Cross-Platform Solution

The get-meza.sh script or dedicated user role should configure both `.bashrc` and `.bash_profile` to:

1. **Source system defaults** (`/etc/bashrc` on RHEL/Rocky, `/etc/bash.bashrc` on Debian)
2. **Explicitly add standard paths** (defensive approach that works even if system defaults fail)
3. **Check before adding** (won't create duplicates if PATH already includes the directories)
4. **Export PATH** (ensures child processes inherit the PATH)

This works across:
- Rocky Linux / RHEL / CentOS
- Debian / Ubuntu
- Other Linux distributions
- Login shells and interactive shells
- `su -` and `sudo su -` invocations

## Prevention

When creating new meza-ansible users (or similar service users), always ensure shell initialization files are properly configured:

```bash
# After creating user, set up their shell environment
MEZA_HOME=$(getent passwd meza-ansible | cut -d: -f6)
cp /etc/skel/.bashrc "$MEZA_HOME/" 2>/dev/null || true
cp /etc/skel/.bash_profile "$MEZA_HOME/" 2>/dev/null || true
chown -R meza-ansible:wheel "$MEZA_HOME"
```

The meza setup scripts will do this automatically in the near future.

## Special Case: "Permission Denied" on VirtualBox Shared Folders

If you get "Permission denied" when running `/usr/bin/meza` (instead of "command not found"), the issue is different:

### Problem

VirtualBox shared folders mounted with `fmode=664` **cannot have executable files**. Even root cannot use `chmod +x` on files in vboxsf - the filesystem enforces the mount options.

```bash
$ /usr/bin/meza help
bash: /usr/bin/meza: Permission denied

$ file /usr/bin/meza
/usr/bin/meza: symbolic link to /opt/meza/src/scripts/meza.py

$ ls -la /opt/meza/src/scripts/meza.py
# If this shows -rw-rw-r-- (no execute bit), the mount is using fmode=664
```

### Solution: Use fmode=755 Mount Option

Mount the shared folder with `fmode=755` to allow execute permissions:

```bash
# Quick fix - run this as root:
sudo bash /opt/meza/src/scripts/fix-vbox-permissions.sh

# Or manually:
# 1. Remount with fmode=755
sudo umount /opt/meza
sudo mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 meza /opt/meza

# 2. Update /etc/fstab for permanent fix
sudo sed -i 's/fmode=664/fmode=755/g' /etc/fstab

# 3. Create symlink
sudo ln -s /opt/meza/src/scripts/meza.py /usr/bin/meza

# Test
meza help
```

The `fmode=755` mount option makes files appear as rwxr-xr-x (executable) in the guest VM, allowing direct execution.

### Why This Happens

When you mount with `mount -t vboxsf -o fmode=664 ...`, the `fmode=664` option sets ALL files to permission 664 (rw-rw-r--) regardless of what chmod you try. This is a VirtualBox filesystem driver limitation.

**Important**: The fmode option only affects how files **appear in the guest VM**. It does not modify the actual files on the host filesystem. Your host files remain unchanged regardless of guest mount options.

Options:
1. **Use fmode=755** (recommended) - Allows execute bit, simple symlink, no wrappers needed
2. **Call python directly** - `python3 /opt/meza/src/scripts/meza.py help` works but inconvenient

The setup scripts in this repo now use fmode=755 by default, so this should "just work" after running setup.
