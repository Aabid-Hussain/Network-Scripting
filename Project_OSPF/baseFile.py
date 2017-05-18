import re
import telnetlib


class deviceClass:
    deviceCount = 0

    def __init__(self):
        self.deviceCount += 1
        # pass


def createResource(dict1):
    div = deviceClass()
    for x in dict1.keys():
        setattr(div, x, dict1[x])
    return div


def readDutFile(filename):
    fileHeader = open(filename, 'r+')
    print "DUT file is opened\n"
    if not fileHeader:
        print "Error:Device file named {} error out".format(filename)
        return 0
    divDict = {}
    for line in fileHeader.readlines():
        print line
        match = re.search(r'(.*)=.*\"(.*)\"', line)
        if not match:
            print "Error"
            return 0
        key = match.group(1)
        value = match.group(2)
        divDict[key.strip()] = value.strip()
    Res = createResource(divDict)
    return Res


def telnetDevice(device, timeout = 2):
    print " Trying telnet to host =",device.device_IP
    telN = telnetlib.Telnet(device.device_IP)
    telN.set_debuglevel(0)

    telN.read_until("Username: ", timeout)
    telN.write(device.device_username)
    telN.read_until("Password: ", timeout)
    telN.write(device.device_password + "\n")

    telN.read_until(device.device_enable_prompt)
    telN.write("enable\n")
    telN.read_until("Password:")
    telN.write(device.device_enable_password + "\n")

    telN.read_until(device.device_prompt, timeout)
    telN.write("terminal length 0" + "\n")
    return telN


def sendCommand(device, command, prompt='',timeout = 2 ):
    dev = device.device_handler

    if not prompt:
        prompt = device.device_prompt
    dev.write(command)
    out = dev.read_until(prompt)
    return out


DUT = readDutFile("E:\\ME\\PythonLearningProg\\textfile\\DUT.txt")
handler = telnetDevice(DUT)
if handler:
    setattr(DUT, 'device_handler', handler)
    print "Successfully open DUT at {}".format(DUT.device_IP)
