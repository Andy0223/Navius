from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.health_data import (
    HealthDataCreate, HealthDataResponse,
    HealthPlanCreate, HealthPlanResponse, HealthPlanUpdate
)
from app.services.health_data_service import HealthDataService
from app.services.ai_service import AIHealthPlanService
from app.models.user import User

router = APIRouter(prefix="/health", tags=["health"])

ai_service = AIHealthPlanService()


# Health Data Endpoints
@router.post("/data", response_model=HealthDataResponse, status_code=status.HTTP_201_CREATED)
async def create_health_data(
    health_data: HealthDataCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit health data"""
    health_record = HealthDataService.create_health_data(db, current_user.id, health_data)
    return health_record


@router.get("/data", response_model=List[HealthDataResponse])
async def get_health_data(
    data_type: Optional[str] = Query(None, description="Data type: exercise, diet, sleep"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health data"""
    health_data = HealthDataService.get_health_data_by_user(
        db, current_user.id, data_type, start_date, end_date
    )
    return health_data


@router.get("/statistics")
async def get_health_statistics(
    days: int = Query(7, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health data statistics"""
    stats = HealthDataService.get_health_data_statistics(db, current_user.id, days)
    return stats


# Health Plan Endpoints
@router.post("/plan", response_model=HealthPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_health_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized health plan"""
    # Use AI service to generate personalized plan
    plan_data = ai_service.generate_personalized_plan(db, current_user)
    
    # Create plan
    created_plan = HealthDataService.create_health_plan(
        db, current_user.id, HealthPlanCreate(**plan_data)
    )
    
    return created_plan


@router.get("/plan", response_model=List[HealthPlanResponse])
async def get_health_plans(
    status_filter: Optional[str] = Query(None, description="Status filter: active, completed, paused"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user health plans"""
    plans = HealthDataService.get_user_health_plans(db, current_user.id, status_filter)
    return plans


@router.get("/plan/{plan_id}", response_model=HealthPlanResponse)
async def get_health_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific health plan"""
    plans = HealthDataService.get_user_health_plans(db, current_user.id)
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update health plan"""
    updated_plan = HealthDataService.update_health_plan(
        db, plan_id, current_user.id, plan_data
    )
    return updated_plan


@router.get("/recommendations")
async def get_ai_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI recommendations"""
    # Analyze user health data
    analysis = ai_service.analyze_health_data(db, current_user.id)
    
    # Generate recommendations
    recommendations = []
    
    # Generate recommendations based on analysis
    if analysis["exercise_frequency"] < 3:
        recommendations.append({
            "type": "exercise",
            "priority": "high",
            "message": "Recommend increasing exercise frequency to at least 3 times per week"
        })
    
    if analysis["average_sleep_hours"] < 7:
        recommendations.append({
            "type": "sleep",
            "priority": "high",
            "message": "Insufficient sleep time, recommend 7-9 hours daily for health"
        })
    
    if analysis["average_sleep_hours"] >= 7:
        recommendations.append({
            "type": "sleep",
            "priority": "low",
            "message": "Adequate sleep, keep it up"
        })
    
    return {
        "user_id": current_user.id,
        "analysis": analysis,
        "recommendations": recommendations
    }

