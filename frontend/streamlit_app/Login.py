import os
import streamlit as st
import requests

# It's better to get the backend URL from an environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:3000")

# Set the title of the app
st.title("Login Page")

# Create a form for user login
with st.form(key='login_form'):
    email = st.text_input("Email Address")
    password = st.text_input("Password", type='password')
    submit_button = st.form_submit_button("Login")

    if submit_button:
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            try:
                # Call the backend API for authentication
                auth_url = f"{BACKEND_URL}/auth/login"
                response = requests.post(
                    auth_url,
                    data={"username": email, "password": password},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=5  # Add a timeout for robustness
                )

                if response.status_code == 200:
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = response.json()
                    st.success("Login successful!")
                    # Use st.switch_page for modern multipage app navigation
                    st.switch_page("pages/01_Dashboard.py")
                else:
                    error_detail = "Unknown error"
                    try:
                        error_detail = response.json().get("detail", error_detail)
                    except requests.exceptions.JSONDecodeError:
                        error_detail = response.text
                    st.error(f"Login failed: {error_detail}")

            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the authentication service: {e}")

# Link to registration page
st.page_link("pages/02_Register_Student.py", label="New User? Register Here")
