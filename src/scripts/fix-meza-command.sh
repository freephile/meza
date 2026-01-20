#!/bin/bash
#
# Quick fix for "Permission denied" when running meza command
# on VirtualBox shared folders
#
# Modern solution: Remount with fmode=755 to allow execute permissions
# and create a simple symlink (no wrapper scripts needed).
#
# For complete setup, use: sudo bash /opt/meza/manual/fix-vbox-permissions.sh
# This script is a simplified version for quick fixes.
#
# Usage: sudo bash fix-meza-command.sh

echo "Fixing meza command for VirtualBox shared folder..."

# Find meza installation
MEZA_SCRIPT="/opt/meza/src/scripts/meza.py"
if [ ! -f "$MEZA_SCRIPT" ]; then
    echo "Error: meza.py not found at $MEZA_SCRIPT"
    exit 1
fi

echo "Found meza.py at: $MEZA_SCRIPT"

# Check current mount
echo ""
echo "Checking current mount options..."
mount | grep vboxsf | grep meza

# Remount with fmode=755
echo ""
echo "Remounting with fmode=755 to allow execute permissions..."
umount /opt/meza 2>/dev/null || true
mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 meza /opt/meza

if [ $? -eq 0 ]; then
    echo "✓ Remounted successfully with fmode=755"
else
    echo "✗ Remount failed. Check VirtualBox shared folder configuration."
    exit 1
fi

# Remove old symlinks
if [ -L /usr/bin/meza ]; then
    echo "Removing old symlink: /usr/bin/meza"
    rm -f /usr/bin/meza
fi

# Create simple symlink
echo "Creating symlink: /usr/bin/meza → $MEZA_SCRIPT"
ln -s "$MEZA_SCRIPT" /usr/bin/meza

if [ $? -eq 0 ]; then
    echo "✓ Created symlink"
else
    echo "✗ Failed to create symlink"
    exit 1
fi

# Update /etc/fstab if entry exists
if grep -q "meza.*vboxsf.*fmode=664" /etc/fstab; then
    echo ""
    echo "Updating /etc/fstab to use fmode=755..."
    sed -i 's/fmode=664/fmode=755/g' /etc/fstab
    echo "✓ Updated /etc/fstab"
fi

# Verify
echo ""
echo "===================="
echo "Verification"
echo "===================="
echo ""

# Check mount options
echo "Mount options:"
mount | grep vboxsf | grep meza

# Check meza.py is executable
echo ""
echo "meza.py permissions:"
ls -la "$MEZA_SCRIPT"

# Check symlink
echo ""
echo "Symlink:"
ls -la /usr/bin/meza

# Check which meza
WHICH_MEZA=$(which meza 2>/dev/null)
if [ -n "$WHICH_MEZA" ]; then
    echo ""
    echo "✓ meza found in PATH: $WHICH_MEZA"
else
    echo ""
    echo "✗ meza not found in PATH"
    echo "  Make sure /usr/bin is in your PATH"
fi

# Test the command
echo ""
echo "Testing meza command..."
if meza help &>/dev/null || meza --version &>/dev/null; then
    echo "✓ meza command works!"
else
    echo "⚠ meza command may have issues. Try running: meza help"
fi

echo ""
echo "===================="
echo "Complete!"
echo "===================="
echo ""
echo "The meza command should now work with direct execution (no wrapper scripts)."
echo ""
echo "Test with:"
echo "  meza help"
echo "  meza --version"
echo ""
echo "Note: This uses fmode=755 which allows execute permissions on all files."
echo "This is safe because VirtualBox mount options only affect the guest VM,"
echo "not the actual files on your host machine."
