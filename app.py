import os
# ये लाइनें OpenCV के ग्राफिक्स एरर को रोकती हैं
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="Neuro-Wellness AI", layout="wide")

# 2. साइडबार में कानूनी चेतावनी
st.sidebar.title("⚠️ महत्वपूर्ण सूचना")
st.sidebar.warning(
    "डिस्क्लेमर: यह केवल एक स्क्रीनिंग टूल है, न कि कोई मेडिकल डायग्नोस्टिक टूल। "
    "अंतिम स्वास्थ्य संबंधी निर्णय के लिए हमेशा किसी डॉक्टर से परामर्श करें।"
)

# 3. मुख्य टाइटल
st.title("🧠 Neuro-Wellness Diagnostic Suite")
st.write("---")

# 4. फेस लैंडमार्क इंजन (पूरा कोड)
class FaceLandmarkTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = self.face_mesh.process(img_rgb)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )
        return img

# 5. स्ट्रीमिंग इंजन
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
st.subheader("कैमरा का उपयोग करके लैंडमार्क एनालिसिस शुरू करें:")
webrtc_streamer(
    key="face-analysis",
    video_transformer_factory=FaceLandmarkTransformer,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True
)

# 6. प्रोफेशनल एंडिंग
st.write("---")
st.subheader("टूल का उद्देश्य (Screening vs Diagnosis)")
st.write(
    "यह स्क्रीनिंग टूल न्यूरोलॉजिकल लक्षणों की शुरुआती पहचान में मदद करने के लिए डिज़ाइन किया गया है। "
    "इसका उद्देश्य डेटा प्रदान करना है ताकि आप अपने स्वास्थ्य को बेहतर समझ सकें।"
)
st.success("Neuro-Wellness का उपयोग करने के लिए धन्यवाद।")
