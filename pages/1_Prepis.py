import streamlit as st
import whisper
import tempfile
import google.generativeai as genai

st.title("Prepis audia")

# API KEY (zatiaľ natvrdo, potom zlepšíme)
genai.configure(api_key="AIzaSyCN_lGaxahKHXGrKW8cX60AXZIskQbXa3E")

# upload
audio_file = st.file_uploader("Nahraj audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.info("Spracovávam audio...")

    # uloženie do temp súboru
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    # Whisper model
    model = whisper.load_model("base")

    # prepis
    result = model.transcribe(tmp_path)
    raw_text = result["text"]

    st.subheader("Surový prepis")
    st.write(raw_text)

    # Gemini čistenie
    model_gemini = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
    Vyčisti tento prepis:
    - odstráň výplňové slová
    - oprav gramatiku
    - zachovaj význam

    Text:
    {raw_text}
    """

    response = model_gemini.generate_content(prompt)
    cleaned_text = response.text

    st.subheader("Vyčistený text")
    st.write(cleaned_text)

    st.download_button("Stiahnuť text", cleaned_text)
