import streamlit as st 
import os
from PIL import Image
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import time

# Configure API key for Google Generative AI
genai.configure(api_key="AIzaSyBjARp9j3dMyRlsfOFoC59kI9UJX15dZ_M")  # Replace with your actual API key
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
st.set_page_config(page_title="RescueBot")
st.sidebar.header("RescueBot")
st.sidebar.write("AI Bot for Injury Recognition and First Aid")
st.sidebar.write("""Disclaimer: I am an AI-powered injury recognition tool. While I can provide information on injuries and first aid instructions, my advice is not a substitute for professional medical guidance. 
Always consult a licensed healthcare provider for accurate diagnosis and treatment.""")
st.sidebar.write("Powered by Mithra")
st.header("RescueBot")
st.subheader("Hello!!!...I'm RescueBot...Your first aid assistant!")

input_text = st.text_input("Describe the injury or ask for help:", key="input")
uploaded_file = st.file_uploader("Please upload an image of the injury", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image of injury", use_column_width=True)

submit = st.button("Analyze The Problem")

input_prompt = """You are an expert in recognizing injuries and providing first aid advice.
I am developing an AI system designed to assist users by identifying injuries,fractures,rashes and skin disease from images and providing actionable first aid instructions. Using the details from the uploaded image of the injury, perform the following tasks:
Injury Identification: Based on the image, identify the type of injury (e.g., cut, bruise, sprain, fracture). Provide a brief description of the injury and any visual signs to look for.
Injury Analysis: Analyze the injury or infection to assess its severity. Include details on possible complications or concerns based on the injury or infection type and appearance.
First Aid Instructions: Offer clear and concise first aid instructions for the recognized injury. Include steps on how to treat the injury, any necessary materials or tools, and when to seek professional medical help.
Precautions and Recommendations: Provide any important precautions to take while treating the injury or infection. If applicable, suggest follow-up actions based on the injury type.
Emergency Protocol: If the injury or infection appears severe, provide emergency protocols that the user should follow immediately.
When presenting the first aid instructions, structure your response in a user-friendly format and in a brief way without using # and * and*, such as: "For a [type of injury], apply [specific treatment] and follow these steps...".
"""

# Handle AI response when the user submits the input
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.write(response)
    print(f"AI Response: {response}")
    speak(response)
