class Scroll(object):
    Down = {'direction': 'down', 'startX': 0,
            'endX': 0, 'startY': 0.8, 'endY': 0.15}
    Up = {'direction': 'up', 'startX': 0,
          'endX': 0, 'startY': 0.2, 'endY': 0.7}
    Left = {'direction': 'left', 'startX': 0,
            'endX': 0.8, 'startY': 0.5, 'endY': 0.5}
    Right = {'direction': 'right', 'startX': 0.8,
             'endX': 0, 'startY': 0.5, 'endY': 0.5}

class Page(object):
    Undefined = -1
    FRE_SCREEN = 0
    WELCOME_SCREEN = 1
    MAIN_SCREEN = 2
    PRECALL_SCREEN = 3
    INCALL_SCREEN = 4
    CALLRATING_SCREEN = 5
    MEETINGDETAIL_SCREEN = 6
    SETTINGS_SCREEN = 7
    PARTNER_SCREEN = 8,
    ACCT_SCREEN = 9,
    DIALCALL_SCREEN = 10


class NavigationWindows(object):
    MainWindow = 1
    MainWindowContactMenu = 3
    CaptureWindow = 4
    CaptureWindowCapturedPhoto = 5
    HighlightsWindow = 6
    HighlightsWindowMyHighlights = 7
    SendFeedbackWindow = 8
    SearchPeopleWindow = 9
    SearchSkypeWindow = 10
    # Profile
    ProfileWindow = 11
    ProfileWindowMyProfile = 12
    ProfileWindowAboutWindow = 13
    # Contact window
    ContactWindow = 14
    # Call window found in Main Window
    MainWindowCallWindow = 15
    CallMultiplePeopleWindow = 16
    CallWindowDialPadWindow = 17
   # Settings
    MoreWindow = 18
    MoreWindowSettings = 19
    MoreWindowSettingsSingOut = 20
    ChatWindow = 21
    TeamsWindow = 22
    ActivityWindow = 23
    MeetingsWindow = 24
    VoicemailsWindow = 25
    CallsWindow = 26

class ADBCommands(object):
    cpuInfoCommand = 'shell " top -n 1  | grep com.microsoft.skype.teams.ipphone"'
    processIDCommand = 'shell "ps | grep com.microsoft.skype.teams.ipphone"'
    memStateCommand = 'shell "dumpsys procstats com.microsoft.skype.teams.ipphone | grep running"'
    heapDumpCommand = 'shell am dumpheap com.microsoft.skype.teams.ipphone /data/heapdump.hprof'
    dumpPullCommand = 'pull /data/heapdump.hprof '
    heapDelCommand = 'shell rm /data/heapdump.hprof'
    memInfoCommand = 'shell " dumpsys meminfo com.microsoft.skype.teams.ipphone"'
    # memInfoCommand = 'shell " dumpsys meminfo com.microsoft.skype.teams.ipphone | grep \'Dalvik Heap\'"'
    bugReportCommand = 'bugreport'
    resetProcStatsCommand = 'shell dumpsys batterystats --reset'
    dateCommand = 'shell date'
    screenStatedroid4Command = 'shell "dumpsys power | grep mScreenOn"'
    screenStateCommand = 'shell "dumpsys power | grep mWakefulness="'
    powerCommand = 'shell input keyevent KEYCODE_POWER'
    randomTapCommand = 'shell input tap 200 200'

class Intents(object):
    MUTE_STATE_OFF=1
    MUTE_STATE_ON=2
    MISSED_CALL_STATE_ON=3
    MISSED_CALL_STATE_OFF=4
    INCOMING_CALL_STATE_ON=5
    INCOMING_CALL_STATE_OFF=6
    VOICEMAIL_PLAYING_ON_HEADSET=7
    VOICEMAIL_PLAYING_ON_HANDSET=8
    VOICEMAIL_PLAYING_ON_SPEAKER=9
    VOICEMAIL_PLAYING_OFF=10
    AUDIO_STATE_ON_HEADSET=11
    AUDIO_STATE_ON_HANDSET=12
    AUDIO_STATE_ON_SPEAKER=13
    AUDIO_STATE_OFF=14
    IN_CALL_STATE_ON=15
    IN_CALL_STATE_OFF=16
    APP_USER_STATE_SIGNED_OUT=17
    APP_USER_STATE_SIGNED_IN=18
    PHONE_STATE_UPDATED_HEADSET=19
    PHONE_STATE_UPDATED_HANDSET=20
    PHONE_STATE_UPDATED_SPEAKER=21
    PHONE_STATE_UPDATED_OFF=22
    MISSED_VOICEMAIL_STATE_ON=23
    MISSED_VOICEMAIL_STATE_OFF=24


class KeyCodes(object):
    VOLUME_UP=24
    VOLUME_DOWN=25
    MUTE=91
    ZERO=7
    ONE=8
    TWO=9
    THREE=10
    FOUR=11
    FIVE=12
    SIX=13
    SEVEN=14
    EIGHT=15
    NINE=16
    STAR=17
    POUND=18
    CONTACTS=207
    VOICEMAIL=500
    HOLD=501
    RESUME=501
    TRANSFER=502
    VOICESKILLS=503
    REDIAL=504
    HEADSET=505
    SPEAKER=506
    HANDSET=507
    ENTER=66

class DeviceType(object):
    PERSONAL=0
    CONFERENCE=1
    ALL=2
