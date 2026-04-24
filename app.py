import streamlit as st
import pandas as pd
from openai import OpenAI
import tempfile
import os
import io

# API key zo Secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎤 Prepis rozhovoru (coach)")

uploaded_file = st.file_uploader("Nahraj audio", type=["mp3", "m4a", "wav"])

if uploaded_file:

    with st.spinner("⏳ Prepisujem audio..."):

        # uloženie do temp súboru
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_audio_path = tmp_file.name

        # transcription
        try:
            with open(temp_audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file
                )
        except Exception as e:
            st.error(f"Chyba: {e}")
            st.stop()

        text = transcript.text

        # rozdelenie na vety
        sentences = text.split(". ")

        data = []
        for i, s in enumerate(sentences):
            data.append({
                "id": i,
                "text": s.strip()
            })

        df = pd.DataFrame(data)

        st.success("Hotovo ✅")
        st.write(text)

        # Excel export
        df_excel = pd.DataFrame({
            "cas": list(range(len(data))),
            "text": [d["text"] for d in data]
        })

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_excel.to_excel(writer, index=False)

        st.download_button(
            "Stiahnuť Excel",
            output.getvalue(),
            "transcript.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
