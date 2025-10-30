# Copy the AI service implementation from the original
# This is a placeholder - you may want to refactor it to call user-service for user data
# and health-data-service for health data via HTTP calls

from typing import Dict, Optional
from sqlalchemy.orm import Session
from datetime import date, timedelta
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.cluster import KMeans

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from shared.models import User, ExerciseData, DietData, SleepData


class AIHealthPlanService:
    def __init__(self):
        self.model = None
        self.kmeans = None
        self.scaler = StandardScaler()
        self.text_generator = None
        self.load_model()
    
    def load_model(self):
        """Load or initialize AI models"""
        try:
            self.kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            self.model = KNeighborsRegressor(n_neighbors=5, weights='distance')
            if HAS_TRANSFORMERS:
                try:
                    self.text_generator = pipeline(
                        "text-generation",
                        model="gpt2",
                        device=-1,
                        max_length=200
                    )
                except Exception as e:
                    print(f"Could not load text generation model: {e}")
                    self.text_generator = None
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def calculate_bmr(self, user: User) -> Optional[float]:
        """Calculate Basal Metabolic Rate"""
        if not user.weight or not user.height or not user.date_of_birth:
            return None
        
        age = (date.today() - user.date_of_birth).days // 365
        
        if user.gender == "male":
            bmr = 10 * user.weight + 6.25 * user.height - 5 * age + 5
        elif user.gender == "female":
            bmr = 10 * user.weight + 6.25 * user.height - 5 * age - 161
        else:
            bmr = 10 * user.weight + 6.25 * user.height - 5 * age - 78
        
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        
        if user.activity_level:
            multiplier = activity_multipliers.get(user.activity_level, 1.2)
            bmr *= multiplier
        
        return bmr
    
    def analyze_health_data(self, db: Session, user_id: int) -> Dict:
        """Analyze user's health data"""
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        # Query each data type separately - much more efficient now!
        exercise_data = db.query(ExerciseData).filter(
            ExerciseData.user_id == user_id,
            ExerciseData.date >= start_date,
            ExerciseData.date <= end_date
        ).all()
        
        sleep_data = db.query(SleepData).filter(
            SleepData.user_id == user_id,
            SleepData.date >= start_date,
            SleepData.date <= end_date
        ).all()
        
        diet_data = db.query(DietData).filter(
            DietData.user_id == user_id,
            DietData.date >= start_date,
            DietData.date <= end_date
        ).all()
        
        analysis = {
            "exercise_frequency": 0,
            "average_exercise_duration": 0,
            "total_calories_burned": 0,
            "average_sleep_hours": 0,
            "average_sleep_quality": "good",
            "average_daily_calories": 0
        }
        
        if exercise_data:
            analysis["exercise_frequency"] = len(exercise_data)
            analysis["average_exercise_duration"] = sum(d.duration or 0 for d in exercise_data) / len(exercise_data)
            analysis["total_calories_burned"] = sum(d.calories_burned or 0 for d in exercise_data)
        
        if sleep_data:
            analysis["average_sleep_hours"] = sum(d.sleep_duration or 0 for d in sleep_data) / len(sleep_data)
            analysis["average_sleep_quality"] = "good" if analysis["average_sleep_hours"] >= 7 else "needs_improvement"
        
        if diet_data:
            analysis["average_daily_calories"] = sum(d.calories or 0 for d in diet_data) / max(len(diet_data), 1)
        
        return analysis
    
    def generate_personalized_plan(self, db: Session, user: User) -> Dict:
        """Generate personalized health plan"""
        bmr = self.calculate_bmr(user)
        health_analysis = self.analyze_health_data(db, user.id)
        
        goal = user.health_goal or "general_health"
        
        # Simplified plan generation - extend with full logic from original
        plan = {
            "plan_type": "general",
            "title": f"{goal.replace('_', ' ').title()} Health Plan",
            "description": f"A personalized AI-powered health plan for {user.full_name or user.username}.",
            "duration_days": 30,
            "exercise_minutes_per_day": 30.0,
            "weekly_exercise_days": 3,
            "calories_target": bmr or 2000,
            "exercise_plan": "AI-optimized exercise plan",
            "diet_suggestions": "Balanced nutrition recommendations",
            "status": "active",
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=30)
        }
        
        return plan

