import time
import subprocess
from subprocess import Popen, PIPE
from threading import Timer
import shlex

serial = "10.176.33.199"

def check_output_with_timeout( cmd, timeout_sec):

    # start = timer()
    # with Popen('sleep 30', shell=True, stdout=PIPE, preexec_fn=os.setsid) as process:
    #     try:
    #         output = process.communicate(timeout=1)[0]
    #     except TimeoutExpired:
    #         os.killpg(process.pid, signal.SIGINT) # send signal to the process group
    #         output = process.communicate()[0]
    # print('Elapsed seconds: {:.2f}'.format(timer() - start))
    # return output

    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
        return stdout
    finally:
        timer.cancel()
        return stdout

def execute_command(command ):
    commandStatus = 0
    i = 0
    ## Try for upto 30 minutes; This time is to make sure we cover upgrade during reboot.
    while (commandStatus != 1 and i <= (10*60) ):
        try :
            if 'adb' not in command :
                command = "adb -s " +serial +" " + command
            print("Running command : "+ command + " for "+ str(i)+" th time")
            adb_output = check_output_with_timeout(command,5*60)
            print("command run successfully")
            if (adb_output is not None and len(str(adb_output)) > 0) :
                print("ADB OUTPUT : "+ adb_output)
                return adb_output
        except Exception as e:
                print " ADB Command cannot be executed ", e
                # if ('.' in self.serial):
                #     try :
                #         subprocess.check_output("adb connect "+self.serial)
                #         subprocess.check_output("adb " + "-s " + self.serial+"  root")
                #         subprocess.check_output("adb connect "+self.serial)
                #     except Exception:
                #         Logger.error("Trying to reconnect")
                # else :
                #     subprocess.check_output("adb reconnect")                
                time.sleep(1)

def main():
    output = execute_command(" shell dumpsys meminfo com.microsoft.skype.teams.ipphone")
    print output


if __name__ == '__main__':
    main()