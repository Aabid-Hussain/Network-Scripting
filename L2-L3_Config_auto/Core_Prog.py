# main_program.py

import time

import telnet_connection as telnet
import Device_Config as config
import Read_Excel_File as excel


class NetworkDevice(object):
	'''
	Container for network device attributes
	'''
	def __init__(self, name = '', ip = '', username = '', telnet_password = '', enable_password = ''):
		self.name = name
		self.ip = ip
		self.username = username
		self.telnet_password = telnet_password
		self.enable_password = enable_password
		self.output = ''
		
	def get_name_and_ip(self):
		return "Name: %s,\tIP: %s" % (self.name, self.ip)


def telnet_main(device, command_list):
	'''
	Process show version using telnet
	'''

	test_device = NetworkDevice(device.ip, device.username, device.telnet_password, device.enable_password)

	remote_conn = telnet.establish_connection(device.ip, device.username, device.telnet_password)

	telnet.disable_paging(remote_conn)
	
	if type(command_list) is str:
	
		if command_list == "show version\n":
			remote_conn.write(command_list)
			time.sleep(2)
		
		else:
			telnet.enter_enable_mode(remote_conn, enable_password)
			remote_conn.write(command_list)
			time.sleep(2)
		
	elif type(command_list) is list:

		# enter enable mode
		telnet.enter_enable_mode(remote_conn, enable_password)
	
		# enter config mode
		telnet.enter_config_mode(remote_conn)
		test_device.output = remote_conn.read_until("CNTL/Z.", 6)
	
		# send commands from command_list to a switch
		print "Applying configuration..."
		for command in command_list:
			remote_conn.write(command)
			time.sleep(1)
		
		
	# read output
	test_device.output = remote_conn.read_very_eager()
	
	print test_device.output

	remote_conn.close()


def switch_list(workbook_name):
	info_list = []
	worksheet = excel.open_excel_file(workbook_name)
	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = -1
	while curr_row < num_rows:
		curr_row += 1
		row = worksheet.row(curr_row)
		curr_cell = -1
		while curr_cell < num_cells:
			curr_cell += 1
			# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
			cell_type = worksheet.cell_type(curr_row, curr_cell)
			cell_value = worksheet.cell_value(curr_row, curr_cell)
			
			if curr_row > 0:
				info_list.append(str(cell_value))
				
				
	return info_list			
	
def main():
	'''
	Run an interactive config program and
	Login to a network device (using telnet)
	'''
	running = True
	
	info_list = switch_list("switch_list.xlsx")
	devices = [NetworkDevice() for i in range(len(info_list) / 5)]
	
	for device in devices:
		device.name = info_list.pop(0)
		device.ip = info_list.pop(0)
		device.username = info_list.pop(0)
		device.telnet_password = info_list.pop(0)
		device.enable_password = info_list.pop(0)
	
	
	while running:
		print 
		print "Network Devices List"
		
		i = 0
		for device in devices:
			i += 1
			print str(i) + ". " + device.get_name_and_ip()
			
		device_choice = raw_input("Select device: ")
		
		# i is a number of devices
		if int(device_choice) > 0 and int(device_choice) <= i:
		
			print
			print devices[int(device_choice) - 1].get_name_and_ip()
			
			command_list = config.main()
		
			# exit program
			if command_list == 0:
				running = False
			
			# go back to device selection
			elif command_list == 1:
				pass
			
			# send command
			elif command_list != []:
				print
				print "Using telnet:"
				telnet_main(devices[int(device_choice) - 1], command_list)
				
		else:
			print
			print "Invalid choice"


if __name__ == "__main__":
	main()