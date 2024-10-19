import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import pyttsx3

genai.configure(api_key="AIzaSyBjARp9j3dMyRlsfOFoC59kI9UJX15dZ_M")

model=genai.GenerativeModel('gemini-1.5-flash')

# Initialize the pyttsx3 engine
import streamlit as st
import pyttsx3
import threading
import re

def sanitize_text(text):
    # Remove unwanted characters (e.g., asterisks, etc.)
    return re.sub(r'[^a-zA-Z0-9\s.,!?\'"()\-]', '', text)

def speak(text):
    sanitized_text = sanitize_text(text)
    
    def run_tts():
        engine = pyttsx3.init()
        engine.say(sanitized_text)
        engine.runAndWait()
    
    threading.Thread(target=run_tts).start()


def get_gemini_response(input_text,image_data,prompt):
    response =model.generate_content([input_text,image_data[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("no file was uploaded")
    
st.set_page_config(page_title="Healio")
st.sidebar.header("Healio")
st.sidebar.write("Health Test Analyzer Bot")
st.sidebar.write("""Disclaimer: I am an AI-powered report analyzer. 
While I can offer insights on medications and potential conditions, my advice is not a replacement for professional medical guidance. Always consult a licensed healthcare provider for accurate diagnosis and treatment.""")
st.sidebar.write("Powered by Mithra")
st.header("Healio")
st.subheader("Hey!!! I’m Healio, Mithra’s health partner!")
st.subheader("I’m here to help you analyse your condition using the reports you give me")
input =st.text_input("How can I help you?",key="input")
uploaded_file=st.file_uploader("Please upload your reports given by your doctor",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="uploaded image",use_column_width=True)
ssubmit=st.button("lets go!")
input_prompt="""you are an expert in analysing the scans, reports and test results 

I am developing a healthcare analysis tool that requires comprehensive insights into various medical tests and scans. Using the list provided, please perform the following tasks:

Categorization: Organize the tests and scans into their respective categories (e.g., Laboratory Tests, Imaging Scans, etc.) as outlined in the list.

Purpose and Applications: For each test or scan, provide a brief explanation of its purpose, common applications, and any relevant information regarding its importance in healthcare.

Interpretation of Results: Explain how the results of each test or scan can impact patient diagnosis, treatment, and management decisions.
Complete Blood Count (CBC)
Blood Glucose Test
Lipid Panel
Liver Function Tests
Kidney Function Tests
Urinalysis
Pregnancy Test
Stool Tests
Imaging Scans
X-ray
Ultrasound
CT (Computed Tomography) Scan
MRI (Magnetic Resonance Imaging)
PET (Positron Emission Tomography) Scan
Cardiovascular Tests
Electrocardiogram (ECG/EKG)
Echocardiogram
Stress Test
Respiratory Tests
Spirometry
Chest X-ray
Cancer Screening Tests
Mammography
Colonoscopy
Pap Smear
Genetic Testing
DNA/Genetic Screening
Neurological Tests
EEG (Electroencephalogram)
Nerve Conduction Study (NCS)
Please provide the analysis in a structured format and within 10 lines for easy reference
"""
if ssubmit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.write(response)
    print(response)
    speak(response)
