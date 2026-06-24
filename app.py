import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# 1. Page Config
st.set_page_config(page_title="Neuro-Wellness AI", layout="centered")

# 2. UI
st.title("🧠 Neuro-Wellness AI")

# 3. WebRTC Configuration (यह कनेक्शन एरर को कम करेगा)
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# 4. Face Transformer
class FaceTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, 
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
    
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    img, face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION
                )
        return img

# 5. App Flow
webrtc_streamer(
    key="example",
    video_transformer_factory=FaceTransformer,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False}
)
