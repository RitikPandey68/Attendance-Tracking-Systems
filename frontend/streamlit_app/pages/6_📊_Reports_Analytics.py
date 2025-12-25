import streamlit as st

st.set_page_config(page_title="Reports & Analytics", layout="wide")

st.title("📊 Reports & Analytics")

# Check login status
if not st.session_state.get('logged_in'):
    st.error("You must be logged in to view this page.")
    st.page_link("pages/1_🔐_Login.py", label="Go to Login")
    st.stop()

user_role = st.session_state.get('user', {}).get('role')

if user_role == 'faculty':
    st.info("Faculty reports and results management section is under construction.")
    # Placeholder for faculty-specific reports
    st.page_link("pages/2_🧑‍🏫_Faculty_Dashboard.py", label="Back to Dashboard")
elif user_role == 'student':
    st.info("Your detailed attendance and result reports will be displayed here.")
    # Placeholder for student-specific reports
    st.page_link("pages/3_🎓_Student_Dashboard.py", label="Back to Dashboard")
else:
    st.error("Invalid user role.")