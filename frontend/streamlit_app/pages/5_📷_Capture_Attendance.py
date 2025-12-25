import streamlit as st

st.set_page_config(page_title="Capture Attendance", layout="wide")

st.title("📷 Capture Attendance")

# Check login status and role
if not st.session_state.get('logged_in') or st.session_state.get('user', {}).get('role') != 'faculty':
    st.error("You must be logged in as a faculty member to view this page.")
    st.page_link("pages/1_🔐_Login.py", label="Go to Login")
    st.stop()

st.info("This feature is under construction. The AI-powered face recognition attendance system will be implemented here.")

# Placeholder for camera input and attendance marking logic
# e.g., st.camera_input("Scan faces for attendance")

st.page_link("pages/2_🧑‍🏫_Faculty_Dashboard.py", label="Back to Dashboard")