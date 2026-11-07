# RiskRadar: Student Performance Prediction and Academic Risk Detection

A Flask web app for teachers. Enter a student's marks and the system predicts the expected
total score, classifies the risk (🟢 Low, 🟡 Moderate, 🔴 High), shows the key factors,
gives advice, and keeps every student's prediction history. Students can log in and see their own result.

## Run it (VS Code, Windows)

1. VS Code: **File → Open Folder** and choose this folder (the one that contains `app.py`).
2. Open the terminal: **Terminal → New Terminal**.
3. Install the libraries (once):
   ```
   python -m pip install -r requirements.txt
   ```
4. Start the app:
   ```
   python app.py
   ```
5. Open **http://127.0.0.1:5000** in the browser. Stop with **Ctrl + C**.

(`python -m flask run` works too. If port 5000 is busy on a Mac, use `python -m flask run --port 5001`.)

### Logins

| Role | ID | Password |
|---|---|---|
| Teacher | `T01` | `admin123` |
| Student | `S1000` | `omar@1000` |

Every student's password is `firstname@number`, for example Maria Brown, `S1001` → `maria@1001`.

## Project structure

### Frontend (what the user sees)
```
templates/   base, role_select, login, teacher_layout, dashboard, predict, students,
             history, upload, insights, student_me, macros      (12 HTML pages)
static/      app.js                                              (1 file)
```

### ML (`ml/`: 16 files)
| File | Job |
|---|---|
| `config.py` | feature names, risk bands, model settings, thresholds |
| `data_loader.py` | read `students.csv` and check its columns |
| `eda.py` | print a summary of the dataset |
| `preprocessing.py` | pick the 7 inputs and the target |
| `splitter.py` | 80/20 train/test split |
| `model_builder.py` | create the Random Forest |
| `trainer.py` | fit the model and print the report |
| `evaluator.py` | MAE, RMSE, R² and feature importance |
| `model_store.py` | save/load `model.pkl` (loaded once, then cached) |
| `pipeline.py` | the whole training run in order |
| `features.py` | form values → numbers for the model |
| `predictor.py` | score + risk + factors + tips |
| `risk.py` | score → High / Moderate / Low |
| `explain.py` | key factors of a prediction |
| `recommendations.py` | rule-based advice |
| `__init__.py` | package marker |

Plus `train_model.py` (run `python train_model.py` to retrain), `model.pkl` and `students.csv`.

### Backend (`backend/`: 24 files)
| Layer | Files |
|---|---|
| Settings and helpers | `config.py`, `security.py`, `utils.py`, `decorators.py`, `__init__.py` |
| Database (`db/`) | `connection.py`, `schema.py`, `seed.py`, `__init__.py` |
| SQL (`repositories/`) | `teacher_repository.py`, `student_repository.py`, `prediction_repository.py`, `__init__.py` |
| Actions (`services/`) | `auth_service.py`, `student_service.py`, `dashboard_service.py`, `prediction_service.py`, `history_service.py`, `roster_service.py`, `__init__.py` |
| Web addresses (`routes/`) | `auth_routes.py`, `teacher_routes.py`, `student_routes.py`, `__init__.py` |

Plus the entry files `app.py`, `services.py`, `database.py`, and `mock.py` (a fake backend), and `riskradar.db`.

## How one prediction flows

```
predict.html form ──► routes/teacher_routes.py ──► ml/features.py (form → numbers)
                                    │
                                    ▼
                     services/prediction_service.py
                        ├─► ml/predictor.py ─► ml/model_store.py (model.pkl)
                        │        ├─► ml/risk.py   ├─► ml/explain.py   └─► ml/recommendations.py
                        └─► repositories/prediction_repository.py ─► riskradar.db
                                    │
                                    ▼
                         predict.html shows score, risk, factors, tips
```

## Tests

```
python -m pip install pytest
python -m pytest
```

100 tests cover the ML modules, the database layer, the services and every page. They run on a
temporary copy of the data, so `riskradar.db` is never touched.

## Notes

* `model.pkl` is about 60 MB. GitHub accepts it (limit 100 MB) but shows a warning.
* If `riskradar.db` is deleted, the first start re-creates it from `students.csv`. This takes several minutes because 5,000 passwords are hashed.
* The Insights page currently shows fixed demo numbers (it says charts appear once the model is connected).
