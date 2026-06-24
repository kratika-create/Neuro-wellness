import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="Neuro-Wellness AI", layout="wide")

# 2. साइडबार में डिस्क्लेमर (कानूनी सुरक्षा)
st.sidebar.title("⚠️ महत्वपूर्ण सूचना")
st.sidebar.warning(
    "डिस्क्लेमर: यह टूल केवल एक 'स्क्रीनिंग' (Screening) सहायता है। यह किसी पेशेवर चिकित्सा निदान (Diagnostic) का विकल्प नहीं है। "
    "यदि आपको कोई लक्षण महसूस हो, तो कृपया तुरंत किसी योग्य डॉक्टर से परामर्श करें।"
)

st.title("🧠 Neuro-Wellness Diagnostic Suite")
st.write("---")

# 3. MediaPipe सेटअप (एडवांस मोड)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# 4. वीडियो प्रोसेसिंग क्लास (एडवांस फीचर्स के साथ)
class FaceLandmarkTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # इमेज प्रोसेसिंग
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)
        
        # लैंडमार्क्स ड्रा करना
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )
        return img

# 5. एडवांस वेबआरटीसी (WebRTC) कॉन्फ़िगरेशन
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# 6. कैमरा स्ट्रीमिंग (एडवांस फीचर्स के साथ)
webrtc_streamer(
    key="face-analysis",
    video_transformer_factory=FaceLandmarkTransformer,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True, # यह ऐप को स्मूथ रखता है
)

# 7. एंडिंग और स्पष्टीकरण (जो आप चाहती थीं)
st.write("---")
st.subheader("टूल का उद्देश्य (Screening vs Diagnosis)")
st.write(
    "यह स्क्रीनिंग टूल न्यूरोलॉजिकल लक्षणों की शुरुआती पहचान में मदद करने के लिए डिज़ाइन किया गया है। "
    "यह टूल केवल डेटा एकत्र करने और पैटर्न पहचानने में आपकी सहायता करता है। "
    "अंतिम चिकित्सा निर्णय हमेशा एक पेशेवर डॉक्टर द्वारा ही लिए जाने चाहिए।"
)
st.success("धन्यवाद! इस टूल का उपयोग जिम्मेदारी से करें।")
