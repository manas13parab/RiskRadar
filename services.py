"""
RiskRadar — backend services (kept for older imports).

The real code now lives in backend/services/ (one file per action) and ml/.
This file only re-exports the same 7 functions mock.py has.
"""
from backend.services import (check_login, get_dashboard_stats, get_history,  # noqa: F401
                              get_latest, get_students, predict, validate_roster)
from ml.config import MODEL_PATH  # noqa: F401
from ml.model_store import get_model as _get_model  # noqa: F401
