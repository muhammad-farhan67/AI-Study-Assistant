import streamlit as st
import os
from groq import Groq
import pytesseract
from PIL import Image
import io
import requests
import time
import speech_recognition as sr
import fitz  # PyMuPDF

# Initialize session state
if 'previous_responses' not in st.session_state:
    st.session_state.previous_responses = []

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path for Windows

# Granite API for coding and math
# GRANITE_API_KEY = os.environ.get("GRANITE_API_KEY")
# GRANITE_API_URL = "https://api.granite.ai/v1/chat/completions"

def process_voice(audio_file):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        st.error(f"Error processing voice input: {str(e)}")
        return None

def process_image(image_file):
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

# Replace the old PDF processing function with PyMuPDF
def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def get_ai_response(input_text, model="llama3-8b-8192"):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI study assistant. Provide hints and approaches to solve problems, but don't give exact answers. Focus on education-related topics."
                },
                {
                    "role": "user",
                    "content": input_text,
                }
            ],
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

# def get_granite_response(input_text):
#     try:
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {GRANITE_API_KEY}"
#         }
#         data = {
#             "model": "granite-v1",
#             "messages": [
#                 {"role": "system", "content": "You are a coding and math assistant. Provide hints and approaches, not full solutions."},
#                 {"role": "user", "content": input_text}
#             ]
#         }
#         response = requests.post(GRANITE_API_URL, headers=headers, json=data)
#         response.raise_for_status()
#         return response.json()['choices'][0]['message']['content']
#     except Exception as e:
#         st.error(f"Error getting Granite response: {str(e)}")
#         return None

# Streamlit UI
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")
st.markdown("""
<style>
    /* Overall app background */
    .stApp {
        background: linear-gradient(to bottom right, #2C3E50, #1E1E1E);
    }
    
    /* Text color and font */
    body {
        color: #E0E0E0;
        font-family: 'Arial', sans-serif;
    }
    
    /* Center content */
    .stContainer {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Response container styling */
    .response-card {
        background-color: #34495E;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #4A5568;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Style the hint text */
    .hint-text {
        background-color: #2C3E50;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border-left: 5px solid #3498DB;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3498DB;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #3498DB;
        text-align: center;
    }

    /* Divider between responses */
    .response-divider {
        border-top: 1px solid #4A5568;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.image("eduai.png", width=250)
# st.sidebar.title("Options")
input_type = st.sidebar.radio("Choose input type:", ("Text", "Voice", "Image", "PDF"))
topic_type = st.sidebar.radio("Topic type:", ("General", "Coding/Math"))

# Main content
st.markdown("<h1 class='main-header'>AI Study Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Welcome! How can we help you today?</h2>", unsafe_allow_html=True)

if input_type == "Text":
    user_input = st.text_area("Enter your question:")
elif input_type == "Voice":
    audio_file = st.file_uploader("Upload audio file", type=["wav"])
elif input_type == "Image":
    image_file = st.file_uploader("Upload image file", type=["png", "jpg", "jpeg"])
elif input_type == "PDF":
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

if st.button("Get Hint"):
    with st.spinner("Processing..."):
        if input_type == "Text" and user_input:
            text = user_input
        elif input_type == "Voice" and audio_file:
            text = process_voice(audio_file)
        elif input_type == "Image" and image_file:
            text = process_image(image_file)
        elif input_type == "PDF" and pdf_file:
            text = extract_text_from_pdf(pdf_file)  # Updated to use PyMuPDF for PDF extraction
        else:
            st.warning("Please provide input based on the selected type.")
            st.stop()

        if text:
            st.markdown("<div class='response-card'>", unsafe_allow_html=True)
            st.markdown("### Processed text:")
            st.write(text)
            
            if topic_type == "General":
                hint = get_ai_response(text)
            # else:
            #     hint = get_granite_response(text)
            
            if hint:
                st.markdown("### Hint:")
                st.markdown(f'<div class="hint-text">{hint}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add to session state
            st.session_state.previous_responses.append((text, hint))

# Display previous responses
if st.session_state.previous_responses:
    st.markdown("### Previous Responses:")
    for i, (question, answer) in enumerate(reversed(st.session_state.previous_responses[:-1]), 1):
        st.markdown("<div class='response-card'>", unsafe_allow_html=True)
        st.markdown(f"<h4>Question {i}:</h4>", unsafe_allow_html=True)
        st.write(question)
        st.markdown(f"<h4>Answer {i}:</h4>", unsafe_allow_html=True)
        st.markdown(f'<div class="hint-text">{answer}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if i < len(st.session_state.previous_responses) - 1:
            st.markdown("<div class='response-divider'></div>", unsafe_allow_html=True)

# Footer
st.markdown("© 2024 AI Study Assistant. All rights reserved.")

# Progress bar in sidebar
progress_bar = st.sidebar.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
st.sidebar.success("Ready!")
