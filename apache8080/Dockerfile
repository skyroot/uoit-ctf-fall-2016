# UOIT CTF Fall 2016 - Apache Alt Service Dockerfile
# docker build -t "uoit-ctf-2016-apache8080" .
#
# Vulnerabilities:
# - Weak admin login (adama:lee)
# - Search sweetrice 1.5.1 on exploit-db.com
# - mysql running as root as well with \! enabled

FROM ubuntu:14.04
MAINTAINER G Hayes

RUN echo "America/Toronto" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

ENV DEBIAN_FRONTEND noninteractive

# Basic Environment Build
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get dist-upgrade -y
RUN apt-get install net-tools nano curl iputils-ping vim-runtime screen python -y

# OpenSSH
RUN apt-get install openssh-server -y
RUN mkdir /root/.ssh
RUN chmod 700 /root/.ssh
COPY pubkey /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config

# Apache2
RUN apt-get install apache2 php5-mysql php5 libapache2-mod-php5 php5-mcrypt -y
RUN apt-get install unzip -y
COPY sweetrice-1.5.1-configured.zip /var/www/html/
RUN unzip /var/www/html/sweetrice-1.5.1-configured.zip -d /var/www/html
RUN rm -rf /var/www/html/index.html
RUN rm -rf /var/www/html/sweetrice-1.5.1-configured.zip
RUN rm -rf /var/www/html/__MACOSX
RUN chown -R www-data:www-data /var/www/html
RUN sed -i 's/Listen 80/Listen 0.0.0.0:80/g' /etc/apache2/ports.conf

# MySQL
RUN apt-get install mysql-server mysql-client -y
RUN sed -i 's/= mysql/= root/g' /etc/mysql/my.cnf

COPY pubkey /root/.ssh/authorized_keys

# Start Script
RUN echo '#!/bin/bash' > /root/start.sh
RUN echo 'service rsyslog start' >> /root/start.sh
RUN echo 'service apache2 start' >> /root/start.sh
RUN echo 'service mysql start' >> /root/start.sh
RUN echo 'service ssh start' >> /root/start.sh
RUN echo 'mysql -u root -e "CREATE DATABASE sweetrice;"' >> /root/start.sh
RUN echo 'mysql -u root sweetrice < /var/www/html/db.sql' >> /root/start.sh
RUN echo 'bash' >> /root/start.sh
RUN chmod +x /root/start.sh

ENTRYPOINT ["/root/start.sh"]
