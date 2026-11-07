"""Services: the 7 actions the website uses (same names as in mock.py)."""
from backend.services.auth_service import check_login
from backend.services.dashboard_service import get_dashboard_stats
from backend.services.history_service import get_history, get_latest
from backend.services.prediction_service import predict
from backend.services.roster_service import validate_roster
from backend.services.student_service import get_students

__all__ = ["check_login", "get_students", "get_dashboard_stats", "predict",
           "get_history", "get_latest", "validate_roster"]
