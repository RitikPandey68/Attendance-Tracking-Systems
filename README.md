⚠️ **LICENSE NOTICE**

This project is **NOT open-source**.
Unauthorized copying, reuse, modification, or distribution
of this code is strictly prohibited without written permission.



# 🎓 AI-Powered Attendance Tracking System

## 📚 Project Overview
A **secure, scalable, and AI-ready** backend + dashboard application designed to manage:

- **Student attendance**
- **Academic results & CGPA**
- **Leave & holiday workflows**
- **Faculty-student coordination**

Built with **FastAPI**, **MongoDB**, **JWT authentication**, and **Streamlit dashboards**.

## 🎯 Core Objectives

- ✅ Automate daily attendance tracking
- ✅ Provide role-based access (**Student / Faculty / Admin**)
- ✅ Maintain academic performance records
- ✅ Enable faculty-controlled attendance & results
- ✅ Prepare system for **AI-based attendance** (Face / Location)

## 🚀 Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance REST API |
| **MongoDB** | NoSQL database with indexing |
| **JWT** | Token-based authentication |
| **bcrypt** | Secure password hashing |
| **Python** | Core backend language |

### Frontend
- **Streamlit** - Interactive dashboards

### Future Integrations
- 👤 Face recognition
- 📍 Location-based attendance
- 🔑 OTP login
- 🔗 Google OAuth

## 🧠 System Architecture

Client (Web / Mobile)
↓
Streamlit Dashboard
↓
FastAPI Backend (JWT + RBAC)
↓
MongoDB Database


## 🏗️ Project Structure
Attendance-Tracking-Systems/
│
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── auth/
│ │ │ ├── jwt_handler.py
│ │ │ └── password_utils.py
│ │ │
│ │ ├── models/
│ │ │ ├── user.py
│ │ │ ├── student.py
│ │ │ ├── faculty.py
│ │ │ ├── attendance.py
│ │ │ ├── results.py
│ │ │ ├── leaves.py
│ │ │ ├── holidays.py
│ │ │ └── events.py
│ │ │
│ │ ├── routes/
│ │ │ ├── auth_routes.py
│ │ │ ├── attendance_routes.py
│ │ │ ├── results_routes.py
│ │ │ ├── leave_routes.py
│ │ │ ├── holiday_routes.py
│ │ │ └── event_routes.py
│ │ │
│ │ ├── services/
│ │ │ ├── attendance_service.py
│ │ │ ├── cgpa_service.py
│ │ │ └── email_service.py
│ │ │
│ │ └── utils/
│ │ ├── validators.py
│ │ └── response_helper.py
│ │
│ ├── database/
│ │ ├── mongodb.py
│ │ └── indexes.py
│ │
│ ├── scripts/
│ │ └── clear_database.py
│ │
│ └── requirements.txt
│
├── frontend/
│ ├── student_dashboard.py
│ ├── faculty_dashboard.py
│ └── admin_dashboard.py
│
├── tests/
│ ├── test_complete_system.py
│ ├── test_requirements.txt
│ └── run_tests.bat
│
├── docs/
│ ├── API_Documentation.md
│ └── Architecture.md
│
├── .env.example
├── README.md
└── LICENSE


## ✅ Implemented Features

### 🔐 Authentication & Authorization
- JWT-based login
- Role-based access control (RBAC)
- Secure password hashing with bcrypt

### 📊 Attendance Management
- Daily attendance records
- Period-wise tracking
- Faculty-controlled marking
- Student attendance view

### 📈 Academic Records
- Results management
- Semester-wise CGPA
- Faculty write access

### 🗓️ Utilities
- Leave management system
- Holiday calendar
- Events & announcements

## 🚧 Features In Progress

- 📧 Email verification
- 📊 Attendance percentage calculation
- 📈 CGPA calculation service
- ✅ Leave approval workflow
- 📍 Location-based attendance validation

## 🤖 AI & Advanced Features (Planned)

| Feature | Status |
|---------|--------|
| 👤 Face recognition attendance | Planned |
| 🔑 OTP-based login | Planned |
| 🔗 Google OAuth integration | Planned |
| 🔔 Real-time notifications | Planned |
| 🔄 Multi-device synchronization | Planned |
| 📤 Data export (CSV / PDF) | Planned |

## 🧪 Testing

### Covered Tests
- API connectivity
- Authentication flow
- Attendance operations
- Results operations

### Run Tests
pip install -r tests/test_requirements.txt
python tests/test_complete_system.py


## ⚙️ Getting Started

### Prerequisites
- Python 3.8+
- MongoDB
- Git

### Installation
git clone https://github.com/RitikPandey68/Attendance-Tracking-Systems.git
cd backend
pip install -r requirements.txt


### Run Backend Server
uvicorn app.main:app --reload --port 8000


### Access Points
| Endpoint | URL |
|----------|-----|
| **API** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

## 🚀 Deployment Roadmap

1. **Docker containerization**
2. **SSL & security hardening**
3. **Monitoring & logging**
4. **Automated database backups**

## 📄 License
This project is **NOT open-source**.

All rights are reserved by the author.
Unauthorized copying, modification, redistribution, or usage
of this code in any form is strictly prohibited.

See the `LICENSE` file for full details.

## 👨‍💻 Author
**Ritik Pandey**  
*Final Year CSE Student*  
[GitHub](https://github.com/RitikPandey68)
