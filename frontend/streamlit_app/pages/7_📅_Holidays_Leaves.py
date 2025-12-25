import streamlit as st

st.set_page_config(page_title="Holidays & Leaves", layout="wide")

st.title("📅 Holidays & Leaves")

# Check login status
if not st.session_state.get('logged_in'):
    st.error("You must be logged in to view this page.")
    st.page_link("pages/1_🔐_Login.py", label="Go to Login")
    st.stop()

user_role = st.session_state.get('user', {}).get('role')

st.info("This feature is under construction.")

if user_role == 'faculty':
    st.page_link("pages/2_🧑‍🏫_Faculty_Dashboard.py", label="Back to Dashboard")
elif user_role == 'student':
    st.page_link("pages/3_🎓_Student_Dashboard.py", label="Back to Dashboard")
