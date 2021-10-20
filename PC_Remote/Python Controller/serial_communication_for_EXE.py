# this script is suppost to be started after arduino connecting
# and all other scripts are suppost to be run after this one
import serial

import traceback  # for debugging

# my scripts:
from execute_commands import executeCommand, setVolumesToDefaults
from display_notifications import welcomeMe, displayRemoteMode, shutDownAudio


IS_PC_MODE_ON = True
SHOULD_CLOSE = False


def main(ser):
    global IS_PC_MODE_ON
    global SHOULD_CLOSE

    input_bytes = ser.readline()
    decoded_bytes = None
    try:  # try to get input data
        # length - 2: because it is the end of string indicator:
        decoded_bytes = str(input_bytes[0:len(input_bytes)-2].decode("utf-8"))
    except Exception as e:
        pass

    if not decoded_bytes:
        print("Decoded bytes is null.")
        return

    command = decoded_bytes

    if command == "Power ON/OFF":  # change of mode(PC/Custom App)
        IS_PC_MODE_ON = not IS_PC_MODE_ON
        displayRemoteMode(IS_PC_MODE_ON)
        return

    # FOR PROPER CLOSING:
    # clicking Mute in the App mode is a Kill switch
    if command == "MUTE" and not IS_PC_MODE_ON:
        setVolumesToDefaults()
        print("SHUTTING DOWN !!")
        shutDownAudio()
        SHOULD_CLOSE = True
        return

    executeCommand(command, IS_PC_MODE_ON)  # handle any other command
    return


if __name__ == "__main__":
    setVolumesToDefaults()  # set Chrome and PC volumes back to defaults
    welcomeMe()
    with serial.Serial('COM3', 9600) as ser:
        ser.flushInput()

        IS_PC_MODE_ON = True  # PC mode as the default
        displayRemoteMode(IS_PC_MODE_ON)  # show user the default option

        while not SHOULD_CLOSE:
            try:
                main(ser)
            except Exception as err:
                setVolumesToDefaults()
                print("Quit the loop due to: " + str(err))
                traceback.print_exc()
                break
