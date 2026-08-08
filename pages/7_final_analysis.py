import os
import streamlit as st

from utils.pdf_report import generate_final_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Final Interview Analysis",
    page_icon="🎯",
    layout="wide",
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🎯 Final AI Interview Analysis"
)

st.write(
    "Combined AI analysis of your Voice "
    "and Video interview performance."
)


# ============================================================
# HELPER
# ============================================================

def get_score(
    key,
    default=0
):

    value = st.session_state.get(
        key,
        default
    )

    try:

        return int(
            float(value)
        )

    except Exception:

        return default


# ============================================================
# VOICE RESULTS
# ============================================================

voice_available = st.session_state.get(
    "voice_analysis_available",
    False
)

voice_score = get_score(
    "voice_overall_score"
)

voice_confidence = get_score(
    "voice_confidence"
)

voice_fluency = get_score(
    "voice_fluency"
)

voice_clarity = get_score(
    "voice_clarity"
)

voice_speed = get_score(
    "voice_speaking_speed"
)

voice_wpm = get_score(
    "voice_wpm"
)

voice_filler = get_score(
    "voice_filler_count"
)

transcript = st.session_state.get(
    "voice_transcript",
    ""
)

voice_feedback = st.session_state.get(
    "voice_feedback",
    ""
)


# ============================================================
# VIDEO RESULTS
# ============================================================

video_available = st.session_state.get(
    "video_analysis_available",
    False
)

video_score = get_score(
    "video_score"
)

face_presence = get_score(
    "face_score"
)

face_position = get_score(
    "position_score"
)

eye_contact = get_score(
    "eye_contact_score"
)

expression = get_score(
    "expression_score"
)


# ============================================================
# ANALYSIS STATUS
# ============================================================

st.markdown("---")

st.subheader(
    "📡 Analysis Status"
)

status1, status2 = st.columns(2)


with status1:

    if voice_available:

        st.success(
            "🎤 Voice Analysis Available"
        )

    else:

        st.warning(
            "🎤 Voice Analysis Not Available"
        )


with status2:

    if video_available:

        st.success(
            "🎥 Video Analysis Available"
        )

    else:

        st.warning(
            "🎥 Video Analysis Not Available"
        )


# ============================================================
# FINAL SCORE
# ============================================================

if voice_available and video_available:

    final_score = round(
        (
            voice_score * 0.50
        )
        +
        (
            video_score * 0.50
        )
    )

elif voice_available:

    final_score = voice_score

elif video_available:

    final_score = video_score

else:

    final_score = 0


final_score = max(
    0,
    min(final_score, 100)
)


st.session_state[
    "final_score"
] = final_score


# ============================================================
# FINAL SCORE DISPLAY
# ============================================================

st.markdown("---")

st.subheader(
    "🏆 Final Interview Score"
)


if final_score >= 80:

    st.success(
        f"🏆 Excellent Performance — "
        f"{final_score}/100"
    )

elif final_score >= 60:

    st.warning(
        f"⭐ Good Performance — "
        f"{final_score}/100"
    )

elif final_score > 0:

    st.error(
        f"⚠️ Needs Improvement — "
        f"{final_score}/100"
    )

else:

    st.info(
        "Complete Voice and Video Analysis first."
    )


st.progress(
    min(max(final_score, 0), 100)
)

st.caption(
    f"Overall Interview Score: "
    f"{final_score}/100"
)


# ============================================================
# VOICE ANALYSIS
# ============================================================

st.markdown("---")

st.subheader(
    "🎤 Voice Analysis"
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Voice Score",
        f"{voice_score}/100"
    )


with c2:

    st.metric(
        "😊 Confidence",
        f"{voice_confidence}%"
    )


with c3:

    st.metric(
        "⚡ Fluency",
        f"{voice_fluency}%"
    )


with c4:

    st.metric(
        "🗣️ Clarity",
        f"{voice_clarity}%"
    )


# ============================================================
# VIDEO ANALYSIS
# ============================================================

st.markdown("---")

st.subheader(
    "🎥 Video Analysis"
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Video Score",
        f"{video_score}/100"
    )


with c2:

    st.metric(
        "👤 Face Presence",
        f"{face_presence}%"
    )


with c3:

    st.metric(
        "👀 Eye Contact",
        f"{eye_contact}%"
    )


with c4:

    st.metric(
        "😊 Expression",
        f"{expression}%"
    )


# ============================================================
# VOICE PERFORMANCE
# ============================================================

st.markdown("---")

st.subheader(
    "📊 Voice Performance"
)

c1, c2 = st.columns(2)


with c1:

    st.write(
        "🎤 Speaking Speed"
    )

    st.progress(
        min(max(voice_speed, 0), 100)
    )

    st.caption(
        f"{voice_speed}%"
    )


with c2:

    st.write(
        "⚡ Fluency"
    )

    st.progress(
        min(max(voice_fluency, 0), 100)
    )

    st.caption(
        f"{voice_fluency}%"
    )


# ============================================================
# VIDEO PERFORMANCE
# ============================================================

st.subheader(
    "🎥 Video Performance"
)

c1, c2 = st.columns(2)


with c1:

    st.write(
        "👤 Face Presence"
    )

    st.progress(
        min(max(face_presence, 0), 100)
    )

    st.caption(
        f"{face_presence}%"
    )


with c2:

    st.write(
        "📍 Face Position"
    )

    st.progress(
        min(max(face_position, 0), 100)
    )

    st.caption(
        f"{face_position}%"
    )


# ============================================================
# VOICE STATISTICS
# ============================================================

st.markdown("---")
st.subheader("📈 Voice Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "📝 Words",
        st.session_state.get(
            "voice_word_count",
            0
        )
    )

with c2:
    st.metric(
        "⚡ WPM",
        st.session_state.get(
            "voice_wpm",
            0
        )
    )

with c3:
    st.metric(
        "🔁 Filler Words",
        st.session_state.get(
            "voice_filler_count",
            0
        )
    )


# ============================================================
# AI FEEDBACK
# ============================================================

if voice_feedback:

    st.markdown("---")

    st.subheader(
        "🤖 AI Interview Feedback"
    )

    st.write(
        voice_feedback
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.markdown("---")

st.subheader(
    "💡 Personalized Recommendations"
)

recommendations = []


if voice_available:

    if voice_confidence < 70:

        recommendations.append(
            "Improve confidence while speaking."
        )


    if voice_fluency < 70:

        recommendations.append(
            "Practice fluency and reduce "
            "unnecessary pauses."
        )


    if voice_filler > 5:

        recommendations.append(
            "Reduce filler words such as "
            "um, uh and like."
        )


if video_available:

    if eye_contact < 70:

        recommendations.append(
            "Maintain better eye contact "
            "with the camera."
        )


    if face_presence < 70:

        recommendations.append(
            "Keep your face clearly visible "
            "in the camera."
        )


    if face_position < 70:

        recommendations.append(
            "Keep your face centered "
            "in the camera frame."
        )


    if expression < 70:

        recommendations.append(
            "Maintain a natural and "
            "professional facial expression."
        )


if not recommendations:

    if voice_available or video_available:

        recommendations.append(
            "Excellent performance! "
            "Keep practicing."
        )

    else:

        recommendations.append(
            "Complete Voice and Video Analysis "
            "to receive personalized recommendations."
        )


for item in recommendations:

    st.write(
        f"• {item}"
    )


# ============================================================
# FINAL PDF
# ============================================================

st.markdown("---")

st.subheader(
    "📄 Final Interview Report"
)

st.write(
    "Generate a complete PDF containing "
    "Voice + Video analysis."
)


if st.button(
    "📄 Generate Final PDF Report",
    use_container_width=True,
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    pdf_path = (
        "reports/final_interview_report.pdf"
    )


    try:

        generate_final_report(

            filename=pdf_path,

            candidate_name="Samiksha",

            final_score=final_score,

            # Voice
            voice_score=voice_score,
            confidence=voice_confidence,
            fluency=voice_fluency,
            voice_clarity=voice_clarity,
            speaking_speed=voice_speed,
            wpm=voice_wpm,
            filler_words=voice_filler,

            # Video
            video_score=video_score,
            face_presence=face_presence,
            face_position=face_position,
            eye_contact=eye_contact,
            expression=expression,

            # Text
            transcript=transcript,
            ai_feedback=voice_feedback,
            recommendations=recommendations,
        )


        st.success(
            "✅ Final PDF Report Generated Successfully!"
        )


        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            pdf_data = pdf_file.read()


        st.download_button(
            label="⬇️ Download Final Interview Report",
            data=pdf_data,
            file_name="AI_Interview_Final_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


    except Exception as e:

        st.error(
            f"❌ PDF Generation Error: {e}"
        )


# ============================================================
# SAVE FINAL RESULTS
# ============================================================

st.markdown("---")

if st.button(
    "💾 Save Final Analysis",
    use_container_width=True,
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    save_path = (
        "reports/final_analysis.txt"
    )


    try:

        with open(
            save_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "===== AI INTERVIEW FINAL ANALYSIS =====\n\n"
            )

            file.write(
                "Candidate: Samiksha\n\n"
            )

            file.write(
                f"Final Score: "
                f"{final_score}/100\n\n"
            )

            file.write(
                f"Voice Score: "
                f"{voice_score}/100\n"
            )

            file.write(
                f"Confidence: "
                f"{voice_confidence}%\n"
            )

            file.write(
                f"Fluency: "
                f"{voice_fluency}%\n"
            )

            file.write(
                f"Voice Clarity: "
                f"{voice_clarity}%\n"
            )

            file.write(
                f"Speaking Speed: "
                f"{voice_speed}%\n"
            )

            file.write(
                f"WPM: {voice_wpm}\n"
            )

            file.write(
                f"Filler Words: "
                f"{voice_filler}\n\n"
            )

            file.write(
                f"Video Score: "
                f"{video_score}/100\n"
            )

            file.write(
                f"Face Presence: "
                f"{face_presence}%\n"
            )

            file.write(
                f"Face Position: "
                f"{face_position}%\n"
            )

            file.write(
                f"Eye Contact: "
                f"{eye_contact}%\n"
            )

            file.write(
                f"Expression: "
                f"{expression}%\n\n"
            )

            file.write(
                "===== TRANSCRIPT =====\n"
            )

            file.write(
                transcript
            )

            file.write(
                "\n\n===== AI FEEDBACK =====\n"
            )

            file.write(
                voice_feedback
            )

            file.write(
                "\n\n===== RECOMMENDATIONS =====\n"
            )

            for item in recommendations:

                file.write(
                    f"- {item}\n"
                )


        st.success(
            "✅ Final Analysis Saved Successfully!"
        )


    except Exception as e:

        st.error(
            f"❌ Save Error: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Voice + Video + AI Evaluation"
)