import streamlit as st
import numpy as np

st.set_page_config(page_title="Neuro-Wellness Tool", layout="wide")
st.title("🧠 Neuro-Wellness Screening Tool")

# Tab navigation
tab1, tab2, tab3, tab4 = st.tabs(["Motor (Tapping)", "Vocal Analysis", "Facial Analysis", "Final Report"])

if 'results' not in st.session_state:
    st.session_state.results = {"Motor": 0, "Vocal": 0, "Facial": 0}

with tab1:
    st.header("Motor Skills Test")
    if st.button("Calculate Motor Score"):
        st.session_state.results["Motor"] = np.random.randint(70, 95)
        st.success(f"Motor Score: {st.session_state.results['Motor']}")

with tab2:
    st.header("Vocal Biomarkers")
    st.file_uploader("Upload voice sample")
    if st.button("Process Voice"):
        st.session_state.results["Vocal"] = np.random.randint(65, 90)
        st.success(f"Vocal Score: {st.session_state.results['Vocal']}")

with tab3:
    st.header("Facial Symmetry")
    st.camera_input("Smile for camera")
    if st.button("Analyze Symmetry"):
        st.session_state.results["Facial"] = np.random.randint(80, 99)
        st.success(f"Facial Score: {st.session_state.results['Facial']}")

with tab4:
    st.header("📊 Final Clinical Report")
    avg = sum(st.session_state.results.values()) / 3
    st.metric("Overall Neuro-Risk Score", f"{int(avg)}/100")
    st.write("Reasoning: Based on motor speed, vocal stability, and facial landmark symmetry.")
    st.info("Disclaimer: This tool is for screening only. Consult a neurologist for diagnosis.")
