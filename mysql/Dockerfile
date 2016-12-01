# UOIT CTF Fall 2016 - MySQL Service Dockerfile
# docker build -t "uoit-ctf-2016-mysql" .
#
# Vulnerabilities - Gaining Access:
# - Log in using adama:lee
#
# Vulnerabilities - Escalation
# - Runs as root
# - Remote root login, adama login
# - Command exec with \!, sys_exec, sys_eval, sys_get, sys_set
# - SUID on kill, killall, service
# - SGID on kill.bak

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

# MySQL
RUN apt-get install mysql-server mysql-client -y
RUN sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf
RUN sed -i 's/= mysql/= root/g' /etc/mysql/my.cnf

# OpenSSH
RUN apt-get install openssh-server -y
RUN mkdir /root/.ssh
RUN chmod 700 /root/.ssh
COPY pubkey /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config

# Vulns
COPY lib_mysqludf_sys.so /usr/lib/mysql/plugin/
RUN sed -i "s/skip-external-locking/skip-external-locking\nsecure-file-priv = ''/g" /etc/mysql/my.cnf
RUN cp /bin/kill /bin/kill.bak
RUN chmod g+s /bin/kill.bak
RUN chmod u+s /bin/kill
RUN chmod u+s /usr/bin/killall
RUN chmod u+s /usr/sbin/service
RUN chown -R mysql:mysql /var/lib/mysql

COPY pubkey /root/.ssh/authorized_keys

# Start Script
RUN echo '#!/bin/bash' > /root/start.sh
RUN echo 'service mysql start' >> /root/start.sh
#RUN echo 'mysqladmin -u root password password' >> /root/start.sh
RUN echo "mysql -u root  -e \"CREATE USER 'adama'@'localhost' IDENTIFIED BY 'lee';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"CREATE USER 'adama'@'%' IDENTIFIED BY 'lee';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"GRANT ALL ON *.* TO 'adama'@'localhost';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"GRANT ALL ON *.* TO 'adama'@'%';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"GRANT ALL ON *.* TO 'root'@'localhost';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"GRANT ALL ON *.* TO 'root'@'%';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"CREATE FUNCTION sys_exec RETURNS int SONAME 'lib_mysqludf_sys.so';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"CREATE FUNCTION sys_eval RETURNS string SONAME 'lib_mysqludf_sys.so';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"CREATE FUNCTION sys_set RETURNS int SONAME 'lib_mysqludf_sys.so';\"" >> /root/start.sh
RUN echo "mysql -u root  -e \"CREATE FUNCTION sys_get RETURNS string SONAME 'lib_mysqludf_sys.so';\"" >> /root/start.sh
RUN echo "sleep 5"
RUN echo 'service rsyslog start' >> /root/start.sh
RUN echo 'service ssh start' >> /root/start.sh
RUN echo 'bash' >> /root/start.sh
RUN chmod +x /root/start.sh

EXPOSE 3306
ENTRYPOINT ["/root/start.sh"]