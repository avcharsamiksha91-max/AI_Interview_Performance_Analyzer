import streamlit as st
from streamlit_webrtc import webrtc_streamer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Live AI Interview",
    page_icon="🎥",
    layout="wide",
)


# ============================================================
# FLOATING CAMERA CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN PAGE
       ===================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }


    /* =====================================================
       WHATSAPP STYLE FLOATING CAMERA
       ===================================================== */

    .st-key-live-ai-interview {

        position: fixed !important;

        right: 25px !important;
        bottom: 25px !important;

        width: 360px !important;
        height: 270px !important;

        z-index: 999999 !important;

        background: #000000 !important;

        border-radius: 20px !important;

        border: 3px solid white !important;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.60) !important;

        overflow: hidden !important;

        padding: 0 !important;
        margin: 0 !important;
    }


    /* =====================================================
       WEBRTC CONTENT
       ===================================================== */

    .st-key-live-ai-interview > div {

        width: 100% !important;
        height: 100% !important;

        padding: 0 !important;
        margin: 0 !important;
    }


    .st-key-live-ai-interview iframe {

        width: 100% !important;
        height: 100% !important;

        border: none !important;

        border-radius: 17px !important;
    }


    /* =====================================================
       CAMERA LABEL
       ===================================================== */

    .st-key-live-ai-interview::before {

        content: "🎥 You";

        position: absolute;

        top: 8px;
        left: 10px;

        z-index: 1000000;

        background: rgba(0, 0, 0, 0.70);

        color: white;

        padding: 5px 10px;

        border-radius: 14px;

        font-size: 12px;

        font-weight: 600;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {

        .st-key-live-ai-interview {

            width: 240px !important;
            height: 180px !important;

            right: 12px !important;
            bottom: 12px !important;

            border-radius: 16px !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False

if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""

if "candidate_email" not in st.session_state:
    st.session_state.candidate_email = ""


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

questions = [

    "Tell me about yourself.",

    "What are your strengths and weaknesses?",

    "Why should we hire you?",

    "Where do you see yourself in five years?",

    "Why do you want to join our company."

]


# ============================================================
# HEADER
# ============================================================

st.title("🎥 Live AI Interview")

st.write(
    "Practice your interview with AI and improve "
    "your communication and presentation skills."
)


# ============================================================
# CANDIDATE INFORMATION
# ============================================================

if not st.session_state.interview_started:

    st.markdown(
        '<div class="interview-card">',
        unsafe_allow_html=True
    )

    st.subheader("👤 Candidate Information")

    name = st.text_input(
        "Candidate Name",
        value=st.session_state.candidate_name
    )

    email = st.text_input(
        "Email",
        value=st.session_state.candidate_email
    )

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        if not name.strip():

            st.warning(
                "Please enter your name."
            )

        else:

            st.session_state.candidate_name = name.strip()

            st.session_state.candidate_email = email.strip()

            st.session_state.interview_started = True

            st.session_state.question_index = 0

            st.session_state.answers = []

            st.session_state.interview_completed = False

            st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# INTERVIEW COMPLETED
# ============================================================

if st.session_state.interview_completed:

    st.success(
        "🎉 Interview Completed Successfully!"
    )

    st.subheader(
        "📋 Your Interview Answers"
    )

    for i, answer in enumerate(
        st.session_state.answers
    ):

        st.markdown(
            f"### Question {i + 1}"
        )

        st.write(
            questions[i]
        )

        st.markdown(
            "**Your Answer:**"
        )

        st.write(
            answer
            if answer
            else "No answer provided."
        )

        st.markdown("---")

    st.info(
        "Go to **Final Interview Analysis** "
        "to view your Voice + Video performance."
    )

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        st.session_state.interview_started = False

        st.session_state.question_index = 0

        st.session_state.answers = []

        st.session_state.interview_completed = False

        st.session_state.voice_transcript = ""

        st.rerun()

    st.stop()


# ============================================================
# CURRENT QUESTION
# ============================================================

current_question = questions[
    st.session_state.question_index
]


# ============================================================
# INTERVIEW PROGRESS
# ============================================================

total_questions = len(questions)

current_number = (
    st.session_state.question_index + 1
)


st.progress(
    current_number / total_questions
)

st.caption(
    f"Question {current_number} "
    f"of {total_questions}"
)


# ============================================================
# QUESTION
# ============================================================

st.markdown(
    '<div class="question-box">',
    unsafe_allow_html=True
)

st.write(
    f"🤖 Interviewer: {current_question}"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# CAMERA + MICROPHONE
# ============================================================

st.markdown(
    "### 🎥 Camera & Microphone"
)

st.write(
    "Click START and allow camera + microphone access. "
    "Your camera preview will stay floating at the "
    "bottom-right like a video call."
)


# ============================================================
# WEBRTC STREAM
# ============================================================

webrtc_ctx = webrtc_streamer(

    key="live-ai-interview",

    media_stream_constraints={
        "video": True,
        "audio": True,
    },

    async_processing=True,
)


# ============================================================
# CAMERA STATUS
# ============================================================

if webrtc_ctx.state.playing:

    st.success(
        "🟢 Camera and microphone are active."
    )

else:

    st.info(
        "📷 Click START above and allow "
        "camera + microphone permissions."
    )


# ============================================================
# ANSWER SECTION
# ============================================================

st.markdown("---")

st.subheader(
    "🎤 Your Answer"
)


answer_key = (
    f"answer_{st.session_state.question_index}"
)


answer = st.text_area(

    "Type your answer here:",

    key=answer_key,

    height=150,

    placeholder=(
        "Type your interview answer here..."
    ),
)


# ============================================================
# BUTTONS
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# SUBMIT / NEXT QUESTION
# ============================================================

with col1:

    if st.button(
        "➡️ Submit & Next Question",
        use_container_width=True
    ):

        st.session_state.answers.append(
            answer.strip()
        )

        if (
            st.session_state.question_index
            < total_questions - 1
        ):

            st.session_state.question_index += 1

            st.rerun()

        else:

            st.session_state.interview_completed = True

            st.session_state.voice_transcript = (
                "\n\n".join(
                    st.session_state.answers
                )
            )

            st.rerun()


# ============================================================
# SKIP QUESTION
# ============================================================

with col2:

    if st.button(
        "⏭️ Skip Question",
        use_container_width=True
    ):

        st.session_state.answers.append(
            ""
        )

        if (
            st.session_state.question_index
            < total_questions - 1
        ):

            st.session_state.question_index += 1

            st.rerun()

        else:

            st.session_state.interview_completed = True

            st.session_state.voice_transcript = (
                "\n\n".join(
                    st.session_state.answers
                )
            )

            st.rerun()


# ============================================================
# INTERVIEW INFORMATION
# ============================================================

st.markdown("---")

st.subheader(
    "ℹ️ Interview Information"
)

info1, info2, info3 = st.columns(3)


with info1:

    st.metric(
        "Question",
        f"{current_number}/{total_questions}"
    )


with info2:

    st.metric(
        "Answers Recorded",
        len(st.session_state.answers)
    )


with info3:

    st.metric(
        "Candidate",
        st.session_state.candidate_name
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Live Interview"
)