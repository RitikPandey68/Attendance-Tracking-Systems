import streamlit as st
import requests
import json
from datetime import datetime, timedelta

def login():
    st.title("🔐 Login")
    st.markdown("---")
    
    # Check if user is already logged in
    if "access_token" in st.session_state and "user_role" in st.session_state:
        st.success(f"Already logged in as {st.session_state.user_role}")
        if st.button("Go to Dashboard"):
            if st.session_state.user_role == "student":
                st.switch_page("pages/3_🎓_Student_Dashboard.py")
            else:
                st.switch_page("pages/2_🧑‍🏫_Faculty_Dashboard.py")
        return
    
    email = st.text_input("📧 Email Address")
    password = st.text_input("🔒 Password", type="password")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("🚪 Login", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password")
                return
                
            try:
                response = requests.post(
                    "http://127.0.0.1:3000/auth/login", 
                    data={"username": email, "password": password}
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.access_token = token_data["access_token"]
                    
                    # Decode token to get user role
                    import jwt
                    from backend.core.config import settings
                    
                    try:
                        payload = jwt.decode(
                            token_data["access_token"], 
                            settings.SECRET_KEY, 
                            algorithms=[settings.ALGORITHM]
                        )
                        st.session_state.user_role = payload.get("role")
                        st.session_state.user_email = payload.get("sub")
                        
                        st.success("✅ Login successful!")
                        st.rerun()
                        
                    except jwt.PyJWTError:
                        st.error("Token validation failed")
                        
                else:
                    st.error("❌ Login failed. Please check your credentials.")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to server. Please make sure the backend is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("📝 New User? Register Here", use_container_width=True):
            st.switch_page("pages/Register_Student.py")
    
    st.markdown("---")
    st.info("💡 **Login Instructions:**")
    st.write("- Students: Use your registered email and password")
    st.write("- Faculty: Use your institutional email and password")
    st.write("- Forgot password? Contact your institution administrator")

if __name__ == "__main__":
    login()
