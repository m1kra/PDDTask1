#!/bin/bash
set -xe
source /vagrant/vars.env

echo "spark.master  yarn" >> $SPARK_HOME/conf/spark-defaults.conf

cat >$SPARK_HOME/conf/spark-env.sh <<EOF 
export PYSPARK_PYTHON=python3
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export YARN_CONF_DIR=$HADOOP_CONF_DIR
EOF