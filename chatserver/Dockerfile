# UOIT CTF Fall 2016 - Chat Service Dockerfile
# docker build -t "uoit-ctf-2016-chat" .
#
# Vulnerabilities - Gaining Access
# - Log in remotely as a system user (no password required)
#
# Vulnerabilities - Escalation:
# - Chat server runs as root only and has command injection in the username field... GG
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

# Chat Server
COPY chat-server /root/

# OpenSSH
RUN apt-get install openssh-server -y
RUN mkdir /root/.ssh
RUN chmod 700 /root/.ssh
COPY pubkey /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config

# Vulns
RUN echo "root:password" | chpasswd
RUN useradd adama; useradd apollo; useradd athena; useradd baltar; useradd cain
RUN apt-get install iptables -y

COPY pubkey /root/.ssh/authorized_keys

# Start Script
RUN echo '#!/bin/bash' > /root/start.sh
RUN echo 'service rsyslog start' >> /root/start.sh
RUN echo 'python /root/chat-server &' >> /root/start.sh
RUN echo 'service ssh start' >> /root/start.sh
RUN echo 'bash' >> /root/start.sh
RUN chmod +x /root/start.sh

ENTRYPOINT ["/root/start.sh"]