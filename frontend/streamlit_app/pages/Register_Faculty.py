import streamlit as st
import requests
from datetime import date
import re

def validate_password(password):
    """Validate password strength"""
    if len(password) < 10:
        return False, "Password must be at least 10 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least 1 uppercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least 1 number"
    
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return False, "Password must contain at least 1 special character"
    
    # Check for repeated characters
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            return False, "Password cannot contain repeated characters"
    
    return True, "Password is strong"

def register_faculty():
    st.title("👨🏫 Faculty Registration")
    st.markdown("---")
    
    # Personal Information
    st.header("👤 Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        email = st.text_input("Email Address*", placeholder="faculty@example.com")
        
        # Password with validation
        password = st.text_input("Password*", type="password", placeholder="Minimum 10 characters")
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        
        st.info("""📋 **Password Requirements:**
        • Minimum 10 characters
        • At least 1 uppercase letter
        • At least 1 number
        • At least 1 special character (!@#$%^&*)
        • No repeated characters""")
        
        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Re-enter your password")
        mobile_no = st.text_input("Mobile Number*", placeholder="+91 XXXXXXXXXX")
        
    with col2:
        dob = st.date_input("Date of Birth*", min_value=date(1940, 1, 1), max_value=date(2050, 12, 31))
        address = st.text_area("Address*", placeholder="Complete postal address")
        employee_id = st.text_input("Employee ID*", placeholder="e.g., EMP001")
    
    # Professional Information
    st.header("🏫 Professional Information")
    col1, col2 = st.columns(2)
    
    with col1:
        # College/University Selection (same as student)
        college_options = [
            "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur", "IIT Roorkee", "IIT Guwahati",
            "IIT Hyderabad", "IIT Indore", "IIT Mandi", "IIT Patna", "IIT Ropar", "IIT Bhubaneswar", "IIT Gandhinagar",
            "IIT Jodhpur", "IIT Tirupati", "IIT Bhilai", "IIT Goa", "IIT Jammu", "IIT Dharwad", "IIT Palakkad",
            "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Rourkela", "NIT Durgapur",
            "NIT Jamshedpur", "NIT Kurukshetra", "NIT Surat", "NIT Allahabad", "NIT Bhopal", "NIT Nagpur",
            "NIT Jalandhar", "NIT Hamirpur", "NIT Silchar", "NIT Agartala", "NIT Arunachal Pradesh", "NIT Delhi",
            "NIT Goa", "NIT Manipur", "NIT Meghalaya", "NIT Mizoram", "NIT Nagaland", "NIT Puducherry",
            "NIT Sikkim", "NIT Uttarakhand", "NIT Andhra Pradesh", "NIT Patna", "NIT Raipur", "NIT Jaipur",
            "IIIT Hyderabad", "IIIT Bangalore", "IIIT Delhi", "IIIT Allahabad", "IIIT Gwalior", "IIIT Jabalpur",
            "IIIT Kancheepuram", "IIIT Lucknow", "IIIT Vadodara", "IIIT Nagpur", "IIIT Pune", "IIIT Kota",
            "IIIT Sonepat", "IIIT Kalyani", "IIIT Tiruchirappalli", "IIIT Una", "IIIT Surat", "IIIT Manipur",
            "IIIT Kottayam", "IIIT Ranchi", "IIIT Bhagalpur", "IIIT Bhopal", "IIIT Dharwad", "IIIT Raichur",
            "AKTU (Dr. A.P.J. Abdul Kalam Technical University)", "VTU (Visvesvaraya Technological University)",
            "Anna University", "Osmania University", "Jawaharlal Nehru University", "Delhi University",
            "Pune University", "Mumbai University", "Calcutta University", "Madras University",
            "Bangalore University", "Mysore University", "Kerala University", "Andhra University",
            "Rajasthan University", "Gujarat University", "Utkal University", "Gauhati University",
            "Jamia Millia Islamia", "Aligarh Muslim University", "Banaras Hindu University",
            "Jadavpur University", "Indian Statistical Institute", "Tata Institute of Social Sciences",
            "Manipal Academy of Higher Education", "SRM Institute of Science and Technology",
            "Vellore Institute of Technology", "Birla Institute of Technology and Science",
            "Amity University", "Lovely Professional University", "Chandigarh University",
            "Other"
        ]
        
        college = st.selectbox("College/University*", college_options)
        if college == "Other":
            college = st.text_input("Enter College/University Name*", placeholder="Type your college name")
        
        # Department Selection - Feature 2 (same as student streams)
        department_options = [
            "Computer Science and Engineering (CSE)", 
            "Information Science and Engineering (ISE)", 
            "Computer Science and Information Technology (CSE IT)",
            "Information Technology (IT)",
            "Artificial Intelligence & Machine Learning (AI&ML)",
            "Data Science and Engineering",
            "Cyber Security and Digital Forensics",
            "Electrical and Electronics Engineering (EEE)", 
            "Electronics and Communication Engineering (ECE)",
            "Mechanical Engineering", 
            "Civil Engineering",
            "Chemical Engineering",
            "Biotechnology Engineering", 
            "Aerospace Engineering", 
            "Automobile Engineering",
            "Industrial Engineering and Management",
            "Environmental Engineering",
            "Mining Engineering",
            "Petroleum Engineering",
            "Textile Engineering",
            "Agricultural Engineering",
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology and Life Sciences",
            "Statistics",
            "Business Administration and Management",
            "Management Studies",
            "Commerce and Accounting",
            "Economics and Finance",
            "English Literature and Language",
            "Other - Specify Department"
        ]
        
        department = st.selectbox("Department* (Choose from list)", department_options)
        if department == "Other - Specify Department":
            st.info("📝 Please specify your department below:")
            department = st.text_input("Specify Your Department*", placeholder="Type your department name here")
            if not department:
                st.warning("⚠️ Please enter your department name")
    
    with col2:
        # Designation Selection - Feature 1
        designation_options = [
            "Professor", 
            "Associate Professor", 
            "Assistant Professor", 
            "Lecturer",
            "Head of Department (HOD)",
            "Principal",
            "Accountant",
            "Librarian"
        ]
        
        designation = st.selectbox("Position/Designation*", designation_options)
        
        # Education Qualification - Feature 2
        education_options = [
            "Ph.D (Doctor of Philosophy)",
            "M.Tech (Master of Technology)",
            "M.E (Master of Engineering)",
            "M.Sc (Master of Science)",
            "MBA (Master of Business Administration)",
            "MCA (Master of Computer Applications)",
            "M.A (Master of Arts)",
            "M.Com (Master of Commerce)",
            "B.Tech (Bachelor of Technology)",
            "B.E (Bachelor of Engineering)",
            "B.Sc (Bachelor of Science)",
            "BBA (Bachelor of Business Administration)",
            "BCA (Bachelor of Computer Applications)",
            "B.A (Bachelor of Arts)",
            "B.Com (Bachelor of Commerce)",
            "Other - Specify Education"
        ]
        
        highest_education = st.selectbox("Highest Education Qualification*", education_options)
        if highest_education == "Other - Specify Education":
            st.info("📝 Please specify your highest education:")
            highest_education = st.text_input("Specify Your Highest Education*", placeholder="Type your qualification here")
            if not highest_education:
                st.warning("⚠️ Please enter your education qualification")
        
        experience_years = st.number_input("Years of Experience*", min_value=0, max_value=50, value=0)
        
        specialization = st.text_input("Specialization/Subject*", placeholder="e.g., Machine Learning, Database Systems")
    
    st.markdown("---")
    
    if st.button("📝 Register Faculty", type="primary", use_container_width=True):
        # Validation
        if not all([name, email, password, confirm_password, mobile_no, department, designation, 
                   college, highest_education, specialization, employee_id, dob, address]):
            st.error("❌ Please fill all required fields (*)")
            return
            
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
            return
            
        # Password validation
        is_valid, message = validate_password(password)
        if not is_valid:
            st.error(f"❌ {message}")
            return
            
        if len(mobile_no) < 10:
            st.error("❌ Please enter a valid mobile number!")
            return
            
        try:
            response = requests.post(
                "http://127.0.0.1:8000/auth/register/faculty", 
                json={
                    "name": name,
                    "email": email,
                    "password": password,
                    "mobile_no": mobile_no,
                    "department": department,
                    "designation": designation,
                    "college": college,
                    "highest_education": highest_education,
                    "specialization": specialization,
                    "employee_id": employee_id,
                    "dob": dob.isoformat(),
                    "address": address,
                    "experience_years": experience_years
                }
            )
            
            if response.status_code == 200:
                st.success("✅ Faculty registered successfully!")
                st.balloons()
                st.info("📧 Please check your email for verification instructions.")
                
                if st.button("🚪 Go to Login", use_container_width=True):
                    st.switch_page("pages/1_🔐_Login.py")
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"❌ Registration failed: {error_detail}")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to server. Please make sure the backend is running.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    st.info("💡 **Note:** All fields marked with * are mandatory. After registration, you'll receive an email verification link.")

if __name__ == "__main__":
    register_faculty()