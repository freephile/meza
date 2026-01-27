#!/bin/sh
#
# Bootstrap meza
#
# @TODO refactor and document this script better
# @See https://github.com/freephile/meza/issues/172#issuecomment-3141998590
# We use INSTALL_DIR rather than m_install since this script is run without paths.yml and the set_vars role

if [ "$(whoami)" != "root" ]; then
	echo "Try running this script with sudo: \"sudo bash getmeza.sh\""
	exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

INSTALL_DIR=$(dirname $(dirname $(dirname ${SCRIPT_DIR})))

for ARG in "$@"; do
	if [ "${ARG}" = "--skip-conn-check" ]; then
		SKIP_CONNECTION_CHECK="true"
	fi
done

checkInternetConnection() {
	declare -i pingRetries=100
	declare -i sleepDuration=3
	declare -i minutes=$(($pingRetries * $sleepDuration / 60))

	while [[ $pingRetries -gt 0 ]] && ! ping -c 1 -W 1 cdn.redhat.com >/dev/null 2>&1; do
		echo "Could not connect to cdn.redhat.com. Internet connection might be down. Retrying (#$pingRetries) in $sleepDuration seconds..."
		((pingRetries -= 1))
		sleep $sleepDuration
	done

	if [[ ! $pingRetries -gt 0 ]]; then
		echo "Meza has been trying to install but hasn't found an internet connection for $minutes minutes. Verify internet connectivity and try again."
		exit 1
	fi
}

if [ ! -z "${SKIP_CONNECTION_CHECK}" ]; then
	echo "Skipping connection check"
else
	checkInternetConnection
fi

# Set umask to ensure group-writable files during bootstrap
# Without this, restrictive umask (0022 or 077) causes permission issues
# for git clones, file creation, and deployment operations
# This matches m_umask in config/defaults.yml (currently 0002)
# Ref: https://github.com/freephile/meza/issues/272
umask 002

# Check distro and version to determine what needs to be installed
if [ ! -f /etc/redhat-release ]; then
    echo "Error: Only RedHat-based systems (Rocky Linux 8+, RHEL 8+) are supported"
    exit 1
fi

# Detect RedHat variant and version
RH_VARIANTS="redhat rocky"
for VARIANT in ${RH_VARIANTS}; do
    version=$(rpm -q ${VARIANT}-release --queryformat "%{VERSION}" 2>/dev/null | grep -v "not installed" || true)
    if [ -n "${version}" ]; then
        distro=${VARIANT}
        break
    fi
done

if [ -z "${distro}" ]; then
    echo "Error: Could not detect supported RedHat variant"
    exit 1
fi

# Verify supported version
case ${distro} in
    rocky)
        if [[ ! "${version}" =~ ^8\. ]]; then
            echo "Error: Only Rocky Linux 8.x is currently supported (detected: ${version})"
            exit 1
        fi
        ;;
    redhat)
        if [[ ! "${version}" =~ ^8\. ]]; then
            echo "Error: Only Red Hat Enterprise Linux 8.x is currently supported (detected: ${version})"
            exit 1
        fi
        ;;
esac

echo "Detected: ${distro} ${version}"

# Create conf-meza directory structure
mkdir -p ${INSTALL_DIR}/conf-meza/secret
chmod 755 ${INSTALL_DIR}/conf-meza
chmod 775 ${INSTALL_DIR}/conf-meza/secret

# Configure repositories based on distro
case ${distro} in
    rocky)
        # Install dnf-plugins-core (required for config-manager command)
        if ! rpm -q dnf-plugins-core >/dev/null 2>&1; then
            echo "Installing dnf-plugins-core..."
            dnf install -y dnf-plugins-core
        fi

        # Enable PowerTools/CRB repository (check if already enabled first)
        if ! dnf repolist enabled --quiet | grep -qE 'powertools|crb'; then
            echo "Enabling PowerTools repository..."

            # Show what we found
            echo "Available PowerTools repositories:"
            dnf repolist all --quiet | grep -iE 'powertools|crb' | grep -v 'debug\|source'

            # The repo ID is just "powertools" on generic/rocky8
            dnf config-manager --set-enabled powertools 2>/dev/null || \
            dnf config-manager --set-enabled PowerTools 2>/dev/null || \
            dnf config-manager --set-enabled crb 2>/dev/null

            # Verify it was enabled
            if dnf repolist enabled --quiet | grep -qE 'powertools|crb'; then
                echo "✓ Successfully enabled PowerTools repository"
            else
                echo "⚠ WARNING: Failed to enable PowerTools repository"
                echo "Enabled repositories:"
                dnf repolist enabled
            fi
        else
            echo "✓ PowerTools repository already enabled"
        fi

        # Install EPEL repository if not present
        if [ ! -f "/etc/yum.repos.d/epel.repo" ]; then
            echo "Installing EPEL repository..."
            dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
        fi

        # Reset PHP module to allow version selection
        dnf module -y reset php 2>/dev/null || true
        ;;

    redhat)
        # Enable CodeReady Builder repository
        if ! subscription-manager repos --list-enabled | grep -q codeready-builder; then
            echo "Enabling CodeReady Builder repository..."
            subscription-manager repos --enable codeready-builder-for-rhel-8-$(arch)-rpms
        fi

        # Install EPEL if not present
        if [ ! -f "/etc/yum.repos.d/epel.repo" ]; then
            echo "Installing EPEL repository..."
            dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
        fi

        # Reset PHP module
        dnf module -y reset php 2>/dev/null || true
        ;;
esac

# Install base system packages
echo "Installing base system packages..."
dnf install -y \
    git \
    python36 \
    ansible \
    python3-libselinux \
    python3-devel \
    gcc \
    make \
    autoconf \
    automake \
    pkgconfig \
    libffi-devel \
    openssl-devel \
    cargo \
    rust

# Set python3 as default python
alternatives --set python /usr/bin/python3 2>/dev/null || true

# Verify PowerTools/CRB is enabled
echo "Verifying repository configuration..."
if dnf repolist enabled | grep -iE '(powertools|crb|codeready)' >/dev/null; then
    echo "✓ Development repository enabled"
else
    echo "⚠ WARNING: Development repository may not be enabled"
    echo "This may cause package installation failures during deployment"
    echo "Enabled repositories:"
    dnf repolist enabled
fi

# Meza repository URL and branch configuration
# Example overrides:
# export MEZA_REPOSITORY_URL='https://github.com/freephile/meza.git';
# export MEZA_BRANCH_NAME='dev';
MEZA_REPOSITORY_URL="${MEZA_REPOSITORY_URL:-https://github.com/nasa/meza.git}"
MEZA_BRANCH_NAME="${MEZA_BRANCH_NAME:-main}"

# Clone meza repository if it doesn't exist
if [ ! -d "${INSTALL_DIR}/meza" ]; then
    echo "Cloning Meza repository..."
    echo "using Repository URL: ${MEZA_REPOSITORY_URL}"
    echo "using Branch name: ${MEZA_BRANCH_NAME}"
    git clone ${MEZA_REPOSITORY_URL} --branch ${MEZA_BRANCH_NAME} "${INSTALL_DIR}/meza"
fi

# Set proper permissions on meza directory
echo "Setting repository permissions..."
chmod a+r ${INSTALL_DIR}/meza -R
find ${INSTALL_DIR}/meza -type d -exec chmod 755 {} +

# Create meza command symlink
if [ ! -f "/usr/bin/meza" ]; then
    ln -s "${INSTALL_DIR}/meza/src/scripts/meza.py" "/usr/bin/meza"
fi

# Create .deploy-meza directory with basic config
mkdir -p ${INSTALL_DIR}/.deploy-meza
chmod 755 ${INSTALL_DIR}/.deploy-meza

if [ ! -f ${INSTALL_DIR}/.deploy-meza/config.sh ]; then
    echo "m_scripts='${INSTALL_DIR}/meza/src/scripts'; ansible_user='meza-ansible';" > ${INSTALL_DIR}/.deploy-meza/config.sh
fi

# Create data directory for lock files (@TODO: better location? - need write access to enable deploys without sudo)
mkdir -p ${INSTALL_DIR}/data-meza

# Setup or verify meza-ansible user
ret=false
getent passwd meza-ansible >/dev/null 2>&1 && ret=true

if $ret; then
    echo "Verifying meza-ansible user configuration..."
    homedir=$( getent passwd "meza-ansible" | cut -d: -f6 )
    if [ "$homedir" != "${INSTALL_DIR}/conf-meza/users/meza-ansible" ]; then
        echo "Updating meza-ansible home directory..."
        mkdir -p "${INSTALL_DIR}/conf-meza/users"
        usermod -m -d "${INSTALL_DIR}/conf-meza/users/meza-ansible" "meza-ansible"
    fi
else
    echo "Creating meza-ansible user with Ansible..."

    # Run the meza-user role via Ansible playbook
    # This replaces the bash script setup-master-user.sh with a proper Ansible role
    # Ref: GitHub issue #272
    ANSIBLE_CONFIG="${INSTALL_DIR}/meza/config/ansible.cfg" \
    ansible-playbook \
        -i localhost, \
        --connection=local \
        "${INSTALL_DIR}/meza/src/playbooks/setup-meza-user.yml"
    # @TODO: this script is deprecated and needs to be removed in 6 months
    if [ $? -ne 0 ]; then
        echo "WARNING: Ansible user setup failed. Falling back to bash script..."
        source "${INSTALL_DIR}/meza/src/scripts/ssh-users/setup-master-user.sh"
    fi
fi

# Set ownership on meza directories
chown meza-ansible:wheel ${INSTALL_DIR}/conf-meza
chown meza-ansible:wheel ${INSTALL_DIR}/conf-meza/secret
chown meza-ansible:wheel ${INSTALL_DIR}/meza

# Configure sudoers for passwordless ansible operations
# @TODO: setup-minion-user.sh needs to be refactored/updated
echo "Configuring sudo permissions..."
sed -r -i "s/^Defaults\\s+requiretty/#Defaults requiretty/g;" /etc/sudoers
sed -r -i "s/^Defaults\\s+\!visiblepw/#Defaults \\!visiblepw/g;" /etc/sudoers

# Upgrade pip to avoid cryptography build issues (ignore root warning - intentional system-wide install)
echo "Upgrading pip and installing Ansible..."
python3 -m pip install --upgrade pip setuptools wheel 2>&1 | grep -v "WARNING: Running pip as the 'root' user" || true

# Install ansible system-wide (newer pip supports --root-user-action flag)
python3 -m pip install ansible --root-user-action=ignore 2>/dev/null || python3 -m pip install ansible

# Install ansible collections as meza-ansible user
echo "Installing Ansible collections..."
sudo -H -u meza-ansible bash -c 'cd /opt/meza/config && ansible-galaxy collection install -r ../requirements.yml'

# @TODO [Run meza as non-root user](https://github.com/freephile/meza/issues/72)
# Display completion message with next steps
if id -u vagrant >/dev/null 2>&1; then
    echo ""
    echo "✓ Meza bootstrap complete (Vagrant environment detected)"
    echo ""
    echo "Vagrant provisioning will automatically run 'meza setup env vagrant'"
    echo "After provisioning completes, deploy with:"
    echo "  vagrant ssh"
	echo "  sudo su - meza-ansible"
	echo "  cd /opt/meza/config"
    echo "  sudo meza deploy vagrant -vvv"
else
    echo ""
    echo "✓ Meza bootstrap complete"
    echo ""
	echo "Remember to always become the meza-ansible user"
	echo "and navigate to /opt/meza/config before deploying:"
	echo ""
	echo "  sudo su - meza-ansible"
	echo "  cd /opt/meza/config"
	echo ""
    echo "Next steps:"
    echo "  1. Setup environment:  sudo meza setup env <env-name>"
    echo "     Example (single server): sudo meza setup env prod --fqdn=wiki.example.com --db_pass=SecurePass123"
    echo ""
    echo "  2. Deploy MediaWiki:   sudo meza deploy <env-name> -vvv"
    echo ""
    echo "For local testing on this server:"
    echo "  sudo meza setup env monolith --fqdn=\$(hostname -I | awk '{print \$1}') --db_pass=TestPass123"
    echo "  sudo meza deploy monolith -vvv"
fi
