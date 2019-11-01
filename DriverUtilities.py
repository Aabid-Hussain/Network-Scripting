from collections import namedtuple
from collections import OrderedDict
from threading import Thread
import Queue
import subprocess
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time
import Logger
from Logger import Logger
from LogParser import LogcatThread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ADBDriver import ADBDriver
from PerformanceCounters import PerfCollection
from enums import ADBCommands
import datetime
import os
from WindowsCmdHelper import WindowsCmdHelper
teamsAppLogger = None

class DriverUtilities():

    def __init__(self,driver,udid):
        try:
            self.windows_helper = WindowsCmdHelper()
            self.test_driver = driver
            self.window_size = None
            self.udid = udid
            self.adb_driver = ADBDriver(self.udid)
            # self.reset_app()
            self.adb_driver.execute_command("shell pm clear com.microsoft.skype.teams.ipphone")
            self.adb_driver.execute_command("shell pm clear com.microsoft.windowsintune.companyportal")
            self.adb_driver.execute_command("shell pm grant com.microsoft.skype.teams.ipphone android.permission.RECORD_AUDIO")
            self.windows_helper.sleep_with_timeout(10)
            self.adb_driver.execute_command("shell am start -n com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.Launcher")
            self.start_logcat_capture()
            # self.device_info = {}
            # self.populate_device_info()
            self.firmware_launch_time = None
        except Exception as e :
            Logger.error("Exception caught when initializing. " + str(e))
        

    def cleanup(self):
        try:
            Logger.info ("Trying to stop logcat reader")
            self.logcat_reader.stop()
            Logger.info ("Stopped logcat reader")
            Logger.info ("Trying to stop perfcollector")
            self.perf_collector.stop()
            Logger.info ("Stopped perfcollector")
        
        except Exception as e:
            Logger.error("Exception caught when cleaning up driver. "+ str(e))
    ## Utilities ##


    def reset_app(self):
        self.adb_driver.execute_command("shell pm clear com.microsoft.skype.teams.ipphone")

    def install_apk(self, apk_path):
        for file in os.listdir(apk_path):
            if file.endswith(".apk"):
                apk_path = os.path.join(apk_path, file)
        Logger.info ("Before : apk_path "+ apk_path)
        apk_path = apk_path.replace('\\',"\\\\")
        Logger.info ("After : apk_path "+ apk_path)
        self.adb_driver.execute_command("install -r -d "  + apk_path)
        self.adb_driver.execute_command("shell am start -n com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.Launcher")

    def populate_device_info(self):
        try:
            device_info = {}
            cmd = 'shell getprop ro.build.version.release'
            device_info['android-version'] =self.adb_driver.execute_command(cmd).strip()
            cmd = 'shell getprop ro.product.device'
            device_info['model'] =self.adb_driver.execute_command(cmd).strip()
            cmd = 'shell "dumpsys package com.microsoft.skype.teams.ipphone | grep versionName "'
            device_info['teams-app-version'] =self.adb_driver.execute_command(cmd).splitlines()[0].split('\r')[0].strip()
            cmd = 'shell "dumpsys package com.microsoft.windowsintune.companyportal | grep versionName "'
            device_info['company-portal-version'] =self.adb_driver.execute_command(cmd).splitlines()[0].split('\r')[0].strip()
            return device_info

        except Exception as e:
            Logger.error("Exception caught when populating device info." + str(e))

    def get_perf_data(self):

        perf_data = {}
        try:
            perf_data = self.logcat_reader.get_perf_data()
            perf_data["cpu"] = self.perf_collector.get_collected_cpu_data()
            perf_data["device_info"] = self.populate_device_info()
            if self.firmware_launch_time is not None :
                perf_data["firmware_launch_time"] = self.firmware_launch_time
            Logger.info("Perf data, " + str(perf_data))
        except Exception as e:
            Logger.error("Exception getting perf data . "+ str(e))
        finally:
            return perf_data

    def reset_perf_data(self):
        try:
            self.logcat_reader.reset_perf_data()
            self.perf_collector.reset_cpu_data()
            Logger.info("PERF RESET was successful.")
        except Exception as e:
            Logger.error("Exception resetting perf data. " + str(e))
        
    def get_app_launch_time(self):
        self.logcat_reader.getAppLaunchTime()

    def start_logcat_capture(self):
        self.logcat_reader = LogcatThread(self.udid, Logger.LoggingDir)
        self.logcat_reader.start()
        self.perf_collector = PerfCollection(self.udid)
        self.perf_collector.start()

    def is_memory_critical(self):
        return self.perf_collector.is_memory_critical()

    def clear_text_in_element(self, element):
        # Logger.info("Clear text from app!")
        # #Logger.info ("TBD Not clearing text")
        # cmd = 'shell getprop ro.build.version.release'
        # android_version = self.adb_driver.execute_command(cmd).strip()
        # element.clear()
        # if ("7.1.2" in android_version):
        #     Logger.error("Element.clear() doesnt't work on android > 7")
        #     text = element.text
        #     Logger.error("Before Text : "+ text + " lenght :" + str(len(text)))
        #     if text is not None and len(text) == 1:
        #         cmd = "shell input keyevent KEYCODE_DEL"
        #         self.adb_driver.execute_command(cmd)
        #         text = element.text
        #         Logger.error("Text length : " + str(len(text)))
        #         Logger.error("Before Text : "+ text + " length :" + str(len(text)))

    def click_element(self, element):
        try:
            element.click()
        except Exception as e:
            Logger.error("Error clicking element : " + str(e))

    def scroll(self, direction):
        self.wakeup_device()
        width, height = self.get_window_size()

        start_x = width * direction['startX']
        end_x = width * direction['endX']

        start_y = height * direction['startY']
        end_y = height * direction['endY']

        swipe_cmd = "shell input swipe " + str(start_x) + " " + str(start_y) + " "+ str(end_x) + " " + str(end_y) + " 500"
        #self.test_driver.swipe(start_x, start_y, end_x, end_y, 500)
        self.adb_driver.execute_command(swipe_cmd)
    
    def wakeup_device(self):
        screen_state = self.adb_driver.execute_command(ADBCommands.screenStateCommand)
        Logger.info("screen_state : "+ screen_state)
        ## If teams app in dreaming state (screensaver mode) , then tap at random position to wakeup device) ##
        if "dreaming" in screen_state.lower() :
            self.adb_driver.execute_command(ADBCommands.randomTapCommand)
            self.windows_helper.sleep_with_timeout(10)
            screen_state = self.adb_driver.execute_command(ADBCommands.screenStateCommand)
            Logger.info("screen_state after tap: "+ screen_state)

        if "awake" not in screen_state.lower() :
            self.adb_driver.execute_command(ADBCommands.powerCommand)
            self.windows_helper.sleep_with_timeout(10)        

    def get_window_size(self):
        if self.window_size is None:
            try:
                self.window_size = self.test_driver.get_window_size()
            except:
                Logger.warning("Cannot get window size")

        self.original_window_size = self.window_size

        return self.window_size["width"], self.window_size["height"]

    def get_ui_element_filename(self, ui_element_map):
        filename = 'unknown'
        if 'accessibility_id' in ui_element_map:
            filename = ui_element_map['accessibility_id']
        elif 'text' in ui_element_map:
            filename = ui_element_map['text']
        return filename + '.xml'

    def wait_for_element(self, ui_element_map, multiple=False, retries=16, verbose_mode=False):
        self.wakeup_device()
        if multiple:
            Logger.info("Waiting for elements: "+ str(ui_element_map)+" to get visible")
        else:
            Logger.info("Waiting for the element:"+ str(ui_element_map)+" to get visible")
        element = None
        for i in range(retries):
            try:
                Logger.info("Attempt: "+ str(i + 1))
                self.wakeup_device()
                element = self.find_element(
                    ui_element_map, multiple)
                if element is None :
                    raise Exception("No elements found")
                if multiple is False:
                    Logger.info("Element Visible")
                elif multiple is True and  len(element) == 0:
                    raise Exception("No elements found")
                break
            except Exception as e:
                Logger.info("Attempt "+ str(i + 1)+" Failed: "+ str(e))
            finally :
                self.windows_helper.sleep_with_timeout(1)
        if (element is None) :
            self.take_screenshot("ERROR_finding_element")
        return element

    def is_element_present(self,ui_element_map,multiple=False):
        self.wakeup_device()
        element_timeout = 10
        self.take_screenshot("Is_Element_Present")
        try:
            if 'command' in ui_element_map:
                Logger.info("is_element_present : Inside command")
                cmd = ui_element_map['command']
                try:
                    if multiple:
                        return self.test_driver.find_elements_by_android_uiautomator(cmd) is not None
                    else:
                        return self.test_driver.find_element_by_android_uiautomator(cmd) is not None
                except:
                    Logger.warning("Element "+ str(ui_element_map) + " not found")
        except :
            self.take_screenshot("ERROR_finding_element")
            Logger.warning("Element "+ str(ui_element_map) + " not found")

        if 'id' in ui_element_map:
            try:
                Logger.info("is_element_present : Inside id")
                element_id = ui_element_map['id']
                cmd = "new UiSelector().resourceId(\"{0}\")".format(element_id)
                if multiple:
                    return self.test_driver.find_elements_by_android_uiautomator(cmd) is not None
                else:
                    return self.test_driver.find_element_by_android_uiautomator(cmd) is not None
            except Exception as e:
                Logger.error("is_element_present : Exception getting id element : "+ str(ui_element_map) +"Exception message : " + str(e))
                return False

        if 'accessibility_id' in ui_element_map and ui_element_map['accessibility_id'] != "":
            try:
                element_id = ui_element_map['accessibility_id']
                if multiple:
                    return self.test_driver.find_elements_by_accessibility_id(element_id) is not None
                else:
                    return self.test_driver.find_element_by_accessibility_id(element_id) is not None
            except:
                return False

        if 'text' in ui_element_map and ui_element_map['text'] != "":
            try:
                command = u"new UiSelector().text(\"{0}\")".format(ui_element_map['text'])
                if multiple:
                    return self.test_driver.find_elements_by_android_uiautomator(command) is not None
                else:
                    return self.test_driver.find_element_by_android_uiautomator(command) is not None
            except:
                return False

        if 'xpath' in ui_element_map:
            try:
                selector = (By.XPATH, ui_element_map['xpath'])
                if multiple:
                    return self.test_driver.find_elements(*selector)
                else:
                    element = self.test_driver.find_element(*selector)
                    WebDriverWait(self.test_driver, element_timeout).until(
                        EC.visibility_of_element_located(selector))
                    return element is not None
            except:
                return False
        return False
        
    def find_element(self, ui_element_map, multiple=False):
        element_timeout = 10
        self.wakeup_device()
        if 'command' in ui_element_map:
            cmd = ui_element_map['command']
            try:
                if multiple:
                    #find_elements - for multiple elments execution
                    return self.test_driver.find_elements_by_android_uiautomator(cmd)
                else:
                    return self.test_driver.find_element_by_android_uiautomator(cmd)
            except:
                pass

        if 'id' in ui_element_map:
            try:
                element_id = ui_element_map['id']
                cmd = "new UiSelector().resourceId(\"{0}\")".format(element_id)
                if multiple:
                    return self.test_driver.find_elements_by_android_uiautomator(cmd)
                else:
                    return self.test_driver.find_element_by_android_uiautomator(cmd)
            except:
                pass

        if 'accessibility_id' in ui_element_map and ui_element_map['accessibility_id'] != "":
            try:
                element_id = ui_element_map['accessibility_id']
                if multiple:
                    return self.test_driver.find_elements_by_accessibility_id(element_id)
                else:
                    return self.test_driver.find_element_by_accessibility_id(element_id)
            except:
                pass

        if 'text' in ui_element_map and ui_element_map['text'] != "":
            try:
                command = u"new UiSelector().text(\"{0}\")".format(ui_element_map['text'])
                if multiple:
                    return self.test_driver.find_elements_by_android_uiautomator(command)
                else:
                    return self.test_driver.find_element_by_android_uiautomator(command)
            except:
                pass

        if 'xpath' in ui_element_map:
            try:
                selector = (By.XPATH, ui_element_map['xpath'])
                if multiple:
                    return self.test_driver.find_elements(*selector)
                else:
                    element = self.test_driver.find_element(*selector)
                    WebDriverWait(self.test_driver, element_timeout).until(
                        EC.visibility_of_element_located(selector))
                    return element
            except:
                pass
        Logger.error("ERROR_finding_element : "+ str(ui_element_map))
        self.take_screenshot("ERROR_finding_element")
        raise Exception("Could not find element")

    def take_screenshot (self, name):
        try:
            self.adb_driver.execute_command(" shell screencap -p /data/local/temp.png")
            directory = Logger.LoggingDir+"screenshots/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            currentTime = time.strftime("%Y%m%d-%H%M%S")
            self.adb_driver.execute_command(" pull  /data/local/temp.png "+ directory +name+"_"+currentTime+".png")
            self.adb_driver.execute_command(" shell rm /data/local/temp.png")
        except Exception as e :
            Logger.error("Exception caught when taking screenshot : " + str(e))

    def hide_keyboard(self):
        hide_keyboard_cmd = 'shell input keyevent KEYCODE_ESCAPE'
        self.adb_driver.execute_command(hide_keyboard_cmd)
        for _ in range(3):
            if not self.is_android_keyboard_present():
                return
            self.windows_helper.sleep_with_timeout(1)

    def is_android_keyboard_present(self):
        keyboard_present_cmd = 'shell "dumpsys input_method | grep mInputShown"'
        keyboard_presence = "mInputShown=true"
        if keyboard_presence in self.adb_driver.execute_command(keyboard_present_cmd):
            return True
        else:
            return False

    def type_text_in_companyportal_element (self, element, text, editable=False):
        block_size = 500
        for _ in range(3):
            Logger.info("In type_text_in_element before is_android_keyboard_present")
            text = self.sanitize_adb_text_input(text)
            Logger.info("In type text. sanitized text :" + text)
            text_length = len(text)
            if text_length < block_size:
                self.wakeup_device()
                self.adb_driver.execute_command("shell input keyboard text \"{0}\"".format(text))
            else:
                for _ in range(0, text_length, block_size):
                    self.adb_driver.execute_command("shell input keyboard text \"{0}\"".format(text[_:_+block_size]))
            return

    def type_text_in_element(self, element, text, editable=False):
        block_size = 500
        Logger.info("In type_text_in_element before click")
        element.click()
        Logger.info("In type_text_in_element after click")
        for _ in range(3):
            Logger.info("In type_text_in_element before is_android_keyboard_present")
            if self.is_android_keyboard_present():
                text = self.sanitize_adb_text_input(text)
                Logger.info("In type text. sanitized text :" + text)
                text_length = len(text)
                if text_length < block_size:
                    if editable is True:
                        current = element.text
                        Logger.info("BEFORE typing text " + current)
                        if (len(current) == 1):                            
                            cmd = "shell input keyevent KEYCODE_DEL"
                            self.adb_driver.execute_command(cmd)
                            current = element.text
                            Logger.info("AFTER deleting extra letter " + current)
                    self.adb_driver.execute_command("shell input keyboard text \"{0}\"".format(text))
                else:
                    for _ in range(0, text_length, block_size):
                        self.adb_driver.execute_command("shell input keyboard text \"{0}\"".format(text[_:_+block_size]))
                return
            self.windows_helper.sleep_with_timeout(1)
        element.send_keys(text)

    def get_text_of_element(self, element):
        return element.get_attribute("name")

    def sanitize_adb_text_input(self, text):
        text = text.replace(';', r'\;')
        text = text.replace('*', r'\*')
        text = text.replace(' ', '')
        text = text.replace('(', r'\(')
        text = text.replace(')', r'\)')
        return text

    def reboot(self):
        self.adb_driver.execute_command(" reboot")
        begin_reboot = datetime.datetime.now()
        Logger.info("Issued reboot command. waiting for app to launch.")
        activity = self.get_current_focused_activity()
        while(activity is not None and "ipphone" not in activity):
            self.windows_helper.sleep_with_timeout(1)
            activity = self.get_current_focused_activity()
        launched_time = datetime.datetime.now()
        Logger.info("App launch detected at : " + str(launched_time))
        Logger.info("Begin reboot at : " + str(begin_reboot))
        Logger.info("App launch took : " + str(launched_time-begin_reboot))
        self.firmware_launch_time = (launched_time-begin_reboot).total_seconds()

    def get_current_focused_activity(self):
        return self.adb_driver.execute_command(' shell "dumpsys activity activities | grep mFocusedActivity"')

    def exit_partner_settings(self):
        while ("microsoft" not in self.get_current_focused_activity()):
            self.adb_driver.execute_command(' shell input keyevent KEYCODE_BACK')
            self.windows_helper.sleep_with_timeout(1)

    def send_enter_key(self):
        self.adb_driver.execute_command(' shell input keyevent KEYCODE_ENTER')

    def send_new_key(self):
        pass
