import requests
import json

# Test the /reports/list endpoint
url = "http://localhost:8000/reports/list?days=7"

# First login to get token
login_response = requests.post(
    "http://localhost:8000/login",
    json={
        "email": "admin@example.com",
        "password": "admin123"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"✅ Login successful, token: {token[:50]}...")
    
    # Now test the reports list endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Reports list endpoint working!")
        print(f"Total reports: {data['total']}")
        print(f"Days: {data['days']}")
        print(f"Filters: {data['filters']}")
        
        if data['reports']:
            print(f"\n📋 First 3 reports:")
            for i, report in enumerate(data['reports'][:3]):
                print(f"\n  Report #{i+1}:")
                print(f"    ID: {report['id']}")
                print(f"    Region: {report['region']}")
                print(f"    Timestamp: {report['timestamp']}")
                print(f"    Disease: {report['predicted_disease']}")
                print(f"    Risk Level: {report['risk_level']}")
                print(f"    Risk Score: {report['risk_score']}")
                print(f"    Symptoms: {len(report['symptoms'])} symptoms")
        else:
            print("\n⚠️ No reports found!")
            print("This might mean:")
            print("  1. No reports in the last 7 days")
            print("  2. Reports exist but predictions are missing")
            print("  3. Timestamp mismatch between reports and predictions")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
