import streamlit as st
import pandas as pd
import requests
import os

# It's better to get the backend URL from an environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:3000")

def student_dashboard():
    st.set_page_config(page_title="Student Dashboard", layout="wide")
    st.title("🎓 Student Dashboard")

    # Check login status
    if not st.session_state.get('logged_in') or st.session_state.get('user', {}).get('role') != 'student':
        st.error("You must be logged in as a student to view this page.")
        st.page_link("pages/1_🔐_Login.py", label="Go to Login")
        st.stop()

    user = st.session_state.get('user', {})
    st.write(f"Welcome, {user.get('name', 'Student')}!")

    st.sidebar.header("Student Menu")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/1_🔐_Login.py")

    DEV_MODE = st.sidebar.checkbox("Use Mock Data (Dev Mode)", value=True)

    # --- Dashboard Features ---
    st.header("Your Profile")
    # Assuming the user object from login contains all necessary details
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {user.get('name')}")
        st.write(f"**USN:** {user.get('usn')}")
        st.write(f"**Course:** {user.get('course', '')} ({user.get('specialization', '')})")
        st.write(f"**Email:** {user.get('email')}")
    with col2:
        st.write(f"**Father's Name:** {user.get('father_name')}")
        st.write(f"**Mother's Name:** {user.get('mother_name')}")
        st.write(f"**DOB:** {user.get('dob')}")
        st.write(f"**Mobile:** {user.get('mob_no')}")

    st.divider()

    st.header("Academic Summary")
    attendance_summary = None
    results_summary = None
    
    if DEV_MODE:
        st.success("DEV MODE: Using mock data.")
        attendance_summary = {"overall_percentage": 85.5, "total_classes": 100, "attended_classes": 85}
        results_summary = {"total_cgpa": 8.8, "sem_cgpa": {"Sem 1": 8.5, "Sem 2": 8.8, "Sem 3": 9.1}}
    else:
        try:
            st.info("DEV MODE OFF: Calling real backend API...")
            headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
            # In a real app, you would fetch this data from your backend
            # For now, we'll just show a message.
            st.warning("Backend endpoints for student summary are not yet implemented.")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend: {e}")
    
    if attendance_summary and results_summary:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Attendance")
            st.metric(
                "Overall Attendance",
                f"{attendance_summary['overall_percentage']}%",
                f"{attendance_summary['attended_classes']} / {attendance_summary['total_classes']} classes"
            )
            st.page_link("pages/6_📊_Reports_Analytics.py", label="View Detailed Attendance Report")
    
        with col2:
            st.subheader("Results")
            st.metric("Total CGPA", f"{results_summary['total_cgpa']}")
            st.page_link("pages/6_📊_Reports_Analytics.py", label="View Detailed Results")
    
        st.subheader("Semester-wise CGPA")
        st.line_chart(pd.DataFrame.from_dict(results_summary['sem_cgpa'], orient='index', columns=['CGPA']))

    st.divider()

    st.header("Leaves & Holidays")
    st.page_link("pages/7_📅_Holidays_Leaves.py", label="View Holidays and Manage Leaves")

if __name__ == "__main__":
    student_dashboard()