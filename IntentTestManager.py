from ADBDriver import ADBDriver
from Logger import Logger
from enums import Intents
from enums import KeyCodes
from enums import DeviceType
from IntentUtilities import IntentUtilities
import os, colorama
from colorama import Fore,Style,Back
# os.system("mode con: cols=120 lines=30")
import time
import re
import sys
from threading import Timer
import shlex
from subprocess import Popen, PIPE
class IntentTestManager:   

    def __init__(self, serial,device_type):
        self.passed_tests = []
        self.failed_tests = []
        self.not_applicable_tests = []
        self.COMBO_TESTS = [
                    ('Dialtone 101 (SPEAKER)',DeviceType.PERSONAL, self.must_hear_dialtone_speaker),
                    ('Dialtone 101 (HEADPHONE)',DeviceType.PERSONAL, self.must_hear_dialtone_headphone),
                    ('Dialtone 101 (HANDSET)',DeviceType.PERSONAL, self.must_hear_dialtone_handset),
                    ('Mute 101',DeviceType.ALL, self.verify_mute_status),
                    ('MissedCall 101',DeviceType.PERSONAL, self.verify_missedcall_mwi),
                    ('VM 101',DeviceType.PERSONAL, self.verify_voicemail_mwi),
                    ('INCOMING CALL 101',DeviceType.ALL, self.verify_incoming_call),
                    # ('Dialtone_Neg_1',DeviceType.PERSONAL, self.dialtone_neg_1),
                    # ('Dialtone_Neg_2',DeviceType.PERSONAL, self.dialtone_neg_2),
                    # ('Dialtone_Neg_3',DeviceType.PERSONAL, self.dialtone_neg_3),
                    # ('Dialtone_Speaker_Neg_1',DeviceType.PERSONAL, self.dialtone_neg_speaker_1),
                    # ('Dialtone_Speaker_Neg_2',DeviceType.PERSONAL, self.dialtone_neg_speaker_2),
                    # ('Dialtone_Speaker_Neg_3',DeviceType.PERSONAL, self.dialtone_neg_speaker_3),
                    # ('Mute_Neg_1',DeviceType.PERSONAL, self.mute_neg_1),
                    # ('Mute_Neg_2',DeviceType.PERSONAL, self.mute_neg_2),
                    # ('Mute_Neg_3',DeviceType.PERSONAL, self.mute_neg_3),
                    # ('Ringing 101',DeviceType.ALL, self.verify_)
        ]
        self.intent_manager = IntentUtilities(serial)
        self.adb_driver = ADBDriver(serial)
        self.device_type = self.get_device_type(device_type)

    def start(self):
        try:
            print "#################"
            print('INTENT VALIDATOR')
            print "#################"
            print "\n"
            print "0 to run intent validator"
            print "1 to test individual intent\n2 to test individual keycodes"
            input = self.read_and_validate_integer_input(0,2)
            
            if input == 1 :            
                while True:                
                    self.available_intents = self.intent_manager.get_available_intents()
                    for test in self.available_intents :
                        print test , " : " , self.available_intents[test]["name"]
                    print "Ctrl+C to quit"
                    input = self.read_and_validate_integer_input(1,len(self.available_intents))          
                    self.intent_manager.broadcast_intent(input)

            elif input == 2 :               
                self.available_keycodes = self.intent_manager.get_available_keycodes()
                for test in self.available_keycodes :
                    test_name = self.available_keycodes[test]["name"]
                    expected_keycode = self.available_keycodes[test]["action"]
                    print "Press " + test_name +" on device and ENTER to continue. (Press x if not applicable)"
                    char = raw_input()                    
                    if char.lower() == 'x':
                        self.not_applicable_tests.append(test_name)
                    else :
                        actual_keycode = self.get_lastfound_keycode()
                        if  str(expected_keycode) ==  str(actual_keycode)  :
                            self.passed_tests.append(test_name)
                            print "Keycode successfully validated."
                        else :
                            print "Incorrect keycode. Expected KeyCode: "+ str(expected_keycode) +" Found KeyCode: "+ str(actual_keycode)
                            self.failed_tests.append(test_name)
                        
                self.print_summary()

            elif input == 0:
                for (test_name, device_type, test_method) in self.COMBO_TESTS:
                    if device_type == DeviceType.ALL or self.device_type == device_type:
                        test_method(test_name)
                    else :
                        self.not_applicable_tests.append(test_name)

                self.print_summary()

        except KeyboardInterrupt as e:
            self.intent_manager.stop()
            exit

    def print_summary(self):
        print "\n\n\n\n\n"
        print "#####################"
        print "      SUMMARY"
        print "#####################"

        print "Total tests : " + str(len(self.COMBO_TESTS))
        print "Total passed : " + str(len(self.passed_tests))
        print "Total failed : " + str(len(self.failed_tests))
        # print(Fore.GREEN + "Total passed : " + str(len(self.passed_tests)))
        # print(Fore.RED + "Total failed : " + str(len(self.failed_tests)))
        # print(Style.RESET_ALL)
        print "Total N/A : " + str(len(self.not_applicable_tests))

        print "\n"
        for test in self.failed_tests:
            print "Failed test : "+ test
        print "\n"
        for test in self.passed_tests:
            print "Passed test : "+ test
        print "\n"
        for test in self.not_applicable_tests:
            print "Not applicable test : "+ test

    def stop(self):
        self.intent_manager.stop()
        exit

    def get_device_type(self,device_type):
        result = self.adb_driver.execute_command("shell getprop ro.product.device")
        result = result.strip()
        conf_devices = []
        personal_devices = []
        # if (result in conf_devices) :
        #     return DeviceType.CONFERENCE
        # elif (result in personal_devices) :
        #     return DeviceType.PERSONAL
        # else:
        #     return DeviceType.ALL

        if (device_type == "1") :
            return DeviceType.CONFERENCE
        elif (device_type == "2") :
            return DeviceType.PERSONAL
        else:
            return DeviceType.ALL
        
    def reset_intents(self):
        print "Please wait. RESETting intents.."
        self.intent_manager.reset_intents()
        self.send_dummy_keycode()
        print "RESET Done"

    def read_and_validate_integer_input(self,start_range, end_range):
        while True :
            try :
                input = raw_input('Enter your input: Range['+str(start_range) +"-"+str(end_range) +"] :")
                selected = int(input)
                if (selected >= start_range and selected <= end_range):
                    return selected
            except Exception as e :
                print "Exception caught : " + str(e)
                return None
    
    def read_and_validate_option_input(self):
        options = ["yes", "no","skip"]        
        message = 'Enter your input : '
        for option in options :
            message += (option + ',')
        message += ':'

        while True :
            try :
                input = raw_input(message)
                input = input.lower()
                if input in options:
                    return input
            except Exception as e :
                print "Exception caught : " + str(e)
                return None

    def print_start_test(self,test_name):
        print "##########################"
        print "START " + test_name
        print "##########################"

    def print_stop_test(self,test_name):
        print "##########################"
        print "END " + test_name
        print "##########################"

    

    def must_hear_dialtone_speaker(self,test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)
        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            
        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def must_hear_dialtone_headphone(self,test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        print "Press Headset button on phone."
        self.validate_keycode(KeyCodes.HEADSET)
        print "Is Headset button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            
        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def must_hear_dialtone_handset(self,test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)
        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def dialtone_neg_speaker_1(self, test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        
        print "Sending Incoming Call intent"
        self.intent_manager.broadcast_intent(Intents.INCOMING_CALL_STATE_ON)
        
        
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)
        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False
            
        print "Resetting Incoming Call intent"
        self.intent_manager.broadcast_intent(Intents.INCOMING_CALL_STATE_OFF)
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_OFF)
        
        # self.send_dummy_keycode()
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)

        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False

        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def dialtone_neg_1(self, test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        
        print "Sending Incoming Call intent"
        self.intent_manager.broadcast_intent(Intents.INCOMING_CALL_STATE_ON)
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)
        # self.send_dummy_keycode()

        print "Resetting Incoming Call intent"
        self.intent_manager.broadcast_intent(Intents.INCOMING_CALL_STATE_OFF)
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_OFF)
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def dialtone_neg_2(self, test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        
        print "Sending In Call intent"
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_ON)
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)
        # self.send_dummy_keycode()

        print "Resetting In Call intent"
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_OFF)
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def dialtone_neg_speaker_2(self, test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        
        print "Sending In Call intent"
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_ON)
        
        
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)
        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False
            
        print "Resetting In Call intent"
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_OFF)
        
        # self.send_dummy_keycode()
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)

        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False

        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

        
    def dialtone_neg_3(self, test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        
        print "Sending Voicemail playing intent"
        self.intent_manager.broadcast_intent(Intents.VOICEMAIL_PLAYING_ON_HANDSET)
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)
        # self.send_dummy_keycode()

        print "Resetting Voicemail playing intent"
        self.intent_manager.broadcast_intent(Intents.VOICEMAIL_PLAYING_OFF)
        print "Lift Handset."
        self.validate_keycode(KeyCodes.HANDSET)
        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            
        # self.send_dummy_keycode()
        print "You may hangup now."
        self.validate_keycode(KeyCodes.HANDSET)

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def dialtone_neg_speaker_3(self, test_name):
        test_status = True       
        self.print_start_test(test_name)
        self.reset_intents()
        
        print "Sending Voicemail playing intent"
        self.intent_manager.broadcast_intent(Intents.VOICEMAIL_PLAYING_ON_SPEAKER)
        
        
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)
        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False
            
        print "Resetting Voicemail playing intent"
        self.intent_manager.broadcast_intent(Intents.VOICEMAIL_PLAYING_OFF)
        
        # self.send_dummy_keycode()
        print "Press Speaker button on phone."
        self.validate_keycode(KeyCodes.SPEAKER)

        print "Is Speaker button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False

        
        print "Do you hear dialtone?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
            

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)
    
    def verify_missedcall_mwi(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Sending Missed call intent"
        self.intent_manager.broadcast_intent(Intents.MISSED_CALL_STATE_ON)

       
        print "Is Missed call LED blinking?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False


        print "Resetting missed call state"
        self.intent_manager.broadcast_intent(Intents.MISSED_CALL_STATE_OFF)
        print "Is Missed call LED blinking?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def verify_voicemail_mwi(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Sending New voicemail  intent"
        self.intent_manager.broadcast_intent(Intents.MISSED_VOICEMAIL_STATE_ON)

       
        print "Is VM LED blinking?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False


        print "Resetting voicemail state"
        self.intent_manager.broadcast_intent(Intents.MISSED_VOICEMAIL_STATE_OFF)
        print "Is VM LED blinking?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def verify_incoming_call(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Sending incoming call intent"
        self.intent_manager.broadcast_intent(Intents.INCOMING_CALL_STATE_ON)

       
        print "Is incoming call LED blinking?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False


        print "Resetting incoming call state"
        self.intent_manager.broadcast_intent(Intents.INCOMING_CALL_STATE_OFF)
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_OFF)
        print "Is incoming call LED blinking?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def verify_mute_status(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Sending in call state as ON"
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_ON)

        print "Press MUTE button on phone."
        self.validate_keycode(KeyCodes.MUTE)
        self.intent_manager.broadcast_intent(Intents.MUTE_STATE_ON)
        print "Is MUTE button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False


        print "Resetting in call state"
        self.intent_manager.broadcast_intent(Intents.IN_CALL_STATE_OFF)
        print "Is MUTE button lit?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False


        print "Press MUTE button on phone."
        self.validate_keycode(KeyCodes.MUTE)
        self.intent_manager.broadcast_intent(Intents.MUTE_STATE_ON)
        print "Is MUTE button lit?"
        input = self.read_and_validate_option_input()
        if (input == "yes"):
            test_status = test_status and False

        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def mute_neg_1(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Press MUTE button on phone."
        self.validate_keycode(KeyCodes.MUTE)
        self.intent_manager.broadcast_intent(Intents.MUTE_STATE_ON)
        print "Is MUTE button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)


    def mute_neg_2(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Press MUTE button on phone."
        self.validate_keycode(KeyCodes.MUTE)
        self.intent_manager.broadcast_intent(Intents.MUTE_STATE_ON)
        print "Is MUTE button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def mute_neg_3(self, test_name):
        test_status = True 
        self.print_start_test(test_name)
        self.reset_intents()
        print "Press MUTE button on phone."
        self.validate_keycode(KeyCodes.MUTE)
        self.intent_manager.broadcast_intent(Intents.MUTE_STATE_ON)
        print "Is MUTE button lit?"
        input = self.read_and_validate_option_input()
        if (input == "no"):
            test_status = test_status and False
        if test_status is False:
            self.failed_tests.append(test_name) if test_name not in self.failed_tests else None
        else:
            self.passed_tests.append(test_name) if test_name not in self.failed_tests else None
        self.print_stop_test(test_name)

    def send_dummy_keycode(self):
        self.adb_driver.execute_command(" shell input keyevent "+ str(KeyCodes.ENTER))

    def get_lastfound_keycode(self):
        result = self.adb_driver.execute_command(" shell dumpsys input")
        keyevents_history = []
        start_tracker = False
        for line in result.splitlines() :
            line = line.strip()
            if 'PendingEvent:' in line :
                start_tracker = False
            
            if start_tracker and len(line) > 0:
                keyevents_history.append(line)

            if 'RecentQueue:' in line :                
                start_tracker = True
        try :
            keyevents_history = [ keyevent for keyevent in keyevents_history  if ( 'keyCode=3,' not in keyevent )]
            found_keycode = re.search(r'.*keyCode=(\d+).*',keyevents_history[-1]).groups()[0]
            # print "Found KeyCode : " , str(found_keycode)
        except :
            found_keycode = ""
        return found_keycode

    def validate_keycode(self,expected_keycode, with_wait=True):      
        # print "Expected KeyCode : " , str(expected_keycode)  
        i = 1
        if with_wait :
            ## Wait 3 minutes for keycode press
            max_i = 3* 60
        else :
            max_i = 1
        while True :
            found_keycode = self.get_lastfound_keycode()
            if (int(found_keycode) == int(expected_keycode)) :
                self.send_dummy_keycode()
                return True
            time.sleep(1)
            i = i + 1
            if (i > max_i ):
                self.send_dummy_keycode()
                return False


def main():
    serial = sys.argv[1]
    device_type = sys.argv[2]
    test_manager = IntentTestManager(serial, device_type)
    test_manager.start()

if __name__ == '__main__':
    main()
