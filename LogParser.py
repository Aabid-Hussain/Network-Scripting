
from threading import Thread
import Queue
import datetime
import subprocess
import signal
import re
import time 
from datetime import date
from Logger import Logger
import dateutil.parser as dateParser
import os
ClearLogCatCommand ="logcat -c"
from enums import Page
from collections import OrderedDict
from threading import Timer

class LogcatThread(Thread):
    
    def __init__(self, device_serial, logs_folder):
        Thread.__init__(self)
        self.daemon = True
        self.DATEFORMAT = r'^(\d+-\d+\s?\d+:\d+:\d+.\d+)\s?'
        self.PATTERNS = [
            ('GC_FOR_ALLOC',self.DATEFORMAT+r'.*GC_FOR_ALLOC freed(.*)',self.decodeHeapUsed),
            ('concurrent mark sweep GC freed',self.DATEFORMAT+r'.*concurrent mark sweep GC freed(.*)',self.decodeARTMemUsed),
            ('com.microsoft.skype.teams.Launcher',self.DATEFORMAT+r'.*com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.Launcher.*',self.appLaunchActivity),
            ('Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.MainActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.MainActivity: ((\+\w*)+)(.*)',self.mainActivityDisplayed),
            ('com.microsoft.skype.teams.views.activities.MainActivity',self.DATEFORMAT+r'.*Thread: main, Activity started: com.microsoft.skype.teams.views.activities.MainActivity.*',self.mainActivityRefreshed),
            ('Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.FreAuthActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.FreAuthActivity: ((\+\w*)+)(.*)',self.freAuthActivityDisplayed),
            ('Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.FreActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.FreActivity: ((\+\w*)+)(.*)',self.freActivityDisplayed),
            ('Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.WelcomeActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.WelcomeActivity: ((\+\w*)+)(.*)',self.welcomeActivityDisplayed),
            ('Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.CallRatingActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.CallRatingActivity: ((\+\w*)+)(.*)',self.callRatingDisplayed),           
            ('onCallListViewReady',self.DATEFORMAT+r'.*CallListView: onCallListViewReady:true.*',self.callListReady),
            ('onCallListViewReady',self.DATEFORMAT+r'.*VoiceMailsView: onCallListViewReady:true.*',self.vmListReady),
            ('IPPHONE_UNENROLL',self.DATEFORMAT+r'.*com.microsoft.windowsintune.companyportal.intent.action.IPPHONE_UNENROLL*',self.signingOutActivity),
            ('User successfully signed out',self.DATEFORMAT+r'.*User successfully signed out*',self.signOutActivity),
            ('registering account',self.DATEFORMAT+r'.*registering account\s(.*)\s',self.signingInActivity),
            ('FreAuthActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.FreAuthActivity: ((\+\w*)+)(.*)',self.signingInActivity),
            ('Displayed com.microsoft.windowsintune.companyportal/com.microsoft.aad.adal.unity.AuthenticationActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.windowsintune.companyportal/com.microsoft.aad.adal.unity.AuthenticationActivity: ((\+\w*)+)(.*)',self.signingInActivity),
            ('com.microsoft.skype.teams.views.activities.PreCallActivity',self.DATEFORMAT+r'.*Activity created: com.microsoft.skype.teams.views.activities.PreCallActivity.*',self.callInitiated),
            ('com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.PreCallActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.PreCallActivity: ((\+\w*)+)(.*)',self.preCallActivityStarted),
            ('com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.InCallActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.InCallActivity: ((\+\w*)+)(.*)',self.InCallActivityStarted),
            ('com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.DialCallActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.DialCallActivity: ((\+\w*)+)(.*)',self.dialCallActivity),
            ('com.microsoft.skype.teams.views.activities.InCallActivity',self.DATEFORMAT+r'.*Thread: main, Activity destroyed: com.microsoft.skype.teams.views.activities.InCallActivity.*',self.callEndedActivity),
            #('com.microsoft.skype.teams.views.activities.PreCallActivity',self.DATEFORMAT+r'.*Thread: main, Activity destroyed: com.microsoft.skype.teams.views.activities.PreCallActivity.*',self.callEndedActivity),
            ('com.microsoft.skype.teams.views.activities.SettingsActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.SettingsActivity: ((\+\w*)+)(.*)',self.settingsActivity),
            ('com.microsoft.skype.teams.views.activities.MeetingDetailsActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.MeetingDetailsActivity: ((\+\w*)+)(.*)',self.meetingDetailsActivity),
            ('com.microsoft.skype.teams.views.activities.SearchUsersToStartNewCallActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.SearchUsersToStartNewCallActivity: ((\+\w*)+)(.*)',self.searchForNewCallActivity),
            ('com.microsoft.skype.teams.views.activities.CallRosterActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.CallRosterActivity: ((\+\w*)+)(.*)',self.callRosterActivity),
            ('com.microsoft.skype.teams.views.activities.ContactCardActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.ContactCardActivity: ((\+\w*)+)(.*)',self.contactCardActivity),
            ('com.microsoft.skype.teams.views.activities.SearchActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.SearchActivity: ((\+\w*)+)(.*)',self.searchActivity),
            ('com.microsoft.skype.teams.views.activities.SearchAddParticipantMeetingActivity',self.DATEFORMAT+r'.*Displayed com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.SearchAddParticipantMeetingActivity: ((\+\w*)+)(.*)',self.addParticipantActivity),
            ('msteamspartner://settings',self.DATEFORMAT+r'.*START u0 {act=android.intent.action.VIEW dat=msteamspartner://Common.*',self.partnerSettingsStarted),
            ('voice_mail',self.DATEFORMAT+r'.*voice mail path:/data/data/com.microsoft.skype.teams.ipphone/cache.*',self.vmDetailsActivity),
            ('unhandled crash',self.DATEFORMAT+r'(.*unhandled crash.*)',self.handleCrash),
            ('EXCEPTION_ACCESS_VIOLATION',self.DATEFORMAT+'(.*Exiting due to deadlock in thread.*)',self.handleCrash),
            ('Exiting',self.DATEFORMAT+'(.*EXCEPTION_ACCESS_VIOLATION.*)',self.handleCrash),
            ('MinidumpContainer',self.DATEFORMAT+r'(.*MinidumpContainer.*)',self.handleCrash),
            ('Got signal SIGSEGV',self.DATEFORMAT+r'(.*Got signal SIGSEGV.*)',self.handleCrash),
            ('Got signal SIGABRT',self.DATEFORMAT+r'(.*Got signal SIGABRT.*)',self.handleCrash),
            ('has died',self.DATEFORMAT+r'(.*)has died.*',self.handleCrash)
        ]
        self._device_serial = device_serial
        self.logs_folder = logs_folder
        self.proc = None
        filename = "logcat_" +self._device_serial.replace(":5555","").replace(".","")+".log"
        self.log_file = os.path.join(self.logs_folder, filename)
        self.perf_data = {}
        self.mem_data = OrderedDict()
        self.events_data = {}
        self.latency_data = {}
        self.resetVariables()
        self.iteration = 1
        self.has_been_reset_before = False
        self.last_found_date = None

    def run(self):
        Logger.info("Flushing logcat")
        subprocess.call('adb -s %s logcat -c' % self._device_serial, shell=True)
        # work around for permission denied due to readonly file
        try:
            with open(self.log_file, 'w'):
                pass
        except IOError as e:
            Logger.error("Error in setting up logcat thread. Unable to rewrite file {} Exception: {}".format(self.log_file, str(e)))
            raise
        self.proc = subprocess.Popen('adb -s {} logcat -v time > {}'.format(self._device_serial, self.log_file), shell=True)
        Logger.info("START Logcat collection. PID:" +str (self.proc.pid))

    def get_perf_data(self):
        try:
            # if last_found_date is present, it means that we need to dump newer logs to new file #
            Logger.info("has_been_reset_before " + str(self.has_been_reset_before))
            if (self.has_been_reset_before == True):
                Logger.info("last_found_date " + str(self.last_found_date))
                if (self.last_found_date is not None):
                    ## Android 4.4 supports limited commands ##
                    if ('.' in self._device_serial) :  ## > Android 4.4 devices
                        command = 'adb -s {} logcat -t "{}" -v threadtime > {}'.format(self._device_serial, self.last_found_date, self.log_file)
                        Logger.info("command :" + command)
                        ## Dump all logs after previous run ##
                        self.proc = subprocess.Popen(command, shell=True)
                        (output, err) = self.proc.communicate()  

                        #This makes the wait possible
                        p_status = self.proc.wait()
                    else:
                        command = 'adb -s {} logcat -d -v threadtime > {}'.format(self._device_serial, self.log_file)
                        Logger.info("command :" + command)
                        ## Dump all logs after previous run ##
                        self.proc = subprocess.Popen(command, shell=True)
                        (output, err) = self.proc.communicate()  

                        #This makes the wait possible
                        p_status = self.proc.wait()
                        adb_output = subprocess.check_output("adb -s {} logcat -c".format(self._device_serial))
                        Logger.info("Clearing logcat "+ str(adb_output))
                    

            Logger.info("Reading file")
            with open(self.log_file) as f:
                for line in f :
                    matches = re.compile(self.DATEFORMAT).search(line)
                    if (matches != None):
                        try :                           
                            self.last_found_date = str(matches.groups()[0])
                            self.stringMatchesPatterns(line)
                        except Exception as e:
                            Logger.error("Exception caught when parsing logcat ."+ str(e))
            self.perf_data["mem"] = self.mem_data
            self.perf_data["latency"] = self.latency_data
            self.perf_data["events"] = self.events_data

            
            return self.perf_data
        except Exception as e:
            Logger.error( "Exception when reading logcat" + str(e))
            return None
            
    def reset_perf_data(self):
        try : 
            self.mem_data=OrderedDict()
            self.perf_data={}
            self.events_data={}
            self.latency_data={}
            self.stop_logcat()
            Logger.info("Starting logcat collection at different file location")
            self.log_file = self.log_file.replace(".log","_"+str(self.iteration)+".log")
            self.iteration = self.iteration + 1
            self.has_been_reset_before = True
        except Exception as e:
            Logger.error("Exception when resetting perf data" + str(e))
            

    def stop_logcat(self):
        Logger.info("STOP Logcat collection")
        if self.proc and (self.proc.poll() is None):
            killcmd = 'taskkill /f /T /PID %s' % self.proc.pid
            os.system(killcmd)
            self.proc = None

    def stop(self):
        ## Dump the remaining logcat logs before stopping ##
        if (self.last_found_date is not None):
            command = 'adb -s {} logcat -t "{}" -v time > {}'.format(self._device_serial, self.last_found_date, self.log_file)
            Logger.info("command :" + command)
            ## Dump all logs after previous run ##
            self.proc = subprocess.Popen(command, shell=True)
            timer = Timer(10*60, self.proc.kill)
            try:
                timer.start()
                (output, err) = self.proc.communicate()
                #This makes the wait possible
                p_status = self.proc.wait() 
            finally:
                timer.cancel()      

            
        self.stop_logcat()
        
    def getAppLaunchTime(self):
        if (self.launch_start_time_local is not None):
            return self.launch_start_time_local
        else:
            return None

    def resetVariables(self):
        self.is_app_launched = False
        self.is_call_list_ready = False
        self.is_voicemail_list_ready = False
        self.is_signed_out = False
        self.is_call_connected = False
        self.is_signing_in = False
        self.is_signing_out = False
        self.current_page = Page.Undefined
        self.signing_in_time = None
        self.launch_start_time = None
        self.launch_start_time_local = None
    
    def appLaunchActivity(self,matches):
        if (not self.is_app_launched) :
            Logger.info( "App Launch detected at " + matches[0] ) 
            self.resetVariables()
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")            
            self.events_data[date] = "App launch"
            self.launch_start_time = date
            self.launch_start_time_local = datetime.datetime.now()
            self.is_app_launched = True
    
    def mainActivityDisplayed(self,matches):
        Logger.info( "Signed in. Default Page displayed at " + matches[0] +". Time taken : " + matches[1]) 
        delay = str(matches[1]).strip().replace('ms','')
        delay= delay.replace(":","").replace(" ","")
        if ('s' in delay) :
            delay = delay.replace('s','.').replace('+','')
        else :
            delay = delay.replace('+','.')
        Logger.info("Mainactivity display delay : "+ str(delay))
        if ("MainActivityDisplay" not in self.latency_data):
            self.latency_data["MainActivityDisplay"]=list()
        self.latency_data["MainActivityDisplay"].append(float(delay))

        
        self.is_signing_in = False
        self.is_call_list_ready = False
        self.current_page = Page.MAIN_SCREEN

    def mainActivityRefreshed(self,matches):
        Logger.info("Main page displayed at "+ matches[0])
        self.current_page = Page.MAIN_SCREEN

    def callListReady(self,matches) :
        if not self.is_call_list_ready :
            Logger.info( "Call list ready at " + matches[0])
            self.is_call_list_ready = True
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
            self.events_data[date] = "Call list RDY"
            self.signed_in_time = date
            if (self.signing_in_time):
                signinDelay = self.signed_in_time - self.signing_in_time 
                signinDelay = str(signinDelay.seconds) + "."+ str(signinDelay.microseconds)
                if (float(signinDelay) < 360.0):
                    if ("signin" not in self.latency_data):
                        self.latency_data["signin"]=list()
                    self.latency_data["signin"].append(float(signinDelay))
                    Logger.info( "Sign in took : " + str(signinDelay))



    def meetingDetailsActivity(self,matches) :
        Logger.info( "Meeting detail displayed at " + matches[0] + "with delay : " + matches[1])
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "MTG detail"
        self.current_page = Page.MEETINGDETAIL_SCREEN
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("MTG detail delay : " + delay)
        if "MTGDetail" not in self.latency_data:
                self.latency_data["MTGDetail"]=list()
        self.latency_data["MTGDetail"].append(float(delay))

    def vmDetailsActivity(self,matches) :
        Logger.info( "VM detail displayed at " + matches[0] )
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "VM detail"
        # delay = self.convertActivityTimeToSeconds(matches[1])
        # Logger.info ("VM detail delay : " + delay)
        # if "VMDetail" not in self.latency_data:
        #         self.latency_data["VMDetail"]=list()
        # self.latency_data["VMDetail"].append(float(delay))

    def vmListReady(self,matches) :
        Logger.info( "Voicemail list ready at " + matches[0])
        self.is_voicemail_list_ready = True
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "VM list RDY"

    def freAuthActivityDisplayed(self,matches):
        Logger.info( "FRE sign in page displayed at " + matches[0] +". Time taken : " + matches[1]   )
        self.current_page = Page.FRE_SCREEN

    def freActivityDisplayed(self,matches):
        Logger.info( "FRE page displayed at " + matches[0] +". Time taken : " + matches[1]   )
        self.current_page = Page.WELCOME_SCREEN

    def welcomeActivityDisplayed(self,matches):
        Logger.info( "WELCOME page displayed at " + matches[0] +". Time taken : " + matches[1]   )
        self.current_page = Page.ACCT_SCREEN
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Welcome Page"
        if (self.launch_start_time is not None):
            launchDelay = date -self.launch_start_time
            launchDelay = str(launchDelay.seconds) + "."+ str(launchDelay.microseconds)
            if (float(launchDelay) < 360.0):
                if ("launch_signedout" not in self.latency_data):
                    self.latency_data["launch_signedout"]=list()
                self.latency_data["launch_signedout"].append(float(launchDelay))
                Logger.info("App Launch (Signed-out state) took : " + str(launchDelay))
            

    def settingsActivity(self,matches):
        Logger.info( "Setting page displayed at " + matches[0] +". Time taken : " + matches[1]   )
        self.current_page = Page.SETTINGS_SCREEN


    def callRatingDisplayed(self,matches):
        Logger.info( "Call Rating displayed at " + matches[0] +". Time taken : " + matches[1]   )
        self.current_page = Page.CALLRATING_SCREEN
        
    def partnerSettingsDisplayed(self,matches):
        Logger.info( "Partner settings page displayed at " + matches[0] +". Time taken : " + matches[1])   
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Partner Settings"
        self.current_page = Page.PARTNER_SCREEN
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("Device settings display delay : " + delay)
        if "DeviceSettings" not in self.latency_data:
                self.latency_data["DeviceSettings"]=list()
        self.latency_data["DeviceSettings"].append(float(delay)) 

    def partnerSettingsStarted(self,matches):
        Logger.info( "Partner settings page started at " + matches[0]) 
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Partner Settings STRT"

    def callInitiated(self,matches):
        message = "Call initated at " + str(matches[0])
        Logger.info( message)
        Logger.info(message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Call initiated"

    def convertActivityTimeToSeconds(self, activityTime):
        delay = str(activityTime).strip().replace('ms','')
        delay= delay.replace(":","").replace(" ","")
        if ('s' in delay) :
            delay = delay.replace('s','.').replace('+','')
        else :
            delay = delay.replace('+','.')
        return delay

    def searchForNewCallActivity(self,matches):
        message = "Search For New Call Activity displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "NewCallSRCH"
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("New Call Search delay : " + delay)
        if "NewCallSearch" not in self.latency_data:
                self.latency_data["NewCallSearch"]=list()
        self.latency_data["NewCallSearch"].append(float(delay)) 

    def callRosterActivity(self,matches):
        message = "Call Roster displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Roster"
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("Call Roster delay : " + delay)
        if "CallRoster" not in self.latency_data:
                self.latency_data["CallRoster"]=list()
        self.latency_data["CallRoster"].append(float(delay))
    

    def contactCardActivity(self,matches):
        message = "Contact Card Activity displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "ContactCRD"
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("Contact Card delay : " + delay)
        if "ContactCard" not in self.latency_data:
                self.latency_data["ContactCard"]=list()
        self.latency_data["ContactCard"].append(float(delay))

    def searchActivity(self,matches):
        message = "Search Activity displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Search"
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("Search delay : " + delay)
        if "Search" not in self.latency_data:
                self.latency_data["Search"]=list()
        self.latency_data["Search"].append(float(delay))

    def addParticipantActivity(self,matches):
        message = "Add Participant Activity displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "AddPerson"
        delay = self.convertActivityTimeToSeconds(matches[1])
        Logger.info ("Add Person delay : " + delay)
        if "AddPerson" not in self.latency_data:
                self.latency_data["AddPerson"]=list()
        self.latency_data["AddPerson"].append(float(delay))

    def preCallActivityStarted(self,matches):
        message = "PreCall activity displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        Logger.info(message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Pre-Call"  
        delay = str(matches[1]).strip().replace('ms','')
        delay= delay.replace(":","").replace(" ","")
        if ('s' in delay) :
            preCallDelay = delay.replace('s','.').replace('+','')
        else :
            preCallDelay = delay.replace('+','.')
        Logger.info ("Precall delay : " + preCallDelay)
        Logger.info("Call screen displayed with delay (join/call-connecting/calling) " + preCallDelay)
        if "PreCallDelay" not in self.latency_data:
                self.latency_data["PreCallDelay"]=list()
        self.latency_data["PreCallDelay"].append(float(preCallDelay)) 
        self.current_page = Page.PRECALL_SCREEN

    def dialCallActivity (self, matches):
        message = "DialCall activity displayed at " +str (matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        Logger.info(message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Dial-Call"  
        delay = str(matches[1]).strip().replace('ms','')
        delay= delay.replace(":","").replace(" ","")
        if ('s' in delay) :
            dialCallDelay = delay.replace('s','.').replace('+','')
        else :
            dialCallDelay = delay.replace('+','.')
        Logger.info ("Dialcall delay : " + dialCallDelay)
        if "DialCallDelay" not in self.latency_data:
                self.latency_data["DialPadDisplay"]=list()
        self.latency_data["DialPadDisplay"].append(float(dialCallDelay)) 
        self.current_page = Page.DIALCALL_SCREEN
    def InCallActivityStarted(self,matches):
        message =  "Call connected at " +str(matches[0]) + "with delay : " + str(matches[1])
        Logger.info( message)
        Logger.info(message)
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        self.events_data[date] = "Call connected"
        
        delay = str(matches[1]).strip().replace('ms','')
        delay= delay.replace(":","").replace(" ","")
        if ('s' in delay) :
            inCallDelay = delay.replace('s','.').replace('+','')
        else :
            inCallDelay = delay.replace('+','.')

        Logger.info ("Call connected delay : " + inCallDelay)
        if "InCallDelay" not in self.latency_data:
                self.latency_data["InCallDelay"]=list()
        self.latency_data["InCallDelay"].append(float(inCallDelay)) 
        Logger.info("Call connected delay (connecting-connected) " + inCallDelay)
        self.is_call_connected = True    
        self.current_page = Page.INCALL_SCREEN


    def callEndedActivity(self,matches):
        if (self.is_call_connected):
            message = "Call ended at " + str(matches[0])
            Logger.info( message)
            Logger.info(message)
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
            self.events_data[date] = "Call ended"
            self.is_call_connected = False    

    def signingInActivity(self,matches):
        if not self.is_signing_in :
            message = "Sign In activity detected at " + str(matches[0])
            Logger.info( message)
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
            self.events_data[date] = "Signing in"
            self.signing_in_time = date
            self.is_signing_in = True
            self.is_signed_out = False

    def signOutActivity(self,matches):
        if (self.is_signing_out) :
            message = "User signed out at " + str(matches[0])
            Logger.info( message)
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
            self.events_data[date] = "Signed out"
            self.is_signed_out = True
            self.is_signing_out = False

            if (self.signing_out_time):
                signOutDelay = date - self.signing_out_time 
                signOutDelay = str(signOutDelay.seconds) + "."+ str(signOutDelay.microseconds)
                if (float(signOutDelay) < 360.0):
                    if ("signout" not in self.latency_data):
                        self.latency_data["signout"]=list()
                    self.latency_data["signout"].append(float(signOutDelay))
                    Logger.info( "Sign out took : " + str(signOutDelay))


    def signingOutActivity(self,matches):
            message = "User signing out at " + str(matches[0])
            Logger.info( message)
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
            self.events_data[date] = "Signing out"
            self.signing_out_time = date
            self.is_signing_out = True

    def handleCrash(self,matches):
        app = str(matches[1])
        message = "!!!Crash detected at " +str(matches[0]) + " ::Detailed Info ::" + app+"!!!"
        if "com.microsoft.skype.teams.ipphone" in app :
            date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
            self.events_data[date] = "!Crash!"
            # self.GetADBBugReport()
        Logger.info( message)
        Logger.info(message)
        
    
    def decodeHeapUsed(self,matches):
        #Logger.info( matches
        memAvailable = (int)(matches[1].split('%')[1].strip().split()[1].split('/')[0][:-1])/1024
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        #Below line to capture free percentage
        #memInfo = Common.MEMInfo(date,memAvailable,matches[1].split()[1][:-1])
        self.mem_data[date] = memAvailable

    def decodeARTMemUsed(self,matches):
        #Logger.info( matches
        if (matches[1].split()[8].split('/')[0][-2] == 'K'):
            memAvailable = (int)(matches[1].split()[8].split('/')[0][:-2])/1024
        elif (matches[1].split()[8].split('/')[0][-2] == 'M'):
            memAvailable = (int)(matches[1].split()[8].split('/')[0][:-2])
        else:
            memAvailable = (int)(matches[1].split()[8].split('/')[0][:-2])*1024
        date = datetime.datetime.strptime(matches[0],"%m-%d %H:%M:%S.%f")
        #Below line to capture free percentage
        #memInfo = Common.MEMInfo(date,memAvailable,matches[1].split()[6][:-1])
        self.mem_data[date] = memAvailable
    

   

    def stringMatchesPatterns(self,line):
        for (search,pattern,handler) in self.PATTERNS:
            if (search in line):
                patt = re.compile(pattern)
                match = patt.search(line)
                if match:
                    #Logger.info(("FUNC %s\tRE %s\t\n" % (handler.__name__, line[match.regs[2][1]:-1]))
                    handler(match.groups())
                    #Logger.info( "Pattern match Found For :" + line
    

