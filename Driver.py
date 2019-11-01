from appium import webdriver
import time
import os
import json
from DriverUtilities import DriverUtilities
from Logger import Logger
from enums import Scroll, NavigationWindows
from pprint import pprint
import subprocess
import copy
from WindowsCmdHelper import WindowsCmdHelper


class Driver():
    def __init__(self, udid, appium_port):
        try:
            self.windows_helper = WindowsCmdHelper()
            self.appium_process = None
            Logger.info("START init driver")
            Logger.info("Starting appium!")
            self.start_appium(appium_port)
            Logger.info("Launched appium successfully!")
            self.setup_driver_settings(udid, appium_port)
            self.test_driver = self.initialize_web_driver()
            self.driver_utilities = DriverUtilities(self.test_driver, self.udid)
            self.populate_hash_map()
            Logger.info("END init driver")
        except Exception as e:
            Logger.error("Exception when initializing driver " + str(e))
            self.cleanup()

    # Start appium via command line
    def start_appium(self, appium_port):
        Logger.info("Trying to start appium in port " + appium_port)
        self.appium_process = subprocess.Popen('appium -p {} -bp {}'.format(appium_port, str(int(appium_port) + 1)),
                                               shell=True)
        Logger.info("Started appium process. PID : " + str(self.appium_process.pid))

    def stop_appium(self):
        Logger.info("Trying to stop appium ")
        if self.appium_process and (self.appium_process.poll() is None):
            killcmd = 'taskkill /f /T /PID %s' % self.appium_process.pid
            os.system(killcmd)
            self.appium_process = None
            Logger.info("Killed appium process")
        Logger.info("stopped appium successfully ")

    # Appium specific parameters
    def get_appium_capabilities(self):
        desired_caps = {'platformName': 'Android',
                        'deviceName': 'Android',
                        'newCommandTimeout': 90000,
                        'fullReset': False,
                        'noReset': True, 'autoLaunch': True,
                        'ignoreUnimportantViews': True,
                        'disableAndroidWatchers': True,
                        'udid': self.udid,
                        'appPackage': self.app_id,
                        'appActivity': self.app_main_activity}
        return desired_caps

    def setup_driver_settings(self, udid, appium_port):
        Logger.info("START setup_driver_settings")
        self.driver_args = {'platform': 'android',
                            'appium_port': appium_port,
                            'appium_host': 'http://127.0.0.1',
                            'app_id': 'com.microsoft.skype.teams.ipphone',
                            'app_main_activity': 'com.microsoft.skype.teams.Launcher',
                            'app_name': 'Microsoft Teams',
                            'encrypted_htrace': 'com.microsoft.skype.teams.dev.blog',
                            'optional_intent_arguments': '--ez showAlwaysFullscreenNotificationForCall true --ez hideTinyDancer true '
                                                         '--ez disableAlwaysInCallOptionsAnimation true'}
        # If connected to ADB via IP address add port 5555
        if '.' in udid:
            udid = udid + ':5555'
        self.udid = udid
        self.app_id = self.driver_args['app_id']
        self.app_main_activity = self.driver_args['app_main_activity']
        self.app_name = self.driver_args['app_name']
        self.appium_host = self.driver_args['appium_host']
        self.appium_port = self.driver_args['appium_port']
        self.appium_url = "{h}:{p}/wd/hub".format(h=self.appium_host, p=self.appium_port)
        Logger.info("END setup_driver_settings")

    def initialize_web_driver(self):
        Logger.info("START initialize_web_driver")
        test_driver = None
        last_error = ''
        # retries = 40
        retries = 2
        for i in range(retries):
            try:
                test_driver = webdriver.Remote(self.appium_url, self.get_appium_capabilities())
                Logger.info("wd:" + str(test_driver))
                if test_driver is not None:
                    Logger.info("Connected to Server")
                    break
            except Exception as appium_exception:
                last_error = appium_exception
                self.windows_helper.sleep_with_timeout(1)
                Logger.error("AppiumFailure" + str(appium_exception))
                if hasattr(appium_exception, 'msg'):
                    if 'MainActivity never started' in appium_exception.msg:
                        raise Exception('Application possibly crashed on start')
            if (i + 1) == retries:
                Logger.error("AppiumFailure. Retries exhausted." + str(appium_exception))
                raise Exception("Cannot connect to Appium Server, Maximum retries {0} reached" \
                    "last error failed with message : {1}".format(retries, str(last_error)))
        Logger.info("END initialize_web_driver")
        return test_driver

    def populate_hash_map(self):
        Logger.info("START populate_hash_map")
        ui_path = os.path.join(os.getcwd(), "ui_hash_map.json")
        if os.path.exists(ui_path):
            self.ui_hash_map = self.init_hash_map(ui_path)
            Logger.info("Populating UI HASH MAP succeeded")
        else:
            Logger.error("Populating UI HASH MAP failed. Cannot find path to .json")
            self.ui_hash_map = None
        Logger.info("END populate_hash_map")

    def init_hash_map(self, location):
        Logger.info("START Read ui json")
        with open(location) as data_file:
            data = json.load(data_file)
            Logger.info("END Read ui json")
            return data

    def get_perf_data(self):
        Logger.info("START get_perf_data")
        perf_data = self.driver_utilities.get_perf_data()
        print(str(perf_data))
        Logger.info("END get_perf_data")
        return perf_data

    def reset_perf_data(self):
        Logger.info("START reset_perf_data")
        self.driver_utilities.reset_perf_data()
        Logger.info("END reset_perf_data")

    def cleanup(self):
        Logger.info("START cleanup driver")
        Logger.info("Utilties cleanup start")
        self.driver_utilities.cleanup()
        Logger.info("Utilties cleanup end")
        if self.test_driver is not None:
            try:
                Logger.info("Trying to quit test driver")
                self.test_driver.quit()
                Logger.info("Trying to quit test driver")
            except Exception as e:
                self.test_driver = None
                Logger.error("Cannot quit webdriver :" + str(e))
        self.stop_appium()
        Logger.info("END cleanup driver")

    def install_apk(self, apk_path):
        Logger.info("START install_apk")
        self.driver_utilities.install_apk(apk_path)
        Logger.info("END install_apk")

    def is_memory_critical(self):
        return self.driver_utilities.is_memory_critical()

    ## API ##

    def navigate_home(self):
        Logger.info("START navigate_home")
        Logger.info("Is back button present ? ")
        Logger.info(str(self.driver_utilities.is_element_present(self.ui_hash_map['navigate_back'])))
        while (self.driver_utilities.is_element_present(self.ui_hash_map['navigate_back'])):
            navigate_back = self.driver_utilities.wait_for_element(
                self.ui_hash_map['navigate_back'])
            self.driver_utilities.click_element(navigate_back)
            self.windows_helper.sleep_with_timeout(2)
        while (self.driver_utilities.is_element_present(self.ui_hash_map['signin_back_button'])):
            navigate_back = self.driver_utilities.wait_for_element(
                self.ui_hash_map['signin_back_button'])
            self.driver_utilities.click_element(navigate_back)
            self.windows_helper.sleep_with_timeout(2)
            self.windows_helper.sleep_with_timeout(2)

        Logger.info("END navigate_home")
        return True

    def navigate_to_main_call_page(self):
        Logger.info("START navigate_to_main_call_page")
        # Click on call banner
        element = self.driver_utilities.wait_for_element(
            self.ui_hash_map['call_banner'], False, 20)
        self.driver_utilities.click_element(element)
        self.windows_helper.sleep_with_timeout(2)
        Logger.info("END navigate_to_main_call_page")

    def login(self, username, password, shared=False):
        Logger.info("START login")
        if (not self.is_signed_in()):
            self.driver_utilities.take_screenshot("before_login")
            # wait for the Signin button to appear
            welcome_sigin_element = self.driver_utilities.wait_for_element(
                self.ui_hash_map['welcome_signin_button'], False, 20)
            self.driver_utilities.click_element(welcome_sigin_element)

            self.windows_helper.sleep_with_timeout(5)
            # wait for the username to appear
            username_field = self.driver_utilities.wait_for_element(
                self.ui_hash_map['first_time_username'], False, 20)
            self.driver_utilities.take_screenshot("before_username")
            if (username_field is not None):

                # make sure the username field is empty.
                self.driver_utilities.clear_text_in_element(username_field)

                self.driver_utilities.hide_keyboard()

                next_element = self.driver_utilities.wait_for_element(
                    self.ui_hash_map['first_time_submit'])

                self.driver_utilities.click_element(next_element)

            else:  ## Company portal flow ##
                Logger.info("Company portal signin  flow - signin")
                # wait for the username to appear
                username_field = self.driver_utilities.wait_for_element(
                    self.ui_hash_map['cp_username'], False, 20)
                self.driver_utilities.click_element(username_field)
                self.driver_utilities.type_text_in_companyportal_element(username_field, username, True)
                self.wakeup_device()
                self.driver_utilities.send_enter_key()

            self.driver_utilities.take_screenshot("after_username")

            password_field = self.driver_utilities.wait_for_element(
                self.ui_hash_map['company_portal'], False, 20)

            if (password_field is None):

                password_field = self.driver_utilities.wait_for_element(
                    self.ui_hash_map['main_password'], False, 20)
                # set the password
                self.driver_utilities.type_text_in_element(password_field, password)

                self.driver_utilities.hide_keyboard()

                # Find and then click the signin button
                signin_element = self.driver_utilities.wait_for_element(
                    self.ui_hash_map['main_submit'], False, 20)

                self.driver_utilities.click_element(signin_element)

            else:  ## Company portal flow ##
                Logger.info("Company portal signin  flow - password")
                self.windows_helper.sleep_with_timeout(10)
                self.wakeup_device()
                self.driver_utilities.take_screenshot("before_password")
                self.driver_utilities.type_text_in_companyportal_element(password_field, password, False)
                self.wakeup_device()
                self.driver_utilities.send_enter_key()

            self.driver_utilities.take_screenshot("after_password")

            target = self.ui_hash_map['calls_title']
            if (shared == True):
                target = self.ui_hash_map['sliding_menu']
            iterations = 200
            current_iteration = 1
            while (not (self.driver_utilities.is_element_present(target))):
                try:
                    if (self.driver_utilities.is_element_present(self.ui_hash_map['fre_button'])):
                        action_button = self.driver_utilities.wait_for_element(
                            self.ui_hash_map['fre_button'], False, 20)
                        self.driver_utilities.click_element(action_button)

                    if (self.driver_utilities.is_element_present(self.ui_hash_map['fre_last_button'])):
                        action_button = self.driver_utilities.wait_for_element(
                            self.ui_hash_map['fre_last_button'], False, 20)
                        self.driver_utilities.click_element(action_button)

                    # Check for account type selection alert
                    if (self.driver_utilities.is_element_present(self.ui_hash_map['account_type_alert'])):
                        if (shared == True):
                            action_button = self.driver_utilities.wait_for_element(
                                self.ui_hash_map['account_type_shared'])
                        else:
                            action_button = self.driver_utilities.wait_for_element(
                                self.ui_hash_map['account_type_personal'])
                        self.driver_utilities.click_element(action_button)
                        action_button = self.driver_utilities.wait_for_element(self.ui_hash_map['account_type_confirm'])
                        self.driver_utilities.click_element(action_button)

                except Exception as e:
                    Logger.error("Cannot locate " + str(target) + str(e))
                finally:
                    self.windows_helper.sleep_with_timeout(1)
                    if (current_iteration == iterations):
                        Logger.error("Retries for login exhausted")
                        return
                    current_iteration = current_iteration + 1
            self.windows_helper.sleep_with_timeout(60)
            if (shared == True):
                assert not self.driver_utilities.is_element_present(self.ui_hash_map['calls_title'])

            ## Check if default tab is displayed
            self.driver_utilities.take_screenshot("after_login")

        Logger.info("END login")

    def take_screenshot(self, name="default"):
        Logger.info("START take_screenshot")
        self.driver_utilities.take_screenshot(name)
        Logger.info("END take_screenshot")

    def call_first_call_log_item(self):
        Logger.info("START call_first_call_log_item")
        self.navigate_to_page(NavigationWindows.CallsWindow)
        self.windows_helper.sleep_with_timeout(5)
        action_button = self.driver_utilities.wait_for_element(self.ui_hash_map['first_view_item'])
        self.driver_utilities.click_element(action_button)
        audio_call_chat = self.driver_utilities.wait_for_element(self.ui_hash_map['call_from_call_log'])
        self.driver_utilities.click_element(audio_call_chat)
        Logger.info("END call_first_call_log_item")

    def is_signed_in(self):
        self.windows_helper.sleep_with_timeout(10)
        Logger.info("START is_signed_in")
        self.take_screenshot("is_signed_in")
        target = self.ui_hash_map['welcome_signin_button']
        if (self.driver_utilities.is_element_present(target)):
            Logger.info("Device is not signed in")
            return False
        Logger.info("Device is signed in")
        Logger.info("END is_signed_in")
        return True

    def signout(self):
        Logger.info("START signout")
        if (self.is_signed_in() == True):
            self.navigate_home()
            self.open_sliding_menu()
            # self.navigate_more_settings()
            if self.scroll_to_signout() is False:
                raise Exception("Could not find sign out button!")
            # Seccond profile button is in the confirmation modal, we need to click
            # it also
            sign_out_confirm = self.driver_utilities.wait_for_element(
                self.ui_hash_map['profile_window_signout_confirm'])
            self.driver_utilities.click_element(sign_out_confirm)
        Logger.info("END signout")

    def select_user(self, user_name):
        Logger.info("START select_user")

        # Type user name on search field
        self.driver_utilities.wait_for_element(
            self.ui_hash_map['search_textfield'])
        enterusername = self.driver_utilities.find_element(
            self.ui_hash_map['search_textfield'])
        enterusername.send_keys(user_name)

        # Replace xpath ['command']  with receiver user name
        uiHashMap = copy.deepcopy(self.ui_hash_map['user_popup'])
        uiHashMap["command"] = uiHashMap["command"].replace("userName", user_name)

        # Select user
        select_user = self.driver_utilities.wait_for_element(
            uiHashMap)
        self.driver_utilities.click_element(select_user)
        Logger.info("END select_user")

    def search_user(self, user_name):
        Logger.info("START search_user")
        self.driver_utilities.wait_for_element(
            self.ui_hash_map['search_button'])
        enterusername = self.driver_utilities.find_element(
            self.ui_hash_map['search_button'])
        self.driver_utilities.type_text_in_element(enterusername, user_name)
        self.windows_helper.sleep_with_timeout(3)
        self.driver_utilities.hide_keyboard()
        select_participant = self.driver_utilities.wait_for_element(self.ui_hash_map['search_result'])
        self.driver_utilities.click_element(select_participant)
        self.windows_helper.sleep_with_timeout(3)
        Logger.info("END search_user")

    def search_and_start_a_audio_call(self, user_name):
        Logger.info("START search_and_start_a_audio_call")

        # Tap on search button
        clickonsearch = self.driver_utilities.wait_for_element(
            self.ui_hash_map['search_button'])
        self.driver_utilities.click_element(clickonsearch)

        self.select_user(user_name)

        # Given, the user search result window is open, Tap on audio call button
        audio_call_chat = self.driver_utilities.wait_for_element(
            self.ui_hash_map['audiocall_button_ipphone'])
        self.driver_utilities.click_element(audio_call_chat)
        Logger.info("END search_and_start_a_audio_call")

    def accept_call(self):
        Logger.info("START accept_call")
        call_window_accept_video_call = self.driver_utilities.wait_for_element(
            self.ui_hash_map['call_window_accept_video_call'])
        self.driver_utilities.click_element(call_window_accept_video_call)
        Logger.info("END accept_call")

    def is_on_call(self):
        Logger.info("START is_on_call")
        self.take_screenshot("check_if_on_call")
        is_call_ongoing = self.driver_utilities.is_element_present(self.ui_hash_map['call_window_reject_call'])
        Logger.info("is_on_call :" + str(is_call_ongoing))
        Logger.info("END is_on_call")
        return is_call_ongoing

    def end_call(self):
        Logger.info("START end_call")
        if (self.is_on_call()):
            call_window_reject_call = self.driver_utilities.wait_for_element(
                self.ui_hash_map['call_window_reject_call'])
            self.driver_utilities.click_element(call_window_reject_call)

            # for closing the rating screen which appears randomly
            try:
                call_window_close_rating = self.driver_utilities.wait_for_element(
                    self.ui_hash_map['call_window_close_rating'])
                self.driver_utilities.click_element(call_window_close_rating)
            except:
                Logger.info("Cannot find rating screen")
                pass
        ## after hang up, make sure you are in home page ##
        self.navigate_home()
        Logger.info("END end_call")

    def open_sliding_menu(self):
        Logger.info("START open_sliding_menu")
        self.take_screenshot("before_open_slide_menu")
        settings = self.driver_utilities.wait_for_element(self.ui_hash_map['sliding_menu'], False, 10)
        self.driver_utilities.click_element(settings)
        self.take_screenshot("after_open_slide_menu")
        Logger.info("END open_sliding_menu")

    def navigate_more_settings(self):
        Logger.info("START navigate_more_settings")
        settings = self.driver_utilities.wait_for_element(self.ui_hash_map['settings_navigation'], False)
        self.driver_utilities.click_element(settings)
        Logger.info("END navigate_more_settings")

    def scroll_up(self):
        Logger.info("START scroll_up")
        self.driver_utilities.scroll(Scroll.Up)
        Logger.info("END scroll_up")

    def scroll_down(self):
        Logger.info("START scroll_down")
        self.driver_utilities.scroll(Scroll.Down)
        Logger.info("END scroll_down")

    def scroll_to_signout(self):
        Logger.info("START scroll_to_signout")
        # on mobile screens the signout button is at the bottom of the page
        # self.driver_utilities.scroll(Scroll.Down)
        # self.driver_utilities.scroll(Scroll.Down)

        retries = 15
        found_signout = False
        for _ in range(retries):
            try:
                # Looks for the sign out button in the profile window then clicks
                self.take_screenshot("search_signout_button")
                sign_out = self.driver_utilities.wait_for_element(
                    self.ui_hash_map["signout_button"], False, 3)
                self.driver_utilities.click_element(sign_out)
                found_signout = True
                break
            except:
                Logger.error("Need to scroll down even more..")
                self.driver_utilities.scroll(Scroll.Down)
        Logger.info("END scroll_to_signout")
        return found_signout

    def start_a_audio_call(self, recipients_auth_hash_maps=None):
        Logger.info("START start_a_audio_call")
        # Tap on audio call button
        audio_call_chat = self.driver_utilities.wait_for_element(
            self.ui_hash_map['audiocall_button_ipphone'])
        self.driver_utilities.click_element(audio_call_chat)
        Logger.info("END start_a_audio_call")

    def search_and_start_a_pstn_call(self, pstn_number):
        Logger.info("START search_and_start_a_pstn_call")

        # Tap on search button
        clickonsearch = self.driver_utilities.wait_for_element(
            self.ui_hash_map['fab_button'])
        self.driver_utilities.click_element(clickonsearch)

        clickonsearch = self.driver_utilities.wait_for_element(
            self.ui_hash_map['pstn_dialpad'])
        self.driver_utilities.click_element(clickonsearch)

        self.driver_utilities.type_text_in_companyportal_element(clickonsearch, pstn_number, False)

        # self.driver_utilities.hide_keyboard()

        audio_call_chat = self.driver_utilities.wait_for_element(
            self.ui_hash_map['pstn_call_phone'])

        self.driver_utilities.click_element(audio_call_chat)
        Logger.info("END search_and_start_a_pstn_call")

    def start_pstn_call_from_shared_mode(self, pstn_number):
        Logger.info("START start_pstn_call_from_shared_mode")
        clickonsearch = self.driver_utilities.wait_for_element(
            self.ui_hash_map['shared_mode_fab_button'])
        self.driver_utilities.click_element(clickonsearch)

        self.driver_utilities.type_text_in_companyportal_element(clickonsearch, pstn_number, False)

        audio_call_chat = self.driver_utilities.wait_for_element(
            self.ui_hash_map['pstn_call_phone'])

        self.driver_utilities.click_element(audio_call_chat)
        Logger.info("END start_pstn_call_from_shared_mode")

    def join_meeting(self, meeting_name):
        Logger.info("START Join Meeting")
        self.navigate_to_page(NavigationWindows.MeetingsWindow)

        meeting_item = self.ui_hash_map['t120_Meetings']
        meeting_item["xpath"] = meeting_item["xpath"].replace("t120 Meetings", meeting_name)
        # click on the first available t120 meeting
        t120_Meetings = self.driver_utilities.wait_for_element(
            meeting_item)
        self.driver_utilities.click_element(t120_Meetings)

        # check meeting name
        self.driver_utilities.is_element_present(meeting_item)

        # verify join button
        join_button = self.driver_utilities.wait_for_element(
            self.ui_hash_map['join_button'])

        # # verify if it is organizer
        # self.driver_utilities.is_element_present(self.ui_hash_map['organizer_for_meeting'])

        # # verify edit button that appears if the participant is organizer
        # self.driver_utilities.is_element_present(self.ui_hash_map['edit_button_in_meeting_details_page'])

        # # verify see description that appears if particpant details load
        # self.driver_utilities.wait_for_element(self.ui_hash_map['see_description_in_meeting_details_page'])

        # # verify participant summary
        # self.driver_utilities.is_element_present(self.ui_hash_map['t120_meeting_participant_summary'])

        # # check if chat link is present
        # self.driver_utilities.is_element_present(self.ui_hash_map['chat_link_in_meeting_details_page'])

        # # verify participant name
        # self.driver_utilities.is_element_present(self.ui_hash_map['t120_call_participant_name'])

        # # verify meeting date
        # meeting_date = self.driver_utilities.find_element(self.ui_hash_map['meeting_date'])
        # assert len(meeting_date.get_attribute('text')) > 0, "Expected to find date"

        # # verify meeting time
        # meeting_time = self.driver_utilities.find_element(self.ui_hash_map['meeting_time'])
        # assert len(meeting_time.get_attribute('text')) > 0, "Expected to find time"

        # joins the meeting
        self.driver_utilities.click_element(join_button)

        Logger.info("END Join Meeting")

    def add_participant_to_meeting(self, username, expected_displayname):
        Logger.info("BEGIN add_participant_to_meeting")
        # click on the roster
        element = self.driver_utilities.wait_for_element(
            self.ui_hash_map['show_Roaster'])
        self.driver_utilities.click_element(element)

        # click on add participant
        element = self.driver_utilities.wait_for_element(
            self.ui_hash_map['add_participant'])
        self.driver_utilities.click_element(element)
        self.driver_utilities.take_screenshot("add_participant")

        # Type user name on search field
        self.driver_utilities.wait_for_element(
            self.ui_hash_map['search_contact_box'])
        enterusername = self.driver_utilities.find_element(
            self.ui_hash_map['search_contact_box'])
        enterusername.send_keys(username)

        self.driver_utilities.hide_keyboard()

        # Replace xpath ['command']  with receiver user name
        uiHashMap = copy.deepcopy(self.ui_hash_map['user_popup'])
        Logger.info("Before replacing: " + str(uiHashMap))
        Logger.info("Add participant in driver: " + str(expected_displayname))
        uiHashMap["command"] = uiHashMap["command"].replace("userName", expected_displayname)

        Logger.info("After replacing: " + str(uiHashMap))
        # Select user
        select_user = self.driver_utilities.wait_for_element(
            uiHashMap)
        self.driver_utilities.click_element(select_user)
        self.driver_utilities.take_screenshot("select_user")

        # click on save
        element = self.driver_utilities.wait_for_element(
            self.ui_hash_map['save_contact'])
        self.driver_utilities.click_element(element)
        self.driver_utilities.take_screenshot("save_contact")

        self.navigate_to_main_call_page()

        Logger.info("END Join add_participant_to_meeting")

    def navigate_to_page(self, to_window):
        Logger.info("BEGIN navigate_to_page")
        if to_window == NavigationWindows.CallsWindow:
            calls = self.driver_utilities.wait_for_element(
                self.ui_hash_map['calls_title'], False)
            self.driver_utilities.click_element(calls)
        elif to_window == NavigationWindows.MeetingsWindow:
            meetings = self.driver_utilities.wait_for_element(
                self.ui_hash_map['meetings_title'], False)
            self.driver_utilities.click_element(meetings)
        elif to_window == NavigationWindows.VoicemailsWindow:
            voicemails = self.driver_utilities.wait_for_element(
                self.ui_hash_map['voicemails_title'], False)
            self.driver_utilities.click_element(voicemails)
        else:
            raise Exception("Could not navigate to page what we expected to do")
        Logger.info("BEGIN navigate_to_page")

    def wakeup_device(self):
        Logger.info("BEGIN wakeup_device")
        self.driver_utilities.wakeup_device()
        Logger.info("END wakeup_device")

    def is_on_hold(self):
        Logger.info("BEGIN is_on_hold")
        ## The below element will be displayed if the call is on hold ##
        hold_status = self.driver_utilities.is_element_present(self.ui_hash_map['hold_text'])
        Logger.info("Hold status : " + str(hold_status))
        Logger.info("END is_on_hold")
        return hold_status

    def is_held_by(self, holder_tag):
        Logger.info("BEGIN is_held_by")
        ## The below element will be displayed if the call is on hold ##
        hold_status = self.driver_utilities.is_element_present(self.ui_hash_map['held_text'])
        Logger.info("Hold status : " + str(hold_status))
        self.take_screenshot("held_status")
        Logger.info("END is_held_by")
        return hold_status

    def is_muted(self):
        Logger.info("BEGIN is_muted")
        ## The below element will be displayed if the call is on mute ##
        mute_status = self.driver_utilities.is_element_present(self.ui_hash_map['call_window_unmute_call'])
        Logger.info("Mute status : " + str(mute_status))
        Logger.info("END is_muted")
        return mute_status

    def mute_call(self):
        Logger.info("BEGIN mute_call")
        mute_status = self.is_muted()
        ## Do nothing if already in muted state
        if mute_status == False:
            element = self.driver_utilities.wait_for_element(
                self.ui_hash_map['call_window_mute_call'])
            self.driver_utilities.click_element(element)
            self.windows_helper.sleep_with_timeout(10)
        Logger.info("END mute_call")

    def unmute_call(self):
        Logger.info("BEGIN unmute_call")
        mute_status = self.is_muted()
        ## Do nothing if already in unmuted state
        if mute_status == True:
            element = self.driver_utilities.wait_for_element(
                self.ui_hash_map['call_window_unmute_call'])
            self.driver_utilities.click_element(element)
            self.windows_helper.sleep_with_timeout(10)
        Logger.info("END unmute_call")

    def hold_call(self):
        Logger.info("BEGIN hold_call")
        hold_status = self.is_on_hold()
        ## Do nothing if already in hold state
        if hold_status == False:
            self.click_on_call_more_option()
            hold_call = self.driver_utilities.wait_for_element(
                self.ui_hash_map['place_call_on_hold'])
            self.driver_utilities.click_element(hold_call)
            self.windows_helper.sleep_with_timeout(10)
        Logger.info("END hold_call")

    def resume_call(self):
        Logger.info("BEGIN resume_call")
        hold_status = self.is_on_hold()
        ## Do nothing if already resumed
        if hold_status == True:
            self.driver_utilities.is_element_present(self.ui_hash_map['hold_text'])
            unhold_call = self.driver_utilities.wait_for_element(
                self.ui_hash_map['resume_call'])
            self.driver_utilities.click_element(unhold_call)
            self.windows_helper.sleep_with_timeout(10)
        Logger.info("END resume_call")

    def blind_transfer_call(self, transfer_target):
        Logger.info("BEGIN blind_transfer_call")
        self.click_on_call_more_option()
        transfer_options = self.driver_utilities.wait_for_element(
            self.ui_hash_map['transfer_options'])
        self.driver_utilities.click_element(transfer_options)
        self.windows_helper.sleep_with_timeout(5)
        blind_transfer = self.driver_utilities.wait_for_element(
            self.ui_hash_map['transfer_options_blind'])
        self.driver_utilities.click_element(blind_transfer)
        self.windows_helper.sleep_with_timeout(5)

        # Type user name on search field
        self.driver_utilities.wait_for_element(
            self.ui_hash_map['search_contact_box'])
        enterusername = self.driver_utilities.find_element(
            self.ui_hash_map['search_contact_box'])
        enterusername.send_keys(transfer_target)

        # Replace xpath ['command']  with receiver user name
        uiHashMap = copy.deepcopy(self.ui_hash_map['user_popup'])
        Logger.info("Before replacing: " + str(uiHashMap))
        Logger.info("Transfer target in driver: " + str(transfer_target))
        uiHashMap["command"] = uiHashMap["command"].replace("userName", transfer_target)

        Logger.info("After replacing: " + str(uiHashMap))
        # Select user
        select_user = self.driver_utilities.wait_for_element(
            uiHashMap)
        self.driver_utilities.click_element(select_user)
        self.driver_utilities.take_screenshot("after_blind_Transfer")
        Logger.info("END blind_transfer_call")

    def start_consultation(self, transfer_target):
        Logger.info("BEGIN start_consultation")
        self.click_on_call_more_option()
        transfer_options = self.driver_utilities.wait_for_element(
            self.ui_hash_map['transfer_options'])
        self.driver_utilities.click_element(transfer_options)
        self.windows_helper.sleep_with_timeout(5)
        consult_transfer = self.driver_utilities.wait_for_element(
            self.ui_hash_map['transfer_options_consult'])
        self.driver_utilities.click_element(consult_transfer)
        self.windows_helper.sleep_with_timeout(5)

        # Type user name on search field
        self.driver_utilities.wait_for_element(
            self.ui_hash_map['search_contact_box'])
        enterusername = self.driver_utilities.find_element(
            self.ui_hash_map['search_contact_box'])
        enterusername.send_keys(transfer_target)

        # Replace xpath ['command']  with receiver user name
        uiHashMap = copy.deepcopy(self.ui_hash_map['user_popup'])
        Logger.info("Before replacing: " + str(uiHashMap))
        Logger.info("Transfer target in driver: " + str(transfer_target))
        uiHashMap["command"] = uiHashMap["command"].replace("userName", transfer_target)

        Logger.info("After replacing: " + str(uiHashMap))
        # Select user
        select_user = self.driver_utilities.wait_for_element(
            uiHashMap)
        self.driver_utilities.click_element(select_user)
        self.driver_utilities.take_screenshot("after_start_consultation")
        Logger.info("END start_consultation")

    def complete_consulation(self, transfer_target):
        Logger.info("BEGIN complete_consulation")
        complete_transfer = self.driver_utilities.wait_for_element(
            self.ui_hash_map['complete_consult_transfer'])
        self.driver_utilities.click_element(complete_transfer)
        self.windows_helper.sleep_with_timeout(2)
        complete_transfer = self.driver_utilities.wait_for_element(
            self.ui_hash_map['transfer_ok_button'])
        self.driver_utilities.click_element(complete_transfer)
        self.driver_utilities.take_screenshot("after_complete_consultation")
        Logger.info("END complete_consulation")

    def click_on_call_more_option(self):
        Logger.info("BEGIN click_on_call_more_option")

        # Look for the call more options button
        call_more_options = self.driver_utilities.wait_for_element(
            self.ui_hash_map['call_more_options'])

        # click on call more options button
        self.driver_utilities.click_element(call_more_options)
        Logger.info("END click_on_call_more_option")

    def reboot(self):
        Logger.info("START reboot")
        self.driver_utilities.reboot()
        Logger.info("END reboot")

    def get_app_launch_time(self):
        Logger.info("START get_app_launch_time")
        self.driver_utilities.get_app_launch_time()
        Logger.info("END get_app_launch_time")

    def get_current_focused_activity(self):
        Logger.info("START get_current_focused_activity")
        focused_activity = self.driver_utilities.get_current_focused_activity()
        Logger.info("Current focused activity : " + focused_activity)
        Logger.info("END get_current_focused_activity")
        return focused_activity

    def open_fre_partner_settings(self):
        Logger.info("START open_fre_partner_settings")

        ## Temporary: Settings page is in signin page. ##
        # wait for the Signin button to appear
        welcome_sigin_element = self.driver_utilities.wait_for_element(
            self.ui_hash_map['welcome_signin_button'], False, 20)
        self.driver_utilities.click_element(welcome_sigin_element)

        # Look for the fre settings
        fre_settings = self.driver_utilities.wait_for_element(
            self.ui_hash_map['fre_settings_button'])

        # click on fre settings
        self.driver_utilities.click_element(fre_settings)
        Logger.info("END open_fre_partner_settings")

    def reset_app(self):
        Logger.info("START reset_app")
        self.driver_utilities.reset_app()
        Logger.info("END reset_app")

    def exit_partner_settings(self):
        Logger.info("START exit_partner_settings")
        self.driver_utilities.exit_partner_settings()
        self.navigate_home()
        Logger.info("END exit_partner_settings")

