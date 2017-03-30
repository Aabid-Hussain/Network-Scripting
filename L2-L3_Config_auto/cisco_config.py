# cisco_config.py

def main():
	# initialize variables
	command_list = []
	newline = "\n"
	Loop_Life = True

	fa_port = []
	for i in range(1, 49):
		fa_port.append("0/" + str(i))
	
	while Loop_Life :
		# main menu
		print

		print "#        Cisco Configuration        #"
		print "# 1. Hostname                       #"
		print "# 2. Username and password          #"
		print "# 3. IP address and default gateway #"
		print "# 4. Interface                      #"
		print "# 5. Retrieve data                  #" 
		print "# 6. Show all commands              #"
		print "# 7. Apply configurations           #"
		print "# 8. Save configuration changes     #"
		print "# 9. Back to device selection       #"
		print "# 0. Exit                           #"

		
		main_choice = raw_input("Select: ")
		
		# config hostname
		if main_choice == '1':
			print
			hostname = raw_input("Enter hostname: ")
			
			command = "hostname " + str(hostname) + newline
			command_list.append(command)
			
		# config username & password
		elif main_choice == '2':
			print
			username = raw_input("Enter username: ")
			password = raw_input("Enter password: ")
			command = "username " + str(username) + " password " + str(password) + newline
			command_list.append(command)
		
		# config IP address and default-gateway
		elif main_choice == '3':
			print
			ip_addr = raw_input("Enter router/switch IP address (enter 'no' to disable): ")
			
			if ip_addr == "no":
				command = "no ip address" + newline
				
			else:
				subnet = raw_input("Enter subnet mask (255.255.255.0): ")
				command = "ip address %s %s" % (ip_addr, subnet) + newline
				
			command_list.append("interface VLAN1\n")
			command_list.append(command)
			command_list.append("exit\n")
			
			print 
			ip_addr = raw_input("Enter default gateway (enter 'no' to disable): ")
			
			if ip_addr == "no":
				command = "no ip default-gateway" + newline
				
			else:
				command = "ip default-gateway " + str(ip_addr) + newline
				
			command_list.append(command)
		
		
		# config interface
		elif main_choice == '4':
			# interface menu
			print
			print "Select interface"
			print "1. FastEthernet"
			print "2. GigabitEthernet"
			print "3. VLAN"
			print "0. Go back"
			int_choice = raw_input("Select: ")
			
			# config interface - FastEthernet
			if int_choice == '1':
				config_if = True
				print
				port = raw_input("Select FastEthernet port (0/1 - 0/48): ")
				
				# check port number
				if port in fa_port:
					print
					command = "interface FastEthernet" + str(port) + newline
					command_list.append(command)
					
					while config_if:
						print
						print "FastEthernet" + str(port)
						print "1. Description"
						print "2. VLAN"
						print "3. 'spanning-tree portfast'"
						print "0. Back to main menu"
						int_config_choice = raw_input("Select: ")
					
						if int_config_choice == '1':
							print
							description = raw_input("Enter description (enter 'no' to disable): ")
							
							if description == "no":
								command = "no description" + newline
							else:
								command = "description " + str(description) + newline
							command_list.append(command)
					
						elif int_config_choice == '2':
							print
							vlan = raw_input("Enter VLAN number (enter 'no' to disable): ")
							
							if vlan == "no":
								command = "no switchport access vlan" + newline
							else:
								command = "switchport access vlan " + str(vlan) + newline
							command_list.append(command)
						
						elif int_config_choice == '3':
							command = "spanning-tree portfast" + newline
							command_list.append(command)
							
						elif int_config_choice == '0':
							config_if = False
							command_list.append("exit\n")
							
							
				else:
					print
					print "Invalid port, recheck the port format"
			
			# config interface - GigabitEthernet
			elif int_choice == '2':
				config_if = True
				print 
				port = raw_input("Select GigabitEthernet port (0/1 - 0/2): ")
				
				# check port number
				if port == "0/1" or port == "0/2":
					print
					command = "interface GigabitEthernet" + str(port) + newline
					command_list.append(command)
					
					while config_if:
						print
						print "GigabitEthernet" + str(port)
						print "1. 'switchport trunk encapsulation dot1q'"
						print "2. 'switchport trunk native vlan'"
						print "3. 'switchport mode trunk'"
						print "0. Back to main menu"
						int_config_choice = raw_input("Select: ")
						
						if int_config_choice == '1':
							command = "switchport trunk encapsulation dot1q" + newline
							command_list.append(command)
							
						elif int_config_choice == '2':
							print 
							vlan = raw_input("Enter VLAN number: ")
							command = "switchport trunk native vlan " + str(vlan) + newline
							command_list.append(command)
							
						elif int_config_choice == '3':
							command = "switchport mode trunk" + newline
							command_list.append(command)
							
						elif int_config_choice == '0':
							config_if = False
							command_list.append("exit\n")
							
							
				else:
					print
					print "Invalid port"
					
			# config interface - VLAN
			elif int_choice == '3':
				config_if = True
				print
				vlan_num = raw_input("Select VLAN (1-1001): ")
				
				# check VLAN number
				if int(vlan_num) > 0 and int(vlan_num) < 1002:
					print
					command = "interface VLAN" + str(vlan_num) + newline
					command_list.append(command)
					
					while config_if:
						print
						print "VLAN" + str(vlan_num)
						print "1. IP address"
						print "2. 'no ip directed-broadcast'"
						print "3. 'no ip route-cache'"
						print "0. Back to main menu"
						int_config_choice = raw_input("Select: ")
						
						if int_config_choice == '1':
							print
							ip_addr = raw_input("Enter IP address (enter 'no' to disable): ")
							
							if ip_addr == "no":
								command = "no ip address" + newline
								
							else:
								subnet = raw_input("Enter subnet mask (255.255.255.0): ")
								command = "ip address %s %s" % (ip_addr, subnet) + newline
							
							command_list.append(command)
							
						elif int_config_choice == '2':
							command = "no ip directed-broadcast" + newline
							command_list.append(command)
							
						elif int_config_choice == '3':
							command = "no ip route-cache" + newline
							command_list.append(command)
							
						elif int_config_choice == '0':
							config_if = False
							command_list.append("exit\n")
							
							
				else:
					print
					print "Invalid VLAN"
						  
			# back to main menu
			elif int_choice == '0':
				pass
		
		
		elif main_choice == '5':
			print
			print "Select command"
			print "1. 'show version'"
			print "2. 'show show running-config'"
			print "3. 'show ip interface brief'"
			print "4. 'show vlan'"
			print "0. Back to main menu"
			show_choice = raw_input("Select: ")
			
			if show_choice == '1':
				return "show version" + newline
				
			elif show_choice == '2':
				return "show running-config" + newline
				
			elif show_choice == '3':
				return "show ip interface brief" + newline
				
			elif show_choice == '4':
				return "show vlan" + newline
				
			elif show_choice == '0':
				pass
		
		# show all commands
		elif main_choice == '6':
			print 
			print "Command list"
			
			if command_list != []:
				for command in command_list:
					print command
					
			else:
				print "[]"
			
		# apply configuration
		elif main_choice == '7':
			return command_list
			
		# save configuration
		elif main_choice == '8':
			print 
			print "Do you want to save configuration changes? (y/n)"
			choice = raw_input(": ")
			
			if choice == "y":
				return "copy running-config startup-config"
			else:
				pass
		
		# back to device selection - return 1
		elif main_choice == '9':
			return 1
			
		# exit program - return 0
		elif main_choice == '0':
			print
			print "Exit program"
			Loop_Life = False
			
			return 0
		  
			
		else:
			print "Invalid selection"	

		
if __name__ == "__main__":
	command_list = main()
	#print command_list