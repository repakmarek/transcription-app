import streamlit as st
import whisper
import pandas as pd
import os
from io import BytesIO

st.title("🎙️ Prepis Audia (Whisper)")

@st.cache_resource
def get_model():
    return whisper.load_model("small") # 'base' pre rýchlosť, 'small' pre presnosť

uploaded_file = st.file_uploader("Nahrajte audio súbor", type=["mp3", "wav", "m4a"])

if uploaded_file:
    # Zapamätáme si pôvodný názov bez prípony
    base_name = os.path.splitext(uploaded_file.name)[0]
    
    if st.button("Začať prepisovať"):
        with st.spinner("AI teraz počúva nahrávku..."):
            with open("temp_audio", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            model = get_model()
            result = model.transcribe("temp_audio", language="sk")
            
            # Spracovanie dát
            data = []
            for s in result['segments']:
                m, sec = divmod(int(s['start']), 60)
                data.append({
                    "Čas": f"{m:02d}:{sec:02d}",
                    "Text": s['text'].strip()
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Príprava Excelu na stiahnutie
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            
            st.download_button(
                label=f"📥 Stiahnuť {base_name}_surovy.xlsx",
                data=output.getvalue(),
                file_name=f"{base_name}_surovy.xlsx",
                mime="application/vnd.ms-excel"
            )
