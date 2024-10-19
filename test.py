import pvporcupine
import time
import struct
import pyaudio
import pyautogui

def hh():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Initialize Porcupine with the access key and the keyword path
        porcupine = pvporcupine.create(
            access_key='eY5GhGKE3e5zGibUbgtUynzScS1nKe0hRCBlg14hdcw1/iwIK/3YQg==',
            keyword_paths=[r"C:\\mithra\\mithra_en_windows_v3_0_0.ppn"]  # Use raw string for the correct path
        )

        print("Porcupine initialized")  # Confirmation print

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,
                                  channels=1,
                                  format=pyaudio.paInt16,
                                  input=True,
                                  frames_per_buffer=porcupine.frame_length)
        
        print("Listening for hotword...")  # Indicating the program is running
        
        # Loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Process the keyword coming from mic
            keyword_index = porcupine.process(keyword)
            print(f"Keyword Index: {keyword_index}")  # Debugging keyword index

            # Check if the custom keyword is detected
            if keyword_index >= 0:
                print("Hotword detected!")

                # Pressing shortcut key win+j
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except Exception as e:
        print(f"An error occurred: {e}")  # Print the error message for debugging
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

hh()
