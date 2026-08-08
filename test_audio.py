import streamlit as st

st.title("🎤 Audio Test")

audio = st.audio_input("Record your voice")

if audio is not None:
    st.success("✅ Recording received!")
    st.audio(audio)