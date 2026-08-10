from sqlalchemy.orm import Session
from app.models.scenario import Scenario, ScenarioInstance
from app.schemas.scenario import ScenarioStart, ScenarioStep, ScenarioComplete
from fastapi import HTTPException, status
from uuid import UUID
import json
from datetime import datetime

from backend.app.models.user import User

class ScenarioService:
    @staticmethod
    def get_all_scenarios(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Scenario).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_scenario_by_slug(db: Session, slug: str):
        scenario = db.query(Scenario).filter(Scenario.slug == slug).first()
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scenario with slug '{slug}' not found"
            )
        return scenario
    
    @staticmethod
    def start_scenario(db: Session, slug: str, start_data: ScenarioStart):
        scenario = ScenarioService.get_scenario_by_slug(db, slug)
        
        # Check if user has an in-progress instance of this scenario
        existing = db.query(ScenarioInstance).filter(
            ScenarioInstance.user_id == start_data.user_id,
            ScenarioInstance.scenario_id == scenario.id,
            ScenarioInstance.status == "in_progress"
        ).first()
        
        if existing:
            return existing
        
        # Create new instance
        instance = ScenarioInstance(
            user_id=start_data.user_id,
            scenario_id=scenario.id,
            status="in_progress",
            current_step=0,
            user_actions=[],
            chain_data={}
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    
    @staticmethod
    def process_step(db: Session, slug: str, step_data: ScenarioStep):
        scenario = ScenarioService.get_scenario_by_slug(db, slug)
        
        instance = db.query(ScenarioInstance).filter(
            ScenarioInstance.user_id == step_data.user_id,
            ScenarioInstance.scenario_id == scenario.id,
            ScenarioInstance.status == "in_progress"
        ).first()
        
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active instance found"
            )
        
        # Update instance with step data
        if instance.user_actions is None:
            instance.user_actions = []
        
        # Append new action
        actions = instance.user_actions
        actions.append({
            "step": instance.current_step,
            "data": step_data.step_data,
            "timestamp": datetime.now().isoformat()
        })
        instance.user_actions = actions
        
        # Update chain_data if needed (for broken phone)
        if "transmission" in step_data.step_data:
            if instance.chain_data is None:
                instance.chain_data = {"transmissions": []}
            instance.chain_data["transmissions"].append({
                "position": len(instance.chain_data.get("transmissions", [])) + 1,
                "data": step_data.step_data["transmission"]
            })
        
        # Increment step
        instance.current_step += 1
        db.commit()
        db.refresh(instance)
        return instance
    
    @staticmethod
    def complete_scenario(db: Session, slug: str, complete_data: ScenarioComplete):
        scenario = ScenarioService.get_scenario_by_slug(db, slug)
        
        instance = db.query(ScenarioInstance).filter(
            ScenarioInstance.user_id == complete_data.user_id,
            ScenarioInstance.scenario_id == scenario.id,
            ScenarioInstance.status == "in_progress"
        ).first()
        
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active instance found"
            )
        
        # Update instance
        instance.status = "completed"
        instance.completed_at = datetime.now()
        instance.score = complete_data.score
        instance.mistakes_identified = complete_data.mistakes_identified
        
        if complete_data.final_data:
            if instance.user_actions is None:
                instance.user_actions = []
            actions = instance.user_actions
            actions.append({
                "step": "final",
                "data": complete_data.final_data,
                "timestamp": datetime.now().isoformat()
            })
            instance.user_actions = actions
        
        db.commit()
        db.refresh(instance)
        
        # Update user stats
        user = db.query(User).filter(User.id == complete_data.user_id).first()
        if user:
            user.total_scenarios_completed += 1
            # Update avg_confidence_calibration logic here
            db.commit()
        
        return instance
    
    @staticmethod
    def get_instance(db: Session, instance_id: UUID):
        instance = db.query(ScenarioInstance).filter(
            ScenarioInstance.id == instance_id
        ).first()
        
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instance not found"
            )
        return instance
