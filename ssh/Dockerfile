# UOIT CTF Fall 2016 - SSH Service Dockerfile
# docker build -t "uoit-ctf-2016-ssh" .
#
# Vulnerabilities - Gaining Access
# - Log in using adama:lee
#
# Vulnerabilities - Escalation:
# - /usr/sbin/service is SETUID
# - /bin/chown is SETUID
# - /bin/chmod is SETUID
# - /usr/bin/vi is SETUID
# - /bin/modifyme is SETUID, 766
# - 777 /etc/shadow
# - 777 /etc/ssh/sshd_config
# - 777 /etc/init.d/ssh
# - dns (tcp 53) bind shell as root


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

# Vulns
RUN useradd adama
RUN echo "adama:lee" | chpasswd
RUN mkdir /home/adama
RUN chown -R adama:adama /home/adama
RUN chmod 777 /etc/shadow
RUN chmod 777 /etc/init.d/ssh
RUN chmod 777 /etc/ssh/sshd_config
RUN touch /bin/modifyme
RUN chmod 766 /bin/modifyme
COPY dns /usr/bin/
RUN chmod +x /bin/modifyme
RUN chmod u+s /bin/modifyme
RUN chmod u+s /usr/bin/vi
RUN chmod u+s /usr/sbin/service
RUN chmod u+s /bin/chown
RUN chmod u+s /bin/chmod

COPY pubkey /root/.ssh/authorized_keys

# Start Script
RUN echo '#!/bin/bash' > /root/start.sh
RUN echo 'service rsyslog start' >> /root/start.sh
RUN echo 'service ssh start' >> /root/start.sh
RUN echo '/usr/bin/dns &' >> /root/start.sh
RUN echo 'bash' >> /root/start.sh
RUN chmod +x /root/start.sh

ENTRYPOINT ["/root/start.sh"]