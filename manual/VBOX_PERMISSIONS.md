# VirtualBox Shared Folder Permissions Fix

## Problem

When mounting your host directory (e.g., `~/src/meza`) into a VirtualBox guest VM at `/opt/meza`, files may have incorrect ownership and overly restrictive permissions:

- Files owned by `root:vboxsf` instead of `meza-ansible:wheel`
- Permissions like `-rwxrwx---` (770) instead of `-rw-r--r--` (644)
- `meza-ansible` user cannot read/write files
- Prevents development workflow: edit on host, run in guest

## Root Cause

VirtualBox shared folders use the `vboxsf` filesystem which:
1. Maps files to `root:vboxsf` ownership by default
2. Requires users to be in the `vboxsf` group to access files
3. Needs explicit mount options to set proper file vs directory permissions

## Solution

### For New VMs (Vagrant)

The Vagrantfile has been updated to:
01. Mount with proper permissions: `dmode=775,fmode=755`
2. Automatically add `meza-ansible` to `vboxsf` group
3. Set correct ownership on mounted directory

Simply destroy and recreate your VM:
```bash
vagrant destroy -f
vagrant up
```

### For Existing VMs

Run the fix script inside your guest VM:

```bash
# SSH into your VM
vagrant ssh

# Run the fix script
sudo bash /opt/meza/src/scripts/fix-vbox-permissions.sh

# Log out and back in for group changes to take effect
exit
vagrant ssh
```

### Manual Fix (Alternative)

If you prefer to fix manually:

```bash
# Add meza-ansible to vboxsf group
sudo usermod -aG vboxsf meza-ansible

# Fix ownership
sudo chown -R meza-ansible:wheel /opt/meza

# Fix directory permissions (775 = rwxrwxr-x)
sudo find /opt/meza -type d -exec chmod 775 {} \;

# Fix file permissions (664 = rw-rw-r--)
sudo find /opt/meza -type f -exec chmod 664 {} \;

# Make scripts executable
sudo find /opt/meza/src/scripts -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod 775 {} \;

# Log out and back in
exit
vagrant ssh
```

## Verification

Check that permissions are correct:

```bash
# Verify meza-ansible is in vboxsf group
groups meza-ansible
# Should show: meza-ansible : wheel vboxsf ...

# Check file ownership
ls -la /opt/meza/src/playbooks/site.yml
# Should show: -rw-rw-r-- 1 meza-ansible wheel ...

# Test write access as meza-ansible
sudo su - meza-ansible
touch /opt/meza/test-write-random-file
rm /opt/meza/test-write-random-file
```

## Development Workflow

Once fixed, you can:

1. **Edit on host**: Use your favorite IDE/editor on your Linux host
2. **Run in guest**: Execute meza commands as `meza-ansible` user in the VM
3. **Git operations**: Commit from either host or guest

The shared folder keeps everything in sync automatically.

## Technical Details

### Mount Options
- `owner=10000, group=10000`: Maps to UID/GID that `meza-ansible:wheel` uses
- `dmode=775`: Directory permissions (owner+group read/write/execute)
- `fmode=755`: File permissions (owner read/write/execute, others read/execute)

### Why vboxsf Group?
VirtualBox creates the `vboxsf` group to control access to shared folders. Users must be members of this group to access mounted directories.

### Permission Values
- **775 (directories)**: `rwxrwxr-x` - Owner and group can read/write/execute, others can read/execute
- **755 (files)**: `rwxr-xr-x` - Owner can read/write/execute, group and others can read/execute
- Execute bit allowed on files for development convenience (allows direct execution of scripts) This is REQUIRED for all sorts of files and scripts in the MediaWiki source tree e.g. maintenance/run; plus Meza.

## Troubleshooting

### "Permission denied" errors
- Ensure `meza-ansible` is in `vboxsf` group: `groups meza-ansible`
- Log out and back in for group changes to take effect
- Or run: `newgrp vboxsf`

### Files still owned by root:vboxsf
- This is expected for the VirtualBox mount point itself
- The group membership allows access despite root ownership
- Actual files should be accessible by `meza-ansible`

### Cannot write files
- Verify mount options include `dmode=775,fmode=755`
- Check that UID 10000 matches `meza-ansible`: `id meza-ansible`
- Check that GID 10000 matches `wheel`: `getent group wheel`

### "Permission denied" when running meza

If meza command gives permission denied:

```bash
# Ensure it's executable (should be automatic with fmode=755)
sudo chmod +x /opt/meza/src/scripts/meza.py

# Verify symlink
ls -la /usr/bin/meza
# Should show: /usr/bin/meza -> /opt/meza/src/scripts/meza.py

# Test
meza help
```

If your mount uses `fmode=664` (old configuration), you need to remount with `fmode=755` A symptom of using the old configuration would be that even a sudo chmod FAILS (silently) to change file mode:

```bash
sudo umount /opt/meza
sudo mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 meza /opt/meza

# Update /etc/fstab
sudo sed -i 's/fmode=664/fmode=755/g' /etc/fstab

# Re-run setup script
sudo bash /opt/meza/src/scripts/setup-manual-vbox-mount.sh meza /opt/meza
```
