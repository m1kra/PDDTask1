#!/bin/bash
source /vagrant/vars.env

rm -fr /tmp/*
rm -fr $HDFS_DATA/*
mkdir $HDFS_DATA/namenode
mkdir $HDFS_DATA/datanode
echo 'Y' | hdfs namenode -format
