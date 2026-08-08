import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Interview Performance Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    # HERO
    st.title("🤖 AI Interview Performance Analyzer")

    st.subheader(
        "Practice interviews. Analyze performance. Improve your confidence."
    )

    st.write(
        "An AI-powered platform for interview practice, voice analysis, "
        "video analysis and personalized performance evaluation."
    )

    st.divider()

    # BUTTONS
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🚀 Start AI Mock Interview",
            use_container_width=True
        ):
            st.switch_page("pages/1_start_interview.py")

    with col2:
        if st.button(
            "▶️ How It Works",
            use_container_width=True
        ):
            st.switch_page("pages/3_about_projects.py")

    st.divider()

    # ========================================================
    # KEY FEATURES
    # ========================================================

    st.header("✨ Key Features")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown("## 📷")
        st.subheader("Face Analysis")
        st.write(
            "Detect face presence, position and eye contact."
        )

    with c2:
        st.markdown("## 🎤")
        st.subheader("Voice Analysis")
        st.write(
            "Analyze confidence, fluency, clarity and speaking speed."
        )

    with c3:
        st.markdown("## 💬")
        st.subheader("AI Interview")
        st.write(
            "Generate realistic interview questions using AI."
        )

    with c4:
        st.markdown("## 🧠")
        st.subheader("AI Evaluation")
        st.write(
            "Analyze answers and generate personalized feedback."
        )

    with c5:
        st.markdown("## 📄")
        st.subheader("Reports")
        st.write(
            "Generate professional interview performance reports."
        )

    st.divider()

    # ========================================================
    # WHY USE THIS APP
    # ========================================================

    st.header("🎯 Why Use This App?")

    st.write(
        "Turn interview practice into measurable improvement."
    )

    left, right = st.columns([2, 1])

    with left:

        with st.container(border=True):

            st.subheader("📈 Improve Interview Skills")

            st.write(
                "Practice AI-powered mock interviews and improve "
                "your confidence."
            )

            st.divider()

            st.subheader("⚡ Real-time Feedback")

            st.write(
                "Receive voice and video performance analysis."
            )

            st.divider()

            st.subheader("🧠 AI Evaluation")

            st.write(
                "AI evaluates answers and provides personalized "
                "suggestions."
            )

            st.divider()

            st.subheader("📄 Professional Reports")

            st.write(
                "Generate complete interview performance reports."
            )

    with right:

        with st.container(border=True):

            st.markdown(
                "<div style='text-align:center;font-size:80px;'>🤖</div>",
                unsafe_allow_html=True
            )

            st.subheader("AI Interview Assistant")

            st.write(
                "Your intelligent interview partner is ready."
            )

            st.success("🟢 Ready to Interview")

            st.caption(
                "💬 AI Questions • 🎤 Voice Analysis • "
                "🎥 Video Analysis • 🧠 AI Feedback"
            )

    st.divider()

    # ========================================================
    # INTERVIEW ANALYSIS FLOW
    # ========================================================

    st.header("🔄 Interview Analysis Flow")

    st.write(
        "From your first question to your final performance report."
    )

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:
        st.markdown("### 01")
        st.markdown("## 💬")
        st.subheader("AI Interview")
        st.caption("AI Questions")

    with f2:
        st.markdown("### 02")
        st.markdown("## 🎤")
        st.subheader("Voice")
        st.caption("Speech Analysis")

    with f3:
        st.markdown("### 03")
        st.markdown("## 🎥")
        st.subheader("Video")
        st.caption("Face Analysis")

    with f4:
        st.markdown("### 04")
        st.markdown("## 🧠")
        st.subheader("AI Analysis")
        st.caption("Performance Score")

    with f5:
        st.markdown("### 05")
        st.markdown("## 🏆")
        st.subheader("Final Result")
        st.caption("PDF Report")

    st.divider()

    # ========================================================
    # FINAL CTA
    # ========================================================

    st.header("🚀 Ready to Improve Your Interview Performance?")

    st.write(
        "Start an AI-powered mock interview and discover your "
        "strengths and areas for improvement."
    )

    st.divider()

    # FOOTER

    st.caption("🎯 AI Interview Performance Analyzer")

    st.caption(
        "Streamlit • OpenCV • MediaPipe • Groq AI"
    )

    st.caption(
        "Practice • Analyze • Improve 🚀"
    )


# ============================================================
# NAVIGATION
# ============================================================

home = st.Page(
    home_page,
    title="Home",
    icon="🏠",
    default=True,
)

start_interview = st.Page(
    "pages/1_start_interview.py",
    title="AI Interview",
    icon="💬",
)

face_detection = st.Page(
    "pages/4_face_detection.py",
    title="Face Detection",
    icon="📷",
)

voice_analysis = st.Page(
    "pages/5_voice_analysis.py",
    title="Voice Analysis",
    icon="🎤",
)

video_analysis = st.Page(
    "pages/6_video_analysis.py",
    title="Video Analysis",
    icon="🎥",
)

final_analysis = st.Page(
    "pages/7_final_analysis.py",
    title="Final Analysis",
    icon="🏆",
)

view_reports = st.Page(
    "pages/2_view_reports.py",
    title="View Reports",
    icon="📊",
)

live_interview = st.Page(
    "pages/8_live_interview.py",
    title="Live Interview",
    icon="🎥",
)

about_project = st.Page(
    "pages/3_about_projects.py",
    title="About Project",
    icon="ℹ️",
)


# ============================================================
# NAVIGATION MENU
# ============================================================

pg = st.navigation(
    {
        "HOME": [
            home,
        ],

        "INTERVIEW": [
            start_interview,
        ],

        "ANALYSIS": [
            face_detection,
            voice_analysis,
            video_analysis,
            final_analysis,
        ],

        "RESULTS": [
            view_reports,
        ],

        "OTHER": [
            live_interview,
            about_project,
        ],
    },
    position="sidebar",
)


# ============================================================
# SIDEBAR BRANDING
# ============================================================

with st.sidebar:

    st.divider()

    st.markdown("## 🤖 AI Interview")

    st.markdown("### Performance Analyzer")

    st.caption("AI Powered Interview System")

    st.divider()

    st.markdown("### 💡 Interview Tips")

    st.markdown(
        """
        ✅ Good Lighting

        ✅ Look at Camera

        ✅ Sit Straight

        ✅ Speak Clearly

        ✅ Stay Confident

        ✅ Avoid Filler Words
        """
    )


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()