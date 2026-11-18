# RISKRADAR
# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

**Project Name:** RiskRadar – Student Performance Prediction & Academic Risk Detection System  
**Team Members:** Ronit Pednekar, Manas Parab, Usman Khan 
**Programme:** MSc Integrated Data Science — SEM 5  
**Subject:** Software Engineering  
**Institution:** Goa University  
**Document Version:** 1.0  
**Date:** 18 November 2026

---

# 1. INTRODUCTION

## 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) document is to describe the functional and non-functional requirements of RiskRadar, a student performance prediction and academic risk detection system.

RiskRadar enables university faculty to predict student academic performance using machine learning, identify at-risk students early, and provide actionable recommendations. Students can view their own performance summaries and risk assessments.

This document describes the system's purpose, scope, user requirements, system features, interfaces, constraints and major technical requirements.

## 1.2 Project Scope

RiskRadar is a web-based academic analytics platform developed to assist universities in identifying students who may be at academic risk based on their performance metrics.

The system includes:

- Role-based authentication for teachers and students.
- Password hashing using werkzeug.security.
- Dashboard with real-time risk distribution statistics.
- ML-powered student performance prediction using Random Forest Regression.
- Student roster management with search, filter and sort capabilities.
- Individual student performance history tracking.
- CSV roster upload with column validation.
- Model insights and feature importance visualization.
- Student self-service performance view.
- Dark mode and light mode support.
- Responsive design for mobile, tablet and desktop.

The project integrates frontend development, backend services, relational database management, authentication and machine learning model training.

## 1.3 Intended Audience

This document is intended for:

- Project developers and team members.
- Faculty members and project evaluators.
- Academic reviewers.
- Future developers who may maintain or extend RiskRadar.

## 1.4 Definitions and Abbreviations

| Term | Description |
|---|---|
| SRS | Software Requirements Specification |
| ML | Machine Learning |
| EDA | Exploratory Data Analysis |
| DBMS | Database Management System |
| UI | User Interface |
| SQL | Structured Query Language |
| ORM | Object Relational Mapping |
| CSV | Comma Separated Values |
| CDN | Content Delivery Network |
| MAE | Mean Absolute Error |
| RMSE | Root Mean Square Error |
| R² | Coefficient of Determination |

---

# 2. OVERALL DESCRIPTION

## 2.1 Product Perspective

RiskRadar follows a monolithic web application architecture using the Flask framework. The frontend uses Jinja2 server-side templates with Tailwind CSS for styling. The backend handles authentication, business logic, prediction and database operations.

SQLite is used for persistent storage with direct SQL queries via Python's sqlite3 module. A trained Random Forest model provides real-time predictions.

## 2.2 Product Functions

The major functions of RiskRadar include:

1. Role-based user authentication (Teacher and Student).
2. Teacher dashboard with risk distribution statistics.
3. ML-powered student performance prediction.
4. Contributing factor analysis with impact indicators.
5. Personalized academic recommendations.
6. Student roster with search, filter and sort.
7. Individual student performance history with line charts.
8. CSV roster upload with column validation.
9. Model insights and accuracy visualization.
10. Student self-service performance summary.

## 2.3 User Classes and Characteristics

### A. Teacher

A teacher can:

- Log in using their Teacher ID and password.
- View the dashboard with risk distribution statistics.
- Predict student performance using 7 academic metrics.
- View all students with search, filter and sort.
- View individual student performance history.
- Upload student rosters via CSV.
- View model insights and feature importance.
- Log out.

### B. Student

A student can:

- Log in using their Student ID and password.
- View their latest prediction score and risk level.
- View personalized recommendations.
- Log out.

## 2.4 Operating Environment

| Component | Technology |
|---|---|
| Operating System | macOS / Windows / Linux |
| Programming Language | Python 3.12+ |
| Backend Framework | Flask |
| Templating Engine | Jinja2 |
| CSS Framework | Tailwind CSS (CDN) |
| Charting Library | Chart.js (CDN) |
| Icon Library | Lucide Icons (CDN) |
| Font | Inter (Google Fonts) |
| Database | SQLite |
| ML Library | scikit-learn |
| Model Serialization | joblib |
| Data Processing | pandas, NumPy |
| Password Hashing | werkzeug.security |

## 2.5 Design and Implementation Constraints

The following constraints apply:

- The application requires a Python environment with Flask installed.
- SQLite is used as an embedded database (no separate server required).
- The trained model file (model.pkl) must be present for predictions.
- The students.csv dataset must be present for initial database seeding.
- All CSS and JavaScript libraries are loaded via CDN (internet required for first load).
- The application uses Flask sessions for authentication state management.

## 2.6 Assumptions and Dependencies

- Users have access to a modern web browser.
- The Flask development server is available during application usage.
- The students.csv dataset contains the expected column structure.
- Internet connectivity is required for CDN resources on first load.

---

# 3. FUNCTIONAL REQUIREMENTS

## FR-01: Role Selection

The system shall display a landing page allowing users to select their role (Teacher or Student) before proceeding to login.

## FR-02: User Authentication

The system shall allow teachers and students to authenticate using their respective IDs and passwords.

The system shall:

- Verify the supplied password against the stored password hash using werkzeug.security.check_password_hash.
- Reject invalid credentials with an error message.
- Maintain authentication state using Flask sessions.
- Redirect authenticated users to their respective dashboards.

## FR-03: Access Control

The system shall enforce role-based access control using the login_required decorator.

- Teachers can access: Dashboard, Predict, Students, Upload, Insights.
- Students can access: My Performance page.
- Unauthorized access redirects users to the appropriate page.

## FR-04: Teacher Dashboard

The system shall display a dashboard containing:

- Total number of students.
- Count of High Risk, Moderate Risk and Low Risk students.
- A donut chart showing risk distribution.
- A list of the 5 most recent predictions.

## FR-05: Student Performance Prediction

The system shall allow teachers to predict a student's academic performance by entering 7 metrics:

- Midterm Score (0–100)
- Assignments Average (0–100)
- Quizzes Average (0–100)
- Participation Score (0–100)
- Projects Score (0–100)
- Attendance Percentage (0–100)
- Study Hours per Week (0–30)

The system shall:

- Use the trained Random Forest model to generate a predicted score.
- Classify the score into risk categories: High (< 60), Moderate (60–70), Low (≥ 70).
- Display the top contributing factors with impact indicators.
- Provide personalized academic recommendations.
- Save the prediction to the database.

## FR-06: Student Roster

The system shall display all students in a searchable, filterable and sortable table.

The system shall support:

- Text search by student name or ID.
- Filter by risk level (All, High, Moderate, Low).
- Sort by ID, Name, Department or Score.
- Clickable rows to navigate to student history.

## FR-07: Student Performance History

The system shall display a student's prediction history including:

- A line chart showing score progression over time.
- A table of past predictions with dates, scores and risk levels.

## FR-08: CSV Upload

The system shall provide a drag-and-drop CSV upload interface that:

- Displays file information.
- Previews the first 5 rows.
- Validates required columns (student_id, name, department).

## FR-09: Model Insights

The system shall display model performance information including:

- Feature importance horizontal bar chart.
- Model accuracy visualization.
- Risk trend analysis.
- Description of how predictions work.

## FR-10: Student Self-Service

The system shall provide students with a personalized view containing:

- Their latest predicted score.
- Their risk level.
- A progress bar with threshold markers.
- Areas for improvement (if at risk).
- Next steps checklist.

## FR-11: Theme Support

The system shall support dark mode and light mode with:

- Theme toggle button.
- localStorage persistence.
- No-flash inline script in the HTML head.

---

# 4. NON-FUNCTIONAL REQUIREMENTS

## 4.1 Performance Requirements

- The dashboard should load within reasonable time for 5,000 students.
- Predictions should be generated in under 1 second.
- The ML model should be loaded once and cached in memory.

## 4.2 Security Requirements

- Passwords must be stored as hashed values using werkzeug.security.generate_password_hash.
- Flask session secret key must be configured.
- Role-based access control must protect teacher and student routes.

## 4.3 Usability Requirements

- The application should be responsive across mobile, tablet and desktop.
- Dark mode and light mode should be supported.
- The interface should use consistent design patterns via Jinja2 macros.

## 4.4 Maintainability Requirements

- Backend services should be separated from route handlers.
- Database operations should be isolated in database.py.
- The mock.py contract should document expected function signatures and return shapes.

---

# 5. EXTERNAL INTERFACE REQUIREMENTS

## 5.1 User Interface

The frontend consists of the following pages:

| Page | Purpose |
|---|---|
| role_select.html | Landing page with role selection |
| login.html | Authentication for both roles |
| dashboard.html | Teacher dashboard with statistics |
| predict.html | Prediction form and results |
| students.html | Searchable student roster |
| history.html | Individual student history |
| upload.html | CSV roster upload |
| insights.html | Model insights and analytics |
| student_me.html | Student performance view |

Supporting templates:

| Template | Purpose |
|---|---|
| base.html | Base layout with CDN imports and theme support |
| macros.html | Reusable UI components |
| teacher_layout.html | Sidebar layout for teacher pages |

## 5.2 Software Interfaces

The application interacts with:

- Flask web framework for routing and sessions.
- SQLite database for persistent storage.
- scikit-learn for model inference.
- joblib for model serialization.
- Chart.js for data visualization.
- Tailwind CSS for styling.
- Lucide Icons for iconography.

---

# 6. DATABASE REQUIREMENTS

The system uses SQLite as its embedded relational database.

The database contains three tables:

1. `teachers` – Teacher accounts with hashed passwords.
2. `students` – Student records with demographic information.
3. `predictions` – Prediction history with scores, risk levels and contributing factors.

Primary keys and foreign-key relationships maintain data associations.

The database is seeded from students.csv on first application startup.

---

# 7. RISK CLASSIFICATION

RiskRadar classifies students into three risk categories:

| Risk Level | Score Range | Description |
|---|---|---|
| High | < 60 | Student requires immediate academic intervention |
| Moderate | 60 – 70 | Student should be monitored closely |
| Low | ≥ 70 | Student is performing satisfactorily |

---

# 8. CONCLUSION

RiskRadar is designed as an academic risk detection platform that combines web development, database management, authentication, machine learning and data visualization.

This SRS document establishes the functional and non-functional requirements of the system and provides a reference for implementation, testing, maintenance and future development.

---

**END OF DOCUMENT**
