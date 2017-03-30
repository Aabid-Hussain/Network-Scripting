#A program to configure RipV2 on cisco router

import re
import telnetlib
import getpass

fob = open("E:\ME\Github_Network-Scripting\File_Loc\DUT.txt", "r+")


class RESOURCE:
    count =0
    def __init__(self):
        RESOURCE.count +=1


def create_resource(info):
    div = RESOURCE()
    for x in info.keys():
        setattr(div,x,info[x])
    return div


def Device_Details(file_info):
   # div = RESOURCE()
    Device_Info = {}
    fob = open(file_info,"r+")
    for lines in fob.readlines():
        RegEx = r'(.*)=.*\"(.*)\"'
        matches = re.search(RegEx,lines)
        if matches:
            key = matches.group(1)
            value = matches.group(2)
            Device_Info[key.strip()]=value.strip()
    res = create_resource(Device_Info)
   #for i in Device_Info.keys():
    #    setattr(div,i,Device_Info[i])
    return res


fob.close()