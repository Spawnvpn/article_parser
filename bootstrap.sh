#!/usr/bin/env bash
#set -xe
apt-get update
apt-get install -y python-pip python3-pip
apt-get install -y python-virtualenv libcups2-dev build-essential libssl-dev libssh-dev libssh2-1-dev libcurl4-openssl-dev libssh2-1 libffi-dev python-dev python3-dev libffi-dev libpq-dev libxslt1-dev libxml2-dev libz-dev redis-server postgresql postgresql-contrib openjdk-7-jdk nginx
sudo pip install virtualenv
sudo pip install uwsgi
sudo pip install jinja2

apt-get install -y supervisor

/usr/bin/python2.7 -m virtualenv /vagrant/.env
/vagrant/.env/bin/pip install -r /vagrant/requirements.txt

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
cat /home/vagrant/key.rsa.pub >> /home/vagrant/.ssh/authorized_keys
cp /home/vagrant/key.rsa.pub /vagrant/vagrant_worker1
cp /home/vagrant/key.rsa.pub /vagrant/vagrant_worker2
#cat /vagrant/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
ssh-keyscan -H vagrant,192.168.1.23 >> /home/vagrant/.ssh/known_hosts
sudo chown -R -v vagrant /home/vagrant/

python2.7 /vagrant/hadoop_xml.py
#sudo cp /vagrant/hadoop_unit /etc/systemd/system/
#systemctl start SetupHadoopSettings

su vagrant -c '/home/vagrant/hadoop-2.7.3/bin/hdfs namenode -format'

export PGPASSWORD='admin'

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

sudo -E su postgres -c "psql -f /vagrant/postgre_conf.sql"

/vagrant/.env/bin/python /vagrant/manage.py makemigrations
/vagrant/.env/bin/python /vagrant/manage.py migrate

#cat /sbin/ifconfig eth1 | grep "inet addr:" | awk -F' ' '{print $2} ' | awk -F ':' '{print $2}' >> /home/vagrant/hadoop-2.7.3/etc/hadoop/slaves
#cat /home/vagrant/workers-address >> /home/vagrant/hadoop-2.7.3/etc/hadoop/slaves
su vagrant -c '/home/vagrant/hadoop-2.7.3/sbin/start-dfs.sh'
su vagrant -c '/home/vagrant/hadoop-2.7.3/sbin/start-yarn.sh'
cp /vagrant/streaming.py /home/vagrant/spark-2.1.0-bin-hadoop2.7/
cp /vagrant/streaming.py /home/vagrant/hadoop-2.7.3/
cd /home/vagrant/spark-2.1.0-bin-hadoop2.7/
su vagrant -c 'bin/spark-submit --deploy-mode cluster --master yarn streaming.py'
source /vagrant/.env/bin/activate
cd /vagrant/article_bot/spiders/
su vagrant -c 'scrapy runspider article_spider.py'
