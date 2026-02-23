"""
Test script for alert dismiss/resolve functionality
"""

import requests
import json

BASE_URL = "http://localhost:000"

def test_alert_dismiss():
 """Test the alert dismiss and resolve functionality"""

 print(" Testing Alert Dismiss/Resolve Functionality\n")

 # Step : Login as admin
 print("⃣ Logging in as admin...")
 login_response = requests.post(
 f"{BASE_URL}/login",
 json={
 "email": "admin@test.com",
 "password": "admin"
 }
 )

 if login_response.status_code != 00:
 print(f" Login failed: {login_response.text}")
 return

 token = login_response.json()["access_token"]
 headers = {"Authorization": f"Bearer {token}"}
 print(" Login successful\n")

 # Step : Get current alerts
 print("⃣ Fetching current alerts...")
 alerts_response = requests.get(f"{BASE_URL}/alerts", headers=headers)

 if alerts_response.status_code != 00:
 print(f" Failed to fetch alerts: {alerts_response.text}")
 return

 alerts = alerts_response.json()
 print(f" Found {len(alerts)} alerts")

 if len(alerts) == 0:
 print("\n No alerts found. Creating a test alert first...")

 # Create a test alert
 create_response = requests.post(
 f"{BASE_URL}/alerts",
 headers=headers,
 json={
 "region": "TestRegion",
 "alert_message": "Test alert for dismiss functionality",
 "alert_type": "warning"
 }
 )

 if create_response.status_code != 00:
 print(f" Failed to create alert: {create_response.text}")
 return

 print(" Test alert created")

 # Fetch alerts again
 alerts_response = requests.get(f"{BASE_URL}/alerts", headers=headers)
 alerts = alerts_response.json()

 # Display alerts
 print("\n Current Alerts:")
 for alert in alerts[:]: # Show first
 status = alert.get('status', 'active')
 print(f" ID: {alert['id']} | Region: {alert['region']} | Status: {status}")

 # Step : Test dismissing an alert
 if len(alerts) > 0:
 test_alert_id = alerts[0]['id']
 print(f"\n⃣ Testing DISMISS for alert ID {test_alert_id}...")

 dismiss_response = requests.patch(
 f"{BASE_URL}/alerts/{test_alert_id}",
 headers=headers,
 json={
 "status": "dismissed"
 }
 )

 if dismiss_response.status_code == 00:
 result = dismiss_response.json()
 print(f" Alert dismissed successfully")
 print(f" Status: {result['status']}")
 print(f" Resolved at: {result.get('resolved_at', 'N/A')}")
 print(f" Resolved by: {result.get('resolved_by', 'N/A')}")
 else:
 print(f" Failed to dismiss alert: {dismiss_response.text}")

 # Step : Test resolving an alert
 if len(alerts) > :
 test_alert_id = alerts[]['id']
 print(f"\n⃣ Testing RESOLVE for alert ID {test_alert_id}...")

 resolve_response = requests.patch(
 f"{BASE_URL}/alerts/{test_alert_id}",
 headers=headers,
 json={
 "status": "resolved"
 }
 )

 if resolve_response.status_code == 00:
 result = resolve_response.json()
 print(f" Alert resolved successfully")
 print(f" Status: {result['status']}")
 print(f" Resolved at: {result.get('resolved_at', 'N/A')}")
 print(f" Resolved by: {result.get('resolved_by', 'N/A')}")
 else:
 print(f" Failed to resolve alert: {resolve_response.text}")

 # Step : Verify updated alerts
 print("\n⃣ Fetching updated alerts...")
 updated_alerts_response = requests.get(f"{BASE_URL}/alerts", headers=headers)
 updated_alerts = updated_alerts_response.json()

 print(f"\n Alert Status Summary:")
 active = sum( for a in updated_alerts if a.get('status', 'active') == 'active')
 resolved = sum( for a in updated_alerts if a.get('status') == 'resolved')
 dismissed = sum( for a in updated_alerts if a.get('status') == 'dismissed')

 print(f" Active: {active}")
 print(f" Resolved: {resolved}")
 print(f" Dismissed: {dismissed}")

 print("\n All tests completed!")

if __name__ == "__main__":
 try:
 test_alert_dismiss()
 except Exception as e:
 print(f"\n Test failed with error: {e}")
