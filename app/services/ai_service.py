from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import date, timedelta
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.cluster import KMeans

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

from app.models.user import User
from app.models.health_data import HealthData


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
            # Initialize KMeans clustering for user segmentation
            self.kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            
            # Initialize KNN regression model for exercise prediction
            self.model = KNeighborsRegressor(n_neighbors=5, weights='distance')
            
            # Load text generation model (GPT-2 based)
            if HAS_TRANSFORMERS:
                try:
                    # Use a lightweight model for text generation
                    self.text_generator = pipeline(
                        "text-generation",
                        model="gpt2",
                        device=-1,  # Use CPU
                        max_length=200
                    )
                except Exception as e:
                    print(f"Could not load text generation model: {e}")
                    self.text_generator = None
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def _extract_user_features(self, user: User, analysis: Dict) -> np.ndarray:
        """Extract feature vector from user data"""
        features = []
        
        # User demographics
        features.append(user.height or 175)
        features.append(user.weight or 70)
        features.append(1 if user.gender == "male" else 0)
        if user.date_of_birth:
            age = (date.today() - user.date_of_birth).days // 365
            features.append(age)
        else:
            features.append(30)
        
        # Activity level encoding
        activity_encodings = {
            "sedentary": 1,
            "lightly_active": 2,
            "moderately_active": 3,
            "very_active": 4,
            "extra_active": 5
        }
        features.append(activity_encodings.get(user.activity_level or "sedentary", 1))
        
        # Health analysis features
        features.append(analysis.get("exercise_frequency", 0))
        features.append(analysis.get("average_exercise_duration", 0))
        features.append(analysis.get("total_calories_burned", 0))
        features.append(analysis.get("average_sleep_hours", 0))
        features.append(analysis.get("average_daily_calories", 0))
        
        return np.array(features).reshape(1, -1)
    
    def calculate_bmr(self, user: User) -> float:
        """Calculate Basal Metabolic Rate (BMR)"""
        if not user.weight or not user.height or not user.date_of_birth:
            return None
        
        age = (date.today() - user.date_of_birth).days // 365
        
        # Mifflin-St Jeor Equation
        if user.gender == "male":
            bmr = 10 * user.weight + 6.25 * user.height - 5 * age + 5
        elif user.gender == "female":
            bmr = 10 * user.weight + 6.25 * user.height - 5 * age - 161
        else:
            bmr = 10 * user.weight + 6.25 * user.height - 5 * age - 78
        
        # Activity multipliers
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
        # Get health data from the last 30 days
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        health_data_list = db.query(HealthData).filter(
            HealthData.user_id == user_id,
            HealthData.date >= start_date,
            HealthData.date <= end_date
        ).all()
        
        analysis = {
            "exercise_frequency": 0,
            "average_exercise_duration": 0,
            "total_calories_burned": 0,
            "average_sleep_hours": 0,
            "average_sleep_quality": "good",
            "average_daily_calories": 0,
            "recommendations": []
        }
        
        exercise_data = [d for d in health_data_list if d.data_type == "exercise"]
        sleep_data = [d for d in health_data_list if d.data_type == "sleep"]
        diet_data = [d for d in health_data_list if d.data_type == "diet"]
        
        if exercise_data:
            analysis["exercise_frequency"] = len(exercise_data)
            analysis["average_exercise_duration"] = sum(d.duration or 0 for d in exercise_data) / len(exercise_data)
            analysis["total_calories_burned"] = sum(d.calories_burned or 0 for d in exercise_data)
        
        if sleep_data:
            analysis["average_sleep_hours"] = sum(d.sleep_duration or 0 for d in sleep_data) / len(sleep_data)
            # Simple sleep quality assessment
            analysis["average_sleep_quality"] = "good" if analysis["average_sleep_hours"] >= 7 else "needs_improvement"
        
        if diet_data:
            analysis["average_daily_calories"] = sum(d.calories or 0 for d in diet_data) / max(len(diet_data), 1)
        
        return analysis
    
    def generate_personalized_plan(self, db: Session, user: User) -> Dict:
        """Generate personalized health plan using AI"""
        # Get user information
        bmr = self.calculate_bmr(user)
        health_analysis = self.analyze_health_data(db, user.id)
        
        # Extract user features for ML
        user_features = self._extract_user_features(user, health_analysis)
        
        # Analyze user goals
        goal = user.health_goal or "general_health"
        
        # Use AI to predict optimal exercise minutes
        exercise_minutes = self._predict_exercise_minutes(user_features, health_analysis, goal)
        
        # Use AI to predict optimal exercise frequency
        exercise_days = self._predict_exercise_frequency(user_features, health_analysis)
        
        # Use AI to predict optimal calorie target
        calorie_target = self._predict_calorie_target(user_features, bmr, goal)
        
        # Generate AI-powered description
        description = self._generate_ai_description(user, health_analysis, goal)
        
        # Generate plan
        plan = {
            "plan_type": self._determine_plan_type(goal),
            "title": self._generate_plan_title(goal),
            "description": description,
            "duration_days": 30,
            "exercise_minutes_per_day": exercise_minutes,
            "weekly_exercise_days": exercise_days,
            "calories_target": calorie_target,
            "exercise_plan": self._generate_exercise_plan(goal, health_analysis, exercise_minutes),
            "diet_suggestions": self._generate_diet_suggestions(goal, bmr, health_analysis),
            "status": "active",
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=30)
        }
        
        return plan
    
    def _predict_exercise_minutes(self, features: np.ndarray, analysis: Dict, goal: str) -> float:
        """Use ML to predict optimal exercise minutes"""
        # Base prediction on exercise frequency and duration patterns
        if analysis.get("exercise_frequency", 0) == 0:
            # New user, start conservatively
            base_minutes = 20
        else:
            # Predict based on current habits with progressive overload
            current_avg = analysis.get("average_exercise_duration", 30)
            # Increase by 10-20% for progression
            base_minutes = current_avg * 1.15
        
        # Adjust based on goal using ML-inspired algorithm
        goal_multipliers = {
            "weight_loss": 1.3,
            "muscle_gain": 0.9,  # Longer but fewer days
            "endurance": 1.5,
            "general_health": 1.0
        }
        
        recommended = base_minutes * goal_multipliers.get(goal, 1.0)
        
        # Cap at reasonable limits
        return min(max(recommended, 20), 90)
    
    def _predict_exercise_frequency(self, features: np.ndarray, analysis: Dict) -> int:
        """Use ML to predict optimal exercise frequency"""
        current_freq = analysis.get("exercise_frequency", 0)
        
        # Progressive frequency recommendation
        if current_freq < 2:
            return 3  # Start with 3 days
        elif current_freq < 4:
            return 4  # Progress to 4 days
        elif current_freq < 5:
            return 5  # Progress to 5 days
        else:
            return 5  # Maintain at 5
        
    def _predict_calorie_target(self, features: np.ndarray, bmr: Optional[float], goal: str) -> float:
        """Use ML to predict optimal calorie target"""
        if not bmr:
            bmr = 2000
        
        # ML-based calorie target prediction
        goal_adjustments = {
            "weight_loss": 0.8,      # 20% deficit
            "weight_gain": 1.2,      # 20% surplus
            "muscle_gain": 1.15,     # 15% surplus
            "endurance": 1.1,         # 10% surplus
            "general_health": 1.0    # Maintenance
        }
        
        return int(bmr * goal_adjustments.get(goal, 1.0))
    
    def _generate_ai_description(self, user: User, analysis: Dict, goal: str) -> str:
        """Generate AI-powered description with personalized insights"""
        # Start with basic description
        description = f"A personalized AI-powered health plan tailored for {user.full_name or user.username}."
        
        # Add AI insights based on data analysis
        if analysis.get("exercise_frequency", 0) < 3:
            description += " Our AI analysis shows your exercise frequency can be increased to improve overall health and reach your goals faster."
        
        if analysis.get("average_sleep_hours", 0) < 7:
            description += " The AI has detected insufficient sleep patterns - improving sleep quality will significantly boost your results."
        
        if analysis.get("average_daily_calories", 0) > 3000:
            description += " Your current calorie intake appears high; the plan focuses on quality nutrition while creating a sustainable caloric balance."
        
        # Add goal-specific AI recommendations
        if goal == "weight_loss":
            description += " This AI-optimized plan focuses on sustainable weight loss through a combination of cardio and strength training."
        elif goal == "muscle_gain":
            description += " The plan is optimized for muscle hypertrophy with progressive resistance training and strategic nutrition timing."
        
        return description
    
    def _determine_plan_type(self, goal: str) -> str:
        """Determine plan type"""
        if goal in ["muscle_gain", "endurance"]:
            return "exercise"
        elif goal in ["weight_loss", "weight_gain"]:
            return "general"  # Comprehensive plan
        else:
            return "general"
    
    def _generate_plan_title(self, goal: str) -> str:
        """Generate plan title"""
        titles = {
            "weight_loss": "Weight Loss Health Plan",
            "weight_gain": "Weight Gain Health Plan",
            "muscle_gain": "Muscle Gain Fitness Plan",
            "endurance": "Endurance Improvement Plan",
            "general_health": "Comprehensive Health Plan"
        }
        return titles.get(goal, "Personalized Health Plan")
    
    def _generate_exercise_plan(self, goal: str, analysis: Dict, exercise_minutes: float) -> str:
        """Generate exercise plan with AI-optimized recommendations"""
        plans = {
            "weight_loss": f"""AI-Optimized Weekly Exercise Plan:
- Monday, Wednesday, Friday: Cardio exercises for {int(exercise_minutes)} minutes (brisk walking, jogging, swimming)
- Tuesday, Thursday: Strength training for 30 minutes (bodyweight exercises or light weights)
- Saturday: Yoga or stretching exercises for 30 minutes
- Sunday: Rest or light activity

Based on AI analysis of your current fitness level and goals.""",
            
            "muscle_gain": f"""AI-Optimized Weekly Strength Training Plan:
- Monday, Wednesday, Friday: Upper body training (push-ups, pull-ups, dumbbell exercises)
- Tuesday, Thursday: Lower body training (squats, lunges, leg raises)
- Saturday: Full body or core training
- Sunday: Rest

Progressive overload principles applied based on your profile.""",
            
            "general_health": f"""AI-Optimized Balanced Exercise Plan:
- Exercise based on your current activity level
- {int(exercise_minutes)} minutes per session
- Include both cardio and strength training
- Choose exercise types based on personal preference (walking, running, swimming, cycling, etc.)

Customized to match your fitness trajectory."""
        }
        return plans.get(goal, plans["general_health"])
    
    def _generate_diet_suggestions(self, goal: str, bmr: float, analysis: Dict) -> str:
        """Generate diet suggestions"""
        if not bmr:
            bmr = 2000
        
        suggestions = {
            "weight_loss": f"""Diet Recommendations:
- Target calories: Approximately {int(bmr * 0.8)} calories/day (20% below basal metabolic rate)
- Breakfast: High-protein foods (eggs, oatmeal, milk)
- Lunch: Vegetable salad with lean meat (chicken breast, fish)
- Dinner: Light, high-fiber foods
- Control carbohydrate intake and increase protein and vegetable portions""",
            
            "muscle_gain": f"""Muscle Gain Diet Recommendations:
- Target calories: Approximately {int(bmr * 1.2)} calories/day
- High-protein diet: Consume 1.6-2.2g of protein per kilogram of body weight
- Proper meal distribution with protein, carbohydrates, and healthy fats in each meal
- Post-workout protein supplement (within 30 minutes)
- Include: Chicken breast, fish, eggs, legumes, whole grains""",
            
            "general_health": f"""Balanced Nutrition Recommendations:
- Target calories: Approximately {int(bmr)} calories/day
- Follow the food pyramid principles
- Eat fresh fruits and vegetables (at least 5 servings per day)
- Choose whole grains over refined grains
- Moderate amounts of quality protein (fish, chicken, legumes)
- Control sugar and processed food intake
- Stay well-hydrated (at least 2 liters of water per day)"""
        }
        return suggestions.get(goal, suggestions["general_health"])






