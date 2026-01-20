#!/bin/bash
#
# Fix VirtualBox shared folder permissions for meza-ansible user
#
# Run this script inside the guest VM if you're experiencing permission issues
# with VirtualBox shared folders.
#
# Usage:
#   sudo bash fix-vbox-permissions.sh [install_dir]
#
# Default install_dir is /opt

INSTALL_DIR="${1:-/opt}"

echo "Fixing VirtualBox shared folder permissions for ${INSTALL_DIR}/meza"

# Add meza-ansible to vboxsf group if not already a member
if ! groups meza-ansible | grep -q vboxsf; then
    echo "Adding meza-ansible to vboxsf group..."
    usermod -aG vboxsf meza-ansible
    echo "✓ Added meza-ansible to vboxsf group"
else
    echo "✓ meza-ansible already in vboxsf group"
fi

# Verify the user is in the group
echo "Current meza-ansible groups: $(groups meza-ansible)"

# Fix ownership and permissions on the meza directory
echo "Fixing ownership and permissions..."
chown -R meza-ansible:wheel "${INSTALL_DIR}/meza"
find "${INSTALL_DIR}/meza" -type d -exec chmod 775 {} \;
find "${INSTALL_DIR}/meza" -type f -exec chmod 755 {} \;

# Make scripts executable
echo "Making scripts executable..."
find "${INSTALL_DIR}/meza/src/scripts" -type f -name "*.sh" -exec chmod 775 {} \;
find "${INSTALL_DIR}/meza/src/scripts" -type f -name "*.py" -exec chmod 775 {} \;

# Make the meza binary executable
if [ -f "${INSTALL_DIR}/meza/src/scripts/meza.py" ]; then
    chmod 775 "${INSTALL_DIR}/meza/src/scripts/meza.py"
fi

# Remount the shared folder with fmode=755 to allow execute permissions
echo "Remounting ${INSTALL_DIR}/meza with fmode=755..."
umount "${INSTALL_DIR}/meza" 2>/dev/null || true
mount -t vboxsf -o uid=10000,gid=10000,dmode=775,fmode=755 meza "${INSTALL_DIR}/meza"
echo "✓ Remounted with execute permissions enabled"

# Create simple symlink to meza.py
echo "Creating meza symlink..."

# Remove old wrapper or symlink if it exists
rm -f /usr/local/bin/meza /usr/bin/meza

# Create direct symlink
ln -s "${INSTALL_DIR}/meza/src/scripts/meza.py" /usr/bin/meza

echo "✓ Created meza symlink at /usr/bin/meza"

# Configure PATH for meza-ansible user
MEZA_HOME=$(getent passwd meza-ansible | cut -d: -f6)
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

echo ""
echo "✓ Permissions fixed!"
echo ""
echo "IMPORTANT: You may need to log out and log back in (or run 'newgrp vboxsf')"
echo "for the vboxsf group membership to take effect for your current session."
echo ""
echo "To switch to meza-ansible user with new permissions:"
echo "  sudo su - meza-ansible"
echo ""
echo "Or to apply group changes to current session:"
echo "  newgrp vboxsf"
echo ""
echo "PATH should now include /usr/bin. To verify:"
echo "  echo \$PATH"
echo "  which meza"
