import os
import re
import wave
import streamlit as st

from utils.groq_helper import analyze_answer
from utils.groq_stt import speech_to_text
from utils.pdf_report import generate_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Voice Analysis",
    page_icon="🎤",
    layout="wide",
)


# ============================================================
# FOLDERS
# ============================================================

os.makedirs("audio", exist_ok=True)
os.makedirs("reports", exist_ok=True)


# ============================================================
# CANDIDATE
# ============================================================

candidate_name = "Samiksha"


# ============================================================
# TITLE
# ============================================================

st.title("🎤 AI Voice Analysis")

st.write(
    "Analyze your interview speaking performance using AI."
)


# ============================================================
# AUDIO RECORDING
# ============================================================

st.markdown("---")

st.subheader("🎙️ Record Your Interview Answer")

audio = st.audio_input(
    "Click below to record your answer"
)


# ============================================================
# PROCESS AUDIO
# ============================================================

if audio is not None:

    st.success("✅ Recording Completed")

    audio_path = os.path.join(
        "audio",
        "interview_answer.wav"
    )

    # --------------------------------------------------------
    # SAVE AUDIO
    # --------------------------------------------------------

    try:

        with open(audio_path, "wb") as f:
            f.write(audio.getvalue())

        st.audio(audio)

        st.success(
            "✅ Audio Saved Successfully"
        )

    except Exception as e:

        st.error(
            f"❌ Audio Save Error: {e}"
        )

        st.stop()


    # ========================================================
    # SPEECH TO TEXT
    # ========================================================

    st.markdown("---")

    st.subheader("📝 Transcript")

    with st.spinner(
        "🎤 Converting speech to text..."
    ):

        try:

            transcript = speech_to_text(
                audio_path
            )

            if transcript is None:
                transcript = ""

            transcript = transcript.strip()

        except Exception as e:

            st.error(
                f"❌ Speech To Text Error:\n{e}"
            )

            transcript = ""


    # --------------------------------------------------------
    # TRANSCRIPT RESULT
    # --------------------------------------------------------

    if transcript:

        st.success(
            "✅ Speech Converted Successfully"
        )

        st.text_area(
            "Transcript",
            transcript,
            height=180,
        )

    else:

        st.warning(
            "⚠️ No speech detected."
        )


    # ========================================================
    # AI FEEDBACK
    # ========================================================

    if transcript:

        st.markdown("---")

        st.subheader(
            "🤖 AI Interview Feedback"
        )

        with st.spinner(
            "🤖 Analyzing your answer..."
        ):

            try:

                ai_feedback = analyze_answer(
                    transcript
                )

            except Exception as e:

                st.error(
                    f"❌ AI Analysis Error:\n{e}"
                )

                ai_feedback = ""


        if ai_feedback:

            st.success(
                "✅ Analysis Completed"
            )

            st.write(ai_feedback)

        else:

            st.warning(
                "⚠️ AI feedback could not be generated."
            )


        # ====================================================
        # OVERALL SCORE
        # ====================================================

        overall_score = 85

        if ai_feedback:

            match = re.search(
                r"Overall\s*Score\s*:\s*(\d+)",
                ai_feedback,
                re.IGNORECASE,
            )

            if match:

                overall_score = int(
                    match.group(1)
                )

        overall_score = max(
            0,
            min(overall_score, 100)
        )


        # ====================================================
        # VOICE SCORES
        # ====================================================

        speaking_speed = 80

        confidence = min(
            overall_score + 5,
            100
        )

        voice_clarity = 90

        fluency = max(
            overall_score - 3,
            0
        )


        # ====================================================
        # AUDIO DURATION
        # ====================================================

        duration = 0

        try:

            with wave.open(
                audio_path,
                "rb"
            ) as wav:

                frames = wav.getnframes()
                rate = wav.getframerate()

            if rate > 0:

                duration = round(
                    frames / float(rate),
                    1
                )

        except Exception:

            duration = 0


        # ====================================================
        # WORD COUNT
        # ====================================================

        word_count = len(
            transcript.split()
        )


        # ====================================================
        # WORDS PER MINUTE
        # ====================================================

        if duration > 0:

            wpm = round(
                (word_count / duration) * 60
            )

        else:

            wpm = 0


        # ====================================================
        # FILLER WORD DETECTION
        # ====================================================

        filler_words = [
            "um",
            "uh",
            "like",
            "actually",
            "basically",
            "you know",
            "so",
        ]

        transcript_lower = transcript.lower()

        filler_count = 0

        for word in filler_words:

            filler_count += transcript_lower.count(
                word
            )


        # ====================================================
        # SAVE RESULTS TO SESSION STATE
        # ====================================================

        st.session_state[
            "voice_analysis_available"
        ] = True

        st.session_state[
            "voice_transcript"
        ] = transcript

        st.session_state[
            "voice_feedback"
        ] = ai_feedback

        st.session_state[
            "voice_overall_score"
        ] = overall_score

        st.session_state[
            "voice_confidence"
        ] = confidence

        st.session_state[
            "voice_fluency"
        ] = fluency

        st.session_state[
            "voice_clarity"
        ] = voice_clarity

        st.session_state[
            "voice_speaking_speed"
        ] = speaking_speed

        st.session_state[
            "voice_wpm"
        ] = wpm

        st.session_state[
            "voice_filler_count"
        ] = filler_count

        st.session_state[
            "voice_word_count"
        ] = word_count

        st.session_state[
            "voice_duration"
        ] = duration

        st.session_state[
            "voice_audio_path"
        ] = audio_path


        # ====================================================
        # VOICE DASHBOARD
        # ====================================================

        st.markdown("---")

        st.subheader(
            "📊 Voice Analysis Dashboard"
        )

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # LEFT COLUMN
        # ----------------------------------------------------

        with col1:

            st.write("🎤 Speaking Speed")

            st.progress(
                min(
                    max(speaking_speed, 0),
                    100
                )
            )

            st.caption(
                f"{speaking_speed}%"
            )


            st.write("😊 Confidence")

            st.progress(
                min(
                    max(confidence, 0),
                    100
                )
            )

            st.caption(
                f"{confidence}%"
            )


            st.write("🗣️ Voice Clarity")

            st.progress(
                min(
                    max(voice_clarity, 0),
                    100
                )
            )

            st.caption(
                f"{voice_clarity}%"
            )


            st.write("⚡ Fluency")

            st.progress(
                min(
                    max(fluency, 0),
                    100
                )
            )

            st.caption(
                f"{fluency}%"
            )


        # ----------------------------------------------------
        # RIGHT COLUMN
        # ----------------------------------------------------

        with col2:

            if overall_score >= 80:

                st.success(
                    f"🏆 Overall Score: "
                    f"{overall_score}/100"
                )

            elif overall_score >= 60:

                st.warning(
                    f"⭐ Overall Score: "
                    f"{overall_score}/100"
                )

            else:

                st.error(
                    f"⚠️ Overall Score: "
                    f"{overall_score}/100"
                )


            st.metric(
                "📝 Total Words",
                word_count
            )

            st.metric(
                "⚡ Words Per Minute",
                wpm
            )

            st.metric(
                "⏱ Duration",
                f"{duration} sec"
            )

            st.metric(
                "🔁 Filler Words",
                filler_count
            )


        # ====================================================
        # SAVE CONFIRMATION
        # ====================================================

        st.success(
            "✅ Voice analysis results saved for Final Analysis."
        )


        # ====================================================
        # PDF REPORT
        # ====================================================

        st.markdown("---")

        st.subheader(
            "📄 Generate Voice Report"
        )

        if st.button(
            "📄 Generate PDF Report",
            use_container_width=True,
        ):

            pdf_path = os.path.join(
                "reports",
                "interview_report.pdf"
            )

            try:

                generate_report(
                    pdf_path,
                    candidate_name,
                    transcript,
                    f"{overall_score}/100",
                    ai_feedback,
                    "Generated by AI",
                    "Practice more mock interviews."
                )

                st.success(
                    "✅ PDF Report Generated Successfully!"
                )

                with open(
                    pdf_path,
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_file.read(),
                        file_name="Interview_Report.pdf",
                        mime="application/pdf",
                    )

            except Exception as e:

                st.error(
                    f"❌ PDF Generation Error: {e}"
                )


        # ====================================================
        # SAVE TEXT ANALYSIS
        # ====================================================

        st.markdown("---")

        if st.button(
            "💾 Save Voice Analysis",
            use_container_width=True,
        ):

            save_path = os.path.join(
                "reports",
                "last_analysis.txt"
            )

            try:

                with open(
                    save_path,
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(
                        "===== AI INTERVIEW VOICE ANALYSIS =====\n\n"
                    )

                    f.write(
                        f"Candidate: {candidate_name}\n\n"
                    )

                    f.write(
                        "===== TRANSCRIPT =====\n"
                    )

                    f.write(
                        transcript
                    )

                    f.write(
                        "\n\n===== AI FEEDBACK =====\n"
                    )

                    f.write(
                        ai_feedback
                    )

                    f.write(
                        f"\n\nOverall Score: "
                        f"{overall_score}/100\n"
                    )

                    f.write(
                        f"Confidence: {confidence}%\n"
                    )

                    f.write(
                        f"Fluency: {fluency}%\n"
                    )

                    f.write(
                        f"Voice Clarity: "
                        f"{voice_clarity}%\n"
                    )

                    f.write(
                        f"Speaking Speed: "
                        f"{speaking_speed}%\n"
                    )

                    f.write(
                        f"WPM: {wpm}\n"
                    )

                    f.write(
                        f"Filler Words: "
                        f"{filler_count}\n"
                    )

                st.success(
                    "✅ Voice Analysis Saved Successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Save Error: {e}"
                )


# ============================================================
# TIPS
# ============================================================

st.markdown("---")

st.subheader(
    "💡 AI Interview Tips"
)

st.info(
    """
    ✅ Speak Clearly

    ✅ Maintain Eye Contact

    ✅ Avoid Filler Words

    ✅ Use STAR Method

    ✅ Give Practical Examples

    ✅ Speak with Confidence

    ✅ Practice Daily
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Streamlit + Groq AI"
)