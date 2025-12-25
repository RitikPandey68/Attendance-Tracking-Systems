import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import re

# Page config
st.set_page_config(
    page_title="AI Powered Attendance System",
    page_icon="🎓",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8000"

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'token' not in st.session_state:
    st.session_state.token = None

def validate_password(password):
    """Validate password strength according to requirements"""
    errors = []
    
    # Check minimum length
    if len(password) < 10:
        errors.append("❌ Password must be at least 10 characters long")
    
    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        errors.append("❌ Password must contain at least 1 uppercase letter")
    
    # Check for special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("❌ Password must contain at least 1 special character")
    
    # Check for number
    if not re.search(r'[0-9]', password):
        errors.append("❌ Password must contain at least 1 number")
    
    # Check for repeated characters (no more than 2 consecutive same characters)
    if re.search(r'(.)\1{2,}', password):
        errors.append("❌ Password cannot have more than 2 repeated consecutive characters")
    
    return errors

def show_password_requirements():
    """Display password requirements"""
    st.info("""
    **Password Requirements:**
    • Minimum 10 characters
    • At least 1 uppercase letter (A-Z)
    • At least 1 special character (!@#$%^&*)
    • At least 1 number (0-9)
    • No more than 2 repeated consecutive characters
    """)

def make_request(endpoint, method="GET", data=None):
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, response.json().get('detail', 'Error occurred')
    except Exception as e:
        return None, str(e)

def login_user(email, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data["access_token"]
            
            # Get profile
            profile, error = make_request("/auth/profile")
            if profile:
                st.session_state.user_data = profile
                st.session_state.logged_in = True
                return True, "Login successful!"
            return False, "Failed to get profile"
        else:
            return False, response.json().get('detail', 'Login failed')
    except Exception as e:
        return False, str(e)

def show_login():
    st.title("🎓 AI Powered Attendance System")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_btn = st.form_submit_button("Login", use_container_width=True)
            with col_b:
                register_btn = st.form_submit_button("Register", use_container_width=True)
        
        if login_btn and email and password:
            success, msg = login_user(email, password)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        
        if register_btn:
            st.session_state.show_register = True
            st.rerun()
        
        if st.session_state.get('show_register', False):
            show_registration()

def show_registration():
    st.subheader("Registration")
    role = st.selectbox("Select Role", ["Student", "Faculty"])
    
    if role == "Student":
        with st.form("student_reg"):
            st.write("**Student Registration - Complete Profile**")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                dob = st.date_input("Date of Birth *", min_value=date(1940, 1, 1), max_value=date(2050, 12, 31), value=date(2000, 1, 1))
                usn = st.text_input("USN *")
                degree = st.selectbox("Degree *", ["B.Tech", "M.Tech", "BBA", "MBA", "B.E", "BCA", "MCA"])
                # College selection with major Indian universities
                college_options = [
                    # IITs
                    "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur", "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad", "IIT Indore", "IIT Mandi", "IIT Ropar", "IIT Bhubaneswar", "IIT Gandhinagar", "IIT Patna", "IIT Jodhpur", "IIT Varanasi (BHU)", "IIT Dhanbad", "IIT Bhilai", "IIT Goa", "IIT Jammu", "IIT Dharwad", "IIT Palakkad", "IIT Tirupati",
                    # NITs
                    "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Rourkela", "NIT Durgapur", "NIT Kurukshetra", "NIT Jaipur", "NIT Allahabad", "NIT Bhopal", "NIT Nagpur", "NIT Jalandhar", "NIT Hamirpur", "NIT Srinagar", "NIT Silchar", "NIT Agartala", "NIT Patna", "NIT Raipur", "NIT Jamshedpur", "NIT Uttarakhand", "NIT Goa", "NIT Puducherry", "NIT Arunachal Pradesh", "NIT Mizoram", "NIT Manipur", "NIT Sikkim", "NIT Meghalaya", "NIT Nagaland", "NIT Andhra Pradesh", "NIT Delhi", "NIT Karnataka",
                    # IIITs
                    "IIIT Hyderabad", "IIIT Allahabad", "IIIT Gwalior", "IIIT Jabalpur", "IIIT Kancheepuram", "IIIT Lucknow", "IIIT Vadodara", "IIIT Nagpur", "IIIT Pune", "IIIT Kota", "IIIT Sri City", "IIIT Kalyani", "IIIT Tiruchirappalli", "IIIT Una", "IIIT Sonepat", "IIIT Manipur", "IIIT Kottayam", "IIIT Ranchi", "IIIT Bhagalpur", "IIIT Bhopal", "IIIT Dharwad", "IIIT Raichur",
                    # GFTIs
                    "BITS Pilani", "BITS Goa", "BITS Hyderabad", "Thapar University", "Manipal Institute of Technology", "SRM University", "VIT Vellore", "VIT Chennai", "VIT Bhopal", "VIT AP", "Amity University", "LPU Punjab", "Shiv Nadar University", "Ashoka University", "Plaksha University",
                    # State Universities
                    "AKTU (Uttar Pradesh)", "VTU (Karnataka)", "Anna University (Tamil Nadu)", "Mumbai University", "Delhi University", "Pune University", "Calcutta University", "Jadavpur University", "Osmania University", "Andhra University", "Kerala University", "Rajasthan University", "Gujarat University", "Maharaja Sayajirao University", "Banaras Hindu University", "Jamia Millia Islamia", "Aligarh Muslim University", "Jawaharlal Nehru University", "Hyderabad University", "Cochin University", "Madras University", "Bharathiar University", "Bharathidasan University", "Mahatma Gandhi University", "Calicut University", "Kannur University", "APJ Abdul Kalam Technological University", "Visvesvaraya Technological University", "Jawaharlal Nehru Technological University", "Kakatiya University", "Telangana University", "Andhra Pradesh University", "Acharya Nagarjuna University", "Sri Venkateswara University", "Dravidian University", "Palamuru University", "Rayalaseema University", "Yogi Vemana University",
                    # Other major universities
                    "Chandigarh University", "Lovely Professional University", "Chitkara University", "Bennett University", "Galgotias University", "Graphic Era University", "Uttaranchal University", "Dev Bhoomi Uttarakhand University", "Quantum University", "Mangalayatan University", "UPES Dehradun", "DIT University", "Presidency University", "Christ University", "PES University", "Dayananda Sagar University", "Jain University", "Alliance University", "Azim Premji University", "REVA University", "CMR University", "Gitam University", "Koneru Lakshmaiah University", "Vignan University", "Centurion University", "Siksha O Anusandhan University", "Kalinga University", "KIIT University", "CV Raman University", "Amrita University", "Karunya University", "Hindustan University", "Sathyabama University", "SSN College of Engineering", "PSG College of Technology", "Thiagarajar College of Engineering", "Coimbatore Institute of Technology", "Kumaraguru College of Technology", "Bannari Amman Institute of Technology", "Other"
                ]
                college = st.selectbox("College *", college_options)
                
                # Show text input if "Other" is selected
                if college == "Other":
                    college = st.text_input("Specify Your College Name *")
                stream = st.selectbox("Stream *", [
                    "Computer Science", "Information Technology", "Electrical Engineering",
                    "Mechanical Engineering", "Civil Engineering", "Electronics Engineering"
                ])
            
            with col2:
                email = st.text_input("Email-ID *")
                mobile_no = st.text_input("Mobile Number *")
                
                # Password with validation
                show_password_requirements()
                password = st.text_input("Password *", type="password")
                if password:
                    password_errors = validate_password(password)
                    if password_errors:
                        for error in password_errors:
                            st.error(error)
                    else:
                        st.success("✅ Password meets all requirements")
                
                father_name = st.text_input("Father's Name *")
                mother_name = st.text_input("Mother's Name *")
                year = st.number_input("Year", 1, 4, 1)
            
            address = st.text_area("Address *")
            
            if st.form_submit_button("Register Student"):
                if all([name, dob, usn, degree, college, stream, email, mobile_no, password, father_name, mother_name, address]):
                    # Validate password
                    password_errors = validate_password(password)
                    if password_errors:
                        st.error("Password does not meet requirements:")
                        for error in password_errors:
                            st.error(error)
                    else:
                        data = {
                            "name": name, "dob": str(dob), "usn": usn, "degree": degree,
                            "college": college, "stream": stream, "email": email,
                            "mobile_no": mobile_no, "password": password,
                            "father_name": father_name, "mother_name": mother_name,
                            "address": address, "year": year
                        }
                        
                        result, error = make_request("/auth/register/student", "POST", data)
                        if result:
                            st.success("Registration successful!")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {error}")
                else:
                    st.error("Fill all required fields")
    
    else:  # Faculty
        with st.form("faculty_reg"):
            st.write("**Faculty Registration - Complete Profile**")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                email = st.text_input("Email-ID *")
                
                # Password with validation
                show_password_requirements()
                password = st.text_input("Password *", type="password")
                if password:
                    password_errors = validate_password(password)
                    if password_errors:
                        for error in password_errors:
                            st.error(error)
                    else:
                        st.success("✅ Password meets all requirements")
                
                position = st.selectbox("Position *", [
                    "Professor", "Associate Professor", "Assistant Professor", "Lecturer"
                ])
                stream = st.selectbox("Stream *", [
                    "Computer Science", "Information Technology", "Electrical Engineering"
                ])
            
            with col2:
                department = st.selectbox("Department *", [
                    "Computer Science", "Information Technology", "Mathematics", "Physics"
                ])
                # College selection with major Indian universities
                college_options = [
                    # IITs
                    "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur", "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad", "IIT Indore", "IIT Mandi", "IIT Ropar", "IIT Bhubaneswar", "IIT Gandhinagar", "IIT Patna", "IIT Jodhpur", "IIT Varanasi (BHU)", "IIT Dhanbad", "IIT Bhilai", "IIT Goa", "IIT Jammu", "IIT Dharwad", "IIT Palakkad", "IIT Tirupati",
                    # NITs
                    "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Rourkela", "NIT Durgapur", "NIT Kurukshetra", "NIT Jaipur", "NIT Allahabad", "NIT Bhopal", "NIT Nagpur", "NIT Jalandhar", "NIT Hamirpur", "NIT Srinagar", "NIT Silchar", "NIT Agartala", "NIT Patna", "NIT Raipur", "NIT Jamshedpur", "NIT Uttarakhand", "NIT Goa", "NIT Puducherry", "NIT Arunachal Pradesh", "NIT Mizoram", "NIT Manipur", "NIT Sikkim", "NIT Meghalaya", "NIT Nagaland", "NIT Andhra Pradesh", "NIT Delhi", "NIT Karnataka",
                    # IIITs
                    "IIIT Hyderabad", "IIIT Allahabad", "IIIT Gwalior", "IIIT Jabalpur", "IIIT Kancheepuram", "IIIT Lucknow", "IIIT Vadodara", "IIIT Nagpur", "IIIT Pune", "IIIT Kota", "IIIT Sri City", "IIIT Kalyani", "IIIT Tiruchirappalli", "IIIT Una", "IIIT Sonepat", "IIIT Manipur", "IIIT Kottayam", "IIIT Ranchi", "IIIT Bhagalpur", "IIIT Bhopal", "IIIT Dharwad", "IIIT Raichur",
                    # GFTIs
                    "BITS Pilani", "BITS Goa", "BITS Hyderabad", "Thapar University", "Manipal Institute of Technology", "SRM University", "VIT Vellore", "VIT Chennai", "VIT Bhopal", "VIT AP", "Amity University", "LPU Punjab", "Shiv Nadar University", "Ashoka University", "Plaksha University",
                    # State Universities
                    "AKTU (Uttar Pradesh)", "VTU (Karnataka)", "Anna University (Tamil Nadu)", "Mumbai University", "Delhi University", "Pune University", "Calcutta University", "Jadavpur University", "Osmania University", "Andhra University", "Kerala University", "Rajasthan University", "Gujarat University", "Maharaja Sayajirao University", "Banaras Hindu University", "Jamia Millia Islamia", "Aligarh Muslim University", "Jawaharlal Nehru University", "Hyderabad University", "Cochin University", "Madras University", "Bharathiar University", "Bharathidasan University", "Mahatma Gandhi University", "Calicut University", "Kannur University", "APJ Abdul Kalam Technological University", "Visvesvaraya Technological University", "Jawaharlal Nehru Technological University", "Kakatiya University", "Telangana University", "Andhra Pradesh University", "Acharya Nagarjuna University", "Sri Venkateswara University", "Dravidian University", "Palamuru University", "Rayalaseema University", "Yogi Vemana University",
                    # Other major universities
                    "Chandigarh University", "Lovely Professional University", "Chitkara University", "Bennett University", "Galgotias University", "Graphic Era University", "Uttaranchal University", "Dev Bhoomi Uttarakhand University", "Quantum University", "Mangalayatan University", "UPES Dehradun", "DIT University", "Presidency University", "Christ University", "PES University", "Dayananda Sagar University", "Jain University", "Alliance University", "Azim Premji University", "REVA University", "CMR University", "Gitam University", "Koneru Lakshmaiah University", "Vignan University", "Centurion University", "Siksha O Anusandhan University", "Kalinga University", "KIIT University", "CV Raman University", "Amrita University", "Karunya University", "Hindustan University", "Sathyabama University", "SSN College of Engineering", "PSG College of Technology", "Thiagarajar College of Engineering", "Coimbatore Institute of Technology", "Kumaraguru College of Technology", "Bannari Amman Institute of Technology", "Other"
                ]
                college_name = st.selectbox("College Name *", college_options)
                
                # Show text input if "Other" is selected
                if college_name == "Other":
                    college_name = st.text_input("Specify Your College Name *")
                mobile_no = st.text_input("Mobile Number *")
                employee_id = st.text_input("Employee ID")
                experience_years = st.number_input("Experience (Years)", 0, 50, 0)
            
            if st.form_submit_button("Register Faculty"):
                if all([name, email, password, position, stream, department, college_name, mobile_no]):
                    # Validate password
                    password_errors = validate_password(password)
                    if password_errors:
                        st.error("Password does not meet requirements:")
                        for error in password_errors:
                            st.error(error)
                    else:
                        data = {
                            "name": name, "email": email, "password": password,
                            "position": position, "stream": stream, "department": department,
                            "college_name": college_name, "mobile_no": mobile_no,
                            "employee_id": employee_id, "experience_years": experience_years,
                            "qualifications": [], "subjects_taught": []
                        }
                        
                        result, error = make_request("/auth/register/faculty", "POST", data)
                        if result:
                            st.success("Registration successful!")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {error}")
                else:
                    st.error("Fill all required fields")
    
    if st.button("Back to Login"):
        st.session_state.show_register = False
        st.rerun()

def show_student_dashboard():
    st.title("📚 Student Dashboard")
    
    with st.sidebar:
        st.write(f"**Welcome, {st.session_state.user_data.get('name')}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.token = None
            st.rerun()
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "📅 Attendance", "📈 Results", "📝 Notes", "📢 Notices", "💰 Fees"
    ])
    
    with tab1:
        st.subheader("Academic Overview")
        
        # Get dashboard data
        dashboard_data, error = make_request("/students/me/dashboard")
        if dashboard_data:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Attendance", "85%")
            with col2:
                st.metric("CGPA", f"{dashboard_data.get('overall_cgpa', 0):.2f}")
            with col3:
                st.metric("Pending Fees", f"₹{dashboard_data.get('pending_fees', 0):,}")
            with col4:
                st.metric("Assignments", len(dashboard_data.get('pending_assignments', [])))
    
    with tab2:
        st.subheader("📅 Attendance Analytics")
        st.write("**Daily, Weekly, Monthly Count for Each Subject + Overall**")
        
        if st.button("Load Attendance Stats"):
            stats, error = make_request("/students/me/attendance/stats")
            if stats:
                # Overall stats
                overall = stats.get('overall_attendance', {})
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Today", overall.get('daily_count', 0))
                with col2:
                    st.metric("This Week", overall.get('weekly_count', 0))
                with col3:
                    st.metric("This Month", overall.get('monthly_count', 0))
                with col4:
                    st.metric("Overall %", f"{overall.get('average_percentage', 0):.1f}%")
                
                # Subject-wise stats
                st.write("**Subject-wise Attendance (Daily/Weekly/Monthly)**")
                subjects = stats.get('subject_wise_attendance', [])
                if subjects:
                    df = pd.DataFrame([{
                        'Subject': s['subject'],
                        'Daily': s['daily_count'],
                        'Weekly': s['weekly_count'],
                        'Monthly': s['monthly_count'],
                        'Total': s['total_classes'],
                        'Attended': s['attended_classes'],
                        'Percentage': f"{s['percentage']:.1f}%"
                    } for s in subjects])
                    st.dataframe(df, use_container_width=True)
            else:
                st.error(f"Error: {error}")
    
    with tab3:
        st.subheader("📈 Exam Results (Internal & Lab)")
        
        col1, col2 = st.columns(2)
        with col1:
            exam_type = st.selectbox("Exam Type", ["All", "internal", "lab"])
        with col2:
            semester = st.selectbox("Semester", ["All", "1", "2", "3", "4"])
        
        if st.button("Load Results"):
            results, error = make_request("/students/me/results")
            if results:
                st.write("**Internal Exam Results**")
                internal_results = []
                lab_results = []
                
                for sem_result in results:
                    internal_results.extend(sem_result.get('internal_results', []))
                    lab_results.extend(sem_result.get('lab_results', []))
                
                if internal_results:
                    df_internal = pd.DataFrame([{
                        'Subject': r['subject'],
                        'Marks': f"{r['marks_obtained']}/{r['total_marks']}",
                        'Percentage': f"{r['percentage']:.1f}%",
                        'Grade': r['grade'],
                        'Date': r['exam_date']
                    } for r in internal_results])
                    st.dataframe(df_internal, use_container_width=True)
                
                st.write("**Lab Exam Results**")
                if lab_results:
                    df_lab = pd.DataFrame([{
                        'Subject': r['subject'],
                        'Marks': f"{r['marks_obtained']}/{r['total_marks']}",
                        'Percentage': f"{r['percentage']:.1f}%",
                        'Grade': r['grade'],
                        'Date': r['exam_date']
                    } for r in lab_results])
                    st.dataframe(df_lab, use_container_width=True)
            else:
                st.error(f"Error: {error}")
    
    with tab4:
        st.subheader("📝 Faculty Notes by Subject")
        
        if st.button("Load Notes"):
            notes, error = make_request("/students/me/notes")
            if notes:
                for note in notes:
                    with st.expander(f"📄 {note['title']} - {note['subject']}"):
                        st.write(f"**Type:** {note['note_type']}")
                        st.write(f"**Content:** {note['content']}")
                        if note.get('file_url'):
                            st.write(f"[📎 Download]({note['file_url']})")
            else:
                st.info("No notes available")
    
    with tab5:
        st.subheader("📢 Notice Board & Announcements")
        
        if st.button("Load Announcements"):
            announcements, error = make_request("/students/me/announcements")
            if announcements:
                for ann in announcements:
                    urgency = "🚨" if ann.get('is_urgent') else "📢"
                    with st.expander(f"{urgency} {ann['title']}"):
                        st.write(f"**Type:** {ann['announcement_type']}")
                        st.write(ann['content'])
            else:
                st.info("No announcements")
    
    with tab6:
        st.subheader("💰 Fee Details (Connected to Administration)")
        
        if st.button("Load Fee Details"):
            fees, error = make_request("/students/me/fees")
            if fees:
                summary = fees.get('summary', {})
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", f"₹{summary.get('total_fees', 0):,}")
                with col2:
                    st.metric("Paid", f"₹{summary.get('paid_fees', 0):,}")
                with col3:
                    st.metric("Pending", f"₹{summary.get('pending_fees', 0):,}")
                with col4:
                    st.metric("Overdue", f"₹{summary.get('overdue_fees', 0):,}")
                
                fee_details = fees.get('fee_details', [])
                if fee_details:
                    df = pd.DataFrame([{
                        'Type': f['fee_type'],
                        'Amount': f"₹{f['amount']:,}",
                        'Due Date': f['due_date'],
                        'Status': '✅ Paid' if f['is_paid'] else '⏳ Pending'
                    } for f in fee_details])
                    st.dataframe(df, use_container_width=True)
            else:
                st.error(f"Error: {error}")

def show_faculty_dashboard():
    st.title("👨🏫 Faculty Dashboard")
    
    with st.sidebar:
        st.write(f"**Welcome, {st.session_state.user_data.get('name')}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.token = None
            st.rerun()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "📅 Attendance", "📝 Notes", "📢 Announcements", "📈 Results"
    ])
    
    with tab1:
        st.subheader("Teaching Overview")
        
        if st.button("Load Dashboard"):
            dashboard, error = make_request("/faculty/dashboard")
            if dashboard:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Today's Classes", dashboard.get('today_classes_count', 0))
                with col2:
                    st.metric("Notes Created", len(dashboard.get('recent_notes', [])))
                with col3:
                    st.metric("Upcoming Exams", len(dashboard.get('upcoming_exams', [])))
                with col4:
                    st.metric("Pending Submissions", dashboard.get('pending_submissions_count', 0))
    
    with tab2:
        st.subheader("📅 Attendance Management")
        st.write("**Daily, Weekly, Monthly Count for Each Subject + Overall**")
        
        # Mark attendance
        with st.form("mark_attendance"):
            st.write("**Mark Attendance**")
            col1, col2, col3 = st.columns(3)
            with col1:
                subject = st.text_input("Subject")
                date_input = st.date_input("Date", date.today())
            with col2:
                period = st.number_input("Period", 1, 8, 1)
                student_id = st.text_input("Student ID")
            with col3:
                status = st.selectbox("Status", ["present", "absent", "leave"])
            
            if st.form_submit_button("Mark Attendance"):
                if subject and student_id:
                    data = {
                        "student_id": student_id,
                        "date": str(date_input),
                        "period": period,
                        "subject": subject,
                        "status": status
                    }
                    result, error = make_request("/attendance/enroll", "POST", data)
                    if result:
                        st.success("Attendance marked!")
                    else:
                        st.error(f"Error: {error}")
        
        # View stats
        if st.button("Load Attendance Statistics"):
            stats, error = make_request("/faculty/attendance/stats")
            if stats:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Daily Classes", stats.get('daily_classes', 0))
                with col2:
                    st.metric("Weekly Classes", stats.get('weekly_classes', 0))
                with col3:
                    st.metric("Monthly Classes", stats.get('monthly_classes', 0))
                with col4:
                    st.metric("Total Classes", stats.get('total_classes', 0))
                
                # Subject-wise stats
                subject_stats = stats.get('subject_wise_stats', {})
                if subject_stats:
                    df = pd.DataFrame([{
                        'Subject': subj,
                        'Daily': data['daily_count'],
                        'Weekly': data['weekly_count'],
                        'Monthly': data['monthly_count'],
                        'Total': data['total_classes'],
                        'Avg Attendance': f"{data['average_attendance']:.1f}%"
                    } for subj, data in subject_stats.items()])
                    st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.subheader("📝 Notes Management (Section-wise)")
        
        # Create note
        with st.form("create_note"):
            st.write("**Create New Note**")
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title")
                subject = st.text_input("Subject")
            with col2:
                note_type = st.selectbox("Type", ["Lecture Notes", "Assignment", "Reference Material"])
                file_url = st.text_input("File URL (optional)")
            
            content = st.text_area("Content")
            
            if st.form_submit_button("Create Note"):
                if title and subject and content:
                    data = {
                        "title": title,
                        "subject": subject,
                        "note_type": note_type,
                        "content": content,
                        "file_url": file_url or None
                    }
                    result, error = make_request("/faculty/notes", "POST", data)
                    if result:
                        st.success("Note created!")
                    else:
                        st.error(f"Error: {error}")
        
        # View notes
        if st.button("Load My Notes"):
            notes, error = make_request("/faculty/notes")
            if notes:
                for note in notes:
                    with st.expander(f"📄 {note['title']} - {note['subject']}"):
                        st.write(f"**Type:** {note['note_type']}")
                        st.write(note['content'])
    
    with tab4:
        st.subheader("📢 Announcements & Notice Board")
        
        # Create announcement
        with st.form("create_announcement"):
            st.write("**Create Announcement**")
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title")
                ann_type = st.selectbox("Type", ["General", "Exam", "Assignment", "Event"])
                is_urgent = st.checkbox("Mark as Urgent")
            with col2:
                target_year = st.number_input("Target Year (optional)", 1, 4, value=None)
                target_dept = st.text_input("Target Department (optional)")
            
            content = st.text_area("Content")
            
            if st.form_submit_button("Create Announcement"):
                if title and content:
                    data = {
                        "title": title,
                        "content": content,
                        "announcement_type": ann_type,
                        "is_urgent": is_urgent,
                        "target_year": target_year,
                        "target_department": target_dept or None
                    }
                    result, error = make_request("/faculty/announcements", "POST", data)
                    if result:
                        st.success("Announcement created!")
                    else:
                        st.error(f"Error: {error}")
    
    with tab5:
        st.subheader("📈 Results Management (Internal & Lab)")
        
        # Create result
        with st.form("create_result"):
            st.write("**Enter Exam Results**")
            col1, col2, col3 = st.columns(3)
            with col1:
                student_id = st.text_input("Student ID")
                subject = st.text_input("Subject")
            with col2:
                test_type = st.selectbox("Exam Type", ["internal", "lab"])
                test_date = st.date_input("Exam Date")
            with col3:
                marks_obtained = st.number_input("Marks Obtained", 0, 100, 0)
                total_marks = st.number_input("Total Marks", 1, 100, 100)
                semester = st.number_input("Semester", 1, 8, 1)
            
            if st.form_submit_button("Submit Result"):
                if student_id and subject:
                    data = {
                        "student_id": student_id,
                        "subject": subject,
                        "test_type": test_type,
                        "test_date": str(test_date),
                        "marks_obtained": marks_obtained,
                        "total_marks": total_marks,
                        "semester": semester
                    }
                    result, error = make_request("/results/create", "POST", data)
                    if result:
                        st.success("Result submitted!")
                    else:
                        st.error(f"Error: {error}")

def main():
    if not st.session_state.logged_in:
        show_login()
    else:
        user_role = st.session_state.user_data.get('role')
        if user_role == 'student':
            show_student_dashboard()
        elif user_role == 'faculty':
            show_faculty_dashboard()
        else:
            st.error("Unknown role")

if __name__ == "__main__":
    main()