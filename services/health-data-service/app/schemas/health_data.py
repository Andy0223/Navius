from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime, date


# ==================== Exercise Data Schemas ====================
class ExerciseDataBase(BaseModel):
    exercise_type: str
    duration: float
    calories_burned: Optional[float] = None
    distance: Optional[float] = None
    intensity: Optional[str] = None
    date: date
    notes: Optional[str] = None


class ExerciseDataCreate(ExerciseDataBase):
    pass


class ExerciseDataResponse(ExerciseDataBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Diet Data Schemas ====================
class DietDataBase(BaseModel):
    meal_type: str
    food_name: str
    calories: float
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    date: date
    notes: Optional[str] = None


class DietDataCreate(DietDataBase):
    pass


class DietDataResponse(DietDataBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Sleep Data Schemas ====================
class SleepDataBase(BaseModel):
    sleep_duration: float
    sleep_quality: str
    bed_time: Optional[datetime] = None
    wake_time: Optional[datetime] = None
    date: date
    notes: Optional[str] = None


class SleepDataCreate(SleepDataBase):
    pass


class SleepDataResponse(SleepDataBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Unified Response for mixed queries ====================
class HealthDataResponse(BaseModel):
    """统一响应格式，用于跨类型查询"""
    data_type: str  # "exercise", "diet", or "sleep"
    id: int
    user_id: int
    date: date
    created_at: datetime
    updated_at: datetime
    
    # Exercise fields
    exercise_type: Optional[str] = None
    duration: Optional[float] = None
    calories_burned: Optional[float] = None
    distance: Optional[float] = None
    intensity: Optional[str] = None
    
    # Diet fields
    meal_type: Optional[str] = None
    food_name: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    
    # Sleep fields
    sleep_duration: Optional[float] = None
    sleep_quality: Optional[str] = None
    bed_time: Optional[datetime] = None
    wake_time: Optional[datetime] = None
    
    notes: Optional[str] = None


# ==================== Health Plan Schemas (unchanged) ====================
class HealthPlanBase(BaseModel):
    plan_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    calories_target: Optional[float] = None
    exercise_minutes_per_day: Optional[float] = None
    weekly_exercise_days: Optional[int] = None
    exercise_plan: Optional[str] = None
    diet_suggestions: Optional[str] = None
    status: Optional[str] = "active"
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class HealthPlanCreate(HealthPlanBase):
    pass


class HealthPlanResponse(HealthPlanBase):
    id: int
    user_id: int
    ai_generated_content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HealthPlanUpdate(BaseModel):
    status: Optional[str] = None
    exercise_plan: Optional[str] = None
    diet_suggestions: Optional[str] = None
