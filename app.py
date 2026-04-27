import streamlit as st

st.set_page_config(page_title="Audio AI Studio", layout="wide", page_icon="🎙️")

st.title("🎙️ Vitajte v CoachSkills Audio AI Studio")
st.write("Polo-Profesionálny nástroj na prepis a analýzu rozhovorov 😉.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Krok: Prepis")
    st.write("Nahrajte audio a získajte surový prepis s časovými značkami.")
    if st.button("Spustiť aplikáciu"):
        st.switch_page("pages/1_Prepis.py")

with col2:
    st.subheader("2. Krok: Inteligentná úprava")
    st.write("Identifikujte rečníkov a opravte gramatiku cez Gemini AI.")
    if st.button("Spustiť AI Editor"):
        st.switch_page("pages/2_Cistenie.py")
