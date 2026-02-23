"""
Migration script to add status, resolved_at, and resolved_by columns to alerts table
Run this script to update existing databases with the new alert dismissal functionality
"""

import sqlite
from datetime import datetime

def migrate_alerts_table():
 """Add new columns to alerts table for dismissal functionality"""

 conn = sqlite.connect('health_db.db')
 cursor = conn.cursor()

 print(" Starting alerts table migration...")

 try:
 # Check if columns already exist
 cursor.execute("PRAGMA table_info(alerts)")
 columns = [column[] for column in cursor.fetchall()]

 # Add status column if it doesn't exist
 if 'status' not in columns:
 print(" Adding 'status' column...")
 cursor.execute("""
 ALTER TABLE alerts
 ADD COLUMN status TEXT DEFAULT 'active'
 """)
 # Set existing alerts to 'active' status
 cursor.execute("UPDATE alerts SET status = 'active' WHERE status IS NULL")
 print(" 'status' column added")
 else:
 print(" 'status' column already exists")

 # Add resolved_at column if it doesn't exist
 if 'resolved_at' not in columns:
 print(" Adding 'resolved_at' column...")
 cursor.execute("""
 ALTER TABLE alerts
 ADD COLUMN resolved_at TIMESTAMP
 """)
 print(" 'resolved_at' column added")
 else:
 print(" 'resolved_at' column already exists")

 # Add resolved_by column if it doesn't exist
 if 'resolved_by' not in columns:
 print(" Adding 'resolved_by' column...")
 cursor.execute("""
 ALTER TABLE alerts
 ADD COLUMN resolved_by INTEGER
 """)
 print(" 'resolved_by' column added")
 else:
 print(" 'resolved_by' column already exists")

 conn.commit()
 print(" Migration completed successfully!")

 # Show current alerts status
 cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'active'")
 active_count = cursor.fetchone()[0]

 cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'resolved'")
 resolved_count = cursor.fetchone()[0]

 cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'dismissed'")
 dismissed_count = cursor.fetchone()[0]

 print(f"\n Current Alert Status:")
 print(f" Active: {active_count}")
 print(f" Resolved: {resolved_count}")
 print(f" Dismissed: {dismissed_count}")

 except Exception as e:
 conn.rollback()
 print(f" Migration failed: {e}")
 raise
 finally:
 conn.close()

if __name__ == "__main__":
 migrate_alerts_table()
