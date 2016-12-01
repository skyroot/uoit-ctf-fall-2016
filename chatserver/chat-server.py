#!/usr/bin/env python
 
import socket
import thread
import time
import os
 
HOST = ""
PORT = 4004
 
def accept(conn):

    def threaded():
        while True:
            conn.send("\nWelcome to the Galactica ship chat server!\n")
            conn.send("Note: all usernames will be validated against the system\n")
            conn.send("Please enter your username: ")
            try:
                name = conn.recv(1024).strip()
            except socket.error:
                continue 
            if name in users:
                conn.send("Name entered is already in use.\n")
            elif name:
                cmd = "cat /etc/passwd | grep -q " + name
                namecheck = os.system(cmd)   
                if namecheck:  
                    conn.send("Invalid username.\n")
                else:
                    conn.send(name)
                    conn.setblocking(False)
                    users[name] = conn
                    broadcast(name, "+++ %s arrived +++" % name)
                    break
    thread.start_new_thread(threaded, ())
 
def broadcast(name, message):
    """
    Send a message to all users from the given name.
    """
    print message
    for to_name, conn in users.items():
        if to_name != name:
            try:
                conn.send(message + "\n")
            except socket.error:
                pass

# check if root
if os.geteuid() != 0:
    exit("You need to have root privileges to run this program. Exiting.")

# Set up the server socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(False)
server.bind((HOST, PORT))
server.listen(1)
print "Listening on %s" % ("%s:%s" % server.getsockname())
 
# Main event loop.
users = {}
while True:
    try:
        # Accept new connections.
        while True:
            try:
                conn, addr = server.accept()
            except socket.error:
                break
            accept(conn)
        # Read from connections.
        for name, conn in users.items():
            try:
                message = conn.recv(1024)
            except socket.error:
                continue
            if not message:
                # Empty string is given on disconnect.
                del users[name]
                broadcast(name, "--- %s leaves ---" % name)
            else:
                broadcast(name, "%s> %s" % (name, message.strip()))
        time.sleep(.1)
    except (SystemExit, KeyboardInterrupt):
        break