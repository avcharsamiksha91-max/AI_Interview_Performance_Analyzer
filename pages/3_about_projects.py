import streamlit as st

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide",
)

st.title("ℹ️ About Project")

st.write(
    """
    ## 🤖 AI Interview Performance Analyzer

    An AI-powered platform designed to help candidates
    practice interviews, analyze their performance, and
    improve their confidence.
    """
)

st.markdown("---")

st.subheader("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.write("💬 AI Interview")
    st.write("Generate AI-powered interview questions.")

    st.write("🎤 Voice Analysis")
    st.write("Analyze speaking speed, fluency, clarity and confidence.")

    st.write("📷 Face Detection")
    st.write("Detect face, eyes and facial engagement.")

    st.write("🎥 Video Analysis")
    st.write("Analyze face position and eye contact.")

with col2:
    st.write("🧠 AI Evaluation")
    st.write("Generate personalized interview feedback.")

    st.write("📊 Performance Analysis")
    st.write("Calculate voice and video performance scores.")

    st.write("🏆 Final Analysis")
    st.write("Combine voice and video results into an overall score.")

    st.write("📄 PDF Reports")
    st.write("Generate and download professional interview reports.")

st.markdown("---")

st.subheader("🛠️ Technologies Used")

st.write("🐍 Python")
st.write("🎈 Streamlit")
st.write("📷 OpenCV")
st.write("🧍 MediaPipe")
st.write("🎥 Streamlit WebRTC")
st.write("🤖 Groq AI")

st.markdown("---")

st.subheader("🎯 Project Goal")

st.write(
    """
    The main goal of this project is to provide an intelligent
    interview practice platform where candidates can practice
    mock interviews, analyze their voice and video performance,
    receive AI-based feedback, and improve their interview skills.
    """
)

st.markdown("---")

st.subheader("🔄 Interview Analysis Flow")

st.write("1️⃣ Start AI Interview")
st.write("2️⃣ Answer interview questions")
st.write("3️⃣ Analyze voice performance")
st.write("4️⃣ Analyze video and facial behavior")
st.write("5️⃣ Generate final performance score")
st.write("6️⃣ Generate PDF interview report")

st.markdown("---")

st.success(
    "🚀 Practice • Analyze • Improve"
)

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Python + Streamlit + OpenCV + MediaPipe + Groq AI"
)