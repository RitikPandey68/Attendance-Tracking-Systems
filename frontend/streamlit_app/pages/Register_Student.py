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

def register_student():
    st.title("🎓 Student Registration")
    st.markdown("---")
    
    # Personal Information
    st.header("👤 Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        email = st.text_input("Email Address*", placeholder="student@example.com")
        
        # Password with validation - Feature 3
        password = st.text_input("Password*", type="password", placeholder="Minimum 10 characters with requirements")
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        
        st.info("""📋 **Password Requirements (All Mandatory):**
        • Minimum 10 characters
        • At least 1 uppercase letter (A-Z)
        • At least 1 number (0-9)
        • At least 1 special character (!@#$%^&*)
        • No repeated characters (aa, 11, etc. not allowed)""")
        
        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Re-enter your password")
        dob = st.date_input("Date of Birth*", min_value=date(1940, 1, 1), max_value=date(2050, 12, 31), value=date(2000, 1, 1))
        
    with col2:
        father_name = st.text_input("Father's Name*", placeholder="Father's full name")
        mother_name = st.text_input("Mother's Name*", placeholder="Mother's full name")
        mobile_no = st.text_input("Mobile Number*", placeholder="+91 XXXXXXXXXX")
        address = st.text_area("Address*", placeholder="Complete postal address")
    
    # Academic Information
    st.header("📚 Academic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        usn = st.text_input("USN (University Seat Number)*", placeholder="e.g., 1RV20CS001")
        year = st.selectbox("Academic Year*", [1, 2, 3, 4], index=0)
        
        # College/University Selection - Feature 2
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
            "Other - Specify Your College Name"
        ]
        
        college = st.selectbox("College/University* (Choose from list)", college_options)
        if college == "Other - Specify Your College Name":
            st.info("📝 Please specify your college name below:")
            college = st.text_input("Specify Your College/University Name*", placeholder="Type your college name here")
            if not college:
                st.warning("⚠️ Please enter your college name")
        
        course_options = [
            "B.Tech", "M.Tech", "B.E", "M.E", "BBA", "MBA", "BCA", "MCA",
            "B.Sc", "M.Sc", "B.Com", "M.Com", "BA", "MA"
        ]
        course = st.selectbox("Course*", course_options)
    
    with col2:
        # Updated Specialization options - Feature 4
        if course in ["B.Tech", "M.Tech", "B.E", "M.E"]:
            specialization_options = [
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
                "Agricultural Engineering"
            ]
        elif course in ["BCA", "MCA"]:
            specialization_options = [
                "Computer Applications", 
                "Software Development and Engineering", 
                "Data Science and Analytics",
                "Web Development and Design", 
                "Mobile Application Development", 
                "Cloud Computing and DevOps",
                "Cyber Security",
                "Artificial Intelligence",
                "Machine Learning and Deep Learning",
                "Database Management Systems"
            ]
        elif course in ["B.Sc", "M.Sc"]:
            specialization_options = [
                "B.Sc in Computer Science",
                "B.Sc in Information Technology",
                "B.Sc in Data Science and Analytics",
                "B.Sc in Mathematics", 
                "B.Sc in Physics", 
                "B.Sc in Chemistry", 
                "B.Sc in Biology and Life Sciences",
                "B.Sc in Biotechnology",
                "B.Sc in Electronics",
                "B.Sc in Statistics",
                "B.Sc in Environmental Science"
            ]
        elif course in ["BBA", "MBA"]:
            specialization_options = [
                "Business Administration and Management", 
                "Finance and Accounting", 
                "Marketing and Sales Management", 
                "Human Resources Management",
                "International Business", 
                "Operations and Supply Chain Management", 
                "Entrepreneurship and Innovation",
                "Digital Marketing and E-Commerce",
                "Business Analytics and Intelligence"
            ]
        else:
            specialization_options = [
                "General Studies", 
                "Economics and Finance", 
                "Commerce and Accounting", 
                "English Literature and Language", 
                "History and Political Science", 
                "Psychology and Behavioral Sciences",
                "Sociology and Social Work",
                "Philosophy and Ethics",
                "Geography and Environmental Studies",
                "Fine Arts and Design"
            ]
        
        specialization = st.selectbox("Specialization/Stream*", specialization_options)
    
    st.markdown("---")
    
    if st.button("📝 Register Student", type="primary", use_container_width=True):
        # Validation
        if not all([name, email, password, confirm_password, dob, father_name, mother_name, 
                   address, mobile_no, usn, course, specialization, college]):
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
            # Map specialization to stream
            stream_mapping = {
                "Computer Science and Engineering (CSE)": "Computer Science",
                "Information Science and Engineering (ISE)": "Information Technology",
                "Computer Science and Information Technology (CSE IT)": "Information Technology",
                "Information Technology (IT)": "Information Technology",
                "Artificial Intelligence & Machine Learning (AI&ML)": "Artificial Intelligence",
                "Data Science and Engineering": "Data Science",
                "Cyber Security and Digital Forensics": "Cybersecurity",
                "Electrical and Electronics Engineering (EEE)": "Electrical Engineering",
                "Electronics and Communication Engineering (ECE)": "Electronics Engineering",
                "Mechanical Engineering": "Mechanical Engineering",
                "Civil Engineering": "Civil Engineering",
                "Chemical Engineering": "Chemical Engineering",
                "Biotechnology Engineering": "Biotechnology",
                "Aerospace Engineering": "Aerospace Engineering",
                "Automobile Engineering": "Automobile Engineering",
                "Industrial Engineering and Management": "Industrial Engineering",
                "Environmental Engineering": "Environmental Engineering",
                "Mining Engineering": "Mining Engineering",
                "Petroleum Engineering": "Petroleum Engineering",
                "Textile Engineering": "Textile Engineering",
                "Agricultural Engineering": "Agricultural Engineering",
                "Computer Applications": "Computer Science",
                "Software Development and Engineering": "Computer Science",
                "Data Science and Analytics": "Data Science",
                "Web Development and Design": "Computer Science",
                "Mobile Application Development": "Computer Science",
                "Cloud Computing and DevOps": "Computer Science",
                "Cyber Security": "Cybersecurity",
                "Artificial Intelligence": "Artificial Intelligence",
                "Machine Learning and Deep Learning": "Artificial Intelligence",
                "Database Management Systems": "Computer Science",
                "B.Sc in Computer Science": "Computer Science",
                "B.Sc in Information Technology": "Information Technology",
                "B.Sc in Data Science and Analytics": "Data Science",
                "B.Sc in Mathematics": "Mathematics",
                "B.Sc in Physics": "Physics",
                "B.Sc in Chemistry": "Chemistry",
                "B.Sc in Biology and Life Sciences": "Biology",
                "B.Sc in Biotechnology": "Biotechnology",
                "B.Sc in Electronics": "Electronics",
                "B.Sc in Statistics": "Statistics",
                "B.Sc in Environmental Science": "Environmental Science",
                "Business Administration and Management": "Business Administration",
                "Finance and Accounting": "Finance",
                "Marketing and Sales Management": "Marketing",
                "Human Resources Management": "Human Resources",
                "International Business": "Business Administration",
                "Operations and Supply Chain Management": "Operations Management",
                "Entrepreneurship and Innovation": "Business Administration",
                "Digital Marketing and E-Commerce": "Marketing",
                "Business Analytics and Intelligence": "Data Science",
                "General Studies": "General Studies",
                "Economics and Finance": "Economics",
                "Commerce and Accounting": "Commerce",
                "English Literature and Language": "English",
                "History and Political Science": "History",
                "Psychology and Behavioral Sciences": "Psychology",
                "Sociology and Social Work": "Sociology",
                "Philosophy and Ethics": "Philosophy",
                "Geography and Environmental Studies": "Geography",
                "Fine Arts and Design": "Fine Arts"
            }

            stream = stream_mapping.get(specialization, "Computer Science")  # Default fallback

            response = requests.post(
                "http://127.0.0.1:8000/auth/register/student",
                json={
                    "name": name,
                    "email": email,
                    "password": password,
                    "dob": dob.isoformat(),
                    "father_name": father_name,
                    "mother_name": mother_name,
                    "address": address,
                    "mobile_no": mobile_no,
                    "usn": usn,
                    "degree": course,  # Changed from 'course' to 'degree'
                    "stream": stream,  # Changed from 'specialization' to mapped 'stream'
                    "year": year,
                    "college": college
                }
            )
            
            if response.status_code == 200:
                st.success("✅ Student registered successfully!")
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
    register_student()