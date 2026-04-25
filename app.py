import streamlit as st
import pandas as pd
from openai import OpenAI
import tempfile
import os
import io
import subprocess

# API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔥 SPLIT AUDIO (NOVÉ)
def split_audio(input_path, chunk_length_sec=300):
    output_files = []
    i = 0

    while True:
        output_file = f"chunk_{i}.m4a"

        command = [
            "ffmpeg",
            "-i", input_path,
            "-ss", str(i * chunk_length_sec),
            "-t", str(chunk_length_sec),
            "-c", "copy",
            output_file
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            break

        output_files.append(output_file)
        i += 1

    return output_files


st.title("🎤 Prepis rozhovoru (coach)")

uploaded_file = st.file_uploader("Nahraj audio", type=["mp3", "m4a", "wav"])

if uploaded_file:

    with st.spinner("⏳ Spracovávam audio..."):

        # uloženie
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_audio_path = tmp_file.name

        # 🔥 SPLIT (zatiaľ len test)
        chunks = split_audio(temp_audio_path)

        st.success(f"Audio rozdelené na {len(chunks)} častí ✅")
