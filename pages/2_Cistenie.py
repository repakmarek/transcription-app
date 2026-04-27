import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
from io import BytesIO

st.title("✨ AI Korektúra a Rečníci")

with st.sidebar:
    api_key = st.text_input("Vložte Gemini API kľúč", type="password")

uploaded_excel = st.file_uploader("Nahrajte surový Excel z 1. kroku", type=["xlsx"])

if uploaded_excel and api_key:
    # Extrakcia názvu pre zachovanie kontinuity
    base_name = uploaded_excel.name.replace("_surovy.xlsx", "")
    df_raw = pd.read_excel(uploaded_excel)
    
    if st.button("Spustiť Gemini analýzu"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Príprava textu pre prompt
        full_text = ""
        for _, row in df_raw.iterrows():
            full_text += f"[{row['Čas']}] {row['Text']}\n"
            
        prompt = f"Identify speakers and fix grammar in this Slovak transcript. Output ONLY a JSON array with keys 'cas', 'speaker', 'text'. Text: {full_text}"
        
        with st.spinner("Gemini analyzuje rečníkov a čistí text..."):
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(response.text)
            
            df_final = pd.DataFrame(data)
            st.dataframe(df_final, use_container_width=True)
            
            # Export finálneho súboru
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False)
            
            st.download_button(
                label=f"📥 Stiahnuť {base_name}_FINAL.xlsx",
                data=output.getvalue(),
                file_name=f"{base_name}_FINAL.xlsx",
                mime="application/vnd.ms-excel"
            )
