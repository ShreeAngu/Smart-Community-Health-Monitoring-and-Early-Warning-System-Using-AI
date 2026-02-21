"""
Migration script to add is_active column to alerts table
Run this once to update existing database
"""
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

def migrate_alerts_table():
    """Add is_active column and indexes to alerts table"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Check if is_active column exists
            print("Checking if is_active column exists...")
            result = conn.execute(text("PRAGMA table_info(alerts)"))
            columns = [row[1] for row in result]
            
            if 'is_active' not in columns:
                print("Adding is_active column to alerts table...")
                conn.execute(text("""
                    ALTER TABLE alerts 
                    ADD COLUMN is_active BOOLEAN DEFAULT TRUE
                """))
                conn.commit()
                print("✅ is_active column added")
            else:
                print("✅ is_active column already exists")
            
            # Create index on region if it doesn't exist
            print("Creating index on region...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_alerts_region ON alerts(region)
            """))
            conn.commit()
            print("✅ Index on region created")
            
            # Create index on timestamp if it doesn't exist
            print("Creating index on timestamp...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_alerts_timestamp ON alerts(timestamp)
            """))
            conn.commit()
            print("✅ Index on timestamp created")
            
            # Set all existing alerts to active
            print("Setting existing alerts to active...")
            result = conn.execute(text("""
                UPDATE alerts SET is_active = TRUE WHERE is_active IS NULL
            """))
            conn.commit()
            print(f"✅ Updated {result.rowcount} existing alerts")
            
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate_alerts_table()
