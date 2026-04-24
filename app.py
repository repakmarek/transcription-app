import streamlit as st
import pandas as pd
from openai import OpenAI
import tempfile
import os

# API key zo Secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎤 Prepis rozhovoru (coach)")

st.write("""
👉 Nahraj audio z coaching session  
👉 Počkaj pár sekúnd  
👉 Stiahni prepis
""")

uploaded_file = st.file_uploader("Nahraj audio", type=["mp3", "m4a", "wav"])

if uploaded_file:

    # limit veľkosti (ochrana)
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("Súbor je príliš veľký. Skús kratšie audio (do 10MB).")
        st.stop()

    with st.spinner("⏳ Prepisujem audio..."):

        # uloženie do temp súboru
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_audio_path = tmp_file.name

        # 🔥 TRANSCRIPTION
        try:
            with open(temp_audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file
                )
        except Exception as e:
            st.error(f"Chyba pri prepisovaní: {e}")
            st.stop()

        text = transcript.text

        # 🔥 jednoduché rozdelenie na vety
        sentences = text.split(". ")

        data = []
        for i, s in enumerate(sentences):
            data.append({
                "id": i,
                "text": s.strip()
            })

        df = pd.DataFrame(data)

        st.success("Hotovo ✅")

        st.subheader("📄 Prepis")
        st.write(text)

        # download CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Stiahnuť CSV",
            csv,
            "transcript.csv",
            "text/csv"
        )
