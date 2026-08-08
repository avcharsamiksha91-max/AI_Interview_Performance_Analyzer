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
    "interview_started": False,
    "interview_completed": False,

    "current_question": "",
    "question_number": 0,

    "interview_type": "General",
    "difficulty": "Medium",
    "total_questions": 5,

    "questions": [],
    "answers": [],
    "transcripts": [],

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
        # SAVE SETTINGS
        # ----------------------------------------------------

        st.session_state["interview_type"] = interview_type
        st.session_state["difficulty"] = difficulty
        st.session_state["total_questions"] = total_questions

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
        # SAVE QUESTION
        # ----------------------------------------------------

        st.session_state["current_question"] = str(
            question
        )

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

                    wav.setnchannels(channels)

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

                    except Exception as e:

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
5. Groq AI generates the first question.
6. Start camera + microphone.
7. Answer the question.
8. Click **Finish Answer**.
9. Speech is converted to text.
10. Groq AI generates the next question.
11. Complete the interview.
12. Continue to Voice, Video and Final Analysis.
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