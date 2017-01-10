#!/usr/bin/env bash
#set -xe
apt-get update
apt-get install -y python-pip python3-pip
apt-get install -y python-virtualenv libcups2-dev build-essential libssl-dev libssh-dev libssh2-1-dev libssh2-1 libffi-dev python-dev python3-dev libffi-dev redis-server openjdk-7-jdk
sudo pip install jinja2

if [ ! -d "/usr/java/" ]; then
  sudo mkdir /usr/java/
fi

if [ ! -f "/usr/java/jdk-8u111-linux-x64.tar.gz" ]; then
  sudo wget -nv -P /usr/java/ --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.tar.gz"
  sudo tar -xvzf /usr/java/jdk-8u111-linux-x64.tar.gz -C /usr/java/
fi

if [ ! -f "/home/vagrant/hadoop-2.7.3.tar.gz" ]; then
  sudo wget -nv /home/vagrant/ "http://apache.volia.net/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz"
  sudo tar -xvzf /home/vagrant/hadoop-2.7.3.tar.gz
fi

if [ ! -f "/home/vagrant/spark-2.1.0-bin-hadoop2.7.tgz" ]; then
  sudo wget -nv /home/vagrant/ "http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz"
  sudo tar -xvzf /home/vagrant/spark-2.1.0-bin-hadoop2.7.tgz
fi

cp -R -f /vagrant/hadoop_configs/. /home/vagrant/hadoop-2.7.3/etc/hadoop

\cp /vagrant/.profile /home/vagrant/.profile
echo -e "\tStrictHostKeyChecking no" >> /etc/ssh/ssh_config
ssh-keygen -f key.rsa -t rsa -N ''
ssh-add key.rsa
cat /vagrant/key.rsa.pub >> /home/vagrant/.ssh/authorized_keys
cat /home/vagrant/key.rsa.pub >> /home/vagrant/.ssh/authorized_keys
#cat /vagrant/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
ssh-keyscan -H vagrant,192.168.1.23 >> /home/vagrant/.ssh/known_hosts
ssh-keyscan -H vagrant,192.168.1.24 >> /home/vagrant/.ssh/known_hosts
sudo chown -R -v vagrant /home/vagrant/

python2.7 /vagrant/hadoop_xml.py
#sudo cp /vagrant/hadoop_unit /etc/systemd/system/
#systemctl start SetupHadoopSettings

export JAVA_HOME=/usr/java/jdk1.8.0_111
export HADOOP_INSTALL=/home/vagrant/hadoop-2.7.3
export PATH=$PATH:$HADOOP_INSTALL/bin
export PATH=$PATH:$HADOOP_INSTALL/sbin
export HADOOP_MAPRED_HOME=$HADOOP_INSTALL
export HADOOP_COMMON_HOME=$HADOOP_INSTALL
export HADOOP_HDFS_HOME=$HADOOP_INSTALL
export YARN_HOME=$HADOOP_INSTALL
export HADOOP_HOME=$HADOOP_INSTALL
export HADOOP_CONF_DIR=${HADOOP_HOME}"/etc/hadoop"

#$(cd /home/vagrant/worker1/ && vagrant up --provision)
#$(cd /home/vagrant/worker2/ && vagrant up --provision)

#cat /sbin/ifconfig eth1 | grep "inet addr:" | awk -F' ' '{print $2} ' | awk -F ':' '{print $2}' >> /home/vagrant/hadoop-2.7.3/etc/hadoop/slaves