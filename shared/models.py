from sqlalchemy import Column, Integer, String, Date, Enum, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from shared.database import Base


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTRA_ACTIVE = "extra_active"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(100))
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    height = Column(Float)  # cm
    weight = Column(Float)  # kg
    activity_level = Column(Enum(ActivityLevel))
    health_goal = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExerciseData(Base):
    """运动数据表 - 独立存储运动相关数据，避免 NULL 值"""
    __tablename__ = "exercise_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Exercise specific fields - 所有字段都相关，无 NULL
    exercise_type = Column(String(100), nullable=False)  # Running, Cycling, Swimming, etc.
    duration = Column(Float, nullable=False)  # Duration in minutes
    calories_burned = Column(Float)  # Optional
    distance = Column(Float)  # Distance in km, optional
    intensity = Column(String(50))  # low, moderate, high, optional
    
    # Common fields
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExerciseData(id={self.id}, type={self.exercise_type}, duration={self.duration}min)>"


class DietData(Base):
    """饮食数据表 - 独立存储饮食相关数据，避免 NULL 值"""
    __tablename__ = "diet_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Diet specific fields - 所有字段都相关，无 NULL
    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    food_name = Column(String(200), nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float)  # Optional, grams
    carbs = Column(Float)  # Optional, grams
    fats = Column(Float)  # Optional, grams
    fiber = Column(Float)  # Optional, grams
    
    # Common fields
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DietData(id={self.id}, meal={self.meal_type}, food={self.food_name})>"


class SleepData(Base):
    """睡眠数据表 - 独立存储睡眠相关数据，避免 NULL 值"""
    __tablename__ = "sleep_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Sleep specific fields - 所有字段都相关，无 NULL
    sleep_duration = Column(Float, nullable=False)  # Hours
    sleep_quality = Column(String(50), nullable=False)  # excellent, good, fair, poor
    bed_time = Column(DateTime)  # Optional
    wake_time = Column(DateTime)  # Optional
    
    # Common fields
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SleepData(id={self.id}, duration={self.sleep_duration}h, quality={self.sleep_quality})>"


class HealthPlan(Base):
    __tablename__ = "health_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(String(50), nullable=False)
    
    # Plan content
    title = Column(String(200))
    description = Column(Text)
    duration_days = Column(Integer)
    calories_target = Column(Float)
    exercise_minutes_per_day = Column(Float)
    weekly_exercise_days = Column(Integer)
    
    # AI generated content
    ai_generated_content = Column(Text)
    exercise_plan = Column(Text)
    diet_suggestions = Column(Text)
    
    # Status
    status = Column(String(50), default="active")
    start_date = Column(Date)
    end_date = Column(Date)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

