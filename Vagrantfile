# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'yaml'
require 'digest/sha1'

# Require a minimum Vagrant version that supports vagrant-libvirt and all
# features used in this file (preserve_order provisioners, post_up_message, etc.)
Vagrant.require_version '>= 2.2.0'

# Detect host OS early (before plugin checks) so we can select the right provider.
# Source: https://stackoverflow.com/questions/26811089/vagrant-how-to-have-host-platform-specific-provisioning-steps
module OS
  def OS.windows?
    (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
  end

  def OS.mac?
    (/darwin/ =~ RUBY_PLATFORM) != nil
  end

  def OS.unix?
    !OS.windows?
  end

  # Not ideal. BSD is Unix but is not Mac, but would return true for Linux.
  def OS.linux?
    OS.unix? and not OS.mac?
  end
end

# Determine which Vagrant provider to use.
# On Linux, default to libvirt to avoid the KVM/VirtualBox hypervisor conflict:
# Docker Desktop and other KVM-based tools (which use KVM) cannot run alongside
# VirtualBox on Linux because both require exclusive access to CPU virtualisation.
# On Mac and Windows, VirtualBox remains the default.
# Override with: VAGRANT_DEFAULT_PROVIDER=virtualbox vagrant up
VAGRANT_PROVIDER = (ENV['VAGRANT_DEFAULT_PROVIDER'] || (OS.linux? ? 'libvirt' : 'virtualbox'))
ENV['VAGRANT_DEFAULT_PROVIDER'] = VAGRANT_PROVIDER
USING_LIBVIRT = (VAGRANT_PROVIDER == 'libvirt')

# Vagrant Plugins required
#
# libvirt provider (Linux default): requires vagrant-libvirt plugin
# VirtualBox provider (Mac/Windows default): requires vagrant-vbguest plugin
#
if ARGV[0] != 'plugin' && ARGV[0] != 'destroy'

  required_plugins = USING_LIBVIRT ? ['vagrant-libvirt'] : ['vagrant-vbguest']
  plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }
  if not plugins_to_install.empty?

    puts "Installing plugins: #{plugins_to_install.join(' ')}"
    if system "vagrant plugin install --local #{plugins_to_install.join(' ')}"
      exec "vagrant #{ARGV.join(' ')}"
    else
      abort "Installation of one or more plugins has failed. Aborting."
    end

  end
end

if not File.file?("#{File.dirname(__FILE__)}/.vagrant/id_rsa")
  system("
    ssh-keygen -f \"./.vagrant/id_rsa\" -t rsa -N \"\" -C \"vagrant@vagrant\"
  ")
end

if File.file?("#{File.dirname(__FILE__)}/vagrantconf.yml")
  configuration = YAML::load(File.read("#{File.dirname(__FILE__)}/vagrantconf.yml"))
else
  configuration = YAML::load(File.read("#{File.dirname(__FILE__)}/vagrantconf.default.yml"))
end


if configuration.key?("install_directory")
  install_directory = configuration["install_directory"]
else
  install_directory = "/opt"
end


if configuration.key?("baseBox")

  # Allow custom setting of base bax
  baseBox = configuration["baseBox"]

  # Since we can't determine the OS of an arbitrary base box, just say "custom"
  box_os = "custom"

elsif configuration.key?("box_os")

  box_os = configuration["box_os"]

  if box_os == "debian"
    baseBox = "debian/contrib-stretch64"
  elsif box_os == "rockylinux"
    # Use generic/rocky8 - better VirtualBox compatibility, no GRUB issues
    # baseBox = "rockylinux/8"
    baseBox = "generic/rocky8"
  else
    raise Vagrant::Errors::VagrantError.new, "Configuration option 'box_os' must be 'debian' or 'rockylinux'"
  end

else
  # default to Rocky Linux 8 (using generic/rocky8 for better compatibility)
  baseBox = "generic/rocky8"
  box_os = "rockylinux"
end


# OS module and VAGRANT_PROVIDER / USING_LIBVIRT are defined at the top of this file.

mezaDirName = File.dirname(__FILE__).rpartition("/").last
mezaInstallUnique = Digest::SHA1.hexdigest File.dirname(__FILE__)

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  #
  # CONFIGURE SECOND SERVER IF envtype == 2app
  # envtype=2app vagrant up
  #
  if configuration.key?("app2")

    config.vm.define "app2" do |app2|

      # Increase boot timeout for slower systems
      app2.vm.boot_timeout = 600

      hostname = 'meza-app2-' + box_os
      app2.vm.box = baseBox
      ip_address = configuration["app2"]["ip_address"]
      app2.vm.hostname = hostname

      app2.vm.network :private_network, ip: ip_address

      app2.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ['modifyvm', :id, '--cableconnected1', 'on']
        v.customize ["modifyvm", :id, "--memory", configuration["app2"]["memory"] ]
        v.customize ["modifyvm", :id, "--cpus", configuration["app2"]["cpus"] ]
        v.customize ["modifyvm", :id, "--name", mezaDirName + '-' + hostname + '-' + mezaInstallUnique]
      end

      # libvirt provider (Linux default - avoids KVM/VirtualBox conflict with Docker)
      app2.vm.provider :libvirt do |v|
        v.memory = configuration["app2"]["memory"]
        v.cpus = configuration["app2"]["cpus"]
        v.qemu_use_session = false
      end

      # Non-controlling server should not have meza
      app2.vm.synced_folder ".", "/vagrant", disabled: true

      # Transfer setup-minion-user.sh script to app2
      app2.vm.provision "file", source: "./src/scripts/ssh-users/setup-minion-user.sh", destination: "/tmp/minion.sh"
      app2.vm.provision "file", source: "./.vagrant/id_rsa.pub", destination: "/tmp/meza-ansible.id_rsa.pub"

      #
      # Setup SSH user and unsafe testing config
      #
      app2.vm.provision "minion-ssh", type: "shell", preserve_order: true, binary: true, inline: <<-SHELL
        if [ ! -f #{install_directory}/conf-meza/public/public.yml ]; then

          bash /tmp/minion.sh

          # Turn off host key checking for user meza-ansible, to avoid prompts
          echo "setup .ssh/config"
          bash -c 'echo -e "Host *\n   StrictHostKeyChecking no\n   UserKnownHostsFile=/dev/null" > #{install_directory}/conf-meza/users/meza-ansible/.ssh/config'
          sudo chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/config
          sudo chmod 600 #{install_directory}/conf-meza/users/meza-ansible/.ssh/config

          # Allow password auth
          echo "setup sshd_config password auth"
          sed -r -i 's/PasswordAuthentication no/PasswordAuthentication yes/g;' /etc/ssh/sshd_config
          systemctl restart sshd
        fi
      SHELL
    end

  end

  # FIXME #830: Gross...copy-paste of above
  if configuration.key?("db2")

    config.vm.define "db2" do |db2|

      # Increase boot timeout for slower systems
      db2.vm.boot_timeout = 600

      hostname = 'meza-db2-' + box_os
      db2.vm.box = baseBox
      db2.vm.hostname = hostname
      ip_address = configuration["db2"]["ip_address"]

      db2.vm.network :private_network, ip: ip_address

      db2.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ['modifyvm', :id, '--cableconnected1', 'on']
        v.customize ["modifyvm", :id, "--memory", configuration["db2"]["memory"] ]
        v.customize ["modifyvm", :id, "--cpus", configuration["db2"]["cpus"] ]
        v.customize ["modifyvm", :id, "--name", mezaDirName + '-' + hostname + '-' + mezaInstallUnique]
      end

      # libvirt provider (Linux default - avoids KVM/VirtualBox conflict with Docker)
      db2.vm.provider :libvirt do |v|
        v.memory = configuration["db2"]["memory"]
        v.cpus = configuration["db2"]["cpus"]
        v.qemu_use_session = false
      end

      # Non-controlling server should not have meza
      db2.vm.synced_folder ".", "/vagrant", disabled: true

      # Transfer setup-minion-user.sh script to db2
      db2.vm.provision "file", source: "./src/scripts/ssh-users/setup-minion-user.sh", destination: "/tmp/minion.sh"
      db2.vm.provision "file", source: "./.vagrant/id_rsa.pub", destination: "/tmp/meza-ansible.id_rsa.pub"

      #
      # Setup SSH user and unsafe testing config
      #
      db2.vm.provision "minion-ssh", type: "shell", preserve_order: true, binary: true, inline: <<-SHELL
        if [ ! -f #{install_directory}/conf-meza/public/public.yml ]; then

          bash /tmp/minion.sh

          # Turn off host key checking for user meza-ansible, to avoid prompts
          echo "setup .ssh/config"
          bash -c 'echo -e "Host *\n   StrictHostKeyChecking no\n   UserKnownHostsFile=/dev/null" > #{install_directory}/conf-meza/users/meza-ansible/.ssh/config'
          sudo chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/config
          sudo chmod 600 #{install_directory}/conf-meza/users/meza-ansible/.ssh/config

          # Allow password auth
          echo "setup sshd_config password auth"
          sed -r -i 's/PasswordAuthentication no/PasswordAuthentication yes/g;' /etc/ssh/sshd_config
          systemctl restart sshd
        fi
      SHELL
    end

  end

  config.vm.define "app1", primary: true do |app1|

    # Increase boot timeout for slower systems or first-time box downloads
    app1.vm.boot_timeout = 600

    # Disable VirtualBox Guest Additions auto-update (VirtualBox provider only).
    # Guest Additions install correctly on first boot and don't need reinstalling.
    # If you need to update Guest Additions, run: vagrant vbguest --do install --no-cleanup
    # Guard with Vagrant.has_plugin? so this is safe even if vagrant-vbguest is absent
    # at parse time (pattern from mediawiki-vagrant)
    app1.vbguest.auto_update = false if !USING_LIBVIRT && Vagrant.has_plugin?('vagrant-vbguest')

    hostname = 'meza-app1-' + box_os
    app1.vm.box = baseBox
    app1.vm.hostname = hostname
    app1_ip_address = configuration["app1"]["ip_address"]

    # post_up_message is displayed after `vagrant up` completes - much more visible
    # than a shell provisioner whose output scrolls by during provisioning.
    # (pattern from mediawiki-vagrant)
    config.vm.post_up_message = <<~MSG

      Meza VM is ready. Next steps (copy/paste):

        vagrant ssh app1               # SSH into the VM
        sudo su - meza-ansible         # switch to the service account
        cd /opt/meza/config            # change to the config directory (shared with host)
        sudo meza deploy vagrant -vvv  # deploy (first run creates the demo wiki)

      Then browse:
        https://#{app1_ip_address}/demo

      When done:
        vagrant halt     # stop the VM (data preserved)
        vagrant destroy  # remove the VM and all its data

    MSG

    app1.vm.network :private_network, ip: app1_ip_address

    # Port forwarding for web access
    # This is NOT needed since the vm is on a private network at 192.168.56.56, but left here
    # for reference.
    # app1.vm.network "forwarded_port", guest: 443, host: 8443, host_ip: "127.0.0.1"

    app1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ['modifyvm', :id, '--cableconnected1', 'on']
      v.customize ["modifyvm", :id, "--memory", configuration["app1"]["memory"] ]
      v.customize ["modifyvm", :id, "--cpus", configuration["app1"]["cpus"] ]
      v.customize ["modifyvm", :id, "--name", mezaDirName + '-' + hostname + '-' + mezaInstallUnique]
      # Prevent GRUB timeout issues - boot automatically
      v.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
      v.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
      # Set graphics controller to VMSVGA to prevent flicker
      v.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
    end

    # libvirt provider (Linux default - avoids KVM/VirtualBox conflict with Docker Desktop).
    # Host prerequisites (Debian/Ubuntu):  apt install libvirt-dev libvirt-daemon-system qemu-kvm
    # Host prerequisites (RHEL/Rocky/Alma): dnf install libvirt-devel qemu-kvm
    # Then:                                 vagrant plugin install vagrant-libvirt
    # To override and use VirtualBox on Linux: VAGRANT_DEFAULT_PROVIDER=virtualbox vagrant up
    app1.vm.provider :libvirt do |v|
      v.memory = configuration["app1"]["memory"]
      v.cpus = configuration["app1"]["cpus"]
      v.machine_virtual_size = 40
      # Required on Fedora 30+ hosts to fix private networking (rhbz#1697773)
      # Pattern from mediawiki-vagrant
      v.qemu_use_session = false
    end

    # Disable default synced folder at /vagrant, instead put at /opt/meza
    app1.vm.synced_folder ".", "/vagrant", disabled: true

    if USING_LIBVIRT
      # NFS provides a persistent, bidirectional mount under libvirt — no need to run
      # `vagrant rsync-auto` in a separate terminal while developing.
      # Host prerequisites: nfs-kernel-server (Debian/Ubuntu) or nfs-utils (RHEL/Rocky/Alma)
      # vagrant-libvirt handles adding the NFS export and mounting on `vagrant up`.
      app1.vm.synced_folder ".", install_directory + "/meza",
        type: "nfs",
        nfs_udp: false
    elsif OS.windows?
      # On Windows, VirtualBox shared folders require explicit owner/group UID/GID.
      # meza-ansible and wheel are changed to UID/GID 10000 after they are created.
      # Use dmode=775 for directories, fmode=755 for files (allows execute bit)
      app1.vm.synced_folder ".", install_directory + "/meza", type: "virtualbox", owner: 10000, group: 10000, mount_options: ["dmode=775,fmode=755"]
    else
      # On Mac with VirtualBox, same approach.
      # Use dmode=775 for directories, fmode=755 for files (allows execute bit)
      app1.vm.synced_folder ".", install_directory + "/meza", type: "virtualbox", owner: 10000, group: 10000, mount_options: ["dmode=775,fmode=755"]
    end

    # Transfer keys to app1
    app1.vm.provision "file", source: "./.vagrant/id_rsa", destination: "/tmp/meza-ansible.id_rsa"
    app1.vm.provision "file", source: "./.vagrant/id_rsa.pub", destination: "/tmp/meza-ansible.id_rsa.pub"


    #
    # Bootstrap meza on the controlling VM
    # Note: getmeza.sh now installs Apache before creating meza-ansible user
    # to ensure apache group exists for group membership (Issue #287)
    #
    app1.vm.provision "getmeza", type: "shell", preserve_order: true, inline: <<-SHELL
    # for Vagrant, we'll export env var to avoid error in set-vars which runs before setup-env is run.
      export env=vagrant
      bash #{install_directory}/meza/src/scripts/getmeza.sh
      # Ensure SSH directory exists with correct permissions
      mkdir -p #{install_directory}/conf-meza/users/meza-ansible/.ssh
      chmod 700 #{install_directory}/conf-meza/users/meza-ansible/.ssh

      # Only move keys if they exist
      if [ -f /tmp/meza-ansible.id_rsa ]; then
        mv /tmp/meza-ansible.id_rsa #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa
        chmod 600 #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa
        chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa
      else
        echo "⚠ WARNING: /tmp/meza-ansible.id_rsa not found - SSH key not transferred"
      fi

      if [ -f /tmp/meza-ansible.id_rsa.pub ]; then
        mv /tmp/meza-ansible.id_rsa.pub #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa.pub
        chmod 644 #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa.pub
        chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa.pub

        # Add public key to authorized_keys
        cat #{install_directory}/conf-meza/users/meza-ansible/.ssh/id_rsa.pub >> #{install_directory}/conf-meza/users/meza-ansible/.ssh/authorized_keys
        chmod 600 #{install_directory}/conf-meza/users/meza-ansible/.ssh/authorized_keys
        chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/authorized_keys
      else
        echo "⚠ WARNING: /tmp/meza-ansible.id_rsa.pub not found - SSH key not transferred"
      fi

      # Create empty known_hosts file for Ansible roles that expect it
	  # This was failing on Vagrant dev infrastructure and is probably just covering up other issues. Investigate later.
      touch #{install_directory}/conf-meza/users/meza-ansible/.ssh/known_hosts
      chmod 644 #{install_directory}/conf-meza/users/meza-ansible/.ssh/known_hosts
      chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/known_hosts

      # Change meza-ansible UID and wheel GID to match mount ownership
      usermod -u 10000 meza-ansible
      groupmod -g 10000 wheel

      # Add meza-ansible to vboxsf group for shared folder access (VirtualBox only).
      # The vboxsf group does not exist under libvirt, so guard with getent.
      # Apache group membership and shell init files are handled by the meza-user
      # Ansible role during getmeza.sh or first deploy.
      getent group vboxsf > /dev/null 2>&1 && usermod -aG vboxsf meza-ansible || true

      # Ownership and permissions of #{install_directory}/meza are controlled by the
      # NFS server (libvirt) or by VirtualBox shared folder mount options above.
      # meza-ansible reads project sources via world-readable permissions set by
      # getmeza.sh (chmod a+r -R); no chown or chmod of the mount is needed here.

      # Verify user configuration
      echo "meza-ansible user configured"
      echo "  Groups: $(groups meza-ansible)"
      echo "  Home: $(getent passwd meza-ansible | cut -d: -f6)"
    SHELL

    #
    # Setup meza environment, either monolithic, with 2 app servers, and/or 2 db servers
    #
    envvars = {}
    if configuration.key?("app2") || configuration.key?("db2")
      envvars[:default_servers] = app1_ip_address
    end

    if configuration.key?("app2")
      envvars[:app_servers] = app1_ip_address + "," + configuration["app2"]["ip_address"]
    end

    if configuration.key?("db2")
      envvars[:db_master] = app1_ip_address
      envvars[:db_slaves] = configuration["db2"]["ip_address"]
    end

    # Create vagrant environment if it doesn't exist
    app1.vm.provision "setupenv", type: "shell", preserve_order: true, env: envvars, inline: <<-SHELL
      if [ ! -d #{install_directory}/conf-meza/secret/vagrant ]; then
        meza setup env vagrant --fqdn=#{app1_ip_address} --db_pass=1234 --private_net_zone=public
      fi
    SHELL

    #
    # Setup meza public config
    #
    app1.vm.provision "publicconfig", type: "shell", preserve_order: true, inline: <<-SHELL
      # Create public config dir if not exists
      [ -d #{install_directory}/conf-meza/public ] || mkdir #{install_directory}/conf-meza/public

      # If public config YAML file not present, create with defaults
      if [ ! -f #{install_directory}/conf-meza/public/public.yml ]; then
cat >#{install_directory}/conf-meza/public/public.yml <<EOL
---
blender_landing_page_title: Meza Wikis
m_setup_php_profiling: true
m_force_debug: true

sshd_config_UsePAM: "no"
sshd_config_PasswordAuthentication: "yes"
EOL
      fi

      # Make the vagrant environment configured for development
      echo 'm_opcache_production_mode: False' >> #{install_directory}/conf-meza/public/public.yml

      cat #{install_directory}/conf-meza/public/public.yml
    SHELL

    #
    # If multi-app: turn off hostkey checking
    #
    if configuration.key?("app2") || configuration.key?("db2")

      app1.vm.provision "keytransfer", type: "shell", preserve_order: true, inline: <<-SHELL

        # Turn off host key checking for user meza-ansible, to avoid prompts
        bash -c 'echo -e "Host *\n   StrictHostKeyChecking no\n   UserKnownHostsFile=/dev/null" > #{install_directory}/conf-meza/users/meza-ansible/.ssh/config'
        sudo chown meza-ansible:meza-ansible #{install_directory}/conf-meza/users/meza-ansible/.ssh/config
        sudo chmod 600 #{install_directory}/conf-meza/users/meza-ansible/.ssh/config

        # Allow SSH login
        # WARNING: This is INSECURE and for test environment only
        sed -r -i 's/UsePAM yes/UsePAM no/g;' /etc/ssh/sshd_config
        systemctl restart sshd

        # FIXME $818: Stuff below would be more secure if it worked

        # echo "switch user"
        # sudo su meza-ansible

        # Copy id_rsa.pub to each minion
        # sshpass -p 1234 ssh meza-ansible@INSERT_APP2_IP "echo \"$pubkey\" >> #{install_directory}/conf-meza/users/meza-ansible/.ssh/authorized_keys"

        # Remove password-based authentication for $ansible_user
        #echo "delete password"
        #ssh INSERT_APP2_IP "sudo passwd --delete meza-ansible"

        # Allow SSH login
        # WARNING: This is INSECURE and for test environment only
        # echo "setup sshd_config"
        # ssh INSERT_APP2_IP "sudo sed -r -i 's/UsePAM yes/UsePAM no/g;' /etc/ssh/sshd_config && sudo systemctl restart sshd"
      SHELL

      # else

      #
      # Finally: Deploy if not multi-server
      #
      # app1.vm.provision "deploy", type: "shell", preserve_order: true, inline: <<-SHELL
      #   meza deploy vagrant
      # SHELL
    end

  end

end
