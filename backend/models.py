from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, Float
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(enum.Enum):
 community = "community"
 admin = "admin"

class User(Base):
 __tablename__ = "users"

 id = Column(Integer, primary_key=True, index=True)
 email = Column(String, unique=True, index=True, nullable=False)
 password_hash = Column(String, nullable=False)
 role = Column(Enum(UserRole), default=UserRole.community, nullable=False)
 created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
 __tablename__ = "reports"

 id = Column(Integer, primary_key=True, index=True)
 user_id = Column(Integer, nullable=False)
 region = Column(String, nullable=False)
 symptoms = Column(Text, nullable=False) # JSON string
 water_metrics = Column(Text, nullable=False) # JSON string
 timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
 __tablename__ = "predictions"

 id = Column(Integer, primary_key=True, index=True)
 region = Column(String, nullable=False)
 risk_score = Column(Float, nullable=False)
 risk_level = Column(String, nullable=False) # Low, Medium, High
 predicted_disease = Column(String, nullable=True)
 confidence = Column(Float, nullable=True)
 timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
 __tablename__ = "alerts"

 id = Column(Integer, primary_key=True, index=True)
 region = Column(String, nullable=False, index=True)
 alert_message = Column(Text, nullable=False)
 alert_type = Column(String, default="warning") # info, warning, critical
 timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
 is_read = Column(Boolean, default=False)
 status = Column(String, default="active") # active, resolved, dismissed
 resolved_at = Column(DateTime(timezone=True), nullable=True)
 resolved_by = Column(Integer, nullable=True) # User ID who resolved/dismissed
 # Keeping is_active for backward compatibility
 is_active = Column(Boolean, default=True)
