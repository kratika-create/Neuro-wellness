import os
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

st.set_page_config(page_title="Phase 1: Advanced Face Analysis", layout="wide")

# 1. उन्नत विश्लेषण (स्माइल सिमेट्री और गोल्डन रेश्यो)
def analyze_advanced(landmarks):
    # होंठों के कोने (Left corner: 61, Right corner: 291)
    l_lip = landmarks[61].y
    r_lip = landmarks[291].y
    # स्माइल सिमेट्री का अंतर
    smile_diff = abs(l_lip - r_lip)
    
    # गोल्डन रेश्यो (Face Height vs Width)
    face_height = abs(landmarks[10].y - landmarks[152].y)
    face_width = abs(landmarks[234].x - landmarks[454].x)
    golden_ratio = face_width / face_height if face_height != 0 else 0
    
    # एक्सप्रेशन
    mouth_h = abs(landmarks[13].y - landmarks[14].y)
    state = "Smile" if mouth_h > 0.02 else "Neutral"
    
    return state, smile_diff, golden_ratio

# 2. ट्रांसफॉर्मर क्लास
class FaceLandmarkTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        self.mp_drawing = mp.solutions.drawing_utils

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        if results.multi_face_landmarks:
            for fl in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(img, fl, mp.solutions.face_mesh.FACEMESH_TESSELATION)
                state, sym, ratio = analyze_advanced(fl.landmark)
                # स्क्रीन पर डेटा दिखाएं
                cv2.putText(img, f"State: {state}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(img, f"Smile Sym Diff: {sym:.4f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        return img

# 3. UI
st.title("🧠 Neuro-Wellness: फेस सिमेट्री एनालिसिस")
webrtc_streamer(key="face-analysis", video_transformer_factory=FaceLandmarkTransformer,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

st.write("### पैरामीटर्स:")
st.write("- **Smile Sym Diff:** कम मान का मतलब है कि मुस्कान संतुलित है।")
st.write("- **Golden Ratio:** चेहरे के अनुपात की स्थिरता।")
