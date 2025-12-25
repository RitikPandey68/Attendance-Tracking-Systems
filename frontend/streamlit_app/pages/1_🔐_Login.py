import streamlit as st
import requests
import os
from datetime import datetime

# It's better to get the backend URL from an environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:3000")

st.set_page_config(page_title="Login", layout="centered")

def login_user(email, password=None, usn=None, dob=None):
    """Function to authenticate user and handle response."""
    login_data = {
        "username": email,
        "password": password,
        "usn": usn,
        "dob": dob,
    }
    # Filter out None values and create a dummy password for student login if needed
    if login_as == "Student":
        login_data["password"] = "student_login_dummy_pass" # FastAPI's OAuth2PasswordRequestForm needs a password

    login_data = {k: v for k, v in login_data.items() if v is not None}

    try:
        # The backend should determine if it's a student or faculty login
        # based on the fields provided.
        auth_url = f"{BACKEND_URL}/auth/login"
        response = requests.post(
            auth_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )

        if response.status_code == 200:
            user_data = response.json()
            st.session_state['logged_in'] = True
            st.session_state['user'] = user_data  # Contains role, name, token, etc.
            st.success("Login successful!")

            # Redirect based on role
            role = user_data.get("role")
            if role == 'faculty':
                st.switch_page("pages/2_🧑‍🏫_Faculty_Dashboard.py")
            elif role == 'student':
                st.switch_page("pages/3_🎓_Student_Dashboard.py")
            else:
                st.error("Unknown user role. Please contact support.")

        else:
            error_detail = "Unknown error"
            try:
                error_detail = response.json().get("detail", error_detail)
            except requests.exceptions.JSONDecodeError:
                error_detail = response.text
            st.error(f"Login failed: {error_detail}")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the authentication service: {e}")

# --- UI ---
st.title("Welcome to the Attendance & Result Portal")

login_as = st.radio("Login as:", ("Faculty", "Student"), horizontal=True)

if login_as == "Faculty":
    with st.form(key='faculty_login_form'):
        st.subheader("Faculty Login")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type='password')
        if st.form_submit_button("Login"):
            login_user(email=email, password=password)

elif login_as == "Student":
    with st.form(key='student_login_form'):
        st.subheader("Student Login")
        email = st.text_input("Email Address")
        usn = st.text_input("USN (University Seat Number)")
        dob = st.date_input("Date of Birth", value=None, min_value=datetime(1980, 1, 1))
        if st.form_submit_button("Login"):
            login_user(email=email, usn=usn, dob=str(dob))

st.divider()

# --- Developer Mode Login ---
st.sidebar.subheader("Developer Login")
if st.sidebar.button("Login as Faculty (Dev)"):
    st.session_state['logged_in'] = True
    st.session_state['user'] = {
        "name": "Dr. Dev Faculty",
        "email": "faculty.dev@example.com",
        "role": "faculty",
        "access_token": "fake_token_for_dev"
    }
    st.success("Logged in as developer faculty!")
    st.switch_page("pages/2_🧑‍🏫_Faculty_Dashboard.py")

if st.sidebar.button("Login as Student (Dev)"):
    st.session_state['logged_in'] = True
    st.session_state['user'] = {
        "name": "Dev Student", "usn": "1DEV21CS001", "course": "Computer Science",
        "specialization": "AI/ML", "email": "student.dev@example.com",
        "father_name": "Mr. Dev", "mother_name": "Mrs. Dev", "dob": "2003-01-01",
        "mob_no": "1234567890", "role": "student", "access_token": "fake_token_for_dev"
    }
    st.success("Logged in as developer student!")
    st.switch_page("pages/3_🎓_Student_Dashboard.py")

st.page_link("pages/4_📝_Register_New_User.py", label="New User? Register Here")