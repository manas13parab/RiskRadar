# RISKRADAR
# FUNCTIONAL TESTING REPORT

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

This document describes the functional testing performed on RiskRadar. It lists the test cases executed to verify that the application's features work as specified in the Software Requirements Specification (SRS).

## 1.2 Scope

Functional testing covers all user-facing features of the RiskRadar application including:

- Role selection and login.
- Teacher dashboard and statistics.
- Student performance prediction.
- Student roster management.
- Student performance history.
- CSV roster upload.
- Model insights.
- Student self-service view.
- Authentication and access control.
- Theme support.
- Responsive design.

## 1.3 Testing Approach

RiskRadar functional testing was performed through manual browser-level verification. Each feature was tested by navigating through the application interface, entering inputs and verifying the expected outputs and behaviours.

The Flask development server was run locally at http://127.0.0.1:5002 during all testing activities.

# 2. TEST ENVIRONMENT

| Component | Details |
|---|---|
| Operating System | macOS |
| Python Version | 3.12+ |
| Flask Version | Latest stable |
| Browser | Chrome / Safari |
| Server Address | http://127.0.0.1:5002 |
| Database | SQLite (riskradar.db) |
| Dataset | 5,000 students from students.csv |
| ML Model | model.pkl (Random Forest, 200 trees) |

# 3. FUNCTIONAL TEST CASES

## 3.1 Role Selection and Authentication

### TC-01: Role Selection Page Load

| Field | Value |
|---|---|
| Test ID | TC-01 |
| Feature | Role Selection |
| Description | Verify the landing page displays Teacher and Student role options |
| Precondition | Application is running |
| Steps | 1. Navigate to http://127.0.0.1:5002/ |
| Expected Result | Page displays two role cards: "Teacher" and "Student" |
| Actual Result | Both role cards displayed correctly with icons and descriptions |
| Status | **PASS** |

### TC-02: Teacher Login – Valid Credentials

| Field | Value |
|---|---|
| Test ID | TC-02 |
| Feature | Authentication |
| Description | Verify teacher can log in with valid credentials |
| Precondition | Teacher account T01 exists in database |
| Steps | 1. Click "Teacher" on role selection. 2. Enter ID: T01. 3. Enter Password: admin123. 4. Click Login. |
| Expected Result | Redirect to teacher dashboard |
| Actual Result | Successfully redirected to /teacher dashboard |
| Status | **PASS** |

### TC-03: Teacher Login – Invalid Credentials

| Field | Value |
|---|---|
| Test ID | TC-03 |
| Feature | Authentication |
| Description | Verify teacher login fails with wrong password |
| Precondition | Application is running |
| Steps | 1. Navigate to /login/teacher. 2. Enter ID: T01. 3. Enter Password: wrongpassword. 4. Click Login. |
| Expected Result | Error message displayed, remain on login page |
| Actual Result | Flash message "Invalid credentials" displayed, login page retained |
| Status | **PASS** |

### TC-04: Student Login – Valid Credentials

| Field | Value |
|---|---|
| Test ID | TC-04 |
| Feature | Authentication |
| Description | Verify student can log in with valid credentials |
| Precondition | Student STU0001 exists in database |
| Steps | 1. Click "Student" on role selection. 2. Enter ID: STU0001. 3. Enter correct password. 4. Click Login. |
| Expected Result | Redirect to student performance page |
| Actual Result | Successfully redirected to /me with performance data |
| Status | **PASS** |

### TC-05: Student Login – Invalid Credentials

| Field | Value |
|---|---|
| Test ID | TC-05 |
| Feature | Authentication |
| Description | Verify student login fails with wrong password |
| Precondition | Application is running |
| Steps | 1. Navigate to /login/student. 2. Enter ID: STU0001. 3. Enter Password: wrongpassword. 4. Click Login. |
| Expected Result | Error message displayed, remain on login page |
| Actual Result | Flash message "Invalid credentials" displayed |
| Status | **PASS** |

### TC-06: Logout

| Field | Value |
|---|---|
| Test ID | TC-06 |
| Feature | Authentication |
| Description | Verify logout terminates session |
| Precondition | User is logged in |
| Steps | 1. Click Logout in sidebar/navigation. |
| Expected Result | Session terminated, redirect to role selection page |
| Actual Result | Redirected to / (role selection) |
| Status | **PASS** |

## 3.2 Access Control

### TC-07: Unauthenticated Access to Teacher Route

| Field | Value |
|---|---|
| Test ID | TC-07 |
| Feature | Access Control |
| Description | Verify unauthenticated users cannot access teacher dashboard |
| Precondition | No active session |
| Steps | 1. Navigate directly to /teacher. |
| Expected Result | Redirect to login page |
| Actual Result | Redirected to /login/teacher |
| Status | **PASS** |

### TC-08: Unauthenticated Access to Student Route

| Field | Value |
|---|---|
| Test ID | TC-08 |
| Feature | Access Control |
| Description | Verify unauthenticated users cannot access student page |
| Precondition | No active session |
| Steps | 1. Navigate directly to /me. |
| Expected Result | Redirect to login page |
| Actual Result | Redirected to /login/student |
| Status | **PASS** |

### TC-09: Role-Based Access – Teacher Accessing Student Route

| Field | Value |
|---|---|
| Test ID | TC-09 |
| Feature | Access Control |
| Description | Verify teacher cannot access student-only routes |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate directly to /me. |
| Expected Result | Redirect to appropriate page |
| Actual Result | Redirected away from student route |
| Status | **PASS** |

### TC-10: Role-Based Access – Student Accessing Teacher Route

| Field | Value |
|---|---|
| Test ID | TC-10 |
| Feature | Access Control |
| Description | Verify student cannot access teacher-only routes |
| Precondition | Logged in as student |
| Steps | 1. Navigate directly to /teacher. |
| Expected Result | Redirect to appropriate page |
| Actual Result | Redirected away from teacher route |
| Status | **PASS** |

## 3.3 Teacher Dashboard

### TC-11: Dashboard Statistics Display

| Field | Value |
|---|---|
| Test ID | TC-11 |
| Feature | Dashboard |
| Description | Verify dashboard shows correct statistics |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /teacher. |
| Expected Result | Display total students, High Risk count, Moderate Risk count, Low Risk count |
| Actual Result | Statistics cards show: Total 5000, High 279, Moderate 1760, Low 2961 |
| Status | **PASS** |

### TC-12: Dashboard Donut Chart

| Field | Value |
|---|---|
| Test ID | TC-12 |
| Feature | Dashboard |
| Description | Verify risk distribution donut chart renders |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /teacher. 2. Observe the chart area. |
| Expected Result | Donut chart displays risk distribution with color coding |
| Actual Result | Chart.js donut chart rendered with High (red), Moderate (amber), Low (green) segments |
| Status | **PASS** |

### TC-13: Dashboard Recent Predictions

| Field | Value |
|---|---|
| Test ID | TC-13 |
| Feature | Dashboard |
| Description | Verify recent predictions list displays |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /teacher. 2. Scroll to recent predictions section. |
| Expected Result | List of 5 most recent predictions with student name, score and risk |
| Actual Result | 5 recent prediction entries displayed correctly |
| Status | **PASS** |

## 3.4 Student Performance Prediction

### TC-14: Prediction Form Load

| Field | Value |
|---|---|
| Test ID | TC-14 |
| Feature | Prediction |
| Description | Verify prediction form displays with student dropdown and 7 input fields |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /predict. |
| Expected Result | Student dropdown and 7 metric input fields displayed |
| Actual Result | Form shows student selector and all 7 inputs with appropriate ranges |
| Status | **PASS** |

### TC-15: Prediction Submission – Valid Inputs

| Field | Value |
|---|---|
| Test ID | TC-15 |
| Feature | Prediction |
| Description | Verify prediction generates results with valid inputs |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /predict. 2. Select a student. 3. Enter: Midterm 75, Assignments 80, Quizzes 70, Participation 65, Projects 85, Attendance 90, Study Hours 15. 4. Submit. |
| Expected Result | Predicted score, risk level, contributing factors and recommendations displayed |
| Actual Result | Prediction result displayed with score, Low risk classification, top factors and recommendations |
| Status | **PASS** |

### TC-16: Prediction – High Risk Student

| Field | Value |
|---|---|
| Test ID | TC-16 |
| Feature | Prediction |
| Description | Verify prediction correctly identifies High Risk |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /predict. 2. Select a student. 3. Enter low scores across all metrics (e.g. all below 40). 4. Submit. |
| Expected Result | Score < 60, risk classified as "High" |
| Actual Result | Predicted score below 60, red "High Risk" badge displayed |
| Status | **PASS** |

### TC-17: Prediction – Contributing Factors

| Field | Value |
|---|---|
| Test ID | TC-17 |
| Feature | Prediction |
| Description | Verify contributing factors display after prediction |
| Precondition | A prediction has been submitted |
| Steps | 1. Submit a prediction. 2. Observe the contributing factors section. |
| Expected Result | Top contributing factors listed with impact indicators |
| Actual Result | Factors displayed with names, values and positive/negative impact indicators |
| Status | **PASS** |

### TC-18: Prediction – Recommendations

| Field | Value |
|---|---|
| Test ID | TC-18 |
| Feature | Prediction |
| Description | Verify personalized recommendations display after prediction |
| Precondition | A prediction has been submitted |
| Steps | 1. Submit a prediction. 2. Observe the recommendations section. |
| Expected Result | Academic recommendations displayed based on prediction results |
| Actual Result | Context-specific recommendations shown based on risk level and weak areas |
| Status | **PASS** |

### TC-19: Prediction Saved to Database

| Field | Value |
|---|---|
| Test ID | TC-19 |
| Feature | Prediction |
| Description | Verify prediction is saved and appears in student history |
| Precondition | A prediction has been submitted |
| Steps | 1. Submit a prediction for a student. 2. Navigate to /history/{student_id}. |
| Expected Result | New prediction appears in the student's history |
| Actual Result | Prediction record visible in history with correct score, risk and timestamp |
| Status | **PASS** |

## 3.5 Student Roster

### TC-20: Student Roster Display

| Field | Value |
|---|---|
| Test ID | TC-20 |
| Feature | Student Roster |
| Description | Verify all students display in the roster table |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /students. |
| Expected Result | Table displays student records with ID, name, department, score and risk |
| Actual Result | Student table loaded with all records |
| Status | **PASS** |

### TC-21: Student Roster – Search

| Field | Value |
|---|---|
| Test ID | TC-21 |
| Feature | Student Roster |
| Description | Verify search filters students by name or ID |
| Precondition | On /students page |
| Steps | 1. Type a student name in the search box. |
| Expected Result | Table filters to show only matching students |
| Actual Result | Real-time filtering shows matching students as text is typed |
| Status | **PASS** |

### TC-22: Student Roster – Filter by Risk

| Field | Value |
|---|---|
| Test ID | TC-22 |
| Feature | Student Roster |
| Description | Verify risk level filter works |
| Precondition | On /students page |
| Steps | 1. Select "High Risk" from the filter dropdown. |
| Expected Result | Only High Risk students displayed |
| Actual Result | Table filtered to show only High Risk students |
| Status | **PASS** |

### TC-23: Student Roster – Sort

| Field | Value |
|---|---|
| Test ID | TC-23 |
| Feature | Student Roster |
| Description | Verify column sorting works |
| Precondition | On /students page |
| Steps | 1. Click the "Score" column header. |
| Expected Result | Table sorts by score |
| Actual Result | Students sorted by score, toggles ascending/descending on repeated click |
| Status | **PASS** |

### TC-24: Student Roster – Navigate to History

| Field | Value |
|---|---|
| Test ID | TC-24 |
| Feature | Student Roster |
| Description | Verify clicking a student row navigates to their history |
| Precondition | On /students page |
| Steps | 1. Click on a student row in the table. |
| Expected Result | Navigate to /history/{student_id} |
| Actual Result | Navigated to the correct student history page |
| Status | **PASS** |

## 3.6 Student Performance History

### TC-25: History Page Load

| Field | Value |
|---|---|
| Test ID | TC-25 |
| Feature | History |
| Description | Verify student history page displays correctly |
| Precondition | Logged in as teacher, navigated to a student's history |
| Steps | 1. Navigate to /history/STU0001. |
| Expected Result | Student info, line chart and prediction table displayed |
| Actual Result | Page shows student details, Chart.js line chart and history table |
| Status | **PASS** |

### TC-26: History – Line Chart

| Field | Value |
|---|---|
| Test ID | TC-26 |
| Feature | History |
| Description | Verify line chart shows score progression over time |
| Precondition | Student has multiple predictions |
| Steps | 1. Navigate to a student's history with multiple predictions. |
| Expected Result | Line chart plots scores over time |
| Actual Result | Chart.js line chart rendered with score data points |
| Status | **PASS** |

### TC-27: History – Prediction Table

| Field | Value |
|---|---|
| Test ID | TC-27 |
| Feature | History |
| Description | Verify prediction history table shows all records |
| Precondition | Student has predictions |
| Steps | 1. Navigate to a student's history. 2. Observe the predictions table. |
| Expected Result | Table shows date, score and risk level for each prediction |
| Actual Result | All prediction records displayed in chronological order |
| Status | **PASS** |

## 3.7 CSV Upload

### TC-28: Upload Page Load

| Field | Value |
|---|---|
| Test ID | TC-28 |
| Feature | CSV Upload |
| Description | Verify upload page displays drag-and-drop interface |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /upload. |
| Expected Result | Drag-and-drop zone with upload instructions displayed |
| Actual Result | Upload area with drag-and-drop zone and file input rendered |
| Status | **PASS** |

### TC-29: Upload – File Selection

| Field | Value |
|---|---|
| Test ID | TC-29 |
| Feature | CSV Upload |
| Description | Verify file selection shows file information |
| Precondition | On /upload page |
| Steps | 1. Select a CSV file or drag it onto the drop zone. |
| Expected Result | File name and size displayed |
| Actual Result | File information displayed after selection |
| Status | **PASS** |

### TC-30: Upload – Preview

| Field | Value |
|---|---|
| Test ID | TC-30 |
| Feature | CSV Upload |
| Description | Verify CSV preview shows first 5 rows |
| Precondition | A CSV file has been selected |
| Steps | 1. Select a valid CSV file. 2. Observe the preview area. |
| Expected Result | First 5 rows of the CSV displayed in a table |
| Actual Result | Preview table rendered with up to 5 data rows |
| Status | **PASS** |

## 3.8 Model Insights

### TC-31: Insights Page Load

| Field | Value |
|---|---|
| Test ID | TC-31 |
| Feature | Model Insights |
| Description | Verify insights page displays model information |
| Precondition | Logged in as teacher T01 |
| Steps | 1. Navigate to /insights. |
| Expected Result | Feature importance chart and model information displayed |
| Actual Result | Horizontal bar chart with feature importance values and model description sections |
| Status | **PASS** |

### TC-32: Insights – Feature Importance Chart

| Field | Value |
|---|---|
| Test ID | TC-32 |
| Feature | Model Insights |
| Description | Verify feature importance chart shows correct ranking |
| Precondition | On /insights page |
| Steps | 1. Observe the feature importance chart. |
| Expected Result | Projects_Score highest, followed by Midterm_Score, Assignments_Avg, etc. |
| Actual Result | Chart shows correct feature ranking matching trained model importances |
| Status | **PASS** |

## 3.9 Student Self-Service

### TC-33: Student Performance View

| Field | Value |
|---|---|
| Test ID | TC-33 |
| Feature | Student Self-Service |
| Description | Verify student can view their performance |
| Precondition | Logged in as student |
| Steps | 1. Log in as a student. |
| Expected Result | Performance page shows latest score, risk level and progress bar |
| Actual Result | Score, risk badge, progress bar with threshold markers displayed |
| Status | **PASS** |

### TC-34: Student – Recommendations for At-Risk Student

| Field | Value |
|---|---|
| Test ID | TC-34 |
| Feature | Student Self-Service |
| Description | Verify at-risk students see improvement areas and next steps |
| Precondition | Logged in as a student with High or Moderate risk |
| Steps | 1. Log in as an at-risk student. |
| Expected Result | Areas for improvement and next steps checklist displayed |
| Actual Result | Improvement areas and actionable next steps shown |
| Status | **PASS** |

## 3.10 Theme Support

### TC-35: Dark Mode Toggle

| Field | Value |
|---|---|
| Test ID | TC-35 |
| Feature | Theme |
| Description | Verify dark mode can be toggled |
| Precondition | Application is loaded |
| Steps | 1. Click the theme toggle button. |
| Expected Result | UI switches between dark and light mode |
| Actual Result | Theme toggles correctly with smooth transition |
| Status | **PASS** |

### TC-36: Theme Persistence

| Field | Value |
|---|---|
| Test ID | TC-36 |
| Feature | Theme |
| Description | Verify theme choice persists across pages |
| Precondition | Theme set to dark mode |
| Steps | 1. Set dark mode. 2. Navigate to another page. |
| Expected Result | Dark mode retained on the new page |
| Actual Result | Dark mode persisted via localStorage, no flash on page load |
| Status | **PASS** |

## 3.11 Responsive Design

### TC-37: Mobile Viewport

| Field | Value |
|---|---|
| Test ID | TC-37 |
| Feature | Responsive Design |
| Description | Verify application renders correctly on mobile viewport |
| Precondition | Application is loaded |
| Steps | 1. Resize browser to 375px width (mobile). |
| Expected Result | Layout adapts to single column, sidebar collapses |
| Actual Result | Responsive layout applied, sidebar toggleable via hamburger menu |
| Status | **PASS** |

### TC-38: Tablet Viewport

| Field | Value |
|---|---|
| Test ID | TC-38 |
| Feature | Responsive Design |
| Description | Verify application renders correctly on tablet viewport |
| Precondition | Application is loaded |
| Steps | 1. Resize browser to 768px width (tablet). |
| Expected Result | Layout adapts to tablet dimensions |
| Actual Result | Layout responsive at tablet breakpoint |
| Status | **PASS** |

# 4. TEST SUMMARY

## 4.1 Test Results Overview

| Category | Tests | Passed | Failed |
|---|---|---|---|
| Role Selection & Authentication | 6 | 6 | 0 |
| Access Control | 4 | 4 | 0 |
| Teacher Dashboard | 3 | 3 | 0 |
| Student Performance Prediction | 6 | 6 | 0 |
| Student Roster | 5 | 5 | 0 |
| Student Performance History | 3 | 3 | 0 |
| CSV Upload | 3 | 3 | 0 |
| Model Insights | 2 | 2 | 0 |
| Student Self-Service | 2 | 2 | 0 |
| Theme Support | 2 | 2 | 0 |
| Responsive Design | 2 | 2 | 0 |
| **Total** | **38** | **38** | **0** |

## 4.2 Pass Rate

**38 / 38 test cases passed — 100% pass rate.**

# 5. CONCLUSION

All 38 functional test cases passed successfully. The testing covered all major features of the RiskRadar application including authentication, dashboard statistics, ML-powered prediction, student roster management, history tracking, CSV upload, model insights, student self-service, theme support and responsive design.

Browser-level verification confirmed that the application meets its functional requirements as specified in the SRS.

---

**END OF DOCUMENT**
