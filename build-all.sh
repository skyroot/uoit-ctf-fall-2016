#!/bin/bash
# NOTE: you must add a public key in the root directory in order to SSH into all services!
cp pubkey ./apache80/pubkey
cp pubkey ./apache8080/pubkey
cp pubkey ./chatserver/pubkey
cp pubkey ./mysql/pubkey
cp pubkey ./ssh/pubkey
docker build -t "uoit-ctf-2016-apache80" ./apache80/
docker build -t "uoit-ctf-2016-apache8080" ./apache8080/
docker build -t "uoit-ctf-2016-chat" ./chatserver
docker build -t "uoit-ctf-2016-mysql" ./mysql/
docker build -t "uoit-ctf-2016-ssh" ./ssh/