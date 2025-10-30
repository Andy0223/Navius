from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from shared.database import get_db
from shared.security import get_user_id_from_token
from shared.models import User
from app.services.ai_service import AIHealthPlanService

router = APIRouter()

ai_service = AIHealthPlanService()


@router.post("/plan/generate")
async def generate_health_plan(
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Generate personalized health plan using AI"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    plan_data = ai_service.generate_personalized_plan(db, user)
    return plan_data


@router.get("/analyze")
async def analyze_health_data(
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Analyze user's health data"""
    analysis = ai_service.analyze_health_data(db, user_id)
    
    # Generate recommendations
    recommendations = []
    
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
        "user_id": user_id,
        "analysis": analysis,
        "recommendations": recommendations
    }

