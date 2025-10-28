from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class HealthDataBase(BaseModel):
    data_type: str  # exercise, diet, sleep
    date: date
    
    # Exercise data
    exercise_type: Optional[str] = None
    duration: Optional[float] = None
    calories_burned: Optional[float] = None
    distance: Optional[float] = None
    intensity: Optional[str] = None
    
    # Diet data
    meal_type: Optional[str] = None
    food_name: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    
    # Sleep data
    sleep_duration: Optional[float] = None
    sleep_quality: Optional[str] = None
    bed_time: Optional[datetime] = None
    wake_time: Optional[datetime] = None
    
    notes: Optional[str] = None


class HealthDataCreate(HealthDataBase):
    pass


class HealthDataResponse(HealthDataBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HealthPlanBase(BaseModel):
    plan_type: str  # exercise, diet, general
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






