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

st.set_page_config(page_title="Register", layout="centered")

st.title("📝 New User Registration")

# User type selection
user_type = st.selectbox("Select User Type", ["Student", "Faculty"])

if user_type == "Student":
    st.header("🎓 Student Registration")
    
    # Personal Information
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)

    # Initialize validation flags
    validation_errors = {}

    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        if not name.strip():
            validation_errors['name'] = "Full Name is required"
        elif len(name.strip()) < 2:
            validation_errors['name'] = "Full Name must be at least 2 characters"

        email = st.text_input("Email Address*", placeholder="student@example.com")
        if not email.strip():
            validation_errors['email'] = "Email Address is required"
        elif '@' not in email or '.' not in email:
            validation_errors['email'] = "Please enter a valid email address"

        # Feature 3: Password with validation
        password = st.text_input("Password*", type="password", placeholder="Minimum 10 characters with requirements")
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
                validation_errors['password'] = message
        else:
            validation_errors['password'] = "Password is required"

        st.info("""📋 **Password Requirements (All Mandatory):**
        • Minimum 10 characters
        • At least 1 uppercase letter (A-Z)
        • At least 1 number (0-9)
        • At least 1 special character (!@#$%^&*)
        • No repeated characters (aa, 11, etc. not allowed)""")

        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Re-enter your password")
        if confirm_password and password != confirm_password:
            validation_errors['confirm_password'] = "Passwords do not match"
        elif not confirm_password:
            validation_errors['confirm_password'] = "Please confirm your password"

        # Feature 1: DOB range 1940-2050 with calendar
        dob = st.date_input("Date of Birth*", min_value=date(1940, 1, 1), max_value=date(2050, 12, 31), value=date(2000, 1, 1))

    with col2:
        father_name = st.text_input("Father's Name*", placeholder="Father's full name")
        if not father_name.strip():
            validation_errors['father_name'] = "Father's Name is required"
        elif len(father_name.strip()) < 2:
            validation_errors['father_name'] = "Father's Name must be at least 2 characters"

        mother_name = st.text_input("Mother's Name*", placeholder="Mother's full name")
        if not mother_name.strip():
            validation_errors['mother_name'] = "Mother's Name is required"
        elif len(mother_name.strip()) < 2:
            validation_errors['mother_name'] = "Mother's Name must be at least 2 characters"

        mobile_no = st.text_input("Mobile Number*", placeholder="+91 XXXXXXXXXX", max_chars=10)
        if not mobile_no.strip():
            validation_errors['mobile_no'] = "Mobile Number is required"
        elif not mobile_no.isdigit():
            validation_errors['mobile_no'] = "Mobile Number must contain only digits"
        elif len(mobile_no) != 10:
            validation_errors['mobile_no'] = "Mobile Number must be exactly 10 digits"

        address = st.text_area("Address*", placeholder="Complete postal address")
        if not address.strip():
            validation_errors['address'] = "Address is required"
        elif len(address.strip()) < 10:
            validation_errors['address'] = "Address must be at least 10 characters"
    
    # Academic Information
    st.subheader("📚 Academic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        usn = st.text_input("USN (University Seat Number)*", placeholder="e.g., 1RV20CS001")
        if not usn.strip():
            validation_errors['usn'] = "USN is required"
        elif len(usn.strip()) < 5:
            validation_errors['usn'] = "USN must be at least 5 characters"

        year = st.selectbox("Academic Year*", [1, 2, 3, 4], index=0)
        
        # Feature 2: College/University Selection - Comprehensive Indian Universities
        college_options = [
            # IITs
            "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur", "IIT Roorkee", "IIT Guwahati",
            "IIT Hyderabad", "IIT Indore", "IIT Mandi", "IIT Patna", "IIT Ropar", "IIT Bhubaneswar", "IIT Gandhinagar",
            "IIT Jodhpur", "IIT Tirupati", "IIT Bhilai", "IIT Goa", "IIT Jammu", "IIT Dharwad", "IIT Palakkad",
            
            # NITs
            "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Rourkela", "NIT Durgapur",
            "NIT Jamshedpur", "NIT Kurukshetra", "NIT Surat", "NIT Allahabad", "NIT Bhopal", "NIT Nagpur",
            "NIT Jalandhar", "NIT Hamirpur", "NIT Silchar", "NIT Agartala", "NIT Arunachal Pradesh", "NIT Delhi",
            "NIT Goa", "NIT Manipur", "NIT Meghalaya", "NIT Mizoram", "NIT Nagaland", "NIT Puducherry",
            "NIT Sikkim", "NIT Uttarakhand", "NIT Andhra Pradesh", "NIT Patna", "NIT Raipur", "NIT Jaipur",
            
            # IIITs
            "IIIT Hyderabad", "IIIT Bangalore", "IIIT Delhi", "IIIT Allahabad", "IIIT Gwalior", "IIIT Jabalpur",
            "IIIT Kancheepuram", "IIIT Lucknow", "IIIT Vadodara", "IIIT Nagpur", "IIIT Pune", "IIIT Kota",
            "IIIT Sonepat", "IIIT Kalyani", "IIIT Tiruchirappalli", "IIIT Una", "IIIT Surat", "IIIT Manipur",
            "IIIT Kottayam", "IIIT Ranchi", "IIIT Bhagalpur", "IIIT Bhopal", "IIIT Dharwad", "IIIT Raichur",
            
            # GFTIs (Government Funded Technical Institutions)
            "BITS Pilani", "BITS Goa", "BITS Hyderabad", "Thapar Institute of Engineering and Technology",
            "Birla Institute of Technology Mesra", "Jadavpur University", "Bengal Engineering and Science University",
            "Cochin University of Science and Technology", "Motilal Nehru National Institute of Technology",
            
            # State Technical Universities
            "AKTU (Dr. A.P.J. Abdul Kalam Technical University)", "VTU (Visvesvaraya Technological University)",
            "GTU (Gujarat Technological University)", "JNTU Hyderabad", "JNTU Kakinada", "JNTU Anantapur",
            "BPUT (Biju Patnaik University of Technology)", "WBUT (West Bengal University of Technology)",
            "RGPV (Rajiv Gandhi Proudyogiki Vishwavidyalaya)", "RTU (Rajasthan Technical University)",
            "PTU (Punjab Technical University)", "UPTU (Uttar Pradesh Technical University)",
            
            # Central Universities
            "Anna University", "Osmania University", "Jawaharlal Nehru University", "Delhi University",
            "Pune University", "Mumbai University", "Calcutta University", "Madras University",
            "Bangalore University", "Mysore University", "Kerala University", "Andhra University",
            "Rajasthan University", "Gujarat University", "Utkal University", "Gauhati University",
            
            # Deemed Universities
            "Jamia Millia Islamia", "Aligarh Muslim University", "Banaras Hindu University",
            "Indian Statistical Institute", "Tata Institute of Social Sciences", "IISC Bangalore",
            
            # Private Universities
            "Manipal Academy of Higher Education", "SRM Institute of Science and Technology",
            "Vellore Institute of Technology", "Birla Institute of Technology and Science",
            "Amity University", "Lovely Professional University", "Chandigarh University",
            "Shiv Nadar University", "Ashoka University", "O.P. Jindal Global University",
            "Bennett University", "Plaksha University", "Krea University",
            
            # Other Prominent Institutions
            "Indian Institute of Science (IISc)", "Indian School of Mines Dhanbad",
            "National Institute of Technology", "Indian Institute of Engineering Science and Technology",
            "Sardar Vallabhbhai National Institute of Technology", "Malaviya National Institute of Technology",
            
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
        if not course:
            validation_errors['course'] = "Course is required"

    with col2:
        # Feature 4: Updated Specialization options
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
        if not specialization:
            validation_errors['specialization'] = "Specialization/Stream is required"

        if college == "Other - Specify Your College Name":
            college_input = st.text_input("Specify Your College/University Name*", placeholder="Type your college name here")
            if not college_input.strip():
                validation_errors['college'] = "College name is required"
            else:
                college = college_input
        elif not college:
            validation_errors['college'] = "College/University is required"

    st.markdown("---")
    
    # Display validation errors if any
    if validation_errors:
        st.error("❌ Please fix the following errors:")
        for field, error in validation_errors.items():
            st.error(f"• {error}")

    if st.button("📝 Register Student", type="primary", use_container_width=True):
        # Check for validation errors
        if validation_errors:
            st.error("❌ Please fix all validation errors before submitting!")
            st.stop()

        # Additional validation checks
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
            st.stop()
        elif not validate_password(password)[0]:
            st.error(f"❌ {validate_password(password)[1]}")
            st.stop()
        else:
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
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Registration failed: {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to server. Please make sure the backend is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif user_type == "Faculty":
    st.header("👨🏫 Faculty Registration")

    # Initialize validation flags for faculty
    faculty_validation_errors = {}

    # Personal Information
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name", key="faculty_name")
        if not name.strip():
            faculty_validation_errors['name'] = "Full Name is required"
        elif len(name.strip()) < 2:
            faculty_validation_errors['name'] = "Full Name must be at least 2 characters"

        email = st.text_input("Email Address*", placeholder="faculty@example.com", key="faculty_email")
        if not email.strip():
            faculty_validation_errors['email'] = "Email Address is required"
        elif '@' not in email or '.' not in email:
            faculty_validation_errors['email'] = "Please enter a valid email address"

        # Password with validation
        password = st.text_input("Password*", type="password", placeholder="Minimum 10 characters with requirements", key="faculty_password")
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
                faculty_validation_errors['password'] = message
        else:
            faculty_validation_errors['password'] = "Password is required"

        st.info("""📋 **Password Requirements (All Mandatory):**
        • Minimum 10 characters
        • At least 1 uppercase letter (A-Z)
        • At least 1 number (0-9)
        • At least 1 special character (!@#$%^&*)
        • No repeated characters (aa, 11, etc. not allowed)""")

        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Re-enter your password", key="faculty_confirm_password")
        if confirm_password and password != confirm_password:
            faculty_validation_errors['confirm_password'] = "Passwords do not match"
        elif not confirm_password:
            faculty_validation_errors['confirm_password'] = "Please confirm your password"

        mobile_no = st.text_input("Mobile Number*", placeholder="+91 XXXXXXXXXX", max_chars=10, key="faculty_mobile")
        if not mobile_no.strip():
            faculty_validation_errors['mobile_no'] = "Mobile Number is required"
        elif not mobile_no.isdigit():
            faculty_validation_errors['mobile_no'] = "Mobile Number must contain only digits"
        elif len(mobile_no) != 10:
            faculty_validation_errors['mobile_no'] = "Mobile Number must be exactly 10 digits"

    with col2:
        dob = st.date_input("Date of Birth*", min_value=date(1940, 1, 1), max_value=date(2050, 12, 31), value=date(1980, 1, 1), key="faculty_dob")
        address = st.text_area("Address*", placeholder="Complete postal address", key="faculty_address")
        if not address.strip():
            faculty_validation_errors['address'] = "Address is required"
        elif len(address.strip()) < 10:
            faculty_validation_errors['address'] = "Address must be at least 10 characters"

        employee_id = st.text_input("Employee ID*", placeholder="e.g., EMP001", key="faculty_employee_id")
        if not employee_id.strip():
            faculty_validation_errors['employee_id'] = "Employee ID is required"
        elif len(employee_id.strip()) < 3:
            faculty_validation_errors['employee_id'] = "Employee ID must be at least 3 characters"
    
    # Professional Information
    st.subheader("🏫 Professional Information")
    col1, col2 = st.columns(2)
    
    with col1:
        # College/University Selection (same comprehensive list as student)
        college_options = [
            # IITs
            "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur", "IIT Roorkee", "IIT Guwahati",
            "IIT Hyderabad", "IIT Indore", "IIT Mandi", "IIT Patna", "IIT Ropar", "IIT Bhubaneswar", "IIT Gandhinagar",
            "IIT Jodhpur", "IIT Tirupati", "IIT Bhilai", "IIT Goa", "IIT Jammu", "IIT Dharwad", "IIT Palakkad",
            
            # NITs
            "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Rourkela", "NIT Durgapur",
            "NIT Jamshedpur", "NIT Kurukshetra", "NIT Surat", "NIT Allahabad", "NIT Bhopal", "NIT Nagpur",
            "NIT Jalandhar", "NIT Hamirpur", "NIT Silchar", "NIT Agartala", "NIT Arunachal Pradesh", "NIT Delhi",
            "NIT Goa", "NIT Manipur", "NIT Meghalaya", "NIT Mizoram", "NIT Nagaland", "NIT Puducherry",
            "NIT Sikkim", "NIT Uttarakhand", "NIT Andhra Pradesh", "NIT Patna", "NIT Raipur", "NIT Jaipur",
            
            # IIITs
            "IIIT Hyderabad", "IIIT Bangalore", "IIIT Delhi", "IIIT Allahabad", "IIIT Gwalior", "IIIT Jabalpur",
            "IIIT Kancheepuram", "IIIT Lucknow", "IIIT Vadodara", "IIIT Nagpur", "IIIT Pune", "IIIT Kota",
            "IIIT Sonepat", "IIIT Kalyani", "IIIT Tiruchirappalli", "IIIT Una", "IIIT Surat", "IIIT Manipur",
            "IIIT Kottayam", "IIIT Ranchi", "IIIT Bhagalpur", "IIIT Bhopal", "IIIT Dharwad", "IIIT Raichur",
            
            # GFTIs (Government Funded Technical Institutions)
            "BITS Pilani", "BITS Goa", "BITS Hyderabad", "Thapar Institute of Engineering and Technology",
            "Birla Institute of Technology Mesra", "Jadavpur University", "Bengal Engineering and Science University",
            "Cochin University of Science and Technology", "Motilal Nehru National Institute of Technology",
            
            # State Technical Universities
            "AKTU (Dr. A.P.J. Abdul Kalam Technical University)", "VTU (Visvesvaraya Technological University)",
            "GTU (Gujarat Technological University)", "JNTU Hyderabad", "JNTU Kakinada", "JNTU Anantapur",
            "BPUT (Biju Patnaik University of Technology)", "WBUT (West Bengal University of Technology)",
            "RGPV (Rajiv Gandhi Proudyogiki Vishwavidyalaya)", "RTU (Rajasthan Technical University)",
            "PTU (Punjab Technical University)", "UPTU (Uttar Pradesh Technical University)",
            
            # Central Universities
            "Anna University", "Osmania University", "Jawaharlal Nehru University", "Delhi University",
            "Pune University", "Mumbai University", "Calcutta University", "Madras University",
            "Bangalore University", "Mysore University", "Kerala University", "Andhra University",
            "Rajasthan University", "Gujarat University", "Utkal University", "Gauhati University",
            
            # Deemed Universities
            "Jamia Millia Islamia", "Aligarh Muslim University", "Banaras Hindu University",
            "Indian Statistical Institute", "Tata Institute of Social Sciences", "IISC Bangalore",
            
            # Private Universities
            "Manipal Academy of Higher Education", "SRM Institute of Science and Technology",
            "Vellore Institute of Technology", "Birla Institute of Technology and Science",
            "Amity University", "Lovely Professional University", "Chandigarh University",
            "Shiv Nadar University", "Ashoka University", "O.P. Jindal Global University",
            "Bennett University", "Plaksha University", "Krea University",
            
            # Other Prominent Institutions
            "Indian Institute of Science (IISc)", "Indian School of Mines Dhanbad",
            "National Institute of Technology", "Indian Institute of Engineering Science and Technology",
            "Sardar Vallabhbhai National Institute of Technology", "Malaviya National Institute of Technology",
            
            "Other - Specify Your College Name"
        ]
        
        college = st.selectbox("College/University* (Choose from list)", college_options)
        if college == "Other - Specify Your College Name":
            st.info("📝 Please specify your college name below:")
            college = st.text_input("Specify Your College/University Name*", placeholder="Type your college name here")
            if not college:
                st.warning("⚠️ Please enter your college name")
        
        # Department Selection (same as student streams)
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
        # Designation Selection
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
        
        # Education Qualification
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

    # Display faculty validation errors if any
    if faculty_validation_errors:
        st.error("❌ Please fix the following errors:")
        for field, error in faculty_validation_errors.items():
            st.error(f"• {error}")

    if st.button("📝 Register Faculty", type="primary", use_container_width=True):
        # Check for faculty validation errors
        if faculty_validation_errors:
            st.error("❌ Please fix all validation errors before submitting!")
            st.stop()
        # Validation
        if not all([name, email, password, confirm_password, mobile_no, department, designation, 
                   college, highest_education, specialization, employee_id, dob, address]):
            st.error("❌ Please fill all required fields (*)")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif not validate_password(password)[0]:
            st.error(f"❌ {validate_password(password)[1]}")
        elif len(mobile_no) < 10:
            st.error("❌ Please enter a valid mobile number!")
        else:
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
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Registration failed: {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to server. Please make sure the backend is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.info("💡 **Note:** All fields marked with * are mandatory. After registration, you'll receive an email verification link.")

st.page_link("pages/1_🔐_Login.py", label="← Back to Login")