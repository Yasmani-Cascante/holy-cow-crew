import pytest
from typing import Dict, Any, List
from datetime import datetime
from src.reporting.report_generator import ReportGenerator

def test_report_generation():
    generator = ReportGenerator()
    assert generator is not None