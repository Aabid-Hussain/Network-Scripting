#!/usr/bin/env python
import collections
import subprocess
import time
import os
import errno
import threading

class Logger(object): 
    LoggingDir = ""
    fd = None
    is_started = False
    @staticmethod
    def Start():
        try :
            Logger.is_started = True
            if (Logger.fd is None):
                print "Test Logging started"
                currentTime = time.strftime("%Y%m%d-%H%M%S")
                if Logger.LoggingDir == "":
                    Logger.LoggingDir = "Logs_"+currentTime+"/"
                file_name = Logger.LoggingDir + "TestLog.log"
                if not os.path.exists(os.path.dirname(file_name)):
                    try:
                        os.makedirs(os.path.dirname(file_name))
                    except OSError as exc: # guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                Logger.fd = open(file_name,"a+")
        except Exception as e:            
            print "Exception when starting logger : " , e
            
    @staticmethod
    def IsStarted():
        return Logger.is_started
    @staticmethod
    def WriteToLog(level,message):
        lock = threading.Lock()
        lock.acquire()
        try :
            Logger.fd.write(time.strftime("%Y-%m-%d-%H:%M:%S ")+ "----- "+ level.upper() +" -----" + message +"\n")
        except Exception as e:
            print "Failure writing to file : ", message, "Exception : ", e
        finally:
            lock.release()

    @staticmethod
    def error(message):
        try :
            Logger.WriteToLog("error", message)
        except Exception as e:
            print "Failure writing to file : ", message, "Exception : ", e

    @staticmethod
    def info(message):
        try :
            Logger.WriteToLog("info", message)
        except Exception as e:
            print "Failure writing to file : ", message, "Exception : ", e

    @staticmethod
    def warning(message):
        try :
            Logger.WriteToLog("warning", message)
        except Exception as e:
            print "Failure writing to file : ", message, "Exception : ", e

    @staticmethod
    def Stop():
        #print "Stopping logs"
        if (Logger.fd is not None):
            Logger.fd.close()
            Logger.fd = None
        else:
            print "Logger.fd stopped already"
