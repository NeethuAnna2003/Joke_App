import streamlit as st
import requests
from googletrans import Translator
from gtts import gTTS
import os
import base64
import uuid

# -------------------------
# 🔊 Generate & Play Audio using st.audio
# -------------------------
def speak_text(text):
    tts = gTTS(text)
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    st.audio(filename, format='audio/mp3')
    return filename

# -------------------------
# 🖼️ Background image from local file
# -------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
        }}
        .main-card {{
            background: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            max-width: 750px;
            margin: 0 auto;
        }}
        .stButton > button {{
            background-color: #f63366;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 25px;
            border-radius: 12px;
            font-size: 18px;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: #e62e2e;
            transform: scale(1.05);
        }}
        h1, h4, p {{
            color: #111 !important;
            text-align: center;
        }}
        .emoji {{
            font-size: 50px;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add your new background image
add_bg_from_local("animated-laughing-elements-flat-cartoon-style-hd-footage-funny-joke-sense-of-humor-positive-feeling-color-illustration-on-white-background-with-alpha-channel-transparency-for-animation-video.jpg")

# -------------------------
# App Setup
# -------------------------
st.set_page_config(page_title="🤣 Joke Generator", layout="centered")
translator = Translator()

# -------------------------
# App Layout
# -------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.markdown("<div class='emoji'>🤣</div>", unsafe_allow_html=True)
st.markdown("<h1>Endless Joke Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4>Click to laugh, translate, and listen!</h4>", unsafe_allow_html=True)

# Language Selector
language = st.selectbox(
    "🌐 Translate joke into:",
    [("English", "en"), ("Hindi", "hi"), ("Malayalam", "ml"),
     ("Tamil", "ta"), ("Telugu", "te"), ("French", "fr"),
     ("Spanish", "es"), ("German", "de")],
    format_func=lambda x: x[0]
)

# Joke API
def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} {data['punchline']}"
    else:
        return "Oops! Couldn't fetch a joke."

# Show Joke
if st.button("😂 Tell Me a Joke"):
    joke = get_joke()

    st.markdown("### 🗣️ Original Joke:")
    st.success(joke)

    speak_text(joke)

    if language[1] != "en":
        try:
            translated = translator.translate(joke, dest=language[1]).text
            st.markdown("### 🌍 Translated Joke:")
            st.info(translated)
        except:
            st.error("❌ Translation failed.")
else:
    st.info("Click above to hear and read a joke!")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Joke + Translation + TTS 😄")
