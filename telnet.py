import telnetlib
import os
import time
import getpass

#take the input from user about host IP address
Device_Ip = raw_input("Enter Remote Host IP: ")

#used to telnet host
Router_1 = telnetlib.Telnet(Device_Ip)

#use getpass.getpass() to prompt for password
Password_Logging = getpass.getpass(prompt='Enter Logging Password: ')

# If Password_Logging is not empty that perform below operation
if Password_Logging:
    Router_1.read_until("Password:",3)
    Router_1.write(Password_Logging + "\n")
    Router_1.read_until("R1>",2)
    en = raw_input("Enter the Enable cmd: ")
    Router_1.write(en +"\n")
    time.sleep(20)
# If Password_Enable is not empty that perform below operation
Password_Enable = getpass.getpass(prompt='Enter Enable Password: ')
if Password_Enable:
    Router_1.read_until("Password:",4)
    Router_1.write(Password_Enable + "\n")
    Router_1.read_until("R1#",5)
    cmd = raw_input("Enter the command: ")
    Router_1.write(cmd + "\r\n")
    Inter_Brief = Router_1.read_until("R1#",3)
    Router_1.write("show running-config | section interface"+ "\r\n")
    Router_1.write("show ip route"+ "\r\n")
    Run_Conf = Router_1.read_until("R1#",5)
    print Inter_Brief
    print Run_Conf
print Router_1.read_all()
Router_1.close()



