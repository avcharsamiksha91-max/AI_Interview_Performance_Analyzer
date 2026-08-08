import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Live Interview",
    page_icon="🎥",
    layout="wide",
)


# =====================================================
# TITLE
# =====================================================

st.title("🎥 Live AI Interview")

st.write(
    "Answer AI-generated interview questions "
    "using your camera and microphone."
)


# =====================================================
# INTERVIEW STATUS
# =====================================================

st.markdown("---")

st.subheader("🎙️ Live Interview Recording")

st.info(
    "Click START below and allow camera and microphone access."
)


# =====================================================
# VIDEO PROCESSOR
# =====================================================

class InterviewVideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.frame_count = 0

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        self.frame_count += 1

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24",
        )


# =====================================================
# CAMERA + MICROPHONE
# =====================================================

ctx = webrtc_streamer(
    key="live-interview",

    video_processor_factory=InterviewVideoProcessor,

    media_stream_constraints={
        "video": True,
        "audio": True,
    },

    async_processing=True,
)


# =====================================================
# RECORDING STATUS
# =====================================================

st.markdown("---")

if ctx.state.playing:

    st.success(
        "🟢 Camera and microphone are active."
    )

    st.write(
        "🎤 Speak your answer clearly."
    )

else:

    st.warning(
        "🔴 Interview recording is not active."
    )


# =====================================================
# INFORMATION
# =====================================================

st.markdown("---")

st.subheader("📋 Interview Flow")

st.write(
    """
    1. AI generates an interview question.

    2. Camera and microphone start.

    3. Candidate answers the question.

    4. Voice and video information is collected.

    5. AI generates the next question.

    6. Final Voice + Video + AI report is generated.
    """
)


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Live Voice + Video Interview"
)