import time
import subprocess
from Logger import Logger
from ADBDriver import ADBDriver
from threading import Thread
from enums import ADBCommands
import dateutil.parser as dateParser
from datetime import datetime
from collections import OrderedDict
from WindowsCmdHelper import WindowsCmdHelper


class CPUDataCollector(Thread):

    def __init__(self,serial):
        super(CPUDataCollector, self).__init__()
        #super(Thread, self).__init__()
        self.daemon = True
        self.adb_driver = ADBDriver(serial)
        self._is_running = True
        self.cpu_data = OrderedDict()
        self.native_heap_data = OrderedDict()
        self.windows_helper = WindowsCmdHelper()

    def run(self):
        while self._is_running:    
                try :
                    Logger.info ("Getting cpu data")
                    adb_output_cpu = self.adb_driver.execute_command(ADBCommands.cpuInfoCommand)
                    #   eg data 
                    # 24803 u0_a47   16  -4   3% S   135 1488352K 335276K  fg com.microsoft.skype.teams.ipphone
                    if (adb_output_cpu is not None):                    
                        
                        if (len(adb_output_cpu) > 1):
                            split_words = adb_output_cpu.split()
                            ## Find % in word ; -1 to skip %##
                            currentCpu= [s for s in split_words if "%" in s][0][:-1]
                            currentCpu = float(currentCpu)
                            if (currentCpu >= 0.0 and currentCpu <= 100.0):                                
                                adb_output = self.adb_driver.execute_command(ADBCommands.dateCommand)
                                datetime_object = dateParser.parse(adb_output.strip())
                                datetime_object = datetime_object.strftime("%m-%d %H:%M:%S")
                                datetime_object = (datetime.strptime(datetime_object,"%m-%d %H:%M:%S"))
                                Logger.info( "Current CPU : "+ str(currentCpu ) +" at time : " + str(datetime_object))
                                #cpuInfo = Common.CPUInfo(datetime_object,currentCpu)      
                                self.cpu_data[datetime_object] = currentCpu        
                                #Common.cpu_data.append(cpuInfo)
                except Exception:
                    Logger.error("Exception caught : Cannot get CPU data")
                finally:
                    self.windows_helper.sleep_with_timeout(10)

    def get_collected_cpu_data(self):
        return self.cpu_data

    def reset_cpu_data(self):
        self.cpu_data=OrderedDict()

    def stop(self):
        Logger.info("Stopping CPU collector..")
        self._is_running = False

class MemStateCollector(Thread):
    def __init__(self,serial):
        super(MemStateCollector, self).__init__()
        self.daemon = True
        self.adb_driver = ADBDriver(serial)
        self._is_running = True
        self.cpu_data = OrderedDict()
        self.is_memory_critical = False
        self.windows_helper = WindowsCmdHelper()

    def run(self):
        Logger.info("Before memory state")
        while self._is_running:    
                try:
                    Logger.info("Inside memory state")
                    adb_output = self.adb_driver.execute_command(ADBCommands.dateCommand)
                    datetime_object = dateParser.parse(adb_output.strip())
                    datetime_object = datetime_object.strftime("%m-%d %H:%M:%S")
                    datetime_object = (datetime.strptime(datetime_object,"%m-%d %H:%M:%S"))
                    adb_output_memState = self.adb_driver.execute_command(ADBCommands.memStateCommand)
                    if "Norm" in adb_output_memState:
                        Logger.info("Memory State : NORMAL " + " at time : " + str(datetime_object))
                    elif "Mod" in adb_output_memState:
                        Logger.warning("Memory State : MODERATE " + " at time : " + str(datetime_object))
                    elif "Low" in adb_output_memState:
                        Logger.warning("Memory State : LOW " + " at time : " + str(datetime_object))
                    elif "Crit" in  adb_output_memState:
                        Logger.error("Memory State : CRITICAL " + " at time : " + str(datetime_object))
                        self.is_memory_critical = True
                    else:
                        Logger.info( "Cant't get memory status")
                    output = self.adb_driver.execute_command(ADBCommands.memInfoCommand)
                    Logger.info("Memory info : "+ str(output))
                except Exception:
                    Logger.error("Exception caught : Cannot get MEMORY data")
                finally:
                    self.windows_helper.sleep_with_timeout(5*60)

    def is_critical_mem_detected(self):
        return self.is_memory_critical
                
    def stop(self):
        Logger.info("Stopping MEM State collector..")
        self._is_running = False

class PerfCollection(Thread):
    def __init__(self,serial):
        super(PerfCollection, self).__init__()
        self.daemon = True
        self.adb_driver = ADBDriver(serial)
        ## Reset procstats ##
        adb_output = self.adb_driver.execute_command(ADBCommands.resetProcStatsCommand)
        self.serial = serial
        self.windows_helper = WindowsCmdHelper()

    def run(self):
        try:
            self.cpuThread=CPUDataCollector(self.serial)
            self.memStateThread=MemStateCollector(self.serial)
            self.cpuThread.start()
            self.memStateThread.start()
        except (KeyboardInterrupt, SystemExit):
            pass

    def get_collected_cpu_data(self):
        return self.cpuThread.get_collected_cpu_data()

    def reset_cpu_data(self):
        self.cpuThread.reset_cpu_data()

    def is_memory_critical(self):
        return self.memStateThread.is_critical_mem_detected()

    def stop(self):
        self.cpuThread.stop()
        self.memStateThread.stop()

    