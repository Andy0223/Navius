from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from shared.database import get_db
from shared.security import get_user_id_from_token
from shared.models import ExerciseData, DietData, SleepData, HealthPlan
from app.schemas.health_data import (
    ExerciseDataCreate, DietDataCreate, SleepDataCreate,
    ExerciseDataResponse, DietDataResponse, SleepDataResponse,
    HealthDataResponse, HealthPlanCreate, HealthPlanResponse, HealthPlanUpdate
)
from app.services.health_data_service import HealthDataService

router = APIRouter()


# ==================== Exercise Data Endpoints ====================
@router.post("/exercise", response_model=ExerciseDataResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise_data(
    exercise_data: ExerciseDataCreate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Submit exercise data"""
    return HealthDataService.create_exercise_data(db, user_id, exercise_data)


@router.get("/exercise", response_model=List[ExerciseDataResponse])
async def get_exercise_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get exercise data"""
    return HealthDataService.get_exercise_data(db, user_id, start_date, end_date)


# ==================== Diet Data Endpoints ====================
@router.post("/diet", response_model=DietDataResponse, status_code=status.HTTP_201_CREATED)
async def create_diet_data(
    diet_data: DietDataCreate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Submit diet data"""
    return HealthDataService.create_diet_data(db, user_id, diet_data)


@router.get("/diet", response_model=List[DietDataResponse])
async def get_diet_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get diet data"""
    return HealthDataService.get_diet_data(db, user_id, start_date, end_date)


# ==================== Sleep Data Endpoints ====================
@router.post("/sleep", response_model=SleepDataResponse, status_code=status.HTTP_201_CREATED)
async def create_sleep_data(
    sleep_data: SleepDataCreate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Submit sleep data"""
    return HealthDataService.create_sleep_data(db, user_id, sleep_data)


@router.get("/sleep", response_model=List[SleepDataResponse])
async def get_sleep_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get sleep data"""
    return HealthDataService.get_sleep_data(db, user_id, start_date, end_date)


# ==================== Unified Endpoints (Backward Compatibility) ====================
@router.post("/data", response_model=HealthDataResponse, status_code=status.HTTP_201_CREATED)
async def create_health_data(
    health_data: dict,  # Accept flexible dict for backward compatibility
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Submit health data (unified endpoint - automatically routes to correct type)"""
    data_type = health_data.get("data_type")
    
    if data_type == "exercise":
        exercise_data = ExerciseDataCreate(**{k: v for k, v in health_data.items() if k != "data_type"})
        result = HealthDataService.create_exercise_data(db, user_id, exercise_data)
        return HealthDataResponse(
            data_type="exercise",
            id=result.id,
            user_id=result.user_id,
            date=result.date,
            created_at=result.created_at,
            updated_at=result.updated_at,
            exercise_type=result.exercise_type,
            duration=result.duration,
            calories_burned=result.calories_burned,
            distance=result.distance,
            intensity=result.intensity,
            notes=result.notes
        )
    elif data_type == "diet":
        diet_data = DietDataCreate(**{k: v for k, v in health_data.items() if k != "data_type"})
        result = HealthDataService.create_diet_data(db, user_id, diet_data)
        return HealthDataResponse(
            data_type="diet",
            id=result.id,
            user_id=result.user_id,
            date=result.date,
            created_at=result.created_at,
            updated_at=result.updated_at,
            meal_type=result.meal_type,
            food_name=result.food_name,
            calories=result.calories,
            protein=result.protein,
            carbs=result.carbs,
            fats=result.fats,
            fiber=result.fiber,
            notes=result.notes
        )
    elif data_type == "sleep":
        sleep_data = SleepDataCreate(**{k: v for k, v in health_data.items() if k != "data_type"})
        result = HealthDataService.create_sleep_data(db, user_id, sleep_data)
        return HealthDataResponse(
            data_type="sleep",
            id=result.id,
            user_id=result.user_id,
            date=result.date,
            created_at=result.created_at,
            updated_at=result.updated_at,
            sleep_duration=result.sleep_duration,
            sleep_quality=result.sleep_quality,
            bed_time=result.bed_time,
            wake_time=result.wake_time,
            notes=result.notes
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data_type: {data_type}. Must be 'exercise', 'diet', or 'sleep'"
        )


@router.get("/data", response_model=List[HealthDataResponse])
async def get_health_data(
    data_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get health data (unified endpoint - supports all types)"""
    return HealthDataService.get_all_health_data(db, user_id, data_type, start_date, end_date)


# ==================== Statistics Endpoint ====================
@router.get("/statistics")
async def get_health_statistics(
    days: int = Query(7, ge=1, le=365),
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get health data statistics"""
    stats = HealthDataService.get_health_data_statistics(db, user_id, days)
    return stats


# ==================== Health Plan Endpoints (unchanged) ====================
@router.post("/plan", response_model=HealthPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_health_plan(
    plan_data: HealthPlanCreate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Create health plan"""
    created_plan = HealthDataService.create_health_plan(db, user_id, plan_data)
    return created_plan


@router.get("/plan", response_model=List[HealthPlanResponse])
async def get_health_plans(
    status_filter: Optional[str] = Query(None),
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get user health plans"""
    plans = HealthDataService.get_user_health_plans(db, user_id, status_filter)
    return plans


@router.get("/plan/{plan_id}", response_model=HealthPlanResponse)
async def get_health_plan(
    plan_id: int,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Get specific health plan"""
    plans = HealthDataService.get_user_health_plans(db, user_id)
    plan = next((p for p in plans if p.id == plan_id), None)
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health plan not found"
        )
    
    return plan


@router.put("/plan/{plan_id}", response_model=HealthPlanResponse)
async def update_health_plan(
    plan_id: int,
    plan_data: HealthPlanUpdate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Update health plan"""
    updated_plan = HealthDataService.update_health_plan(
        db, plan_id, user_id, plan_data
    )
    return updated_plan

