import streamlit as st
import whisper
import pandas as pd

st.title("🎤 Prepis rozhovoru (coach)")

uploaded_file = st.file_uploader("Nahraj audio", type=["mp3", "m4a", "wav"])

if uploaded_file:
    st.write("Spracovávam...")

    # uloženie súboru
    with open("audio.m4a", "wb") as f:
        f.write(uploaded_file.read())

    model = whisper.load_model("small")
    result = model.transcribe("audio.m4a", language="sk")

    segments = result["segments"]

    data = []
    for seg in segments:
        data.append({
            "čas": int(seg["start"]),
            "text": seg["text"]
        })

    df = pd.DataFrame(data)

    st.success("Hotovo ✅")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Stiahnuť CSV", csv, "transcript.csv", "text/csv")
