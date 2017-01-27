# Network-Scripting
This repository contains "Network Automation".

I have written telnet programm using "telnetlib" package. The telnetlib module provides a TELNET class that implements the Telnet protocol. 
Telnet objects are as follows:  
    1. Router_1.read_until(expected[,timeout]) - "Read until a given string, expected, is encountered or until timeout seconds have passed."
    2. Router_1.read_all() - "Read all data until EOF; block until connection closed."
    3. Router_1.close() - "Close the connection"
    4. Router_1.write(buffer) - "Write a string to the socket, This can block if the connection is blocked. socket.error can be used if the connection is closed. 
    
import getpass
import sys
import telnetlib
HOST = "localhost"
user = raw_input("Enter your remote account: ")
password = getpass.getpass()
tn = telnetlib.Telnet(HOST)
tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")
tn.write("ls\n")
tn.write("exit\n")
print tn.read_all()
    
