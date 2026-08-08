import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Face Detection",
    page_icon="📷",
    layout="wide",
)


# ============================================================
# TITLE
# ============================================================

st.title("📷 AI Face Detection")

st.write(
    "Live face, eye and smile detection using OpenCV."
)


# ============================================================
# LOAD CASCADE CLASSIFIERS
# ============================================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_eye.xml"
)

smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_smile.xml"
)


# ============================================================
# CHECK CASCADE FILES
# ============================================================

if face_cascade.empty():
    st.error("❌ Face detection model could not be loaded.")
    st.stop()

if eye_cascade.empty():
    st.warning("⚠️ Eye detection model could not be loaded.")

if smile_cascade.empty():
    st.warning("⚠️ Smile detection model could not be loaded.")


# ============================================================
# FACE DETECTOR
# ============================================================

class FaceDetector(VideoProcessorBase):

    def recv(self, frame):

        # Convert WebRTC frame to OpenCV image
        img = frame.to_ndarray(format="bgr24")

        # Convert to grayscale
        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # ----------------------------------------------------
        # LIGHTING
        # ----------------------------------------------------

        brightness = gray.mean()

        if brightness >= 120:
            lighting_text = "Good Lighting"
        else:
            lighting_text = "Low Lighting"

        # ----------------------------------------------------
        # FACE DETECTION
        # ----------------------------------------------------

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # ----------------------------------------------------
        # PROCESS EACH FACE
        # ----------------------------------------------------

        for (x, y, w, h) in faces:

            # Face rectangle
            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

            # Face label
            cv2.putText(
                img,
                "Face",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # ------------------------------------------------
            # FACE REGION
            # ------------------------------------------------

            roi_gray = gray[
                y:y + h,
                x:x + w
            ]

            roi_color = img[
                y:y + h,
                x:x + w
            ]

            # ------------------------------------------------
            # EYE DETECTION
            # ------------------------------------------------

            if not eye_cascade.empty():

                eyes = eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=6,
                    minSize=(20, 20)
                )

                for (ex, ey, ew, eh) in eyes:

                    cv2.rectangle(
                        roi_color,
                        (ex, ey),
                        (ex + ew, ey + eh),
                        (255, 0, 0),
                        2
                    )

            # ------------------------------------------------
            # SMILE DETECTION
            # ------------------------------------------------

            if not smile_cascade.empty():

                smiles = smile_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.7,
                    minNeighbors=15,
                    minSize=(25, 25)
                )

                for (sx, sy, sw, sh) in smiles:

                    cv2.rectangle(
                        roi_color,
                        (sx, sy),
                        (sx + sw, sy + sh),
                        (0, 255, 255),
                        2
                    )

        # ----------------------------------------------------
        # INFORMATION ON VIDEO
        # ----------------------------------------------------

        face_count = len(faces)

        if face_count > 0:

            status_text = "Face Detected"

            status_color = (0, 255, 0)

        else:

            status_text = "No Face Detected"

            status_color = (0, 0, 255)

        cv2.putText(
            img,
            status_text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            status_color,
            2
        )

        cv2.putText(
            img,
            f"Faces: {face_count}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            img,
            lighting_text,
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        # ----------------------------------------------------
        # RETURN VIDEO FRAME
        # ----------------------------------------------------

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


# ============================================================
# CAMERA
# ============================================================

st.markdown("---")

st.subheader("🎥 Live Camera")

st.write(
    "Click **START** and allow camera permission."
)

ctx = webrtc_streamer(
    key="face_detection_camera",
    video_processor_factory=FaceDetector,
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    async_processing=True,
)


# ============================================================
# CAMERA STATUS
# ============================================================

if ctx.state.playing:

    st.success(
        "🟢 Camera is active — Face detection is running."
    )

else:

    st.warning(
        "🔴 Camera is not active. Click START and allow camera access."
    )


# ============================================================
# DETECTION LEGEND
# ============================================================

st.markdown("---")

st.subheader("🎨 Detection Legend")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟩 Face")

with col2:
    st.info("🟦 Eyes")

with col3:
    st.warning("🟨 Smile")


# ============================================================
# INTERVIEW TIPS
# ============================================================

st.markdown("---")

st.subheader("💡 Interview Tips")

st.info(
    """
    ✅ Sit straight

    ✅ Keep your face visible

    ✅ Maintain eye contact

    ✅ Smile naturally

    ✅ Ensure good lighting

    ✅ Avoid background distractions
    """
)