"""
Helper utilities
"""
import os
from datetime import datetime


def ensure_directories():
    """Ensure required directories exist"""
    directories = ['uploads', 'reports', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def format_timestamp(dt: datetime = None) -> str:
    """Format datetime as string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")
