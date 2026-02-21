"""
Seed script to create EXTREME high-risk reports for Coimbatore North
This will create reports with maximum risk factors to trigger HIGH regional risk
"""
import sys
import json
from datetime import datetime
from database import SessionLocal
import models
import joblib
import pandas as pd
import numpy as np

# Load ML models
print("=" * 80)
print("LOADING ML MODELS...")
print("=" * 80)

try:
    mode