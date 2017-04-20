import logging
import re
import telnetlib

class deviceClass:
    deviceCount=0
    def __init__(self):
        deviceClass.deviceCount +=1
        pass


def createResource(dict):
    div =deviceClass()
    for x in dict.key():
        setattr(div,x,dict[x])
    return div


def readDutFile(filename):
    fileHeader = open(filename,'r+')
    print "DUT file is opened\n"
    if not fileHeader:
        print "Error:Device file named \" %s \" error out" %filename
        return 0
    divDict = {}
    for line in fileHeader.readlines():
        print line
        match = re.search(r'(.*)=.*\"(.*)\"',line)
        if not match:
            print "Error"
            return 0
        key = match.group(1)
        value=match.group(2)
        divDict[key.strip()]= value.strip()
    Res = createResource(divDict)
    return Res


def telnetDevice(device):
    telN = telnetlib.Telnet(device.device_IP)
    telN.read_until("Username:")
    telN.write(device.device_username)
    telN.read_until("Password:")
    telN.write(device.device_password + "\n")
    telN.read_until(device.device_enable_prompt)
    telN.write("enable\n")
    telN.read_until("Password:")
    telN.write(device.device_enable_password + "\n")
    telN.read_until(device.device_prompt)
    telN.write("terminal length 0" + "\n")
    return telN

readDutFile("E:\ME\Github_Network-Scripting\File_Loc\DUT.txt")