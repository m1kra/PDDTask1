#!/bin/bash
set -xe

source /vagrant/vars.env

sed -i '/master\|node/d' /etc/hosts

cat >> /etc/hosts << EOF
192.168.69.2 master
192.168.69.4 node1
192.168.69.8 node2
EOF

cat >> /home/vagrant/.ssh/config << EOF
Host *
   StrictHostKeyChecking no
   UserKnownHostsFile=/dev/null
EOF

mkdir $HDFS_DATA
chown -R vagrant:vagrant $HDFS_DATA

tar -xf $JAVA_ARCHIVE -C /opt
tar -xf $HADOOP_ARCHIVE -C /opt
tar -xf $SPARK_ARCHIVE -C /opt

chown -R vagrant:vagrant {$JAVA_HOME,$HADOOP_HOME,$SPARK_HOME,/tmp}


# commands below are roughly equivalent to (on box we use):
#	apt install -y python3-pip
#	pip3 install numpy
dpkg -i /vagrant/resources/archives/*
pip3 install /vagrant/resources/numpy-1.18.3-cp36-cp36m-manylinux1_x86_64.whl