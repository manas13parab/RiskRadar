"""Small helpers shared by the backend."""
from datetime import datetime, timedelta

from backend import config


def today_str():
    return datetime.now().strftime(config.DATE_FORMAT)


def days_ago_str(days):
    return (datetime.now() - timedelta(days=days)).strftime(config.DATE_FORMAT)
