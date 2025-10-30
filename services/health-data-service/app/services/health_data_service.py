from typing import List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from fastapi import HTTPException, status
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from shared.models import ExerciseData, DietData, SleepData, HealthPlan
from app.schemas.health_data import (
    ExerciseDataCreate, DietDataCreate, SleepDataCreate,
    ExerciseDataResponse, DietDataResponse, SleepDataResponse,
    HealthDataResponse, HealthPlanCreate, HealthPlanUpdate
)


class HealthDataService:
    @staticmethod
    def create_exercise_data(db: Session, user_id: int, exercise_data: ExerciseDataCreate) -> ExerciseData:
        """Create exercise data"""
        db_exercise = ExerciseData(
            user_id=user_id,
            exercise_type=exercise_data.exercise_type,
            duration=exercise_data.duration,
            calories_burned=exercise_data.calories_burned,
            distance=exercise_data.distance,
            intensity=exercise_data.intensity,
            date=exercise_data.date,
            notes=exercise_data.notes
        )
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        return db_exercise
    
    @staticmethod
    def create_diet_data(db: Session, user_id: int, diet_data: DietDataCreate) -> DietData:
        """Create diet data"""
        db_diet = DietData(
            user_id=user_id,
            meal_type=diet_data.meal_type,
            food_name=diet_data.food_name,
            calories=diet_data.calories,
            protein=diet_data.protein,
            carbs=diet_data.carbs,
            fats=diet_data.fats,
            fiber=diet_data.fiber,
            date=diet_data.date,
            notes=diet_data.notes
        )
        db.add(db_diet)
        db.commit()
        db.refresh(db_diet)
        return db_diet
    
    @staticmethod
    def create_sleep_data(db: Session, user_id: int, sleep_data: SleepDataCreate) -> SleepData:
        """Create sleep data"""
        db_sleep = SleepData(
            user_id=user_id,
            sleep_duration=sleep_data.sleep_duration,
            sleep_quality=sleep_data.sleep_quality,
            bed_time=sleep_data.bed_time,
            wake_time=sleep_data.wake_time,
            date=sleep_data.date,
            notes=sleep_data.notes
        )
        db.add(db_sleep)
        db.commit()
        db.refresh(db_sleep)
        return db_sleep
    
    @staticmethod
    def get_exercise_data(
        db: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[ExerciseData]:
        """Get user's exercise data"""
        query = db.query(ExerciseData).filter(ExerciseData.user_id == user_id)
        if start_date:
            query = query.filter(ExerciseData.date >= start_date)
        if end_date:
            query = query.filter(ExerciseData.date <= end_date)
        return query.order_by(ExerciseData.date.desc()).all()
    
    @staticmethod
    def get_diet_data(
        db: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[DietData]:
        """Get user's diet data"""
        query = db.query(DietData).filter(DietData.user_id == user_id)
        if start_date:
            query = query.filter(DietData.date >= start_date)
        if end_date:
            query = query.filter(DietData.date <= end_date)
        return query.order_by(DietData.date.desc()).all()
    
    @staticmethod
    def get_sleep_data(
        db: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[SleepData]:
        """Get user's sleep data"""
        query = db.query(SleepData).filter(SleepData.user_id == user_id)
        if start_date:
            query = query.filter(SleepData.date >= start_date)
        if end_date:
            query = query.filter(SleepData.date <= end_date)
        return query.order_by(SleepData.date.desc()).all()
    
    @staticmethod
    def get_all_health_data(
        db: Session,
        user_id: int,
        data_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[HealthDataResponse]:
        """Get all health data (exercise, diet, sleep) - unified format"""
        results = []
        
        # Get exercise data
        if data_type is None or data_type == "exercise":
            exercise_data = HealthDataService.get_exercise_data(db, user_id, start_date, end_date)
            for ex in exercise_data:
                results.append(HealthDataResponse(
                    data_type="exercise",
                    id=ex.id,
                    user_id=ex.user_id,
                    date=ex.date,
                    created_at=ex.created_at,
                    updated_at=ex.updated_at,
                    exercise_type=ex.exercise_type,
                    duration=ex.duration,
                    calories_burned=ex.calories_burned,
                    distance=ex.distance,
                    intensity=ex.intensity,
                    notes=ex.notes
                ))
        
        # Get diet data
        if data_type is None or data_type == "diet":
            diet_data = HealthDataService.get_diet_data(db, user_id, start_date, end_date)
            for diet in diet_data:
                results.append(HealthDataResponse(
                    data_type="diet",
                    id=diet.id,
                    user_id=diet.user_id,
                    date=diet.date,
                    created_at=diet.created_at,
                    updated_at=diet.updated_at,
                    meal_type=diet.meal_type,
                    food_name=diet.food_name,
                    calories=diet.calories,
                    protein=diet.protein,
                    carbs=diet.carbs,
                    fats=diet.fats,
                    fiber=diet.fiber,
                    notes=diet.notes
                ))
        
        # Get sleep data
        if data_type is None or data_type == "sleep":
            sleep_data = HealthDataService.get_sleep_data(db, user_id, start_date, end_date)
            for sleep in sleep_data:
                results.append(HealthDataResponse(
                    data_type="sleep",
                    id=sleep.id,
                    user_id=sleep.user_id,
                    date=sleep.date,
                    created_at=sleep.created_at,
                    updated_at=sleep.updated_at,
                    sleep_duration=sleep.sleep_duration,
                    sleep_quality=sleep.sleep_quality,
                    bed_time=sleep.bed_time,
                    wake_time=sleep.wake_time,
                    notes=sleep.notes
                ))
        
        # Sort by date descending
        results.sort(key=lambda x: x.date, reverse=True)
        return results
    
    @staticmethod
    def get_health_data_statistics(
        db: Session,
        user_id: int,
        days: int = 7
    ) -> dict:
        """Get health data statistics"""
        from datetime import timedelta, datetime, timezone
        
        # Use UTC to ensure consistent date calculation across timezones
        end_date = datetime.now(timezone.utc).date() + timedelta(days=1)
        start_date = end_date - timedelta(days=days+1)
        
        # Get exercise statistics
        exercise_stats = db.query(
            func.sum(ExerciseData.duration).label('total_duration'),
            func.sum(ExerciseData.calories_burned).label('total_calories_burned')
        ).filter(
            ExerciseData.user_id == user_id,
            ExerciseData.date >= start_date,
            ExerciseData.date <= end_date
        ).first()
        
        # Get sleep statistics
        sleep_stats = db.query(
            func.sum(SleepData.sleep_duration).label('total_sleep_hours')
        ).filter(
            SleepData.user_id == user_id,
            SleepData.date >= start_date,
            SleepData.date <= end_date
        ).first()
        
        # Get diet statistics
        diet_stats = db.query(
            func.sum(DietData.calories).label('total_calories_consumed')
        ).filter(
            DietData.user_id == user_id,
            DietData.date >= start_date,
            DietData.date <= end_date
        ).first()
        
        return {
            "total_exercise_minutes": float(exercise_stats[0] or 0),
            "total_calories_burned": float(exercise_stats[1] or 0),
            "total_sleep_hours": float(sleep_stats[0] or 0),
            "total_calories_consumed": float(diet_stats[0] or 0)
        }
    
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
