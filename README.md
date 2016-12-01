UOIT CTF 2016
===========

This is a dockerized version of UOIT's Fall 2016 CTF (attack and defence style). 


Services
--

- SSH on port 22

- Apache on port 80

- MySQL on port 3306

- A custom chat server on port 4004

- Apache (alt) on port 8080


Run
--

Assuming you already have docker installed:
```
git clone https://github.com/ghayes-uoit/uoit-ctf-fall-2016.git
cd uoit-ctf-fall-2016
```

Copy existing team public key to the root directory for the build phase:
```
cp ~/team_rsa.pub pubkey
```

Build all Docker containers:
```
chmod +x build-all.sh
./build-all.sh
```

Run all exploitable services using the generated Docker containers (will prompt for sudo access):
```
chmod +x run-all.sh
./run-all.sh
```

Load the rootkit module to hide the start.sh scripts in each container.
DANGER: This should be done only if you are running a CTF, not when you're using the services locally! This will make your server vulnerable.
```
insmod rootkit/Diamorphine/rootkit.ko
```

Uninstall the rootkit:
```
kill -63 0
rmmod rootkit
```

