import streamlit as st
import pandas as pd
from openai import OpenAI
import tempfile
import os
import io

# API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎤 Prepis rozhovoru (coach)")

uploaded_file = st.file_uploader("Nahraj audio", type=["mp3", "m4a", "wav"])

if uploaded_file:

    # načítanie bytes
    audio_bytes = uploaded_file.read()

    # rozdelenie na časti (5MB)
    chunk_size = 5 * 1024 * 1024
    chunks = [audio_bytes[i:i+chunk_size] for i in range(0, len(audio_bytes), chunk_size)]

    st.write(f"Počet častí: {len(chunks)}")

    full_text = ""

    with st.spinner("⏳ Prepisujem audio..."):

        for i, chunk in enumerate(chunks):

            st.write(f"Spracovávam časť {i+1}/{len(chunks)}")

            # uloženie chunku
            with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
                tmp_file.write(chunk)
                temp_audio_path = tmp_file.name

            try:
                with open(temp_audio_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=audio_file
                    )

                full_text += transcript.text + " "

            except Exception as e:
                st.error(f"Chyba pri časti {i+1}: {e}")
                st.stop()

    # rozdelenie na vety
    sentences = full_text.split(". ")

    data = []
    for i, s in enumerate(sentences):
        data.append({
            "id": i,
            "text": s.strip()
        })

    df = pd.DataFrame(data)

    st.success("Hotovo ✅")
    st.subheader("📄 Prepis")
    st.write(full_text)

    # Excel export
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        "Stiahnuť Excel",
        output.getvalue(),
        "transcript.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
