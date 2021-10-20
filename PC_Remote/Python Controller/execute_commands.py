# this module is used to processes commands sent by Arduino
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from pycaw.pycaw import IAudioEndpointVolume
# my scripts:
from display_notifications import soundMessage, showNotification

# volume control examples:
# https://github.com/AndreMiras/pycaw/blob/develop/examples/audio_controller_class_example.py


class AudioController(object):
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, 'has been muted.')  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, 'has been unmuted.')  # debug

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print('Volume:', interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print('Volume set to', self.volume)  # debug

    def decrease_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # 0.0 is the min value, reduce by decibels
                self.volume = max(0.0, self.volume-decibels)
                interface.SetMasterVolume(self.volume, None)
                print('Volume reduced to', self.volume)  # debug

    def increase_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # 1.0 is the max value, raise by decibels
                self.volume = min(1.0, self.volume+decibels)
                interface.SetMasterVolume(self.volume, None)
                print('Volume raised to', self.volume)  # debug


def setVolumesToDefaults():
    # set Chrome volume to 80%:
    audio_controller = AudioController('chrome.exe')
    audio_controller.set_volume(0.8)  # default
    # set PC volume to 39%:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # unmute if it was muted:
    if volume.GetMute():
        volume.SetMute(0, None)

    volume.SetMasterVolumeLevel(-14, None)  # set to 39%


def setMasterVolume(volumeToSet):
    # volumeToSet: +10 and -10 for UP and DOWN on remote, 0 for (un)mute:
    # set device and audio:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # set mute and return
    if volumeToSet == 0:
        if not volume.GetMute():
            volume.SetMute(1, None)
            print("Set PC volume to mute")
            showNotification('MUTE is on')
        else:
            volume.SetMute(0, None)
            print("Unmuted PC volume")
            showNotification('Unmuted!', duration=3)
        return

    # -0.0 is max volume, -64 is 0%
    # max -> 87% -> 79% -> 72% -> 67% -> 63% -> 57% -> 50% -> 45% -> 39% ->
    # 36% -> 30% -> 24% -> 18% -> 13% -> 6% -> 0%
    volume_values = [0, -2, -3.5, -5, -6, -7, -8.5, -10, -12, -14,
                     -15, -18, -21, -25, -30, -40, -64]  # length is 17
    volume_idx = 0  # volume idx in the volume_values arr

    cur_volume = volume.GetMasterVolumeLevel()

    # store idx of volume in arr closest to current volume
    min_offset_and_idx = [300, 0]
    for i in range(len(volume_values)):
        if abs(cur_volume - volume_values[i]) < min_offset_and_idx[0]:
            min_offset_and_idx[0] = abs(cur_volume - volume_values[i])
            min_offset_and_idx[1] = i
    volume_idx = min_offset_and_idx[1]

    if volume_idx == 0 and volumeToSet > 0:
        print("Volume is already at maximum.")
        return
    if volume_idx == len(volume_values) - 1 and volumeToSet < 0:
        print("Volume is already at minimum.")
        return

    # jump to next volume value in arr based on key pressed
    volume_idx -= volumeToSet
    new_volume = volume_values[volume_idx]
    volume.SetMasterVolumeLevel(new_volume, None)


def setMasterVolumeNew(volume_val_idx):  # value from 0 to 16(inclusive)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # -0.0 is max volume, -64 is 0%
    # max -> 87% -> 79% -> 72% -> 67% -> 63% -> 57% -> 50% -> 45% -> 39% ->
    # 36% -> 30% -> 24% -> 18% -> 13% -> 6% -> 0%
    volume_values = [0, -2, -3.5, -5, -6, -7, -8.5, -10, -12, -14,
                     -15, -18, -21, -25, -30, -40, -64]  # length is 17

    # set value from array based on mobile apps seek bar's value
    # Seek bar's 0 is 0% volume which is last element in this arr
    new_volume = volume_values[len(volume_values) - 1 - volume_val_idx]
    volume.SetMasterVolumeLevel(new_volume, None)


def changePlayerVolume(volumeToSetStep):  # positive/negative encrease/decrease
    audio_controller = AudioController('chrome.exe')
    step = abs(volumeToSetStep) / 100  # 10% --> 0.1
    if volumeToSetStep > 1:
        audio_controller.increase_volume(step)
    else:
        audio_controller.decrease_volume(step)


def processPC_ModeCommands(command):
    if command == "MUTE":
        setMasterVolume(0)  # easy to unmute manually unlike Chrome mute cmnd
    elif "PLAYER VOL" in command:  # changes Chrome audio
        # get the number(X) out of "PLAYER VOL X":
        player_vol_value = int(command[len("PLAYER VOL "):])
        # changePlayerVolume(10)
        audio_controller = AudioController('chrome.exe')
        audio_controller.set_volume(player_vol_value / 10)  # 8 -> 0.8
    elif command == "PLAY/PAUSE":
        return  # <-------------------- EDIT THIS WHEN YOU ENABLE THE FEATURE
    elif command == "Unknown button":
        print("Unknown key/command. Try again?")
        msg = "Didn't quite catch that. Could you repeat the key?"
        # soundMessage(msg, 'unknown_button_audio')
    else:
        if command == "setup: in" or \
           command == "Starting the IR Arduino Decoding reciever.." or \
           command == "setup: out":
            print("Status: " + command)
            return
        # It is NEXT/PREVIOUS SONG command
        print("Command not supported in this mode. Try Custom App mode.")
        msg = "This command is not supported. Try switching to app mode."
        # soundMessage(msg, 'cmd_not_supported_audio')
        showNotification(msg, duration=3)


def processApp_Commands(command):
    """
        To be developed..
    """
    if command == "MUTE":  # mute only this app
        # audio_controller = AudioController('app.exe')
        # audio_controller.
        return
    # PLAYER VOLUME UP/DOWN SHOULD CHANGE YT_PLAYER VOLUME FOR CURRENT SONG
    # WHICH IS NORMAL INCREASE/DECREASE IN THE APP
    """
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "chrome.exe":
            print("volume.GetMasterVolume(): " + str(volume.GetMasterVolume()))
            volume.SetMasterVolume(volumeToSet, None)
    """
    # volume.SetMasterVolume(volumeToSet, None)


def executeCommand(command, isPcModeON):
    # process commands incommon for both modes:
    if "PC VOL" in command:
        pc_vol_value = int(command[len("PC VOL ") : ])
        setMasterVolumeNew(pc_vol_value)
        return

    # process commands unique for each mode:
    if isPcModeON:
        processPC_ModeCommands(command)
    else:
        processApp_Commands(command)
