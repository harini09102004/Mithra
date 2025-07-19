import streamlit as st  
import os
from PIL import Image
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import time

# Configure API key for Google Generative AI
genai.configure(api_key="")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(response):
    response = str(response)  # Ensure the response is a string
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Adjust voice if needed
    engine.setProperty('rate', 174)  # Speed of speech
    engine.say(response)
    engine.runAndWait()

# Function to take voice command using speech recognition
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)  # Listening with a timeout

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')  # Language set for India
        print(f"User said: {query}")
        time.sleep(2)
        return query
    except Exception as e:
        print("Error recognizing: ", e)
        return ""  # If no valid command is detected, return empty string

# Function to interact with Gemini API
def get_gemini_response(input_text, image_data):
    response = model.generate_content([input_text, image_data[0]])
    return response.text

# Function to process uploaded image
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file was uploaded")

# Streamlit UI
st.set_page_config(page_title="ExpiryAI")  # Updated AI name here
st.sidebar.header("ExpiryAI")
st.sidebar.write("AI Bot for Expiry Date Checking and Allergy Notifications")
st.sidebar.write("""Disclaimer: I am an AI-powered tool for checking expiry dates and allergy notifications. Always consult a licensed healthcare provider for accurate diagnosis and treatment.""")
st.sidebar.write("Powered by Mithra")
st.header("ExpiryAI")  # Updated AI name here
st.subheader("Hello!!!...I'm ExpiryAI...Your expiry date checker and allergy notifier!")

input_text = st.text_input("Describe the medication or upload an image:", key="input")
uploaded_file = st.file_uploader("Please upload an image of the medication", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image of medication", use_column_width=True)

submit = st.button("Analyze The Medication")

input_prompt = """You are an expert in recognizing medications and providing expiry date alerts and allergy notifications.
I am developing an AI system designed to assist users by identifying medications and checking their expiry dates and potential allergies based on uploaded images and user descriptions. Using the details from the uploaded image of the medication, perform the following tasks:
- Expiry Date Check: Identify the expiry date of the medication and notify the user if it is expired or approaching expiry.
- Allergy Notification: Assess the medication and inform the user if they are allergic to it based on their health profile and history.keep in mind that they are allergic to  chlorphen and check if the medicine prescribed is chlorphen if it is chlorphen tell them to notify the doctor they are allergy to it
- Recommendations: Provide recommendations for alternative medications if applicable.
- Emergency Protocol: If the medication is expired or there is a risk of an allergic reaction, provide emergency protocols that the user should follow immediately.
When presenting the instructions, structure your response in a user-friendly format in a brief way without using # and * and  *, such as: "For [medication], check the expiry date and follow these steps...".
"""

# Handle AI response when the user submits the input
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.write(response)
    print(f"AI Response: {response}")
    speak(response)
