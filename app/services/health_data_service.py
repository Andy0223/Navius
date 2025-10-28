from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, datetime
from fastapi import HTTPException, status

from app.models.health_data import HealthData, HealthPlan
from app.schemas.health_data import HealthDataCreate, HealthPlanCreate, HealthPlanUpdate


class HealthDataService:
    @staticmethod
    def create_health_data(db: Session, user_id: int, health_data: HealthDataCreate) -> HealthData:
        """Create health data"""
        db_health_data = HealthData(
            user_id=user_id,
            data_type=health_data.data_type,
            date=health_data.date,
            exercise_type=health_data.exercise_type,
            duration=health_data.duration,
            calories_burned=health_data.calories_burned,
            distance=health_data.distance,
            intensity=health_data.intensity,
            meal_type=health_data.meal_type,
            food_name=health_data.food_name,
            calories=health_data.calories,
            protein=health_data.protein,
            carbs=health_data.carbs,
            fats=health_data.fats,
            fiber=health_data.fiber,
            sleep_duration=health_data.sleep_duration,
            sleep_quality=health_data.sleep_quality,
            bed_time=health_data.bed_time,
            wake_time=health_data.wake_time,
            notes=health_data.notes
        )
        
        db.add(db_health_data)
        db.commit()
        db.refresh(db_health_data)
        return db_health_data
    
    @staticmethod
    def get_health_data_by_user(
        db: Session,
        user_id: int,
        data_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[HealthData]:
        """Get user's health data"""
        query = db.query(HealthData).filter(HealthData.user_id == user_id)
        
        if data_type:
            query = query.filter(HealthData.data_type == data_type)
        
        if start_date:
            query = query.filter(HealthData.date >= start_date)
        
        if end_date:
            query = query.filter(HealthData.date <= end_date)
        
        return query.order_by(HealthData.date.desc()).all()
    
    @staticmethod
    def get_health_data_statistics(
        db: Session,
        user_id: int,
        days: int = 7
    ) -> dict:
        """Get health data statistics"""
        end_date = date.today()
        start_date = date(end_date.year, end_date.month, end_date.day - days)
        
        health_data = db.query(HealthData).filter(
            HealthData.user_id == user_id,
            HealthData.date >= start_date,
            HealthData.date <= end_date
        ).all()
        
        stats = {
            "total_exercise_minutes": 0,
            "total_calories_burned": 0,
            "total_sleep_hours": 0,
            "total_calories_consumed": 0
        }
        
        for data in health_data:
            if data.data_type == "exercise":
                stats["total_exercise_minutes"] += data.duration or 0
                stats["total_calories_burned"] += data.calories_burned or 0
            elif data.data_type == "sleep":
                stats["total_sleep_hours"] += data.sleep_duration or 0
            elif data.data_type == "diet":
                stats["total_calories_consumed"] += data.calories or 0
        
        return stats
    
    @staticmethod
    def create_health_plan(db: Session, user_id: int, plan_data: HealthPlanCreate) -> HealthPlan:
        """Create health plan"""
        db_plan = HealthPlan(
            user_id=user_id,
            plan_type=plan_data.plan_type,
            title=plan_data.title,
            description=plan_data.description,
            duration_days=plan_data.duration_days,
            calories_target=plan_data.calories_target,
            exercise_minutes_per_day=plan_data.exercise_minutes_per_day,
            weekly_exercise_days=plan_data.weekly_exercise_days,
            exercise_plan=plan_data.exercise_plan,
            diet_suggestions=plan_data.diet_suggestions,
            status=plan_data.status or "active",
            start_date=plan_data.start_date,
            end_date=plan_data.end_date
        )
        
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan
    
    @staticmethod
    def get_user_health_plans(
        db: Session,
        user_id: int,
        status_filter: Optional[str] = None
    ) -> List[HealthPlan]:
        """Get user's health plans"""
        query = db.query(HealthPlan).filter(HealthPlan.user_id == user_id)
        
        if status_filter:
            query = query.filter(HealthPlan.status == status_filter)
        
        return query.order_by(HealthPlan.created_at.desc()).all()
    
    @staticmethod
    def update_health_plan(
        db: Session,
        plan_id: int,
        user_id: int,
        plan_data: HealthPlanUpdate
    ) -> HealthPlan:
        """Update health plan"""
        plan = db.query(HealthPlan).filter(
            HealthPlan.id == plan_id,
            HealthPlan.user_id == user_id
        ).first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Health plan not found"
            )
        
        update_data = plan_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        plan.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(plan)
        return plan






