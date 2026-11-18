# RISKRADAR
# PERFORMANCE TESTING REPORT

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

This document describes the performance testing performed on RiskRadar. It evaluates the application's response times, throughput and behaviour under various load conditions.

## 1.2 Scope

Performance testing covers the following areas:

- Sequential HTTP request testing (single-user simulation).
- Concurrent request testing (multi-user simulation).
- Route-specific response time measurement.
- ML prediction endpoint performance.
- Database query performance with 5,000 student records.
- Page load and rendering performance.

## 1.3 Testing Approach

Performance testing was conducted using Python scripts with the `requests` and `concurrent.futures` libraries to send HTTP requests to the Flask development server.

Response times, status codes and throughput metrics were recorded and analysed.

# 2. TEST ENVIRONMENT

| Component | Details |
|---|---|
| Operating System | macOS |
| Python Version | 3.12+ |
| Server | Flask Development Server |
| Server Address | http://127.0.0.1:5002 |
| Database | SQLite (riskradar.db) |
| Dataset Size | 5,000 students |
| ML Model | model.pkl (RandomForest, 200 trees) |
| Model File Size | ~60 MB |
| Testing Tool | Python requests + concurrent.futures |

# 3. SEQUENTIAL REQUEST TESTING

Sequential tests simulate a single user navigating through the application.

## 3.1 Test Configuration

- Requests sent sequentially (one after another).
- Each request timed individually.
- Authenticated session maintained using Flask session cookies.
- 5 iterations per endpoint for averaging.

## 3.2 Results

### Authentication Endpoints

| Endpoint | Method | Avg Response Time (ms) | Status |
|---|---|---|---|
| `GET /` | GET | ~15 | 200 OK |
| `GET /login/teacher` | GET | ~12 | 200 OK |
| `POST /login/teacher` (valid) | POST | ~85 | 302 Redirect |
| `POST /login/teacher` (invalid) | POST | ~80 | 200 OK |
| `GET /login/student` | GET | ~12 | 200 OK |
| `POST /login/student` (valid) | POST | ~82 | 302 Redirect |
| `GET /logout` | GET | ~8 | 302 Redirect |

### Teacher Dashboard and Pages

| Endpoint | Method | Avg Response Time (ms) | Status |
|---|---|---|---|
| `GET /teacher` | GET | ~250 | 200 OK |
| `GET /students` | GET | ~320 | 200 OK |
| `GET /predict` | GET | ~45 | 200 OK |
| `GET /insights` | GET | ~35 | 200 OK |
| `GET /upload` | GET | ~20 | 200 OK |
| `GET /history/STU0001` | GET | ~40 | 200 OK |

### Prediction Endpoint

| Endpoint | Method | Avg Response Time (ms) | Status |
|---|---|---|---|
| `POST /predict` (first call) | POST | ~1200 | 200 OK |
| `POST /predict` (subsequent) | POST | ~180 | 200 OK |

The first prediction call includes model loading time (~60 MB model.pkl loaded from disk). Subsequent calls use the cached model, reducing response time significantly.

### Student Endpoints

| Endpoint | Method | Avg Response Time (ms) | Status |
|---|---|---|---|
| `GET /me` | GET | ~55 | 200 OK |

## 3.3 Analysis

- Static page renders (login, upload, insights) respond in under 50 ms.
- Dashboard and student roster take longer (~250–320 ms) due to aggregate queries over 5,000 records.
- First prediction call is slow (~1.2 s) due to model loading; subsequent predictions are fast (~180 ms) due to caching.
- Authentication operations (login with password hash verification) take ~80–85 ms.
- All endpoints return appropriate HTTP status codes.

# 4. CONCURRENT REQUEST TESTING

Concurrent tests simulate multiple users accessing the application simultaneously.

## 4.1 Test Configuration

- ThreadPoolExecutor used for concurrent requests.
- Shared authenticated session.
- 5, 10, 20 and 50 concurrent requests per test.
- Each test repeated 3 times for consistency.

## 4.2 Results

### Dashboard Endpoint (`GET /teacher`)

| Concurrent Users | Avg Response Time (ms) | Max Response Time (ms) | Success Rate |
|---|---|---|---|
| 5 | ~280 | ~350 | 100% |
| 10 | ~320 | ~480 | 100% |
| 20 | ~450 | ~720 | 100% |
| 50 | ~680 | ~1100 | 100% |

### Student Roster (`GET /students`)

| Concurrent Users | Avg Response Time (ms) | Max Response Time (ms) | Success Rate |
|---|---|---|---|
| 5 | ~350 | ~420 | 100% |
| 10 | ~420 | ~580 | 100% |
| 20 | ~550 | ~850 | 100% |
| 50 | ~780 | ~1300 | 100% |

### Prediction Endpoint (`POST /predict`)

| Concurrent Users | Avg Response Time (ms) | Max Response Time (ms) | Success Rate |
|---|---|---|---|
| 5 | ~200 | ~280 | 100% |
| 10 | ~250 | ~380 | 100% |
| 20 | ~380 | ~600 | 100% |
| 50 | ~550 | ~950 | 100% |

(Note: Model was pre-loaded before concurrent tests to exclude first-load overhead.)

## 4.3 Analysis

- All endpoints maintained 100% success rate up to 50 concurrent requests.
- Response times increased approximately linearly with concurrent user count.
- SQLite WAL mode enabled concurrent reads without locking issues.
- The prediction endpoint performed well under concurrent load with the cached model.
- Maximum response times remained under 1.5 seconds even at 50 concurrent users.

# 5. DATABASE QUERY PERFORMANCE

## 5.1 Test Configuration

Query execution times measured using Python's time module around database calls.

## 5.2 Results

| Query | Records | Avg Execution Time (ms) |
|---|---|---|
| Authenticate teacher | 1 | ~2 |
| Authenticate student | 1 | ~3 |
| Get all students with latest prediction (JOIN) | 5,000 | ~120 |
| Get dashboard stats (COUNT + GROUP BY) | 5,000+ | ~85 |
| Get recent 5 predictions (ORDER BY + LIMIT) | 5 | ~8 |
| Insert prediction | 1 | ~5 |
| Get student history | Variable | ~6 |
| Get latest prediction | 1 | ~4 |

## 5.3 Analysis

- Simple lookups (authentication, single record) execute in under 5 ms.
- The most expensive query is the student roster JOIN with latest prediction subquery (~120 ms for 5,000 students).
- Dashboard statistics aggregation over 5,000+ predictions takes ~85 ms.
- Insert operations are fast (~5 ms).
- SQLite performs adequately for the application's data volume.

# 6. ML MODEL PERFORMANCE

## 6.1 Model Loading

| Metric | Value |
|---|---|
| Model File Size | ~60 MB |
| Cold Load Time | ~1,000 ms |
| Cached Access Time | < 1 ms |
| Caching Strategy | Global singleton in services.py |

## 6.2 Prediction Inference

| Metric | Value |
|---|---|
| Single Prediction Time | ~8 ms |
| Feature Array Construction | ~1 ms |
| Risk Classification | < 1 ms |
| Factor Calculation | ~2 ms |
| Total Predict Function (cached model) | ~15 ms |
| Total Predict Function + DB Save | ~20 ms |

## 6.3 Model Training Performance

| Metric | Value |
|---|---|
| Dataset Size | 5,000 rows × 23 columns |
| Feature Selection | 7 features |
| Training Time | ~3 seconds |
| n_estimators | 200 |
| max_depth | 15 |
| n_jobs | -1 (all CPU cores) |

## 6.4 Analysis

- Model loading is the primary bottleneck for the first prediction.
- The global singleton caching strategy eliminates repeated load overhead.
- Prediction inference itself is very fast (~8 ms).
- The RandomForest with 200 trees and max depth 15 provides a good balance between accuracy and speed.

# 7. PAGE RENDERING PERFORMANCE

## 7.1 Test Configuration

Page load times measured in the browser using Chrome DevTools Network panel (DOMContentLoaded and Load events).

## 7.2 Results

| Page | DOMContentLoaded (ms) | Full Load (ms) | Notes |
|---|---|---|---|
| Role Selection | ~180 | ~450 | CDN resources loaded |
| Login | ~160 | ~400 | Minimal content |
| Dashboard | ~350 | ~700 | Chart.js donut chart rendered |
| Predict (form) | ~200 | ~500 | Student dropdown loaded |
| Predict (results) | ~250 | ~550 | Results with factors |
| Students | ~500 | ~900 | 5,000 rows rendered |
| History | ~280 | ~600 | Line chart rendered |
| Upload | ~180 | ~450 | Drag-and-drop zone |
| Insights | ~300 | ~650 | Feature importance chart |
| Student Me | ~200 | ~500 | Progress bar rendered |

## 7.3 Analysis

- CDN resources (Tailwind CSS, Chart.js, Lucide Icons, Inter font) contribute to initial load time.
- The Students page has the longest render time due to 5,000 table rows in the DOM.
- Chart.js rendering adds ~100–150 ms to pages with charts.
- All pages load fully in under 1 second, which is acceptable for the application's purpose.
- Subsequent page loads benefit from browser caching of CDN resources.

# 8. PERFORMANCE SUMMARY

## 8.1 Key Metrics

| Metric | Value |
|---|---|
| Fastest endpoint | GET /logout (~8 ms) |
| Slowest endpoint (cold) | POST /predict first call (~1,200 ms) |
| Slowest endpoint (warm) | GET /students (~320 ms) |
| Max concurrent users tested | 50 |
| Concurrent success rate | 100% |
| Database query range | 2–120 ms |
| ML prediction inference | ~8 ms |
| Heaviest page render | Students (~900 ms full load) |

## 8.2 Bottlenecks Identified

| Bottleneck | Cause | Mitigation |
|---|---|---|
| First prediction cold start | 60 MB model loading from disk | Global singleton caching (implemented) |
| Student roster query | JOIN over 5,000 records | Acceptable for current data volume |
| Students page render | 5,000 DOM rows | Client-side search/filter reduces visible rows |
| CDN resource loading | External network requests | Browser caching after first load |

# 9. CONCLUSION

Performance testing confirms that RiskRadar operates within acceptable response times for its intended use case of university-level student performance monitoring.

Key findings:

- All endpoints maintain 100% success rate under concurrent load (up to 50 users).
- The model caching strategy effectively eliminates the cold-start bottleneck after the first prediction.
- Database queries over 5,000 student records execute within acceptable time frames using SQLite.
- Page rendering times are under 1 second for all pages.
- The system is suitable for single-institution deployment with the current data volume.

---

**END OF DOCUMENT**
