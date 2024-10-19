import pyttsx3
import speech_recognition as sr
import eel
import os
import time
import datetime
import pygetwindow as gw
import cv2
import numpy as np
import pickle
from llm.llama import llama
import mediapipe as mp
from contextlib import suppress
from MyAlarm import alarm
import webbrowser
import json
import random
from snake_game import snakegame

class MedicineAnalyzer:
    def __init__(self, model_path):
        self.model_dict = pickle.load(open(model_path, 'rb'))
        self.model = self.model_dict['model']
        self.hands = mp.solutions.hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
        self.labels_dict = {0: 'medicine taken', 1: 'medicine not taken'}

    def analyze_frame(self, frame):
        data_aux = []
        x_ = []
        y_ = []

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

                prediction = self.model.predict([np.asarray(data_aux)])
                return self.labels_dict[int(prediction[0])]

        return None

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


COMMAND_LOG_FILE = 'command_log.json'  # File to store the commands log

# Function to log commands into a JSON file
def log_command(command):
    try:
        # Load existing log or create a new one if it doesn't exist
        if os.path.exists(COMMAND_LOG_FILE):
            with open(COMMAND_LOG_FILE, 'r') as file:
                command_log = json.load(file)
        else:
            command_log = []

        # Add new command entry with timestamp
        command_log.append({
            'command': command,
            'timestamp': str(datetime.datetime.now())
        })

        # Write updated log to the file
        with open(COMMAND_LOG_FILE, 'w') as file:
            json.dump(command_log, file, indent=4)

    except Exception as e:
        print(f"Error logging command: {e}")

# Function to generate a report from the JSON log
def generate_report():
    try:
        # Check if log file exists and read it
        if os.path.exists(COMMAND_LOG_FILE):
            with open(COMMAND_LOG_FILE, 'r') as file:
                command_log = json.load(file)

            # Create a report string
            report = "Command Report:\n\n"
            for entry in command_log:
                report += f"Command: {entry['command']}, Timestamp: {entry['timestamp']}\n"
            
            return report
        else:
            return "No commands have been logged yet."
    except Exception as e:
        print(f"Error generating report: {e}")
        return "Error generating report."

def takecommand():
    r = sr.Recognizer()
    query = ""

    while True:
        try:
            with sr.Microphone() as source:
                print('Listening....')
                eel.DisplayMessage('Listening....')
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=10, phrase_time_limit=6)

                try:
                    print('Recognizing...')
                    eel.DisplayMessage('Recognizing....')
                    query = r.recognize_google(audio, language='en-in')
                    print(f"User said: {query}")
                    eel.DisplayMessage(query)
                    log_command(query)
                    time.sleep(2)
                    break  # exit the loop once a valid query is obtained

                except sr.UnknownValueError:
                    print("Speech recognition could not understand the audio.")
                    eel.DisplayMessage("Could not understand. Please try again.")
                    speak("Could not understand. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    eel.DisplayMessage(f"Error: {e}")
                    speak(f"Error: {e}")
                    break  # exit on error

        except Exception as e:
            print(f"Error accessing the microphone: {e}")
            eel.DisplayMessage(f"Error accessing the microphone: {e}")
            speak(f"Error accessing the microphone: {e}")
            break  # exit on error

    return query.lower()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")

@eel.expose
def allCommands(message=1):
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        analyzer = MedicineAnalyzer('./model.p')

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "yes please" in query:
            from twilio.rest import Client

            account_sid ='ACff45f9d9144d0ed88a4aa583118a1504'
            auth_token ='bca43ddaea438e529fff2cfc11687d55'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body='Patient Harini wants to book an appointment for consultation',
                from_='+12162421956',
                to='+919791805322'
            )

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "close notepad" in query:
            speak("Okay, closing Notepad")
            os.system("taskkill /f /im notepad.exe")

        elif "close google" in query:
            speak("Okay, closing Google")
            os.system("taskkill /f /im chrome.exe")

        elif "close youtube" in query:
            speak("Okay, closing YouTube.")
            youtube_windows = [window for window in gw.getAllTitles() if "YouTube" in window]
            for window in youtube_windows:
                win = gw.getWindowsWithTitle(window)[0]
                win.close()

        elif "i am feeling stressed out" in query:
            speak("I can understant your feelings, you are a human, it is human nature to feel stressed out sometimes.")
            speak("but don't worry let me play your favourite song to ease your stress")
            music_dir = "C:\\Users\\harin\\Music"  # Your music directory path
            songs = os.listdir(music_dir)  # List all files in the directory
            mp3_songs = [song for song in songs if song.endswith('.mp3')]  # Filter to include only .mp3 files

            if mp3_songs:  # Check if there are any .mp3 files
                rd = random.choice(mp3_songs)  # Randomly select an .mp3 file
                os.startfile(os.path.join(music_dir, rd))  # Play the selected .mp3 file
            else:
                speak("No music files found now, let me find out another way to cool you down.")  # If no .mp3 files found

        elif "i am feeling restless" in query:
            speak("Let's practice mindfulness to solve your restlessness")
            speak("on count of 3, close your eyes and take deep breath")
            music_dir = "C:\\Users\\harin\\OneDrive\\Desktop\\music1"  # Your music directory path
            songs = os.listdir(music_dir)  # List all files in the directory
            mp3_songs = [song for song in songs if song.endswith('.mp3')]  # Filter to include only .mp3 files

            if mp3_songs:  # Check if there are any .mp3 files
                rd = random.choice(mp3_songs)  # Randomly select an .mp3 file
                os.startfile(os.path.join(music_dir, rd))  # Play the selected .mp3 file
            else:
                speak("No music files found now, let me find out another way to cool you down.")

        elif "i am feeling depressed" in query:
            speak("don't waste time depressing about something, let's waste our time by playing some games")
            snakegame()
            


            
        elif "send report to my doctor" in query:
            speak("sent report to your doctor")
            from twilio.rest import Client

            account_sid ='ACff45f9d9144d0ed88a4aa583118a1504'
            auth_token ='bca43ddaea438e529fff2cfc11687d55'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=generate_report(),
                from_='+12162421956',
                to='+919791805322'
            )

        elif "emergency" in query:
            from twilio.rest import Client
            account_sid ='ACff45f9d9144d0ed88a4aa583118a1504'
            auth_token='bca43ddaea438e529fff2cfc11687d55'
            client =Client(account_sid,auth_token)
            message=client.calls \
                .create(
                    twiml= '<Response><Say>Harini is in emergency! please checkout what happened to her</Say></Response>',
                    from_='+12162421956',
                    to='+919791805322'
                )

        elif "set alarm for medication" in query:
            speak("Which time should I set the alarm?")
            time_input = takecommand()  # Use the voice command to take input for the time

            try:
                if time_input:
                    speak(f"Setting the alarm for {time_input}")
                    alarm(time_input)  # Call the MyAlarm (alarm) function with the given time
                else:
                    speak("I couldn't understand the time, please try again.")
            except Exception as e:
                speak(f"Error setting alarm: {e}")

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode do you want to use, WhatsApp or mobile?")
                preference = takecommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send SMS" in query:
                        speak("What message to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preference:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send?")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'

                    whatsApp(contact_no, query, message, name)

        elif "check medication intake" in query:
            speak("Checking if medicine has been taken.")

            cap = cv2.VideoCapture(0)
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print("Error: Could not read frame.")
                        break

                    prediction = analyzer.analyze_frame(frame)

                    if prediction:
                        if prediction == 'medicine taken':
                            print("Medicine has been taken.")
                            speak("Medicine has been taken.")
                            break
                        else:
                            print("Medicine has not been taken.")
                            speak("Medicine has not been taken.")
                            from twilio.rest import Client

                            account_sid ='ACff45f9d9144d0ed88a4aa583118a1504'
                            auth_token ='bca43ddaea438e529fff2cfc11687d55'
                            client = Client(account_sid, auth_token)
                            message = client.messages.create(
                                body='Medicine not taken by Harini',
                                from_='+12162421956',
                                to='+919791805322'
                            )

            finally:
                cap.release()
                cv2.destroyAllWindows()

        else:
            reply = llama(query)
            speak(reply)

    except Exception as e:
        print(f"Error: {e}")

    eel.ShowHood()
