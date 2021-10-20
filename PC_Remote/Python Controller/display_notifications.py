# this module contains GUI controls for notifying user
# that certain changes were made
import sys
from os import path

import traceback  # for finding errors
# pip install win10toast
from win10toast import ToastNotifier
# pip install playsound
from playsound import playsound


def showNotification(msg_to_display, duration=5):  # duration in seconds
    # get icon path
    cur_dir_path = path.abspath(path.dirname(sys.argv[0]))
    icon_path = cur_dir_path + '\\couch_tv_icon_perfect_32x32.ico'

    toaster = ToastNotifier()
    toaster.show_toast(msg_to_display,
                       'PC Remote',
                       icon_path=icon_path,  # e.g. 'C:\\icon_32x32.ico'
                       duration=duration)  # seconds


def soundMessage(msg, file_name, isSynchronous=True):
    # file name is unique for each command
    cur_dir_path = path.abspath(path.dirname(sys.argv[0]))
    save_audio_path = cur_dir_path + "\\audio_messages\\" + file_name + '.mp3'
    print("Loading audio from: " + save_audio_path)

    # retrieve and play it if it already exists
    if path.isfile(save_audio_path):
        playsound(save_audio_path, isSynchronous)
    else:
        print("Could not find the audio file. Skipping the audio message.")


def welcomeMe():
    welcomming_msg = "I am ready to serve my lord."
    soundMessage(welcomming_msg, 'welcome_me_audio')


def shutDownAudio():
    msg = 'Shutting down my lord.'
    soundMessage(msg, 'turn_off_audio')


def displayRemoteMode(isPcModeON):
    msg_to_display = ''

    # display notification of mode change:
    # keep track of text2speech message path to escape reuse with same name
    audio_file_name = 'app_mode_on_audio'
    if isPcModeON:
        msg_to_display = 'PC Mode is ON'
        audio_file_name = 'pc_mode_on_audio'
        print("PC Mode ON")
    else:
        msg_to_display = 'App Mode is ON'
        print("App Mode ON")

    # create and save text to speech audio file
    soundMessage(msg_to_display, audio_file_name, isSynchronous=False)
    # display current mode as notification
    showNotification(msg_to_display, duration=3.5)
