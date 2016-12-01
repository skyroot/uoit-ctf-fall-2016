#!/bin/bash

# mmm, rootkit (hides the start.sh scripts from players)
insmod Rootkit/rootkit.ko

# kill old containers
for i in `docker ps -a | grep 'uoit-ctf-2016' | cut -d' ' -f1`; do docker rm -f "$i"; done

# run all services
docker run -itd -p 3306:3306 -p 42003:22 --name=uoit-ctf-2016-mysql -h mysql uoit-ctf-2016-mysql
sudo docker run -itd -p 22:22 -p 42001:22 --name=uoit-ctf-2016-ssh -h ssh uoit-ctf-2016-ssh
sudo docker run -itd -p 80:80 -p 42002:22 --name=uoit-ctf-2016-apache80 -h web uoit-ctf-2016-apache80
docker run -itd -p 4004:4004 -p 42004:22 --name=uoit-ctf-2016-chat -h chat --cap-add=NET_ADMIN --cap-add=NET_RAW uoit-ctf-2016-chat
docker run -itd -p 8080:80 -p 42005:22 --name=uoit-ctf-2016-apache8080 -h webalt uoit-ctf-2016-apache8080

# show status
docker ps
