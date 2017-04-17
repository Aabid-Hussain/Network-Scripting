# Pynet
import paramiko
import getpass
import time
import sys
import re

''' Logic is required to add Regular Express for validation of IP addresses'''

# Define helper functions
def ip_valid(ip_addr):
	valid_ip = True

	# Make sure IP has four octets
	octets = ip_addr.split('.')
	if len(octets) != 4:
		sys.exit("\n\nInvalid IP address: %s\n" % ip_addr)

	# convert octet from string to int
	for i,octet in enumerate(octets):

		try:
			octets[i] = int(octet)
		except ValueError:
			# couldn't convert octet to an integer
			sys.exit("\n\nInvalid IP address: %s\n" % ip_addr)
	# map variables to elements of octets list
	first_octet, second_octet, third_octet, fourth_octet = octets

	# Check first_octet meets conditions
	if first_octet < 1:
		valid_ip = False
	elif first_octet > 223:
		valid_ip = False
	elif first_octet == 127:
		valid_ip = False

	# Check 169.254.X.X condition
	if first_octet == 169 and second_octet == 254:
		print "Address is part of APIPA-Automatic Private IP Address"
		valid_ip = False

	# Check 2nd - 4th octets
	for octet in (second_octet, third_octet, fourth_octet):
		if (octet < 0) or (octet > 255):
			valid_ip = False
	
	return valid_ip
	
	
def open_config_file(filename):
	# Open configuration file, mode: read-only
	f = open(filename, "r")
	
	config = ""
	for line in f:
		if line[0] == "!":
			continue
		elif "version" in line:
			continue
		else:
			config += str(line)

	return config	
		
			
def disable_paging(remote_conn):
	remote_conn.send("terminal length 0\n")
	time.sleep(1)
	
	# Clear the buffer on the screen
	output = remote_conn.recv(1000)
	
	return output

	
# Define main function	
def run(ip, username, password, config):
	# Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()
	
	# Automatically add untrusted hosts 
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "Connecting..."
	
	# Initiate SSH connection
	remote_conn_pre.connect(ip, username = username, password = password)
	print "SSH connection established to %s" %ip
	
	# Use invoke_shell to establish an 'inactive session'
	remote_conn = remote_conn_pre.invoke_shell()
	print "Inactive SSH session established"
	
	# Strip the initial prompt
	output = remote_conn.recv(1000)
	
	# See what we have
	print output
	
	# Turn off paging
	disable_paging(remote_conn)
	
	# Send command
	config_lines = config.split("\n")
	for command_line in config_lines:
		remote_conn.send(command_line)
	
	# Wait for the command complete
	time.sleep(2)
	
	output = remote_conn.recv(5000)
	print output


# IP address and authentication information
ip_addr = raw_input("Please enter an IP address: ")

# Check if IP address is valid
if ip_valid(ip_addr):
	username = raw_input("Username: ")
	password = getpass.getpass()
	#add a Cisco configuration file in the same folder
	config = open_config_file("Config-Cisco controller.cfg")

	run(ip_addr, username, password, config)
else:
	print "\n\nInvalid IP address: %s\n" % ip_addr
