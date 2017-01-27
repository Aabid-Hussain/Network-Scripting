import telnetlib
import os
import time
import getpass

Device_Ip = raw_input("Enter Remote Host IP: ")

Router_1 = telnetlib.Telnet(Device_Ip)

#use getpass.getpass() to prompt for password

Password_Logging = getpass.getpass(prompt='Enter Logging Password: ')

if Password_Logging:
    Router_1.read_until("Password:",3)
    Router_1.write(Password_Logging + "\n")

Router_1.read_until("R1>",2)
Router_1.write("enable"+"\n")

Password_Enable = getpass.getpass(prompt='Enter Enable Password: ')
if Password_Enable:
    Router_1.read_until("Password:",4)
    Router_1.write(Password_Enable + "\n")

Router_1.read_until("R1#",5)
Router_1.write("show ip interface brief"+ "\r\n")

Inter_Brief = Router_1.read_until("R1#",3)
Router_1.write("show running-config | section interface"+ "\r\n")
Router_1.write("show ip route"+ "\r\n")
Run_Conf = Router_1.read_until("R1#",5)
print Inter_Brief

print Run_Conf
Router_1.close()



