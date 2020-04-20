#!/bin/bash
set -xe

source /vagrant/vars.env

cat <<EOF > ${HADOOP_CONF_DIR}/slaves
node1
node2
EOF

echo Editing $HADOOP_CONF_DIR/hadoop-env.sh
sed -i -e "s|^export JAVA_HOME=\${JAVA_HOME}|export JAVA_HOME=$JAVA_HOME|g" ${HADOOP_CONF_DIR}/hadoop-env.sh

cat <<EOF > ${HADOOP_CONF_DIR}/core-site.xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://${HADOOP_NAMENODE}:9000</value>
    <description>NameNode URI</description>
  </property>
  <property>
   <name>fs.default.name</name>
   <value>hdfs://${HADOOP_NAMENODE}:9000/</value>
</property>
</configuration>
EOF

cat <<EOF > ${HADOOP_CONF_DIR}/hdfs-site.xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>

  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file://${HDFS_DATA}/datanode</value>
    <description>Comma separated list of paths on the local filesystem of a DataNode where it should store its blocks.</description>
  </property>
 
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file://${HDFS_DATA}/namenode</value>
    <description>Path on the local filesystem where the NameNode stores the namespace and transaction logs persistently.</description>
  </property>

  <property>
    <name>dfs.namenode.datanode.registration.ip-hostname-check</name>
    <value>false</value>
    <description>http://log.rowanto.com/why-datanode-is-denied-communication-with-namenode/</description>
  </property>
</configuration>
EOF


cat <<EOF > ${HADOOP_CONF_DIR}/mapred-site.xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
EOF


cat <<EOF > ${HADOOP_CONF_DIR}/yarn-site.xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>${HADOOP_NAMENODE}</value>
    </property>
    <property>
        <name>yarn.nodemanager.pmem-check-enabled</name>
        <value>false</value>
    </property>
    <property>
        <name>yarn.nodemanager.vmem-check-enabled</name>
        <value>false</value>
    </property>
</configuration>
EOF

# TODO: added pmem in yarn-site (drugie od końca); added memory in mapred-site (ostatnie 4)

# cat <<EOF > ${HADOOP_CONF_DIR}/mapred-site.xml
# <configuration>
#     <property>
#         <name>mapreduce.framework.name</name>
#         <value>yarn</value>
#     </property>
#     <property>
#         <name>mapreduce.map.java.opts</name>
#         <value>-Xmx1792m</value>
#     </property>
#     <property>
#         <name>yarn.app.mapreduce.am.resource.mb</name>
#         <value>1920</value>
#     </property>
#     <property>
#         <name>mapreduce.map.memory.mb</name>
#         <value>960</value>
#     </property>
#     <property>
#         <name>mapreduce.reduce.memory.mb</name>
#         <value>960</value>
#     </property>
# </configuration>
# EOF


# cat <<EOF > ${HADOOP_CONF_DIR}/yarn-site.xml
# <configuration>
#     <property>
#         <name>yarn.nodemanager.aux-services</name>
#         <value>mapreduce_shuffle</value>
#     </property>
#     <property>
#         <name>yarn.resourcemanager.hostname</name>
#         <value>${HADOOP_NAMENODE}</value>
#     </property>
#       <property>
#       <name>yarn.nodemanager.resource.memory-mb</name>
#       <value>1920</value>
#     </property>
#     <property>
#       <name>yarn.scheduler.maximum-allocation-mb</name>
#       <value>1920</value>
#       <description>Max RAM-per-container</description>
#    </property>
#     <property>
#         <name>yarn.nodemanager.pmem-check-enabled</name>
#         <value>false</value>
#     </property>
#     <property>
#         <name>yarn.nodemanager.vmem-check-enabled</name>
#         <value>false</value>
#     </property>
# </configuration>
# EOF