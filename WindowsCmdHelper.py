
import time
import subprocess32
from Logger import Logger
from subprocess32 import Popen, PIPE
from threading import Timer
import shlex
import os
import threading

# class Command(object):
    # def __init__(self, cmd):
    #     self.cmd = cmd
    #     process = None

    # def run(self, timeout):
    #     def target():
    #         print 'Thread started'
    #         process = subprocess.Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    #         stdout, stderr = process.communicate()
    #         print 'Thread finished'

    #     thread = threading.Thread(target=target)
    #     thread.start()

    #     thread.join(timeout)
    #     if thread.is_alive():
    #         print 'Terminating process'
    #         process.terminate()
    #         thread.join()
    #     return stdout,stderr


class WindowsCmdHelper(object):
    def __init__(self):
        Logger.info("Windows command helper initiated")

    def sleep_with_timeout(self, timeout_sec):
        self.run_cmd_with_timeout("timeout /t "+ str(timeout_sec)+" ", int(timeout_sec)+1)

    def run_cmd_with_timeout(self, cmd, timeout_sec):
        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE,)
        self.timer = Timer(timeout_sec, self.kill_cmd , [proc.pid] )
        stdout = None
        stderr = None
        try:
            self.timer.start()
            Logger.info("Running command with timeout: "+ str(proc.pid) + " - "+ cmd )                
            stdout, stderr = proc.communicate(timeout=timeout_sec)
        except Exception as e :
            Logger.error("Error in run_cmd_with_timeout" + str(e))
        finally:            
            self.timer.cancel()
            if stderr is not None and len(stderr) > 0:
                Logger.info("Command with timeout ended for cmd: "+ cmd +"stderr : "+ str(stderr) )
                return stderr
            if stdout is not None :
                Logger.info("Command with timeout ended for cmd: "+ cmd +"stdout : "+ str(stdout) )
                return stdout
            return None

    def kill_cmd(self, pid):
        try :
            Logger.error("Command execution timeout. trying to kill "+ str(pid) )
            killcmd = 'taskkill /f /T /PID %s' % pid
            os.system(killcmd)
            Logger.error("Command execution timeout. "+ str(pid) + " successfully killed")
        except Exception as e :
            Logger.error("Exception when force killing command. " + str(e))
        finally :
            Logger.info("in finally block")
            