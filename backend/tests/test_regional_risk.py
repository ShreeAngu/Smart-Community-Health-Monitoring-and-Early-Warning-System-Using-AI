"""
Test script to verify regional risk data
"""
from database import SessionLocal
import models
from datetime import datetime, timedelta

db = SessionLocal()

print("=" * 0)
print("DATABASE VERIFICATION")
print("=" * 0)

# Check reports
seven_days_ago = datetime.now() - timedelta(days=)
recent_reports = db.query(models.Report).filter(
 models.Report.timestamp >= seven_days_ago
).all()

print(f"\n Total reports in last days: {len(recent_reports)}")

# Group by region
region_counts = {}
for report in recent_reports:
 region_counts[report.region] = region_counts.get(report.region, 0) +

print("\n Reports by region:")
for region, count in region_counts.items():
 print(f" {region}: {count} reports")

# Check predictions
recent_predictions = db.query(models.Prediction).filter(
 models.Prediction.timestamp >= seven_days_ago
).all()

print(f"\n Total predictions in last days: {len(recent_predictions)}")

# Group predictions by region
pred_by_region = {}
for pred in recent_predictions:
 if pred.region not in pred_by_region:
 pred_by_region[pred.region] = []
 pred_by_region[pred.region].append(pred.risk_score)

print("\n Predictions by region:")
for region, scores in pred_by_region.items():
 avg_score = sum(scores) / len(scores)
 high_risk = sum( for s in scores if s >= 0)
 print(f" {region}: {len(scores)} predictions, avg={avg_score:.f}, high-risk={high_risk}")

# Check Coimbatore North specifically
coimbatore_reports = [r for r in recent_reports if r.region == 'Coimbatore North']
coimbatore_preds = [p for p in recent_predictions if p.region == 'Coimbatore North']

print("\n" + "=" * 0)
print("COIMBATORE NORTH DETAILS")
print("=" * 0)
print(f"Reports: {len(coimbatore_reports)}")
print(f"Predictions: {len(coimbatore_preds)}")

if coimbatore_preds:
 print("\nRecent predictions:")
 for i, pred in enumerate(coimbatore_preds[-:], ):
 print(f" {i}. Risk={pred.risk_level} ({pred.risk_score:.f}%), "
 f"Disease={pred.predicted_disease}, Time={pred.timestamp}")

db.close()
print("\n" + "=" * 0)
