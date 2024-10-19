import multiprocessing
import subprocess
import pvporcupine
import pyaudio
import struct
import time

# To run Mithra
def startMithra():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

# To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 is running.")
        porcupine=None
        paud=None
        audio_stream=None
        try:
        
            # pre trained keywords    
            porcupine = pvporcupine.create(
                access_key='eY5GhGKE3e5zGibUbgtUynzScS1nKe0hRCBlg14hdcw1/iwIK/3YQg==',
                keyword_paths=[r"C:\\mithra\\mithra_en_windows_v3_0_0.ppn"]  # Use raw string for the correct path
            )
            paud=pyaudio.PyAudio()
            audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
            
            # loop for streaming
            while True:
                keyword=audio_stream.read(porcupine.frame_length)
                keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

                # processing keyword comes from mic 
                keyword_index=porcupine.process(keyword)

                # checking first keyword detetcted for not
                if keyword_index>=0:
                    print("hotword detected")

                    # pressing shorcut key win+j
                    import pyautogui as autogui
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("win")
                    
        except:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if paud is not None:
                paud.terminate() 

        

 
    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startMithra)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        #subprocess.call([r'device.bat'])
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")

