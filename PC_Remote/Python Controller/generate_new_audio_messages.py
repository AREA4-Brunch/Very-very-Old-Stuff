import os

# pip install gTTS
from gtts import gTTS
# pip install playsound
from playsound import playsound


def main():
    return


def soundMessage(msg, file_name='last_sound', isSynchronous=True):
    print("Creating a sound message")
    # create and save text to speech audio file
    try:
        tts = gTTS(text=msg, lang='en')
    except Exception as err:
        print("Failed to get Text to Speech. Error: " + str(err))
        return
    cur_dir_path = os.path.dirname(os.path.abspath(__file__))
    save_audio_path = cur_dir_path + '\\audio_messages\\' + file_name + '.mp3'
    """cur_dir_path = Path(__file__).parent
    save_audio_path = Path(cur_dir_path / 'audio_messages' / str(file_name + '.mp3'))"""
    if os.path.isfile(save_audio_path):
        os.remove(save_audio_path)
        print("Deleted existing audio file")
    print("Path to save: " + save_audio_path)
    tts.save(save_audio_path)
    print("Playing a sound message")
    # play the audio file
    playsound(save_audio_path, isSynchronous)



if __name__ == "__main__":
    main()
