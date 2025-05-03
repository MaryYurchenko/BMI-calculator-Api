from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    bmi_records = relationship("BMIRecord", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    # Relationships
    user = relationship("User", back_populates="profile")


class BMIRecord(Base):
    __tablename__ = "bmi_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight_kg = Column(Float)
    height_m = Column(Float)
    bmi_value = Column(Float)
    category_id = Column(Integer, ForeignKey("bmi_categories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="bmi_records")
    category = relationship("BMICategory")


class BMICategory(Base):
    __tablename__ = "bmi_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    min_value = Column(Float)
    max_value = Column(Float)
    description = Column(String)
    health_risk = Column(String)
    recommendations = Column(String)
