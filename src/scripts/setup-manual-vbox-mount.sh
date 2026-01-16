#!/bin/bash
#
# Setup VirtualBox shared folder mount with proper permissions
# For VMs created manually (e.g. using VirtualBox Manager directly,not through Vagrant)
#
# Run this script inside your guest VM after configuring the shared folder
# in VirtualBox Manager.
#
# Usage:
#   sudo bash setup-manual-vbox-mount.sh [share_name] [mount_point]
#
# Example:
#   sudo bash setup-manual-vbox-mount.sh meza /opt/meza

SHARE_NAME="${1:-meza}"
MOUNT_POINT="${2:-/opt/meza}"

echo "Setting up VirtualBox shared folder: $SHARE_NAME -> $MOUNT_POINT"

# Install VirtualBox Guest Additions if not already installed
if ! command -v VBoxControl &> /dev/null; then
    echo "VirtualBox Guest Additions not found. Installing..."
    if command -v dnf &> /dev/null; then
        # Rocky/RHEL
        dnf install -y kernel-devel kernel-headers gcc make perl bzip2
        # You may need to install Guest Additions ISO manually
        echo "Please install VirtualBox Guest Additions from the VirtualBox menu:"
        echo "Devices → Insert Guest Additions CD Image"
        exit 1
    fi
fi

# Check if vboxsf kernel module is loaded
if ! lsmod | grep -q vboxsf; then
    echo "Loading vboxsf kernel module..."
    modprobe vboxsf
fi

# Create mount point if it doesn't exist
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Creating mount point: $MOUNT_POINT"
    mkdir -p "$MOUNT_POINT"
fi

# Unmount if already mounted (to remount with correct options)
if mountpoint -q "$MOUNT_POINT"; then
    echo "Unmounting existing mount..."
    umount "$MOUNT_POINT"
fi

# Get meza-ansible UID and wheel GID (or use 10000 if users don't exist yet)
if id meza-ansible &> /dev/null; then
    MEZA_UID=$(id -u meza-ansible)
    WHEEL_GID=$(getent group wheel | cut -d: -f3)
    echo "Using meza-ansible UID: $MEZA_UID, wheel GID: $WHEEL_GID"
else
    MEZA_UID=10000
    WHEEL_GID=10000
    echo "Warning: meza-ansible user not found, using UID/GID 10000"
    echo "You may need to run this script again after creating meza-ansible user"
fi

# Mount with proper options
echo "Mounting $SHARE_NAME to $MOUNT_POINT with proper permissions..."
mount -t vboxsf -o uid=$MEZA_UID,gid=$WHEEL_GID,dmode=775,fmode=755 "$SHARE_NAME" "$MOUNT_POINT"

if [ $? -eq 0 ]; then
    echo "✓ Mounted successfully!"
    ls -la "$MOUNT_POINT" | head -10
else
    echo "✗ Mount failed. Make sure:"
    echo "  1. VirtualBox Guest Additions are installed"
    echo "  2. Shared folder '$SHARE_NAME' is configured in VirtualBox"
    echo "  3. Shared folder is set to auto-mount"
    exit 1
fi

# Add to /etc/fstab for automatic mounting on boot
if ! grep -q "$SHARE_NAME" /etc/fstab; then
    echo ""
    echo "Adding to /etc/fstab for automatic mounting on boot..."
    echo "$SHARE_NAME    $MOUNT_POINT    vboxsf    uid=$MEZA_UID,gid=$WHEEL_GID,dmode=775,fmode=755    0    0" >> /etc/fstab
    echo "✓ Added to /etc/fstab"
else
    echo ""
    echo "Note: Entry already exists in /etc/fstab"
fi

# Now run the permission fix script if it exists
if [ -f "$MOUNT_POINT/manual/fix-vbox-permissions.sh" ]; then
    echo ""
    echo "Running permission fix script..."
    bash "$MOUNT_POINT/manual/fix-vbox-permissions.sh" "$(dirname $MOUNT_POINT)"
else
    echo ""
    echo "Manually fixing permissions..."

    # Add meza-ansible to vboxsf group
    if id meza-ansible &> /dev/null; then
        usermod -aG vboxsf meza-ansible
        echo "✓ Added meza-ansible to vboxsf group"
    fi

    # Fix ownership
    chown -R meza-ansible:wheel "$MOUNT_POINT"

    # Make scripts executable
    find "$MOUNT_POINT/src/scripts" -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod 775 {} \; 2>/dev/null

    echo "✓ Permissions fixed"
fi

# Create meza wrapper script (files on vboxsf cannot have execute bit with fmode=664)
echo ""
echo "Creating meza wrapper script..."

# Remove old symlink if it exists
if [ -L /usr/bin/meza ]; then
    echo "Removing old symlink /usr/bin/meza"
    rm -f /usr/bin/meza
fi

# Create wrapper script that calls Python on meza.py
cat > /usr/local/bin/meza <<EOF
#!/bin/bash
# Wrapper script for meza command
# Calls Python on meza.py in shared folder (which cannot have execute bit on vboxsf)
exec /usr/bin/python3 $MOUNT_POINT/src/scripts/meza.py "\$@"
EOF

chmod 755 /usr/local/bin/meza

# Also create symlink in /usr/bin for compatibility
if [ ! -e /usr/bin/meza ]; then
    ln -s /usr/local/bin/meza /usr/bin/meza
fi

echo "✓ Created meza wrapper at /usr/local/bin/meza"

# Configure PATH for meza-ansible user
if id meza-ansible &> /dev/null; then
    MEZA_HOME=$(getent passwd meza-ansible | cut -d: -f6)
    echo ""
    echo "Configuring PATH for meza-ansible user..."

    # Create .bashrc if it doesn't exist
    if [ ! -f "$MEZA_HOME/.bashrc" ]; then
        echo "Creating $MEZA_HOME/.bashrc"
        cat > "$MEZA_HOME/.bashrc" <<'EOF'
# .bashrc for meza-ansible user

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]; then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Ensure standard system paths are included
if ! [[ "$PATH" =~ "/usr/local/bin" ]]; then
    PATH="/usr/local/bin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/bin" ]]; then
    PATH="/usr/bin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/local/sbin" ]]; then
    PATH="/usr/local/sbin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/sbin" ]]; then
    PATH="/usr/sbin:$PATH"
fi
export PATH

# User specific aliases and functions
EOF
        chown meza-ansible:wheel "$MEZA_HOME/.bashrc"
        chmod 644 "$MEZA_HOME/.bashrc"
        echo "✓ Created .bashrc"
    else
        # Append PATH configuration if not already present
        if ! grep -q "# Ensure standard system paths" "$MEZA_HOME/.bashrc"; then
            echo "" >> "$MEZA_HOME/.bashrc"
            cat >> "$MEZA_HOME/.bashrc" <<'EOF'

# Ensure standard system paths are included
if ! [[ "$PATH" =~ "/usr/local/bin" ]]; then
    PATH="/usr/local/bin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/bin" ]]; then
    PATH="/usr/bin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/local/sbin" ]]; then
    PATH="/usr/local/sbin:$PATH"
fi
if ! [[ "$PATH" =~ "/usr/sbin" ]]; then
    PATH="/usr/sbin:$PATH"
fi
export PATH
EOF
            echo "✓ Updated .bashrc with PATH configuration"
        else
            echo "✓ .bashrc already configured with PATH"
        fi
    fi

    # Create .bash_profile if it doesn't exist
    if [ ! -f "$MEZA_HOME/.bash_profile" ]; then
        echo "Creating $MEZA_HOME/.bash_profile"
        cat > "$MEZA_HOME/.bash_profile" <<'EOF'
# .bash_profile for meza-ansible user

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# User specific environment and startup programs
EOF
        chown meza-ansible:wheel "$MEZA_HOME/.bash_profile"
        chmod 644 "$MEZA_HOME/.bash_profile"
        echo "✓ Created .bash_profile"
    else
        echo "✓ .bash_profile exists"
    fi
fi

echo ""
echo "===================="
echo "Setup Complete!"
echo "===================="
echo ""
echo "The shared folder is now mounted with proper permissions."
echo ""
echo "IMPORTANT: Log out and log back in for group changes to take effect."
echo ""
echo "To verify:"
echo "  groups meza-ansible    # Should include vboxsf"
echo "  ls -la $MOUNT_POINT/src/playbooks/site.yml"
echo "  sudo su - meza-ansible"
echo "  echo \$PATH    # Should include /usr/bin"
echo "  which meza     # Should show /usr/bin/meza"
echo "  touch $MOUNT_POINT/test && rm $MOUNT_POINT/test"
