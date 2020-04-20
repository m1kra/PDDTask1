
Vagrant.configure("2") do |config|
    config.vm.box = "hashicorp/bionic64"

    config.vm.provision "shell", inline: "echo 'source /vagrant/vars.env' > /etc/profile.d/vars.sh"

    config.vm.provision "file", source: "provision/ssh/id_rsa", destination: "$HOME/.ssh/id_rsa"
    config.vm.provision "file", source: "provision/ssh/id_rsa.pub", destination: "$HOME/.ssh/id_rsa.pub"
    config.vm.provision "shell", privileged: false, inline:<<-END
        cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys &&
        chmod 600 .ssh/id_rsa
    END

    config.vm.provision "shell", path: "provision/install.sh"
    config.vm.provision "shell", path: "provision/setup_hadoop.sh"

    config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
    end

    config.vm.define "master" do |master|
        master.vm.hostname = "master"
        master.vm.network "private_network", ip: "192.168.69.2"
        master.vm.provision "shell", path: "provision/setup_spark.sh"
    end

    config.vm.define "node1" do |node1|
        node1.vm.hostname = "node1"
        node1.vm.network "private_network", ip: "192.168.69.4"
    end

    config.vm.define "node2" do |node2|
        node2.vm.hostname = "node2"
        node2.vm.network "private_network", ip: "192.168.69.8"
    end
end