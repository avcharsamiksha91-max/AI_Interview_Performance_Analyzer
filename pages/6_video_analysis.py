import streamlit as st
import cv2
import av
import mediapipe as mp

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Video Analysis",
    page_icon="🎥",
    layout="wide",
)


# ============================================================
# TITLE
# ============================================================

st.title("🎥 AI Video Analysis")

st.write(
    "Analyze face presence, face position, "
    "eye contact and facial engagement."
)


# ============================================================
# SESSION DEFAULTS
# ============================================================

video_defaults = {
    "video_analysis_available": False,
    "total_frames": 0,
    "face_frames": 0,
    "center_frames": 0,
    "eye_contact_frames": 0,
    "expression_frames": 0,
    "face_score": 0,
    "position_score": 0,
    "eye_contact_score": 0,
    "expression_score": 0,
    "video_score": 0,
}

for key, value in video_defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# MEDIAPIPE
# ============================================================

mp_face_mesh = mp.solutions.face_mesh


# ============================================================
# OPENCV FACE DETECTOR
# ============================================================

cascade_path = (
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(
    cascade_path
)

if face_cascade.empty():

    st.error(
        "❌ OpenCV Haar Cascade could not be loaded."
    )

    st.stop()


# ============================================================
# VIDEO PROCESSOR
# ============================================================

class VideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.total_frames = 0
        self.face_frames = 0
        self.center_frames = 0
        self.eye_contact_frames = 0
        self.expression_frames = 0

        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )


    # ========================================================
    # PROCESS FRAME
    # ========================================================

    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        self.total_frames += 1

        height, width = img.shape[:2]


        # ====================================================
        # OPENCV FACE DETECTION
        # ====================================================

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )


        if len(faces) > 0:

            self.face_frames += 1

            x, y, w, h = max(
                faces,
                key=lambda f: f[2] * f[3]
            )


            # =================================================
            # FACE POSITION
            # =================================================

            face_center_x = x + (w / 2)

            center_ratio = (
                face_center_x / width
            )

            if 0.35 <= center_ratio <= 0.65:

                self.center_frames += 1

                position_text = "GOOD POSITION"

                position_color = (
                    0,
                    255,
                    0
                )

            else:

                position_text = "CENTER YOUR FACE"

                position_color = (
                    0,
                    165,
                    255
                )


            # =================================================
            # FACE BOX
            # =================================================

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )

            cv2.putText(
                img,
                "Face Detected",
                (x, max(y - 35, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                img,
                position_text,
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                position_color,
                2,
            )

        else:

            cv2.putText(
                img,
                "Face Not Detected",
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )


        # ====================================================
        # MEDIAPIPE FACE MESH
        # ====================================================

        rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_mesh.process(
            rgb
        )


        if results.multi_face_landmarks:

            landmarks = (
                results
                .multi_face_landmarks[0]
                .landmark
            )


            # =================================================
            # EYE CONTACT
            # =================================================

            left_outer = landmarks[33]
            left_inner = landmarks[133]
            left_iris = landmarks[468]

            right_inner = landmarks[362]
            right_outer = landmarks[263]
            right_iris = landmarks[473]


            left_eye_width = (
                left_inner.x
                - left_outer.x
            )

            if abs(left_eye_width) > 0.001:

                left_eye_ratio = (
                    left_iris.x
                    - left_outer.x
                ) / left_eye_width

            else:

                left_eye_ratio = 0.5


            right_eye_width = (
                right_outer.x
                - right_inner.x
            )

            if abs(right_eye_width) > 0.001:

                right_eye_ratio = (
                    right_iris.x
                    - right_inner.x
                ) / right_eye_width

            else:

                right_eye_ratio = 0.5


            left_good = (
                0.25
                <= left_eye_ratio
                <= 0.75
            )

            right_good = (
                0.25
                <= right_eye_ratio
                <= 0.75
            )


            if left_good and right_good:

                self.eye_contact_frames += 1

                eye_text = "EYE CONTACT: GOOD"

                eye_color = (
                    0,
                    255,
                    0
                )

            else:

                eye_text = "LOOK AT CAMERA"

                eye_color = (
                    0,
                    165,
                    255
                )


            cv2.putText(
                img,
                eye_text,
                (30, height - 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                eye_color,
                2,
            )


            # =================================================
            # FACIAL ENGAGEMENT
            # =================================================

            left_mouth = landmarks[61]
            right_mouth = landmarks[291]

            upper_lip = landmarks[13]
            lower_lip = landmarks[14]


            mouth_width = abs(
                right_mouth.x
                - left_mouth.x
            )

            mouth_height = abs(
                lower_lip.y
                - upper_lip.y
            )


            if mouth_height > 0:

                mouth_ratio = (
                    mouth_width
                    / mouth_height
                )

            else:

                mouth_ratio = 0


            face_width = abs(
                landmarks[454].x
                - landmarks[234].x
            )


            if face_width > 0:

                normalized_mouth = (
                    mouth_width
                    / face_width
                )

            else:

                normalized_mouth = 0


            if normalized_mouth > 0.18:

                self.expression_frames += 1

                expression_text = (
                    "ENGAGED EXPRESSION"
                )

                expression_color = (
                    0,
                    255,
                    0
                )

            else:

                expression_text = (
                    "NATURAL EXPRESSION"
                )

                expression_color = (
                    255,
                    255,
                    0
                )


            cv2.putText(
                img,
                expression_text,
                (30, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                expression_color,
                2,
            )


        else:

            cv2.putText(
                img,
                "Face Mesh Not Detected",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )


        # ====================================================
        # RETURN FRAME
        # ====================================================

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


# ============================================================
# LIVE CAMERA
# ============================================================

st.markdown("---")

st.subheader("📷 Live Camera")

webrtc_ctx = webrtc_streamer(
    key="video-analysis-final",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    async_processing=True,
)


# ============================================================
# INSTRUCTIONS
# ============================================================

st.markdown("---")

st.info(
    """
    ### 📷 Instructions

    1. Click **START**
    2. Allow camera permission
    3. Sit in front of the camera
    4. Keep your face near the center
    5. Look naturally toward the camera
    6. Keep camera running for 15–20 seconds
    7. Click **🔄 Update Results**
    8. Check your Video Analysis Dashboard
    """
)


# ============================================================
# UPDATE RESULTS
# ============================================================

st.markdown("---")

if st.button(
    "🔄 Update Results",
    use_container_width=True,
):

    if webrtc_ctx.video_processor:

        processor = webrtc_ctx.video_processor

        total_frames = processor.total_frames
        face_frames = processor.face_frames
        center_frames = processor.center_frames
        eye_contact_frames = (
            processor.eye_contact_frames
        )
        expression_frames = (
            processor.expression_frames
        )


        # ====================================================
        # CALCULATE SCORES
        # ====================================================

        if total_frames > 0:

            face_score = int(
                face_frames
                / total_frames
                * 100
            )

            position_score = int(
                center_frames
                / total_frames
                * 100
            )

            eye_contact_score = int(
                eye_contact_frames
                / total_frames
                * 100
            )

            expression_score = int(
                expression_frames
                / total_frames
                * 100
            )

            video_score = int(
                (
                    face_score
                    + position_score
                    + eye_contact_score
                    + expression_score
                )
                / 4
            )

        else:

            face_score = 0
            position_score = 0
            eye_contact_score = 0
            expression_score = 0
            video_score = 0


        # ====================================================
        # SAVE SESSION RESULTS
        # ====================================================

        st.session_state[
            "video_analysis_available"
        ] = total_frames > 0

        st.session_state[
            "total_frames"
        ] = total_frames

        st.session_state[
            "face_frames"
        ] = face_frames

        st.session_state[
            "center_frames"
        ] = center_frames

        st.session_state[
            "eye_contact_frames"
        ] = eye_contact_frames

        st.session_state[
            "expression_frames"
        ] = expression_frames

        st.session_state[
            "face_score"
        ] = face_score

        st.session_state[
            "position_score"
        ] = position_score

        st.session_state[
            "eye_contact_score"
        ] = eye_contact_score

        st.session_state[
            "expression_score"
        ] = expression_score

        st.session_state[
            "video_score"
        ] = video_score


        if total_frames > 0:

            st.success(
                "✅ Video analysis results updated!"
            )

        else:

            st.warning(
                "⚠️ No video frames captured."
            )

    else:

        st.warning(
            "⚠️ Please click START and "
            "turn on the camera first."
        )


# ============================================================
# READ RESULTS
# ============================================================

total_frames = st.session_state.get(
    "total_frames",
    0
)

face_frames = st.session_state.get(
    "face_frames",
    0
)

center_frames = st.session_state.get(
    "center_frames",
    0
)

eye_contact_frames = st.session_state.get(
    "eye_contact_frames",
    0
)

expression_frames = st.session_state.get(
    "expression_frames",
    0
)

face_score = st.session_state.get(
    "face_score",
    0
)

position_score = st.session_state.get(
    "position_score",
    0
)

eye_contact_score = st.session_state.get(
    "eye_contact_score",
    0
)

expression_score = st.session_state.get(
    "expression_score",
    0
)

video_score = st.session_state.get(
    "video_score",
    0
)


# ============================================================
# STATUS
# ============================================================

st.markdown("---")

st.subheader(
    "🔧 Video Processing Status"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Frames",
        total_frames
    )

with c2:

    st.metric(
        "Faces",
        face_frames
    )

with c3:

    st.metric(
        "Eye Contact",
        eye_contact_frames
    )

with c4:

    st.metric(
        "Expression",
        expression_frames
    )


# ============================================================
# DASHBOARD
# ============================================================

st.markdown("---")

st.subheader(
    "📊 Video Analysis Dashboard"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "👤 Face Presence",
        f"{face_score}%"
    )

with c2:

    st.metric(
        "🧍 Face Position",
        f"{position_score}%"
    )

with c3:

    st.metric(
        "👀 Eye Contact",
        f"{eye_contact_score}%"
    )

with c4:

    st.metric(
        "🙂 Expression",
        f"{expression_score}%"
    )


# ============================================================
# VIDEO SCORE
# ============================================================

st.markdown("---")

st.subheader(
    "🎥 Overall Video Score"
)

st.metric(
    "🎥 Video Score",
    f"{video_score}/100"
)

st.progress(
    min(
        max(video_score, 0),
        100
    )
)


# ============================================================
# PROGRESS
# ============================================================

st.write("👤 Face Presence")

st.progress(
    min(
        max(face_score, 0),
        100
    )
)

st.write("🧍 Face Position")

st.progress(
    min(
        max(position_score, 0),
        100
    )
)

st.write("👀 Eye Contact")

st.progress(
    min(
        max(eye_contact_score, 0),
        100
    )
)

st.write("🙂 Facial Engagement")

st.progress(
    min(
        max(expression_score, 0),
        100
    )
)


# ============================================================
# FEEDBACK
# ============================================================

st.markdown("---")

st.subheader(
    "💡 Video Feedback"
)

if total_frames == 0:

    st.info(
        "🎥 Start the camera, record for "
        "15–20 seconds, then click "
        "🔄 Update Results."
    )

elif video_score >= 80:

    st.success(
        "🏆 Excellent video interview presence!"
    )

elif video_score >= 60:

    st.warning(
        "👍 Good performance. Try to improve "
        "eye contact and keep your face centered."
    )

else:

    st.error(
        "⚠️ Improve camera position, eye contact "
        "and facial engagement."
    )


# ============================================================
# TIPS
# ============================================================

st.markdown("---")

st.subheader(
    "💡 Video Interview Tips"
)

st.success(
    """
    ✅ Look toward the camera

    ✅ Keep your face centered

    ✅ Maintain good lighting

    ✅ Sit at a comfortable distance

    ✅ Avoid excessive head movement

    ✅ Keep a natural facial expression

    ✅ Smile naturally when appropriate

    ✅ Maintain professional body language
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | "
    "Video Analysis Module"
)