import streamlit as st

st.title("🧠 Neuro-Wellness Screening Tool")
st.write("Welcome! This tool helps in early screening of neurological markers.")

# Tab system for different tests
tab1, tab2, tab3 = st.tabs(["Motor (Tapping)", "Vocal Analysis", "Facial Symmetry"])

with tab1:
    st.header("Motor Skills Test")
    if st.button("Start Tapping Test"):
        st.info("Tap the button below as fast as you can for 10 seconds!")

with tab2:
    st.header("Vocal Biomarkers")
    uploaded_file = st.file_uploader("Upload voice recording", type=['wav', 'mp3'])
    if uploaded_file:
        st.success("Voice processed!")

with tab3:
    st.header("Facial Symmetry")
    st.write("Using MediaPipe for landmark analysis...")
    st.camera_input("Take a photo for analysis")
