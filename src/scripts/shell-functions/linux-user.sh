#!/bin/sh
#
# Shell functions to add and modify linux users

MEZA_IP=$(dirname $(dirname $(dirname $(dirname $(realpath $(which meza))))))

# Don't create meza application users under /home, ref: #727
meza_user_dir="${MEZA_IP}/conf-meza/users"

mf_user_exists() {
    ret=false
    getent passwd $1 >/dev/null 2>&1 && ret=true

    if $ret; then
        # user exists (bash 0 for true, yuck)
        return 0
    else
        return 1
    fi
}

mf_add_ssh_user() {
    mkdir -p "$meza_user_dir"
    chown root:root "$meza_user_dir"
    chmod 755 "$meza_user_dir"

    if ! mf_user_exists "$1"; then
        useradd "$1" --home-dir "$meza_user_dir/$1"

        # Ensure meza-ansible is in required groups for file operations
        if [ "$1" = "meza-ansible" ] && command -v usermod >/dev/null 2>&1; then
            # Add to apache group for web file access
            if getent group apache >/dev/null 2>&1; then
                usermod -a -G apache "$1"
                echo "Added $1 to apache group"
            elif getent group www-data >/dev/null 2>&1; then
                usermod -a -G www-data "$1"
                echo "Added $1 to www-data group"
            fi

            # Add to wheel group for sudo access
            if getent group wheel >/dev/null 2>&1; then
                usermod -a -G wheel "$1"
                echo "Added $1 to wheel group"
            fi
        fi
    fi

    mkdir -p "$meza_user_dir/$1/.ssh"
    chown -R "$1:$1" "$meza_user_dir/$1/.ssh"
    chmod 700 "$meza_user_dir/$1/.ssh"

    # Make sure user dir properly owned. Not having this was never an issue on
    # RedHat, but causes errors on Debian.
    chown "$1:$1" "$meza_user_dir/$1"

    # Create shell initialization files for proper PATH and umask
    # Ref: PATH_FIX.md and issue #272
    # This ensures:
    # 1. System defaults are sourced (/etc/profile, /etc/bashrc, /etc/bash.bashrc)
    # 2. PATH includes standard directories (/usr/bin, /usr/local/bin, etc.)
    # 3. umask is set to 0002 for group-writable files
    # Works across RHEL/Rocky/Debian/Ubuntu for both login and interactive shells

    # Create .bash_profile (login shells)
    cat > "$meza_user_dir/$1/.bash_profile" <<'BASH_PROFILE_EOF'
# .bash_profile for meza-ansible user
# Sourced by bash for login shells

# Source system-wide profile if it exists
if [ -f /etc/profile ]; then
    . /etc/profile
fi

# Source user's .bashrc for interactive settings
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# Ensure standard paths are in PATH (defensive approach)
for dir in /usr/local/bin /usr/bin /usr/local/sbin /usr/sbin; do
    case ":$PATH:" in
        *":$dir:"*) ;;
        *) PATH="$dir:$PATH" ;;
    esac
done
export PATH

# Set umask for group-writable files (0664) and directories (0775)
# Required for apache group to write to logs, cache, uploads
umask 0002
BASH_PROFILE_EOF

    # Create .bashrc (interactive shells)
    cat > "$meza_user_dir/$1/.bashrc" <<'BASHRC_EOF'
# .bashrc for meza-ansible user
# Sourced by bash for interactive non-login shells

# Source system-wide bashrc if it exists
# RHEL/Rocky uses /etc/bashrc
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi
# Debian/Ubuntu uses /etc/bash.bashrc
if [ -f /etc/bash.bashrc ]; then
    . /etc/bash.bashrc
fi

# Ensure standard paths are in PATH (defensive approach)
for dir in /usr/local/bin /usr/bin /usr/local/sbin /usr/sbin; do
    case ":$PATH:" in
        *":$dir:"*) ;;
        *) PATH="$dir:$PATH" ;;
    esac
done
export PATH

# Set umask for group-writable files (0664) and directories (0775)
# Required for apache group to write to logs, cache, uploads
umask 0002

# User-specific aliases and functions can be added below
BASHRC_EOF

    # Set ownership and permissions
    chown "$1:$1" "$meza_user_dir/$1/.bash_profile"
    chown "$1:$1" "$meza_user_dir/$1/.bashrc"
    chmod 644 "$meza_user_dir/$1/.bash_profile"
    chmod 644 "$meza_user_dir/$1/.bashrc"

    echo "Created shell initialization files for $1"
}

mf_add_ssh_user_with_private_key() {
    mf_add_ssh_user "$1"
    if [ -f "$meza_user_dir/$1/.ssh/id_rsa" ]; then
        echo "SSH keys exist for user $1. Moving on."
    else
        ssh-keygen -f "$meza_user_dir/$1/.ssh/id_rsa" -t rsa -N '' -C "$1@`hostname`"
    fi
    chown -R "$1:$1" "$meza_user_dir/$1/.ssh"
}

mf_add_public_user_with_public_key () {
    mf_add_ssh_user "$1"

    if [ -z "$2" ]; then
        echo "mf_add_public_user_with_public_key requires a public key as second argument"
        exit 1;
    fi

    tmpfile=$(mktemp /tmp/pub.XXXXXX)
    echo "$2" >> "$tmpfile"
    importkey_check=`ssh-keygen -l -f "$tmpfile"`
    rm -f "$tmpfile"
    if [ "$importkey_check" = "$tmpfile is not a public key file." ]; then
        echo "The following is not a valid public key:"
        echo
        echo "$2"
        echo
        exit 1;
    fi

    echo "$2" >> "$meza_user_dir/$1/.ssh/authorized_keys"
    chmod 600 "$meza_user_dir/$1/.ssh/authorized_keys"
    chown -R "$1:$1" "$meza_user_dir/$1/.ssh"
}
