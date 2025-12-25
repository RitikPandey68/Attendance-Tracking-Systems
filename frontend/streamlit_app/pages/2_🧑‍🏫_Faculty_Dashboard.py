import streamlit as st
import pandas as pd
import requests
import os

# It's better to get the backend URL from an environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:3000")

def faculty_dashboard():
    st.set_page_config(page_title="Faculty Dashboard", layout="wide")
    st.title("🧑‍🏫 Faculty Dashboard")

    # Check login status
    if not st.session_state.get('logged_in') or st.session_state.get('user', {}).get('role') != 'faculty':
        st.error("You must be logged in as a faculty member to view this page.")
        st.page_link("pages/1_🔐_Login.py", label="Go to Login")
        st.stop()

    user = st.session_state.get('user', {})
    st.write(f"Welcome, {user.get('name', 'Faculty Member')}!")

    st.sidebar.header("Faculty Menu")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/1_🔐_Login.py")
    
    DEV_MODE = st.sidebar.checkbox("Use Mock Data (Dev Mode)", value=True)

    # --- Dashboard Features ---
    st.header("Student Management")

    # Search for a student
    search_usn = st.text_input("Enter Student USN to fetch details")
    student_data = None

    if st.button("Search Student"):
        if search_usn:
            if DEV_MODE:
                st.success("DEV MODE: Using mock data.")
                with st.spinner("Fetching student data..."):
                    student_data = {
                        "name": "Jane Doe", "father_name": "Robert Doe", "mother_name": "Mary Doe",
                        "usn": search_usn, "dob": "2002-08-15", "address": "456 ML Street",
                        "course": "Electronics", "specialization": "VLSI", "mob_no": "9876543210",
                        "email": "jane.doe@example.com",
                        "sem_cgpa": {"Sem 1": 9.0, "Sem 2": 8.7, "Sem 3": 9.2},
                        "total_cgpa": 8.97,
                        "attendance_percentage": 92.0
                    }
            else:
                try:
                    st.info("DEV MODE OFF: Calling real backend API...")
                    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
                    response = requests.get(f"{BACKEND_URL}/students/{search_usn}", headers=headers, timeout=10)
                    if response.status_code == 200:
                        student_data = response.json()
                    else:
                        st.error(f"Student not found or error: {response.json().get('detail', response.text)}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the backend: {e}")
        else:
            st.warning("Please enter a USN.")

    if student_data:
        st.subheader(f"Details for {student_data['name']} ({student_data['usn']})")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Father's Name:** {student_data['father_name']}")
            st.write(f"**Mother's Name:** {student_data['mother_name']}")
            st.write(f"**DOB:** {student_data['dob']}")
            st.write(f"**Course:** {student_data['course']} ({student_data['specialization']})")
        with col2:
            st.write(f"**Mobile:** {student_data['mob_no']}")
            st.write(f"**Email:** {student_data['email']}")
            st.write(f"**Address:** {student_data['address']}")

        st.metric("Overall Attendance", f"{student_data['attendance_percentage']}%")
        st.metric("Total CGPA", f"{student_data['total_cgpa']}")
        st.subheader("Semester-wise CGPA")
        st.bar_chart(pd.DataFrame.from_dict(student_data['sem_cgpa'], orient='index', columns=['CGPA']))

    st.divider()

    st.header("Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.page_link("pages/5_📷_Capture_Attendance.py", label="📷 Capture Attendance", use_container_width=True)
    with col2:
        st.page_link("pages/6_📊_Reports_Analytics.py", label="📝 Manage Results & Reports", use_container_width=True)
    with col3:
        st.page_link("pages/7_📅_Holidays_Leaves.py", label="📅 Holidays & Leaves", use_container_width=True)

if __name__ == "__main__":
    faculty_dashboard()