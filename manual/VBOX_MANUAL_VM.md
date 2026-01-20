# VirtualBox Manual VM Setup

For VMs created directly in VirtualBox Manager (not Vagrant).

## Quick Setup

### 1. Configure Shared Folder in VirtualBox

In VirtualBox Manager → Settings → Shared Folders:
- **Folder Path**: Your host meza directory (e.g., `/home/greg/src/meza`)
- **Folder Name**: `meza`
- **Mount Point**: `/opt/meza`
- **Auto-mount**: ☑
- **Make Permanent**: ☑

### 2. Run Setup Script

Inside your VM:
```bash
sudo bash /opt/meza/src/scripts/setup-manual-vbox-mount.sh meza /opt/meza
```

The script configures mount options, permissions, PATH, and the meza symlink.

### 3. Verify

```bash
groups meza-ansible  # Should include "vboxsf"
mount | grep vboxsf  # Should show dmode=775,fmode=755
which meza  # Should show /usr/bin/meza
```

## Manual Step-by-Step (If Script Doesn't Work)

### 1. Install VirtualBox Guest Additions

```bash
# Install required packages
sudo dnf install -y kernel-devel kernel-headers gcc make perl bzip2 elfutils-libelf-devel

# Insert Guest Additions CD
# In VirtualBox menu: Devices → Insert Guest Additions CD Image

# Mount and install
sudo mkdir -p /mnt/cdrom
sudo mount /dev/cdrom /mnt/cdrom
sudo /mnt/cdrom/VBoxLinuxAdditions.run

# Reboot
sudo reboot
```

### 2. Create meza-ansible User (if not exists)

```bash
# This is done by getmeza.sh (or successor Ansible role), but if you need to do it manually:
sudo groupadd -g 10000 wheel
sudo useradd -u 10000 -g wheel -d /opt/conf-meza/users/meza-ansible -m meza-ansible
```

### 3. Mount Shared Folder with Proper Options

```bash
# Create mount point
sudo mkdir -p /opt/meza

# Mount with proper permissions
sudo mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 meza /opt/meza

# Verify
ls -la /opt/meza
```

### 4. Add meza-ansible to vboxsf Group

```bash
sudo usermod -aG vboxsf meza-ansible
groups meza-ansible  # Verify
```

### 5. Make Permanent (Add to /etc/fstab)

```bash
echo "meza    /opt/meza    vboxsf    uid=10000,gid=10000,dmode=775,fmode=755    0    0" | sudo tee -a /etc/fstab
```

### 6. Fix Permissions on Scripts

```bash
sudo find /opt/meza/src/scripts -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod 775 {} \;
```

## Troubleshooting

### "mount: unknown filesystem type 'vboxsf'"

VirtualBox Guest Additions not installed or kernel module not loaded:

```bash
# Check if module exists
lsmod | grep vboxsf

# Load module
sudo modprobe vboxsf

# If module doesn't exist, install Guest Additions (see step 1 above)
```

### "Protocol error" when mounting

The shared folder name in VirtualBox doesn't match the mount command:

```bash
# List configured shared folders
VBoxControl sharedfolder list

# Use the exact name shown
sudo mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 <exact_name> /opt/meza
```

### Files still owned by root:vboxsf

Check UID/GID mapping:

```bash
# Check current meza-ansible UID
id -u meza-ansible  # Should be 10000

# Check wheel GID
getent group wheel | cut -d: -f3  # Should be 10000

# If different, either:
# Option A: Change the user/group IDs
sudo usermod -u 10000 meza-ansible
sudo groupmod -g 10000 wheel

# Option B: Use the actual UID/GID in mount command
sudo mount -t vboxsf -o uid=$(id -u meza-ansible),gid=$(getent group wheel | cut -d: -f3),dmode=775,fmode=755 meza /opt/meza
```

### Permission denied even with vboxsf group

Log out and back in for group membership to take effect:

```bash
exit
# SSH back in
groups meza-ansible  # Verify vboxsf is listed
```

Or start a new shell with the group active:

```bash
newgrp vboxsf
```

### "meza: command not found" or /usr/bin not in PATH

The meza-ansible user's shell initialization files need to be configured:

```bash
sudo su - meza-ansible
echo $PATH  # Check if /usr/bin is included

# If PATH is missing standard directories, run the fix script again:
exit
sudo bash /opt/meza/src/scripts/fix-vbox-permissions.sh

# Or manually configure:
cat >> ~/.bashrc <<'EOF'

# Ensure standard system paths are included
if ! [[ "$PATH" =~ "/usr/bin" ]]; then
    PATH="/usr/bin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/local/bin" ]]; then
    PATH="/usr/local/bin:$PATH"
fi
export PATH
EOF

# Then reload shell
exit
sudo su - meza-ansible
```

This ensures the meza command (/usr/bin/meza → /opt/meza/src/scripts/meza.py) is found.

### "Permission denied" running meza command

With `fmode=755`, the meza.py script should be executable. If you still get permission denied:

```bash
# Verify the mount options include fmode=755
mount | grep meza
# Should show: fmode=755

# If not, remount with correct options
sudo umount /opt/meza
sudo mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 meza /opt/meza

# Verify the symlink
ls -la /usr/bin/meza
# Should show: /usr/bin/meza -> /opt/meza/src/scripts/meza.py

# Verify meza.py is executable
ls -la /opt/meza/src/scripts/meza.py
# Should show: -rwxr-xr-x

# If symlink is missing, re-run setup:
sudo bash /opt/meza/src/scripts/setup-manual-vbox-mount.sh meza /opt/meza
```

The `fmode=755` mount option allows execute permissions on vboxsf, enabling direct symlink to meza.py without wrapper scripts.

## Alternative: Use Vagrant with Existing VM (Advanced)

It's possible but complex to import an existing VM into Vagrant. Generally not recommended. Instead:

1. **Export your VM settings** (note your disk size, network config, etc.)
2. **Use Vagrant to create a new VM** with those settings
3. **Migrate your data** if needed

The Vagrantfile in this repo is already configured with all the fixes, so new VMs will work correctly out of the box.

## Comparison: Manual VM vs Vagrant

| Feature | Manual VM | Vagrant VM |
|---------|-----------|------------|
| **Setup time** | More steps | Automated |
| **Shared folders** | Manual mount config | Auto-configured |
| **Permissions** | Manual fixes needed | Pre-configured |
| **Reproducibility** | Manual steps each time | `vagrant up` |
| **Team sharing** | Document all steps | Share Vagrantfile |
| **Recommended for** | Learning, special needs | Development, teams |

## Development Workflow (Once Setup Complete)

1. **Edit on host**: Use your favorite IDE on Linux host at `~/src/meza`
2. **Run in guest**: Execute meza commands as `meza-ansible` in the VM
3. **Git operations**: Commit from either host or guest (files stay in sync)

The shared folder keeps everything synchronized automatically!
