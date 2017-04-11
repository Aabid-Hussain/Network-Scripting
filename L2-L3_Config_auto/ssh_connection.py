#test-ssh.py

import paramiko
import time

def disable_paging(remote_conn):
	#'''Disable paging'''
	remote_conn.send("terminal length 0\n")
	time.sleep(1)
	
	#Clear the buffer on the screen
	output = remote_conn.recv(1000)
	
	return output
	
	
#if __name == '__main__':
if True:
	#VARIABLES THAT NEED CHANGED
	ip = 'x.x.x.x'
	username = 'aabid'
	password = 'xxxxxxx'
	#Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()
	
	#Automatically add untrusted hosts 
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
	#initiate SSH connection
	remote_conn_pre.connect(ip, username = username, password = password)
	print "SSH connection established to %s" %ip
	
	#Use invoke_shell to establish an 'inactive session'
	remote_conn = remote_conn_pre.invoke_shell()
	print "Inactive SSH session established"
	
	#strip the initial prompt
	output = remote_conn.recv(1000)
	#See what we have
	print output
	#Turn off paging
	disable_paging(remote_conn)
	#Send command
	remote_conn.send("\n")
	remote_conn.send("ifconfig -a\n")
	
	#Wait for the command complete
	time.sleep(2)
	
	output = remote_conn.recv(5000)
	print output
	
	
