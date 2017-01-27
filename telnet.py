import telnetlib
import os
import time

Device_Ip = "172.26.106.50"

Router_1 = telnetlib.Telnet(Device_Ip)

Router_1.read_until("Password:",3)
Router_1.write("Cisco"+"\n")

Router_1.read_until("R1>",2)
Router_1.write("enable"+"\n")

Router_1.read_until("Password:",4)
Router_1.write("Cisco"+"\n")

Router_1.read_until("R1#",5)
Router_1.write("show ip interface brief"+ "\r\n")

Inter_Brief = Router_1.read_until("R1#",3)
Router_1.write("show running-config | section interface"+ "\r\n")
Router_1.write("show ip route"+ "\r\n")
Run_Conf = Router_1.read_until("R1#",5)
print Inter_Brief

print Run_Conf
Router_1.close()



