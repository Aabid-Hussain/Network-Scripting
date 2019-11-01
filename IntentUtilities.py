from ADBDriver import ADBDriver
from Logger import Logger
from enums import Intents
from enums import KeyCodes
available_keycodes = {
        1:  {
            "name" : "VOLUME UP",
            "action":KeyCodes.VOLUME_UP,
        },
        2:  {
            "name" : "VOLUME DOWN",
            "action":KeyCodes.VOLUME_DOWN,
        },
        3:  {
            "name" : "MUTE",
            "action":KeyCodes.MUTE,
        },
        4:  {
            "name" : "ZERO",
            "action":KeyCodes.ZERO,
        },
        5:  {
            "name" : "ONE",
            "action":KeyCodes.ONE,
        },
        6:  {
            "name" : "TWO",
            "action":KeyCodes.TWO,
        },
        7:  {
            "name" : "THREE",
            "action":KeyCodes.THREE,
        },
        8:  {
            "name" : "FOUR",
            "action":KeyCodes.FOUR,
        },
        9:  {
            "name" : "FIVE",
            "action":KeyCodes.FIVE,
        },
        10:  {
            "name" : "SIX",
            "action":KeyCodes.SIX,
        },
        11:  {
            "name" : "SEVEN",
            "action":KeyCodes.SEVEN,
        },
        12:  {
            "name" : "EIGHT",
            "action":KeyCodes.EIGHT,
        },
        13:  {
            "name" : "NINE",
            "action":KeyCodes.NINE,
        },
        14:  {
            "name" : "STAR",
            "action":KeyCodes.STAR,
        },
        15:  {
            "name" : "POUND",
            "action":KeyCodes.POUND,
        },
        16:  {
            "name" : "CONTACTS",
            "action":KeyCodes.CONTACTS,
        },
        17:  {
            "name" : "VOICEMAIL",
            "action":KeyCodes.VOICEMAIL,
        },
        18:  {
            "name" : "HOLD",
            "action":KeyCodes.HOLD,
        },
        19:  {
            "name" : "RESUME",
            "action":KeyCodes.RESUME,
        },
        20:  {
            "name" : "TRANSFER",
            "action":KeyCodes.TRANSFER,
        },
        21:  {
            "name" : "SPEAKER",
            "action":KeyCodes.SPEAKER,
        },
        22:  {
            "name" : "VOICESKILLS",
            "action":KeyCodes.VOICESKILLS,
        },
        23:  {
            "name" : "REDIAL",
            "action":KeyCodes.REDIAL,
        },
        24:  {
            "name" : "HEADSET",
            "action":KeyCodes.HEADSET,
        },
        25:  {
            "name" : "HANDSET",
            "action":KeyCodes.HANDSET,
        }
}

available_intents = {
        1:  {
            "name" : "MUTE STATE OFF",
            "action":"com.microsoft.skype.teams.ipphone.APP_MUTE_STATE",
            "data" :
                {
                    "MUTE_STATE" : "0"
                }
            },
        2:  {
            "name" : "MUTE STATE ON",
            "action":"com.microsoft.skype.teams.ipphone.APP_MUTE_STATE",
            "data" :
                {
                    "MUTE_STATE" : "1"
                }
            },
        3:  {
            "name" : "MISSED CALL STATE ON",
            "action":"com.microsoft.skype.teams.ipphone.APP_MISSEDCALL_STATE",
            "data" :
                {
                    "MISSED_CALLS" : "1"
                }
            },
        4:  {
            "name" : "MISSED CALL STATE OFF",
            "action":"com.microsoft.skype.teams.ipphone.APP_MISSEDCALL_STATE",
            "data" :
                {
                    "MISSED_CALLS" : "0"
                }
            },
        5:  {
            "name" : "INCOMING CALL STATE ON",
            "action":"com.microsoft.skype.teams.ipphone.APP_INCOMINGCALL_STATE",
            "data" :
                {
                    "INCOMING_CALL" : "1"
                }
            },
        6:  {
            "name" : "INCOMING CALL STATE OFF",
            "action":"com.microsoft.skype.teams.ipphone.APP_INCOMINGCALL_STATE",
            "data" :
                {
                    "INCOMING_CALL" : "0"
                }
            },
        7:  {
            "name" : "VOICEMAIL PLAYING ON (HEADSET)",
            "action":"com.microsoft.skype.teams.ipphone.APP_VOICEMAILPLAYING_STATE",
            "data" :
                {
                    "PLAYING_VOICEMAIL" : "1",
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "1",
                    "SPEAKER" : "0"
                }
            }, 
        8:  {
            "name" : "VOICEMAIL PLAYING ON (HANDSET)",
            "action":"com.microsoft.skype.teams.ipphone.APP_VOICEMAILPLAYING_STATE",
            "data" :
                {
                    "PLAYING_VOICEMAIL" : "1",
                    "HANDSETHOOK" : "1",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "0"
                }
            }, 
        9:  {
            "name" : "VOICEMAIL PLAYING ON (SPEAKER)",
            "action":"com.microsoft.skype.teams.ipphone.APP_VOICEMAILPLAYING_STATE",
            "data" :
                {
                    "PLAYING_VOICEMAIL" : "1",
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "1"
                }
            }, 
        10:  {
            "name" : "VOICEMAIL PLAYING OFF",
            "action":"com.microsoft.skype.teams.ipphone.APP_VOICEMAILPLAYING_STATE",
            "data" :
                {
                    "PLAYING_VOICEMAIL" : "0",
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "0"
                }
            }, 
        11:  {
            "name" : "AUDIO STATE ON (HEADSET)",
            "action":"com.microsoft.skype.teams.ipphone.partner.APP_AUDIO_STATE",
            "data" :
                {
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "1",
                    "SPEAKER" : "0"
                }
            }, 
        12:  {
            "name" : "AUDIO STATE ON (HANDSET)",
            "action":"com.microsoft.skype.teams.ipphone.partner.APP_AUDIO_STATE",
            "data" :
                {
                    "HANDSETHOOK" : "1",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "0"
                }
            }, 
        13:  {
            "name" : "AUDIO STATE ON (SPEAKER)",
            "action":"com.microsoft.skype.teams.ipphone.partner.APP_AUDIO_STATE",
            "data" :
                {
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "1"
                }
            }, 
        14:  {
            "name" : "AUDIO STATE OFF",
            "action":"com.microsoft.skype.teams.ipphone.partner.APP_AUDIO_STATE",
            "data" :
                {
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "0"
                }
            }, 
        15:  {
            "name" : "IN CALL STATE ON",
            "action":"com.microsoft.skype.teams.ipphone.APP_INCALL_STATE",
            "data" :
                {
                    "IN_CALL" : "1"
                }
        }, 
        16:  {
            "name" : "IN CALL STATE OFF",
            "action":"com.microsoft.skype.teams.ipphone.APP_INCALL_STATE",
            "data" :
                {
                    "IN_CALL" : "0"
                }
        },
        17:  {
            "name" : "APP USER STATE SIGNED OUT",
            "action":"com.microsoft.skype.teams.ipphone.APP_USER_STATE",
            "data" :
                {
                    "SIGNED_IN" : "0"
                }
        },
        18:  {
            "name" : "APP USER STATE SIGNED IN",
            "action":"com.microsoft.skype.teams.ipphone.APP_USER_STATE",
            "data" :
                {
                    "SIGNED_IN" : "1"
                }
        },
        19:  {
            "name" : "PHONE STATE UPDATED (HEADSET)",
            "action":"com.microsoft.skype.teams.ipphone.partner.PHONE_STATE_UPDATED",
            "data" :
                {
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "1",
                    "SPEAKER" : "0"
                }
            }, 
        20:  {
            "name" : "PHONE STATE UPDATED (HANDSET)",
            "action":"com.microsoft.skype.teams.ipphone.partner.PHONE_STATE_UPDATED",
            "data" :
                {
                    "HANDSETHOOK" : "1",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "0"
                }
            }, 
        21:  {
            "name" : "PHONE STATE UPDATED (SPEAKER)",
            "action":"com.microsoft.skype.teams.ipphone.partner.PHONE_STATE_UPDATED",
            "data" :
                {
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "1"
                }
            }, 
        22:  {
            "name" : "PHONE STATE UPDATED OFF",
            "action":"com.microsoft.skype.teams.ipphone.partner.PHONE_STATE_UPDATED",
            "data" :
                {
                    "HANDSETHOOK" : "0",
                    "HEADSETHOOK" : "0",
                    "SPEAKER" : "0"
                }
            },
        23:  {
            "name" : "VOICEMAIL STATE ON",
            "action":"com.microsoft.skype.teams.ipphone.APP_MISSEDVOICEMAIL_STATE",
            "data" :
                {
                    "UNREAD_VOICEMAIL" : "1"
                }
            },
        24:  {
            "name" : "VOICEMAIL STATE OFF",
            "action":"com.microsoft.skype.teams.ipphone.APP_MISSEDVOICEMAIL_STATE",
            "data" :
                {
                    "UNREAD_VOICEMAIL" : "0"
                }
            }
}
class IntentUtilities():
    def __init__(self,serial):
        # Logger.LoggingDir = Logger.LoggingDir +"/INTENT_CHECKER/"
        Logger.Start()
        self.adb_driver = ADBDriver(serial)

    def broadcast_intent(self, command_as_integer):
        message = self.prepare_message(available_intents[command_as_integer]["action"],available_intents[command_as_integer]["data"])            
        self.adb_driver.execute_command("shell am broadcast -a "+ message)

    def broadcast_intent_list_inorder(self, commands):
        for command in commands :        
            self.broadcast_intent(command)

    def stop(self):
        Logger.Stop()

    def reset_intents(self):
        commands = [
                    Intents.MUTE_STATE_OFF,
                    Intents.MISSED_CALL_STATE_OFF,
                    Intents.INCOMING_CALL_STATE_OFF,
                    Intents.VOICEMAIL_PLAYING_OFF,
                    Intents.AUDIO_STATE_OFF,
                    Intents.IN_CALL_STATE_OFF,
                    Intents.APP_USER_STATE_SIGNED_IN,
                    Intents.PHONE_STATE_UPDATED_OFF
        ]      
        self.broadcast_intent_list_inorder(commands)

    def prepare_message(self,action,data):
        message = ""
        message += action
        #print data
        for key in data:
            current_pair = " --ei " + key +" " + data[key]
            message += current_pair
        #print "Message : " + message
        return message

    def get_available_intents(self):
        return available_intents

    def get_available_keycodes(self):
        return available_keycodes







