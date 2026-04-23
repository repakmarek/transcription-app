import streamlit as st
import pandas as pd
from openai import OpenAI
import tempfile

# 🔐 sem vlož svoj API key
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎤 Prepis rozhovoru (coach)")

st.write("""
👉 Nahraj audio z coaching session  
👉 Počkaj pár sekúnd  
👉 Stiahni prepis
""")

uploaded_file = st.file_uploader("Nahraj audio", type=["mp3", "m4a", "wav"])

if uploaded_file:
    with st.spinner("⏳ Prepisujem audio..."):
        
        # uloženie do dočasného súboru
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_audio_path = tmp_file.name

        # 🔥 OpenAI transcription
        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        text = transcript.text

        # jednoduchý output
        df = pd.DataFrame([{"text": text}])

        st.success("Hotovo ✅")
        st.subheader("📄 Prepis")
        st.write(text)

        # download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Stiahnuť CSV",
            csv,
            "transcript.csv",
            "text/csv"
        )
