#!/usr/bin/env bash

echo 'Start!'

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

cd /vagrant

sudo apt-get update
sudo apt-get install tree

# Install mysql8
if ! [ -e /vagrant/mysql-apt-config_0.8.15-1_all.deb ]; then
	wget -c https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb
fi

sudo dpkg -i mysql-apt-config_0.8.15-1_all.deb
sudo DEBIAN_FRONTEND=noninteractivate apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev

if [ ! -f "/usr/bin/pip" ]; then
  sudo apt-get install -y python3-pip
  sudo apt-get install -y python-setuptools
  sudo ln -s /usr/bin/pip3 /usr/bin/pip
else
  echo "pip3 already installed"
fi

# Upgrade pip, it has some issues
# python -m pip install --upgrade pip
## Incase there's issues reinstall pip
## Install pip dependencies
pip install --upgrade setuptools
pip install --ignore-installed wrapt
## Install the latest pip
pip install -U pip
# Install packages, ensure compatibility between all versions
pip install -r requirements.txt


# set mysql user root's password
# create a new database twitter
sudo mysql -u root << EOF
	ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY'cosmo';
	flush privileges;
	show databases;
	CREATE DATABASE IF NOT EXISTS twitter;
EOF
# fi


# if you want to go to /vagrant
# enter vagrant ssh
# enter manually
# enter ls -a
# enter vi .bashrc
# add cd /vagrant

echo 'All Done!'
