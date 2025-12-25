import streamlit as st
import requests

# Set the title of the app
st.title("Login Page")

# Create a form for user login
with st.form(key='login_form'):
    email = st.text_input("Email Address", "")
    password = st.text_input("Password", "", type='password')
    submit_button = st.form_submit_button("Login")

    if submit_button:
        # Log the authentication attempt
        requests.post("http://127.0.0.1:3000/log_authentication/", json={"email": email, "password": password})
        
        # Call the backend API for authentication
        response = requests.post("http://127.0.0.1:3000/auth/login", json={"email": email, "password": password})
        
        if response.status_code == 200:
            st.success("Login successful!")
            # Redirect to the dashboard or another page
            st.session_state['user'] = response.json()
            st.experimental_rerun()
        else:
            st.error("Login failed: " + response.json().get("detail", "Unknown error"))

# Link to registration page
st.write("New User? [Register Here](Register_Student.py)")
