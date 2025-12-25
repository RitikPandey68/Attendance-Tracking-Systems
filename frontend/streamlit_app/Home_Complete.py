import streamlit as st
import requests
import json
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

# Configure page
st.set_page_config(
    page_title="AI Powered Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'token' not in st.session_state:
    st.session_state.token = None

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None, headers: Dict = None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if st.session_state.token:
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
            response = requests.put(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('detail', f'Error {response.status_code}')
            return None, error_msg
    
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to server. Please ensure the backend is running."
    except Exception as e:
        return None, str(e)

def login_user(email: str, password: str):
    """Login user and store session data"""
    data = {"username": email, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", data=data, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data["access_token"]
            st.session_state.logged_in = True
            
            # Get user profile
            profile_data, error = make_api_request("/auth/profile")
            if profile_data:
                st.session_state.user_data = profile_data
                return True, "Login successful!"
            else:
                return False, "Failed to fetch user profile"
        else:
            error_msg = response.json().get('detail', 'Login failed')
            return False, error_msg
    except Exception as e:
        return False, str(e)

def logout_user():
    """Logout user and clear session"""
    st.session_state.logged_in = False
    st.session_state.user_data = None
    st.session_state.token = None
    st.rerun()

def show_login_page():
    """Display login page"""
    st.markdown('<h1 class="main-header">🎓 AI Powered Attendance System</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Your Account")
        
        # Login form
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            with col_register:
                if st.form_submit_button("📝 New User? Register", use_container_width=True):
                    st.session_state.show_registration = True
                    st.rerun()
        
        if login_button and email and password:
            with st.spinner("Logging in..."):
                success, message = login_user(email, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # Registration section
        if st.session_state.get('show_registration', False):
            show_registration_form()

def show_registration_form():
    """Display registration form"""
    st.markdown("---")
    st.markdown("### 📝 Create New Account")
    
    role = st.selectbox("Select Role", ["Student", "Faculty"])
    
    if role == "Student":
        show_student_registration()
    else:
        show_faculty_registration()
    
    if st.button("← Back to Login"):
        st.session_state.show_registration = False
        st.rerun()

def show_student_registration():
    """Student registration form with all required fields"""
    with st.form("student_registration"):
        st.markdown("#### 📚 Student Registration - Complete Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            dob = st.date_input("Date of Birth *")
            usn = st.text_input("USN/Roll Number *")
            degree = st.selectbox("Degree *", ["B.Tech", "M.Tech", "BBA", "MBA", "B.E", "BCA", "MCA", "B.Sc", "M.Sc", "Diploma"])
            college = st.text_input("College Name *")
            stream = st.selectbox("Stream/Specialization *", [
                "Computer Science", "Information Technology", "Electrical Engineering",
                "Mechanical Engineering", "Civil Engineering", "Electronics Engineering",
                "Artificial Intelligence", "Data Science", "Cybersecurity", "Business Administration"
            ])
        
        with col2:
            email = st.text_input("Email-ID *")
            mobile_no = st.text_input("Mobile Number *")
            password = st.text_input("Password *", type="password")
            father_name = st.text_input("Father's Name *")
            mother_name = st.text_input("Mother's Name *")
            year = st.number_input("Year", min_value=1, max_value=4, value=1)
        
        address = st.text_area("Address *")
        
        # Optional fields
        st.markdown("#### Additional Information (Optional)")
        col3, col4 = st.columns(2)
        with col3:
            emergency_contact = st.text_input("Emergency Contact Number")
            blood_group = st.selectbox("Blood Group", ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        with col4:
            guardian_name = st.text_input("Guardian Name")
            guardian_mobile = st.text_input("Guardian Mobile")
        
        if st.form_submit_button("Register as Student", use_container_width=True):
            if all([name, dob, usn, degree, college, stream, email, mobile_no, password, father_name, mother_name, address]):
                student_data = {
                    "name": name,
                    "dob": str(dob),
                    "usn": usn,
                    "degree": degree,
                    "college": college,
                    "stream": stream,
                    "email": email,
                    "mobile_no": mobile_no,
                    "password": password,
                    "father_name": father_name,
                    "mother_name": mother_name,
                    "address": address,
                    "year": year,
                    "emergency_contact": emergency_contact if emergency_contact else None,
                    "blood_group": blood_group if blood_group else None,
                    "guardian_name": guardian_name if guardian_name else None,
                    "guardian_mobile": guardian_mobile if guardian_mobile else None
                }
                
                with st.spinner("Registering student..."):
                    result, error = make_api_request("/auth/register/student", "POST", student_data)
                    if result:
                        st.success("Student registration successful! You can now login.")
                        st.session_state.show_registration = False
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {error}")
            else:
                st.error("Please fill all required fields marked with *")

def show_faculty_registration():
    """Faculty registration form with all required fields"""
    with st.form("faculty_registration"):
        st.markdown("#### 👨🏫 Faculty Registration - Complete Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email-ID *")
            password = st.text_input("Password *", type="password")
            position = st.selectbox("Position *", [
                "Professor", "Associate Professor", "Assistant Professor",
                "Lecturer", "Head of Department", "Dean", "Principal"
            ])
            stream = st.selectbox("Stream *", [
                "Computer Science", "Information Technology", "Electrical Engineering",
                "Mechanical Engineering", "Civil Engineering", "Electronics Engineering",
                "Artificial Intelligence", "Data Science", "Cybersecurity", "Business Administration"
            ])
        
        with col2:
            department = st.selectbox("Department *", [
                "Computer Science", "Information Technology", "Electrical Engineering",
                "Mechanical Engineering", "Civil Engineering", "Electronics Engineering",
                "Mathematics", "Physics", "Chemistry", "Management Studies"
            ])
            college_name = st.text_input("College Name *")
            mobile_no = st.text_input("Mobile Number *")
            employee_id = st.text_input("Employee ID")
            experience_years = st.number_input("Years of Experience", min_value=0, max_value=50, value=0)
        
        # Qualifications section
        st.markdown("#### 🎓 Qualifications")
        qualification_degree = st.text_input("Highest Qualification Degree")
        qualification_institution = st.text_input("Institution")
        qualification_year = st.number_input("Year of Completion", min_value=1970, max_value=2024, value=2020)
        
        # Additional fields
        col3, col4 = st.columns(2)
        with col3:
            office_hours = st.text_input("Office Hours (e.g., 9 AM - 5 PM)")
            cabin_number = st.text_input("Cabin Number")
        with col4:
            subjects_taught = st.text_area("Subjects Taught (comma separated)")
            research_interests = st.text_area("Research Interests (comma separated)")
        
        if st.form_submit_button("Register as Faculty", use_container_width=True):
            if all([name, email, password, position, stream, department, college_name, mobile_no]):
                qualifications = []
                if qualification_degree and qualification_institution:
                    qualifications.append({
                        "degree": qualification_degree,
                        "institution": qualification_institution,
                        "year": qualification_year
                    })
                
                faculty_data = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "position": position,
                    "stream": stream,
                    "department": department,
                    "college_name": college_name,
                    "mobile_no": mobile_no,
                    "employee_id": employee_id if employee_id else None,
                    "experience_years": experience_years,
                    "qualifications": qualifications,
                    "office_hours": office_hours if office_hours else None,
                    "cabin_number": cabin_number if cabin_number else None,
                    "subjects_taught": [s.strip() for s in subjects_taught.split(",")] if subjects_taught else [],
                    "research_interests": [r.strip() for r in research_interests.split(",")] if research_interests else []
                }
                
                with st.spinner("Registering faculty..."):
                    result, error = make_api_request("/auth/register/faculty", "POST", faculty_data)
                    if result:
                        st.success("Faculty registration successful! You can now login.")
                        st.session_state.show_registration = False
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {error}")
            else:
                st.error("Please fill all required fields marked with *")

def show_dashboard():
    """Display role-based dashboard"""
    user_role = st.session_state.user_data.get('role', 'student')
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.user_data.get('name', 'User')}!")
        st.markdown(f"**Role:** {user_role.title()}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
    
    # Main dashboard based on role
    if user_role == 'student':
        show_student_dashboard()
    elif user_role == 'faculty':
        show_faculty_dashboard()
    elif user_role == 'admin':
        show_admin_dashboard()
    else:
        st.error("Unknown user role")

def show_student_dashboard():
    """Complete Student dashboard with all features"""
    st.markdown('<h1 class="main-header">📚 Student Dashboard</h1>', unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", "📅 Attendance", "📈 Results", "📝 Notes", "📢 Notices", "📋 Assignments", "💰 Fees"
    ])
    
    with tab1:
        show_student_overview()
    
    with tab2:
        show_student_attendance()
    
    with tab3:
        show_student_results()
    
    with tab4:
        show_student_notes()
    
    with tab5:
        show_student_notices()
    
    with tab6:
        show_student_assignments()
    
    with tab7:
        show_student_fees()

def show_student_overview():
    """Student overview with all metrics"""
    st.markdown("### 📊 Academic Overview")
    
    # Get dashboard data
    dashboard_data, error = make_api_request("/students/me/dashboard")
    if dashboard_data:
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_attendance = dashboard_data.get('attendance_stats', {}).get('overall_attendance', {})
            st.metric("Overall Attendance", f"{overall_attendance.get('average_percentage', 0):.1f}%")
        
        with col2:
            st.metric("Current CGPA", f"{dashboard_data.get('overall_cgpa', 0):.2f}")
        
        with col3:
            st.metric("Pending Fees", f"₹{dashboard_data.get('pending_fees', 0):,.0f}")
        
        with col4:
            st.metric("Pending Assignments", len(dashboard_data.get('pending_assignments', [])))
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Subject-wise Attendance")
            subject_attendance = dashboard_data.get('attendance_stats', {}).get('subject_wise_attendance', [])
            if subject_attendance:
                subjects = [att['subject'] for att in subject_attendance]
                percentages = [att['percentage'] for att in subject_attendance]
                fig = px.bar(x=subjects, y=percentages, title="Attendance by Subject")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔔 Recent Announcements")
            announcements = dashboard_data.get('recent_announcements', [])
            for ann in announcements[:3]:
                st.markdown(f"**{ann['title']}** - {ann['announcement_type']}")
                st.markdown(f"{ann['content'][:100]}...")
                st.markdown("---")
    else:
        st.error(f"Failed to load dashboard: {error}")

def show_student_attendance():
    """Detailed attendance with daily, weekly, monthly stats per subject"""
    st.markdown("### 📅 Attendance Analytics")
    
    # Get detailed attendance stats
    if st.button("📊 Load Attendance Statistics"):
        with st.spinner("Loading attendance data..."):
            stats_data, error = make_api_request("/students/me/attendance/stats")
            if stats_data:
                st.success("Attendance statistics loaded!")
                
                # Overall stats
                overall = stats_data.get('overall_attendance', {})
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Today's Classes", overall.get('daily_count', 0))
                with col2:
                    st.metric("This Week", overall.get('weekly_count', 0))
                with col3:
                    st.metric("This Month", overall.get('monthly_count', 0))
                with col4:
                    st.metric("Overall %", f"{overall.get('average_percentage', 0):.1f}%")
                
                # Subject-wise detailed stats
                st.markdown("#### 📚 Subject-wise Attendance (Daily, Weekly, Monthly)")
                subject_stats = stats_data.get('subject_wise_attendance', [])
                
                if subject_stats:
                    df = pd.DataFrame([
                        {
                            'Subject': stats['subject'],
                            'Daily Count': stats['daily_count'],
                            'Weekly Count': stats['weekly_count'],
                            'Monthly Count': stats['monthly_count'],
                            'Total Classes': stats['total_classes'],
                            'Attended': stats['attended_classes'],
                            'Percentage': f"{stats['percentage']:.1f}%"
                        }
                        for stats in subject_stats
                    ])
                    st.dataframe(df, use_container_width=True)
                    
                    # Visualization
                    fig = px.bar(
                        df, x='Subject', y=['Daily Count', 'Weekly Count', 'Monthly Count'],
                        title="Attendance Count by Subject (Daily/Weekly/Monthly)",
                        barmode='group'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Failed to load attendance: {error}")

def show_student_results():
    """Student results for internal and lab exams"""
    st.markdown("### 📈 Exam Results (Internal & Lab)")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        semester_filter = st.selectbox("Select Semester", ["All", "1", "2", "3", "4", "5", "6", "7", "8"])
    with col2:
        exam_type_filter = st.selectbox("Exam Type", ["All", "internal", "lab"])
    
    if st.button("📊 Load Results"):
        with st.spinner("Loading results..."):
            results_data, error = make_api_request("/students/me/results")
            if results_data:
                st.success("Results loaded!")
                
                for semester_result in results_data:
                    with st.expander(f"Semester {semester_result['semester']} Results"):
                        
                        # Internal Results
                        if semester_result.get('internal_results'):
                            st.markdown("#### 📝 Internal Exam Results")
                            internal_df = pd.DataFrame([
                                {
                                    'Subject': result['subject'],
                                    'Marks': f"{result['marks_obtained']}/{result['total_marks']}",
                                    'Percentage': f"{result['percentage']:.1f}%",
                                    'Grade': result['grade'],
                                    'Date': result['exam_date']
                                }
                                for result in semester_result['internal_results']
                            ])
                            st.dataframe(internal_df, use_container_width=True)
                        
                        # Lab Results
                        if semester_result.get('lab_results'):
                            st.markdown("#### 🔬 Lab Exam Results")
                            lab_df = pd.DataFrame([
                                {
                                    'Subject': result['subject'],
                                    'Marks': f"{result['marks_obtained']}/{result['total_marks']}",
                                    'Percentage': f"{result['percentage']:.1f}%",
                                    'Grade': result['grade'],
                                    'Date': result['exam_date']
                                }
                                for result in semester_result['lab_results']
                            ])
                            st.dataframe(lab_df, use_container_width=True)
            else:
                st.error(f"Failed to load results: {error}")

def show_student_notes():
    """Faculty notes by subject"""
    st.markdown("### 📝 Faculty Notes by Subject")
    
    # Subject filter
    subject_filter = st.selectbox("Filter by Subject", ["All Subjects", "Mathematics", "Physics", "Chemistry", "Computer Science"])
    
    if st.button("📚 Load Notes"):
        with st.spinner("Loading notes..."):
            notes_data, error = make_api_request("/students/me/notes")
            if notes_data:
                st.success(f"Found {len(notes_data)} notes!")
                
                for note in notes_data:
                    with st.expander(f"📄 {note['title']} - {note['subject']}"):
                        st.markdown(f"**Type:** {note['note_type']}")
                        st.markdown(f"**Subject:** {note['subject']}")
                        st.markdown(f"**Content:** {note['content']}")
                        if note.get('file_url'):
                            st.markdown(f"[📎 Download File]({note['file_url']})")
                        st.markdown(f"**Posted:** {note['created_at'][:10]}")
            else:
                st.error(f"Failed to load notes: {error}")

def show_student_notices():
    """Notice board and announcements"""
    st.markdown("### 📢 Notice Board & Announcements")
    
    if st.button("📋 Load Announcements"):
        with st.spinner("Loading announcements..."):
            announcements_data, error = make_api_request("/students/me/announcements")
            if announcements_data:
                st.success(f"Found {len(announcements_data)} announcements!")
                
                for announcement in announcements_data:
                    urgency = "🚨 URGENT" if announcement.get('is_urgent') else "📢"
                    with st.expander(f"{urgency} {announcement['title']} - {announcement['announcement_type']}"):
                        st.markdown(f"**Type:** {announcement['announcement_type']}")
                        st.markdown(f"**Content:** {announcement['content']}")
                        if announcement.get('valid_until'):
                            st.markdown(f"**Valid Until:** {announcement['valid_until']}")
                        st.markdown(f"**Posted:** {announcement['created_at'][:10]}")
            else:
                st.error(f"Failed to load announcements: {error}")

def show_student_assignments():
    """Assignment submissions"""
    st.markdown("### 📋 Assignment Submissions")
    
    if st.button("📝 Load Assignments"):
        with st.spinner("Loading assignments..."):
            assignments_data, error = make_api_request("/students/me/assignments")
            if assignments_data:
                st.success(f"Found {len(assignments_data)} assignments!")
                
                for assignment in assignments_data:
                    status_color = "🟢" if assignment.get('submission_status') == "Submitted" else "🔴"
                    with st.expander(f"{status_color} {assignment['title']} - {assignment['subject']}"):
                        st.markdown(f"**Subject:** {assignment['subject']}")
                        st.markdown(f"**Description:** {assignment['description']}")
                        st.markdown(f"**Due Date:** {assignment['due_date']}")
                        st.markdown(f"**Max Marks:** {assignment['max_marks']}")
                        st.markdown(f"**Status:** {assignment.get('submission_status', 'Not Submitted')}")
                        if assignment.get('marks_obtained'):
                            st.markdown(f"**Marks Obtained:** {assignment['marks_obtained']}")
                        if assignment.get('file_url'):
                            st.markdown(f"[📎 Assignment File]({assignment['file_url']})")
            else:
                st.error(f"Failed to load assignments: {error}")

def show_student_fees():
    """Fee details connected to administration"""
    st.markdown("### 💰 Fee Management (Connected to Administration)")
    
    if st.button("💳 Load Fee Details"):
        with st.spinner("Loading fee information..."):
            fees_data, error = make_api_request("/students/me/fees")
            if fees_data:
                st.success("Fee information loaded!")
                
                # Fee summary
                summary = fees_data.get('summary', {})
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Fees", f"₹{summary.get('total_fees', 0):,.0f}")
                with col2:
                    st.metric("Paid", f"₹{summary.get('paid_fees', 0):,.0f}")
                with col3:
                    st.metric("Pending", f"₹{summary.get('pending_fees', 0):,.0f}")
                with col4:
                    st.metric("Overdue", f"₹{summary.get('overdue_fees', 0):,.0f}")
                
                # Fee details
                st.markdown("#### 📋 Fee Details")
                fee_details = fees_data.get('fee_details', [])
                if fee_details:
                    df = pd.DataFrame([
                        {
                            'Fee Type': fee['fee_type'],
                            'Amount': f"₹{fee['amount']:,.0f}",
                            'Due Date': fee['due_date'],
                            'Status': '✅ Paid' if fee['is_paid'] else '⏳ Pending',
                            'Semester': fee['semester'],
                            'Academic Year': fee['academic_year']
                        }
                        for fee in fee_details
                    ])
                    st.dataframe(df, use_container_width=True)
            else:
                st.error(f"Failed to load fees: {error}")

def show_faculty_dashboard():
    """Complete Faculty dashboard"""
    st.markdown('<h1 class="main-header">👨🏫 Faculty Dashboard</h1>', unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "📅 Attendance", "📝 Notes", "📢 Announcements", "📋 Assignments", "📈 Results"
    ])
    
    with tab1:
        show_faculty_overview()
    
    with tab2:
        show_faculty_attendance()
    
    with tab3:
        show_faculty_notes()
    
    with tab4:
        show_faculty_announcements()
    
    with tab5:
        show_faculty_assignments()
    
    with tab6:
        show_faculty_results()

def show_faculty_overview():
    """Faculty overview with statistics"""
    st.markdown("### 📊 Teaching Overview")
    
    if st.button("📈 Load Dashboard"):
        with st.spinner("Loading dashboard..."):
            dashboard_data, error = make_api_request("/faculty/dashboard")
            if dashboard_data:
                st.success("Dashboard loaded!")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Today's Classes", dashboard_data.get('today_classes_count', 0))
                
                with col2:
                    st.metric("Recent Notes", len(dashboard_data.get('recent_notes', [])))
                
                with col3:
                    st.metric("Upcoming Exams", len(dashboard_data.get('upcoming_exams', [])))
                
                with col4:
                    st.metric("Pending Submissions", dashboard_data.get('pending_submissions_count', 0))
                
                # Recent activities
                st.markdown("#### 📝 Recent Notes")
                for note in dashboard_data.get('recent_notes', [])[:3]:
                    st.markdown(f"**{note['title']}** - {note['subject']}")
            else:
                st.error(f"Failed to load dashboard: {error}")

def show_faculty_attendance():
    """Faculty attendance management with detailed stats"""
    st.markdown("### 📅 Attendance Management")
    
    # Mark attendance form
    with st.form("mark_attendance"):
        st.markdown("#### ✅ Mark Attendance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            subject = st.text_input("Subject")
            attendance_date = st.date_input("Date", value=date.today())
        
        with col2:
            period = st.number_input("Period", min_value=1, max_value=8, value=1)
            student_id = st.text_input("Student ID")
        
        with col3:
            status = st.selectbox("Status", ["present", "absent", "leave"])
        
        if st.form_submit_button("Mark Attendance"):
            if all([subject, student_id]):
                attendance_data = {
                    "student_id": student_id,
                    "date": str(attendance_date),
                    "period": period,
                    "subject": subject,
                    "status": status
                }
                
                result, error = make_api_request("/attendance/enroll", "POST", attendance_data)
                if result:
                    st.success("Attendance marked successfully!")
                else:
                    st.error(f"Failed to mark attendance: {error}")
            else:
                st.error("Please fill all required fields")
    
    # View attendance statistics
    st.markdown("#### 📊 Attendance Statistics")
    if st.button("📈 Load Attendance Stats"):
        with st.spinner("Loading statistics..."):
            stats_data, error = make_api_request("/faculty/attendance/stats")
            if stats_data:
                st.success("Statistics loaded!")
                
                # Overall stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Daily Classes", stats_data.get('daily_classes', 0))
                with col2:
                    st.metric("Weekly Classes", stats_data.get('weekly_classes', 0))
                with col3:
                    st.metric("Monthly Classes", stats_data.get('monthly_classes', 0))
                with col4:
                    st.metric("Total Classes", stats_data.get('total_classes', 0))
                
                # Subject-wise stats
                subject_stats = stats_data.get('subject_wise_stats', {})
                if subject_stats:
                    st.markdown("#### 📚 Subject-wise Statistics")
                    df = pd.DataFrame([
                        {
                            'Subject': subject,
                            'Daily': stats['daily_count'],
                            'Weekly': stats['weekly_count'],
                            'Monthly': stats['monthly_count'],
                            'Total Classes': stats['total_classes'],
                            'Avg Attendance': f"{stats['average_attendance']:.1f}%"
                        }
                        for subject, stats in subject_stats.items()
                    ])
                    st.dataframe(df, use_container_width=True)
            else:
                st.error(f"Failed to load stats: {error}")

def show_faculty_notes():
    """Faculty notes management section-wise"""
    st.markdown("### 📝 Notes Management (Section-wise)")
    
    # Create note form
    with st.form("create_note"):
        st.markdown("#### ➕ Create New Note")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title")
            subject = st.text_input("Subject")
        
        with col2:
            note_type = st.selectbox("Type", ["Lecture Notes", "Assignment", "Reference Material", "Syllabus", "Practical Notes"])
            file_url = st.text_input("File URL (optional)")
        
        content = st.text_area("Content")
        
        if st.form_submit_button("Create Note"):
            if all([title, subject, content]):
                note_data = {
                    "title": title,
                    "subject": subject,
                    "note_type": note_type,
                    "content": content,
                    "file_url": file_url if file_url else None
                }
                
                result, error = make_api_request("/faculty/notes", "POST", note_data)
                if result:
                    st.success("Note created successfully!")
                else:
                    st.error(f"Failed to create note: {error}")
            else:
                st.error("Please fill all required fields")
    
    # View existing notes
    st.markdown("#### 📚 My Notes")
    if st.button("📖 Load My Notes"):
        notes_data, error = make_api_request("/faculty/notes")
        if notes_data:
            for note in notes_data:
                with st.expander(f"📄 {note['title']} - {note['subject']}"):
                    st.markdown(f"**Type:** {note['note_type']}")
                    st.markdown(f"**Content:** {note['content']}")
                    if note.get('file_url'):
                        st.markdown(f"[📎 File Link]({note['file_url']})")
        else:
            st.info("No notes created yet")

def show_faculty_announcements():
    """Faculty announcements and notice posting"""
    st.markdown("### 📢 Announcements & Notice Board")
    
    # Create announcement form
    with st.form("create_announcement"):
        st.markdown("#### ➕ Create Announcement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title")
            announcement_type = st.selectbox("Type", ["General", "Exam", "Assignment", "Event", "Holiday", "Urgent"])
            is_urgent = st.checkbox("Mark as Urgent")
        
        with col2:
            target_year = st.number_input("Target Year (optional)", min_value=1, max_value=4, value=None)
            target_department = st.text_input("Target Department (optional)")
            valid_until = st.date_input("Valid Until (optional)")
        
        content = st.text_area("Content")
        
        if st.form_submit_button("Create Announcement"):
            if all([title, content]):
                announcement_data = {
                    "title": title,
                    "content": content,
                    "announcement_type": announcement_type,
                    "is_urgent": is_urgent,
                    "target_year": target_year,
                    "target_department": target_department if target_department else None,
                    "valid_until": str(valid_until) if valid_until else None
                }
                
                result, error = make_api_request("/faculty/announcements", "POST", announcement_data)
                if result:
                    st.success("Announcement created successfully!")
                else:
                    st.error(f"Failed to create announcement: {error}")
            else:
                st.error("Please fill title and content")

def show_faculty_assignments():
    """Faculty assignment management"""
    st.markdown("### 📋 Assignment Management")
    st.info("Assignment management features integrated with student submissions")

def show_faculty_results():
    """Faculty results management for internal and lab exams"""
    st.markdown("### 📈 Results Management (Internal & Lab)")
    st.info("Results management for internal and lab exams")

def show_admin_dashboard():
    """Administration dashboard"""
    st.markdown('<h1 class="main-header">⚙️ Administration Dashboard</h1>', unsafe_allow_html=True)
    st.info("Admin dashboard with system management features")

# Main app logic
def main():
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()