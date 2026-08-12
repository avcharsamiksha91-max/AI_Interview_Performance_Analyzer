import os
import wave
import streamlit as st

from streamlit_webrtc import webrtc_streamer

from utils.groq_helper import generate_interview_question
from utils.groq_stt import speech_to_text


# ============================================================
# FOLDERS
# ============================================================

os.makedirs("audio", exist_ok=True)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    # Interview status
    "interview_started": False,
    "interview_completed": False,

    # Candidate Information
    "candidate_name": "",
    "candidate_email": "",
    "interview_date": "",
    "candidate_info_required": False,

    # Interview question data
    "current_question": "",
    "question_number": 0,

    # Interview settings
    "interview_type": "General",
    "difficulty": "Medium",
    "total_questions": 5,

    # Interview data
    "questions": [],
    "answers": [],
    "transcripts": [],

    # Audio
    "audio_files": [],
}


for key, value in DEFAULTS.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PAGE TITLE
# ============================================================

st.title("💬 AI Interview")

st.write(
    "Practice a realistic interview with AI-generated "
    "questions using your camera and microphone."
)


# ============================================================
# INTERVIEW SETTINGS
# ============================================================

st.divider()

st.subheader("⚙️ Interview Settings")

col1, col2, col3 = st.columns(3)


# ============================================================
# INTERVIEW TYPE
# ============================================================

with col1:

    interview_type = st.selectbox(
        "Interview Type",
        [
            "General",
            "HR",
            "Technical",
            "Behavioral",
        ],
        index=[
            "General",
            "HR",
            "Technical",
            "Behavioral",
        ].index(
            st.session_state["interview_type"]
        ),
        key="interview_type_widget",
        disabled=st.session_state["interview_started"],
    )


# ============================================================
# DIFFICULTY
# ============================================================

with col2:

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
        ],
        index=[
            "Easy",
            "Medium",
            "Hard",
        ].index(
            st.session_state["difficulty"]
        ),
        key="difficulty_widget",
        disabled=st.session_state["interview_started"],
    )


# ============================================================
# NUMBER OF QUESTIONS
# ============================================================

with col3:

    total_questions = st.selectbox(
        "Number of Questions",
        [
            5,
            7,
            10,
        ],
        index=[
            5,
            7,
            10,
        ].index(
            st.session_state["total_questions"]
        ),
        key="total_questions_widget",
        disabled=st.session_state["interview_started"],
    )


# ============================================================
# START AI INTERVIEW
# ============================================================

if not st.session_state["interview_started"]:

    st.divider()

    st.subheader("🚀 Start AI Interview")

    st.write(
        "Groq AI will automatically generate your "
        "interview questions."
    )

    if st.button(
        "▶️ Start AI Interview",
        use_container_width=True,
        type="primary",
    ):

        # ----------------------------------------------------
        # SHOW CANDIDATE INFORMATION FORM
        # ----------------------------------------------------

        st.session_state["candidate_info_required"] = True

        st.rerun()


# ============================================================
# CANDIDATE INFORMATION
# ============================================================

if (
    st.session_state["candidate_info_required"]
    and not st.session_state["interview_started"]
):

    st.divider()

    st.subheader("👤 Candidate Information")

    st.write(
        "Please enter your information before starting "
        "the interview."
    )

    # --------------------------------------------------------
    # CANDIDATE NAME
    # --------------------------------------------------------

    candidate_name = st.text_input(
        "👤 Candidate Name",
        value=st.session_state["candidate_name"],
        placeholder="Enter your full name",
        key="candidate_name_input",
    )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    candidate_email = st.text_input(
        "📧 Email",
        value=st.session_state["candidate_email"],
        placeholder="Enter your email address",
        key="candidate_email_input",
    )

    # --------------------------------------------------------
    # INTERVIEW DATE
    # --------------------------------------------------------

    interview_date = st.date_input(
        "📅 Interview Date",
        key="interview_date_input",
    )

    st.divider()

    # --------------------------------------------------------
    # CONTINUE TO INTERVIEW
    # --------------------------------------------------------

    if st.button(
        "🚀 Continue to Interview",
        use_container_width=True,
        type="primary",
    ):

        # ----------------------------------------------------
        # VALIDATE NAME
        # ----------------------------------------------------

        if not candidate_name.strip():

            st.warning(
                "⚠️ Please enter your name."
            )

            st.stop()

        # ----------------------------------------------------
        # VALIDATE EMAIL
        # ----------------------------------------------------

        if not candidate_email.strip():

            st.warning(
                "⚠️ Please enter your email address."
            )

            st.stop()

        # ----------------------------------------------------
        # BASIC EMAIL VALIDATION
        # ----------------------------------------------------

        if (
            "@" not in candidate_email
            or "." not in candidate_email.split("@")[-1]
        ):

            st.warning(
                "⚠️ Please enter a valid email address."
            )

            st.stop()

        # ----------------------------------------------------
        # SAVE CANDIDATE INFORMATION
        # ----------------------------------------------------

        st.session_state["candidate_name"] = (
            candidate_name.strip()
        )

        st.session_state["candidate_email"] = (
            candidate_email.strip()
        )

        st.session_state["interview_date"] = (
            str(interview_date)
        )

        # ----------------------------------------------------
        # SAVE INTERVIEW SETTINGS
        # ----------------------------------------------------

        st.session_state["interview_type"] = (
            interview_type
        )

        st.session_state["difficulty"] = (
            difficulty
        )

        st.session_state["total_questions"] = (
            total_questions
        )

        # ----------------------------------------------------
        # RESET INTERVIEW DATA
        # ----------------------------------------------------

        st.session_state["questions"] = []

        st.session_state["answers"] = []

        st.session_state["transcripts"] = []

        st.session_state["audio_files"] = []

        st.session_state["question_number"] = 1

        st.session_state["interview_completed"] = False

        # ----------------------------------------------------
        # GENERATE FIRST QUESTION
        # ----------------------------------------------------

        with st.spinner(
            "🧠 Groq AI is generating your first question..."
        ):

            try:

                question = generate_interview_question(
                    interview_type,
                    difficulty,
                    [],
                    [],
                )

            except Exception as e:

                st.error(
                    f"❌ Groq AI Error:\n\n{e}"
                )

                st.stop()

        # ----------------------------------------------------
        # CHECK QUESTION
        # ----------------------------------------------------

        if not question:

            st.error(
                "❌ AI question was not generated."
            )

            st.stop()

        # ----------------------------------------------------
        # SAVE FIRST QUESTION
        # ----------------------------------------------------

        st.session_state["current_question"] = str(
            question
        )

        st.session_state["candidate_info_required"] = False

        st.session_state["interview_started"] = True

        st.rerun()


# ============================================================
# ACTIVE INTERVIEW
# ============================================================

if st.session_state["interview_started"]:

    question = st.session_state["current_question"]

    question_number = st.session_state["question_number"]

    total = st.session_state["total_questions"]


    # ========================================================
    # CURRENT QUESTION
    # ========================================================

    st.divider()

    st.subheader(
        f"❓ Question {question_number} of {total}"
    )

    st.success("🤖 AI Interview Question")

    st.info(question)


    # ========================================================
    # CAMERA + MICROPHONE
    # ========================================================

    st.divider()

    st.subheader("🎥🎤 Your Interview")

    st.write(
        "Click START and allow camera + microphone access."
    )


    ctx = webrtc_streamer(
        key="main_ai_interview_stream",

        media_stream_constraints={
            "video": True,
            "audio": True,
        },

        async_processing=True,

        audio_receiver_size=1024,
    )


    # ========================================================
    # CAMERA / MICROPHONE STATUS
    # ========================================================

    if ctx.state.playing:

        st.success(
            "🟢 Camera + Microphone are active."
        )

        st.info(
            "🎤 Speak your answer clearly."
        )

    else:

        st.warning(
            "🔴 Camera + Microphone are not active."
        )

        st.caption(
            "Click START above and allow browser permissions."
        )


    # ========================================================
    # TEXT ANSWER FALLBACK
    # ========================================================

    st.divider()

    st.subheader("💬 Answer")

    st.caption(
        "If voice recording is unavailable, "
        "you can type your answer below."
    )

    typed_answer = st.text_area(
        "Type your answer:",
        height=140,
        key=f"typed_answer_{question_number}",
    )


    # ========================================================
    # FINISH ANSWER
    # ========================================================

    st.divider()

    if st.button(
        "⏹️ Finish Answer",
        use_container_width=True,
        type="primary",
    ):

        transcript = ""

        # ----------------------------------------------------
        # AUDIO FRAMES
        # ----------------------------------------------------

        frames = []

        try:

            audio_receiver = getattr(
                ctx,
                "audio_receiver",
                None,
            )

            if audio_receiver is not None:

                frames = audio_receiver.get_frames(
                    timeout=0.5
                )

                if frames is None:
                    frames = []

        except Exception:

            frames = []


        # ----------------------------------------------------
        # AUDIO FILE PATH
        # ----------------------------------------------------

        audio_path = os.path.join(
            "audio",
            f"interview_answer_{question_number}.wav",
        )


        # ----------------------------------------------------
        # SAVE AUDIO
        # ----------------------------------------------------

        if frames:

            try:

                first_frame = frames[0]

                sample_rate = (
                    first_frame.sample_rate
                    or 48000
                )

                channels = len(
                    first_frame.layout.channels
                )

                audio_bytes = b""

                for frame in frames:

                    array = frame.to_ndarray()

                    audio_bytes += array.tobytes()


                with wave.open(
                    audio_path,
                    "wb",
                ) as wav:

                    wav.setnchannels(
                        channels
                    )

                    wav.setsampwidth(2)

                    wav.setframerate(
                        sample_rate
                    )

                    wav.writeframes(
                        audio_bytes
                    )


                st.success(
                    "✅ Voice recording saved."
                )

                st.audio(audio_path)


                # ------------------------------------------------
                # SPEECH TO TEXT
                # ------------------------------------------------

                with st.spinner(
                    "📝 Converting speech to text..."
                ):

                    try:

                        transcript = speech_to_text(
                            audio_path
                        )

                    except Exception:

                        st.warning(
                            "⚠️ Speech-to-text failed. "
                            "Using typed answer instead."
                        )

                        transcript = ""


            except Exception as e:

                st.warning(
                    f"⚠️ Audio processing failed: {e}"
                )

                transcript = ""


        # ----------------------------------------------------
        # TYPED ANSWER FALLBACK
        # ----------------------------------------------------

        if not transcript:

            transcript = typed_answer.strip()


        # ----------------------------------------------------
        # EMPTY ANSWER
        # ----------------------------------------------------

        if not transcript:

            st.warning(
                "⚠️ Please speak your answer "
                "or type your answer."
            )

            st.stop()


        # ----------------------------------------------------
        # SHOW ANSWER
        # ----------------------------------------------------

        st.divider()

        st.subheader("📝 Your Answer")

        st.write(transcript)


        # ----------------------------------------------------
        # SAVE QUESTION
        # ----------------------------------------------------

        st.session_state["questions"].append(
            question
        )


        # ----------------------------------------------------
        # SAVE ANSWER
        # ----------------------------------------------------

        st.session_state["answers"].append(
            transcript
        )


        # ----------------------------------------------------
        # SAVE TRANSCRIPT
        # ----------------------------------------------------

        st.session_state["transcripts"].append(
            transcript
        )


        # ----------------------------------------------------
        # SAVE AUDIO PATH
        # ----------------------------------------------------

        if os.path.exists(audio_path):

            st.session_state["audio_files"].append(
                audio_path
            )


        # ====================================================
        # LAST QUESTION
        # ====================================================

        if question_number >= total:

            st.session_state["interview_started"] = False

            st.session_state["interview_completed"] = True

            st.session_state["current_question"] = ""

            st.success(
                "🎉 AI Interview Completed Successfully!"
            )

            st.info(
                "🎤 Voice + 🎥 Interview data is ready "
                "for Final Analysis."
            )

            st.rerun()


        # ====================================================
        # GENERATE NEXT QUESTION
        # ====================================================

        with st.spinner(
            "🧠 Groq AI is generating your next question..."
        ):

            try:

                next_question = generate_interview_question(
                    st.session_state["interview_type"],
                    st.session_state["difficulty"],
                    st.session_state["questions"],
                    st.session_state["answers"],
                )

            except Exception as e:

                st.error(
                    f"❌ Groq AI Error:\n\n{e}"
                )

                st.stop()


        # ----------------------------------------------------
        # CHECK NEXT QUESTION
        # ----------------------------------------------------

        if not next_question:

            st.error(
                "❌ Next question was not generated."
            )

            st.stop()


        # ----------------------------------------------------
        # SAVE NEXT QUESTION
        # ----------------------------------------------------

        st.session_state["current_question"] = str(
            next_question
        )

        st.session_state["question_number"] = (
            question_number + 1
        )

        st.rerun()


# ============================================================
# COMPLETED INTERVIEW
# ============================================================

if st.session_state["interview_completed"]:

    st.divider()

    st.subheader("🎉 Interview Completed")

    st.success(
        "Your AI interview has been completed successfully."
    )


    # --------------------------------------------------------
    # CANDIDATE INFORMATION
    # --------------------------------------------------------

    st.subheader("👤 Candidate Information")

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:

        st.markdown("**👤 Candidate Name**")

        st.write(
            st.session_state["candidate_name"]
        )

    with info_col2:

        st.markdown("**📧 Email**")

        st.write(
            st.session_state["candidate_email"]
        )

    with info_col3:

        st.markdown("**📅 Interview Date**")

        st.write(
            st.session_state["interview_date"]
        )


    # --------------------------------------------------------
    # TOTAL QUESTIONS
    # --------------------------------------------------------

    st.metric(
        "Total Questions",
        len(
            st.session_state["questions"]
        ),
    )


    # --------------------------------------------------------
    # VIEW ANSWERS
    # --------------------------------------------------------

    with st.expander(
        "📋 View Interview Answers"
    ):

        for i, (q, a) in enumerate(
            zip(
                st.session_state["questions"],
                st.session_state["answers"],
            ),
            start=1,
        ):

            st.markdown(
                f"### ❓ Question {i}"
            )

            st.write(q)

            st.markdown(
                "### 💬 Answer"
            )

            st.write(a)

            st.divider()


    # --------------------------------------------------------
    # NEXT ANALYSIS
    # --------------------------------------------------------

    st.info(
        "➡️ Your interview answers are now available "
        "for Voice, Video and Final Analysis."
    )


# ============================================================
# START NEW INTERVIEW
# ============================================================

st.divider()

if st.button(
    "🔄 Start New Interview",
    use_container_width=True,
):

    # --------------------------------------------------------
    # RESET CANDIDATE INFORMATION
    # --------------------------------------------------------

    st.session_state["candidate_name"] = ""

    st.session_state["candidate_email"] = ""

    st.session_state["interview_date"] = ""

    st.session_state["candidate_info_required"] = False

    # --------------------------------------------------------
    # RESET INTERVIEW
    # --------------------------------------------------------

    st.session_state["interview_started"] = False

    st.session_state["interview_completed"] = False

    st.session_state["current_question"] = ""

    st.session_state["question_number"] = 0

    st.session_state["questions"] = []

    st.session_state["answers"] = []

    st.session_state["transcripts"] = []

    st.session_state["audio_files"] = []

    st.rerun()


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.subheader("🤖 How AI Interview Works")

st.write(
    """
1. Select interview type.
2. Select difficulty.
3. Select number of questions.
4. Click **Start AI Interview**.
5. Enter candidate name, email and interview date.
6. Click **Continue to Interview**.
7. Groq AI generates the first question.
8. Start camera + microphone.
9. Answer the question.
10. Click **Finish Answer**.
11. Speech is converted to text.
12. Groq AI generates the next question.
13. Complete the interview.
14. Continue to Voice, Video and Final Analysis.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Groq AI + Streamlit + WebRTC"
)