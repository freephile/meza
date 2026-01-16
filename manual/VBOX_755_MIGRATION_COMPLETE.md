# VirtualBox Mount Configuration

## Current Configuration

Meza uses `fmode=755` for VirtualBox shared folder mounts, enabling direct execution of scripts without wrapper complexity.

**Mount Options**: `uid=10000,gid=10000,dmode=775,fmode=755`
- **dmode=775**: Directories are group-writable (rwxrwxr-x)
- **fmode=755**: Files are executable (rwxr-xr-x)

**Benefits**:
- Direct symlink: `/usr/bin/meza -> /opt/meza/src/scripts/meza.py`
- No wrapper scripts needed
- Host filesystem unchanged (mount options only affect guest)

## Setup

### Vagrant Users
```bash
# see the current status of your Vagrant machine
vagrant status
# force destroy any existing vm
vagrant destroy -f
# start and provision the vagrant environment according to your Vagrantfile
vagrant up
```

### Manual VM Users
If you've previously created a VM using VirtualBox Manager (e.g. CMTE)
and you wish to continue using that VM, you can fix permission problems on the VM
```bash
sudo bash /opt/meza/src/scripts/fix-vbox-permissions.sh
```

## Verification

```bash
mount | grep vboxsf  # Should show: dmode=775,fmode=755
ls -la /usr/bin/meza  # Should show: -> /opt/meza/src/scripts/meza.py
meza help  # Should work
```

## Troubleshooting

**meza command not found**: Check PATH includes `/usr/bin`, recreate symlink if missing
**Permission denied**: Ensure `meza-ansible` is in `vboxsf` group, log out/in to apply

**Related Documentation**: [VBOX_PERMISSIONS.md](VBOX_PERMISSIONS.md), [VBOX_MANUAL_VM.md](VBOX_MANUAL_VM.md), [PATH_FIX.md](PATH_FIX.md)
