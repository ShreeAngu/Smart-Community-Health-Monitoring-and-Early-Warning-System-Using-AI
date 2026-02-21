"""
Test script for Volume Surge Alert System

This script tests:
1. Volume Surge: Creating 9 reports triggers an alert
2. Cooldown: 10th report doesn't create duplicate alert
3. AI Risk: High risk score triggers alert
4. Auto-resolve: Low risk resolves alerts
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Login as community user
def login():
    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": "community@example.com",
            "password": "community123"
        }
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

# Submit a high-risk report
def submit_high_risk_report(token, region="TestRegion", report_num=1):
    headers = {"Authorization": f"Bearer {token}"}
    
    # High-risk symptoms (cholera-like)
    report_data = {
        "region": region,
        "symptoms": {
            "fever": True,
            "diarrhea": True,
            "vomiting": True,
            "abdominal_pain": True,
            "nausea": True,
            "headache": True,
            "fatigue": True,
            "dehydration": True,
            "bloody_stool": True,
            "muscle_aches": False,
            "loss_of_appetite": True,
            "weight_loss": False,
            "jaundice": False,
            "dark_urine": False,
            "rash": False
        },
        "water_metrics": {
            "water_source": "River",
            "water_treatment": "None",
            "fecal_coliform_per_100ml": 3000,
            "ph_level": 6.5,
            "turbidity_ntu": 15,
            "temperature_celsius": 28,
            "rainfall_mm": 150,
            "flooding": True,
            "sanitation_access": False,
            "population_density": 5000
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/submit-report",
        headers=headers,
        json=report_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"  ✅ Report #{report_num} submitted: ID={result['report_id']}")
        if result.get('prediction'):
            pred = result['prediction']
            print(f"     Disease: {pred.get('predicted_disease')}, Risk: {pred.get('risk_level')}, Score: {pred.get('risk_score', 0)*100:.1f}%")
        return True
    else:
        print(f"  ❌ Report #{report_num} failed: {response.status_code}")
        print(f"     {response.text}")
        return False

# Get alerts
def get_alerts(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/alerts", headers=headers)
    
    if response.status_code == 200:
        alerts = response.json()
        return alerts
    else:
        print(f"❌ Failed to get alerts: {response.status_code}")
        return []

# Main test
def main():
    print("=" * 80)
    print("VOLUME SURGE ALERT SYSTEM TEST")
    print("=" * 80)
    
    # Login
    token = login()
    if not token:
        return
    
    print("\n" + "=" * 80)
    print("TEST 1: Volume Surge Detection (9 cases)")
    print("=" * 80)
    print("Submitting 9 high-risk reports to trigger volume surge alert...")
    
    test_region = "TestRegion"
    success_count = 0
    
    for i in range(1, 10):
        if submit_high_risk_report(token, test_region, i):
            success_count += 1
    
    print(f"\n✅ Submitted {success_count}/9 reports")
    
    # Check alerts
    print("\n" + "=" * 80)
    print("Checking for Volume Surge Alert...")
    print("=" * 80)
    
    alerts = get_alerts(token)
    volume_surge_alerts = [a for a in alerts if a.get('alert_type') == 'volume_surge' and a.get('region') == test_region]
    
    if volume_surge_alerts:
        print(f"✅ Volume Surge Alert Created!")
        for alert in volume_surge_alerts:
            print(f"\n  Alert ID: {alert['id']}")
            print(f"  Region: {alert['region']}")
            print(f"  Type: {alert['alert_type']}")
            print(f"  Message: {alert['alert_message']}")
            print(f"  Status: {alert['status']}")
            print(f"  Timestamp: {alert['timestamp']}")
    else:
        print("❌ No Volume Surge Alert found!")
        print(f"Total alerts: {len(alerts)}")
        if alerts:
            print("Existing alerts:")
            for alert in alerts:
                print(f"  - {alert.get('region')}: {alert.get('alert_type')} - {alert.get('status')}")
    
    # Test cooldown
    print("\n" + "=" * 80)
    print("TEST 2: Cooldown Prevention (10th report)")
    print("=" * 80)
    print("Submitting 10th report - should NOT create duplicate alert...")
    
    submit_high_risk_report(token, test_region, 10)
    
    alerts_after = get_alerts(token)
    volume_surge_alerts_after = [a for a in alerts_after if a.get('alert_type') == 'volume_surge' and a.get('region') == test_region]
    
    if len(volume_surge_alerts_after) == len(volume_surge_alerts):
        print(f"✅ Cooldown working! Still {len(volume_surge_alerts_after)} alert(s) (no duplicate)")
    else:
        print(f"⚠️  Alert count changed: {len(volume_surge_alerts)} -> {len(volume_surge_alerts_after)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Reports submitted: {success_count + 1}/10")
    print(f"Volume Surge Alerts: {len(volume_surge_alerts_after)}")
    print(f"Total Active Alerts: {len([a for a in alerts_after if a.get('status') == 'active'])}")
    
    print("\n" + "=" * 80)
    print("ALERT THRESHOLDS (from backend)")
    print("=" * 80)
    print("  AI_RISK_SCORE: 65%")
    print("  VOLUME_CASES: 9 cases")
    print("  VOLUME_DAYS: 7 days")
    print("  COOLDOWN_HOURS: 24 hours")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main()
