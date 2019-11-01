import time
import subprocess
from Logger import Logger
from subprocess import Popen, PIPE
from threading import Timer
import shlex
import os
from WindowsCmdHelper import WindowsCmdHelper




class ADBDriver:
    def __init__(self, serial):
        self.serial = serial
        self.windows_helper = WindowsCmdHelper()

    def execute_command(self,command ):
        commandStatus = 0
        i = 0
        ## Try for upto 30 minutes; This time is to make sure we cover upgrade during reboot.
        while (commandStatus != 1 and i <= (10*60) ):
            try :
                if 'adb' not in command :
                    command = "adb -s " + self.serial +" " + command
                Logger.info("Running command : "+ command + " for "+ str(i)+" th time")
                ## Install takes longer time ##
                if "install" in command :
                    adb_output = self.windows_helper.run_cmd_with_timeout(command,2*60)
                else :
                    adb_output = self.windows_helper.run_cmd_with_timeout(command,1*60)
                Logger.info("command run successfully")
                if (adb_output is not None and len(str(adb_output)) > 0) :
                    Logger.info("ADB OUTPUT : "+ adb_output)
                    if "error: no devices/emulators found" in adb_output or "not found" in adb_output or "Permission Denial" in adb_output:
                        raise Exception( 'Device not connected')
                commandStatus = 1
                return adb_output
            except Exception as e:
                #print " ADB Command cannot be executed ", e
                if ('.' in self.serial):
                    try :
                        cmd = "adb connect "+self.serial
                        self.windows_helper.run_cmd_with_timeout(cmd,1*60)
                        cmd = "adb -s "+self.serial+" root"
                        self.windows_helper.run_cmd_with_timeout(cmd,1*60)
                        cmd = "adb connect "+self.serial
                        self.windows_helper.run_cmd_with_timeout(cmd,1*60)
                    except Exception:
                        Logger.error("Reconect failed. Trying again")                 
                self.windows_helper.run_cmd_with_timeout("timeout 1", 2)
            finally:
                i = i + 1