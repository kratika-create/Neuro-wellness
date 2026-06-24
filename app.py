import os
# यह कोड OpenCV को ग्राफिक्स ड्राइवर के बिना चलने के लिए मजबूर करेगा
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

import streamlit as st
try:
    import cv2
except ImportError:
    st.error("OpenCV लाइब्रेरी लोड नहीं हो सकी। कृपया सुनिश्चित करें कि 'opencv-python-headless' आपके requirements.txt में है।")

import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# बाकी आपका ओरिजिनल कोड यहाँ से शुरू होगा...import os
# यह लाइन OpenCV के ग्राफिक्स एरर को ब्लॉक करती है
os.environ["QT_QPA_PLATFORM"] = "offscreen" 

import streamlit as st
import cv2
# ... बाकी कोड import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# 1. पेज सेटअप
st.set_page_config(page_title="Neuro-Wellness AI", layout="wide")

# 2. साइडबार डिस्क्लेमर
st.sidebar.title("⚠️ महत्वपूर्ण सूचना")
st.sidebar.warning("डिस्क्लेमर: यह केवल एक स्क्रीनिंग टूल है, डायग्नोस्टिक नहीं।")

# 3. टाइटल और इंट्रो
st.title("🧠 Neuro-Wellness Diagnostic Suite")
st.write("---")

# 4. MediaPipe का पावरफुल इंजन
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# 5. एडवांस वीडियो ट्रांसफॉर्मर क्लास
class FaceLandmarkTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # यहाँ से शुरू होता है असली फेस एनालिसिस इंजन
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(img_rgb)
            
            # 468 लैंडमार्क्स ड्रा करना
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=img,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                    )
        return img

# 6. एडवांस स्ट्रीमिंग कॉन्फ़िगरेशन
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

webrtc_streamer(
    key="face-analysis",
    video_transformer_factory=FaceLandmarkTransformer,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True,
)

# 7. प्रोफेशनल एंडिंग और स्पष्टीकरण
st.write("---")
st.subheader("टूल का उद्देश्य (Screening vs Diagnosis)")
st.write(
    "यह स्क्रीनिंग टूल न्यूरोलॉजिकल लक्षणों की शुरुआती पहचान में मदद करने के लिए डिज़ाइन किया गया है। "
    "अंतिम चिकित्सा निर्णय हमेशा एक पेशेवर डॉक्टर द्वारा ही लिए जाने चाहिए।"
)
st.success("धन्यवाद! इस टूल का उपयोग जिम्मेदारी से करें।")
