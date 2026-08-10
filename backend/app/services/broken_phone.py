from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.relay import RelayChain, RelayTransmission
from app.models.source import InformationTransformation
from app.models.user import User
from app.services.llm_service import LLMService
from typing import Dict, Any, List, Optional
import json
import time
from datetime import datetime

class BrokenPhoneService:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def start_chain(
        self,
        db: Session,
        user_id: str,
        original_text: str,
        max_links: int = 5,
        scenario_id: Optional[str] = None
    ) -> Dict[str, Any]:
        
        # Check for existing open chain for this user
        existing_chain = db.query(RelayChain).join(
            RelayTransmission
        ).filter(
            RelayTransmission.user_id == user_id,
            RelayChain.status.in_(['open', 'in_progress'])
        ).first()
        
        if existing_chain:
            raise Exception("You already have an active relay chain")
        
        # Create new chain
        chain = RelayChain(
            scenario_id=scenario_id if scenario_id else None,
            original_text=original_text,
            max_links=max_links,
            status='open'
        )
        db.add(chain)
        db.commit()
        db.refresh(chain)
        
        # Create first transmission (original)
        transmission = RelayTransmission(
            chain_id=chain.id,
            position=0,
            user_id=user_id,
            text=original_text,
            elapsed_time_ms=0
        )
        db.add(transmission)
        db.commit()
        
        return {
            "chain_id": str(chain.id),
            "original_text": original_text,
            "max_links": max_links,
            "status": chain.status,
            "current_position": 0,
            "next_user_id": user_id  # The starter is first to transmit
        }
    
    async def transmit(
        self,
        db: Session,
        chain_id: str,
        user_id: str,
        text: str,
        elapsed_time_ms: Optional[int] = None
    ) -> Dict[str, Any]:
        
        # Get chain
        chain = db.query(RelayChain).filter(RelayChain.id == chain_id).first()
        if not chain:
            raise Exception("Chain not found")
        
        if chain.status == 'completed':
            raise Exception("Chain is already completed")
        
        # Get last transmission
        last_transmission = db.query(RelayTransmission).filter(
            RelayTransmission.chain_id == chain_id
        ).order_by(RelayTransmission.position.desc()).first()
        
        if not last_transmission:
            raise Exception("No transmissions found for this chain")
        
        new_position = last_transmission.position + 1
        
        if new_position > chain.max_links:
            raise Exception("Chain has reached maximum length")
        
        # Check if user already transmitted in this chain
        existing = db.query(RelayTransmission).filter(
            and_(
                RelayTransmission.chain_id == chain_id,
                RelayTransmission.user_id == user_id
            )
        ).first()
        
        if existing:
            raise Exception("User has already transmitted in this chain")
        
        # Detect transformations between previous and current text
        transformations = await self._detect_transformations(
            db,
            last_transmission.text,
            text,
            user_id
        )
        
        # Create new transmission
        transmission = RelayTransmission(
            chain_id=chain_id,
            position=new_position,
            user_id=user_id,
            text=text,
            elapsed_time_ms=elapsed_time_ms
        )
        db.add(transmission)
        db.commit()
        db.refresh(transmission)
        
        # Check if chain is complete
        is_complete = new_position == chain.max_links
        if is_complete:
            chain.status = 'completed'
            chain.completed_at = datetime.now()
            db.commit()
            
            # Generate distortion analysis
            distortion_analysis = await self._analyze_distortion(
                db,
                chain_id,
                chain.original_text,
                text
            )
            
            return {
                "transmission_id": str(transmission.id),
                "position": new_position,
                "is_complete": True,
                "chain_status": "completed",
                "next_position": None,
                "distortion_analysis": distortion_analysis,
                "transformations": transformations
            }
        
        # Update chain status
        chain.status = 'in_progress'
        db.commit()
        
        # Find next user (for now, just return the chain ID)
        # In a real implementation, you'd assign the next user
        
        return {
            "transmission_id": str(transmission.id),
            "position": new_position,
            "is_complete": False,
            "chain_status": chain.status,
            "next_position": new_position + 1,
            "transformations": transformations
        }
    
    async def _detect_transformations(
        self,
        db: Session,
        previous_text: str,
        new_text: str,
        user_id: str
    ) -> List[Dict[str, Any]]:
        
        # Use LLM to detect transformations
        transform_prompt = f"""Analyze the transformation between these two texts:

Previous text: {previous_text}

New text: {new_text}

Identify any transformations that occurred:
1. Omissions: What information was removed?
2. Additions: What information was added?
3. Alterations: What information was changed?
4. Simplifications: What was simplified?
5. Elaborations: What was elaborated?

For each transformation, rate its severity from 0.0 to 1.0.

Provide a structured analysis."""

        messages = [
            {"role": "system", "content": "You are an information transformation detector."},
            {"role": "user", "content": transform_prompt}
        ]
        
        response = await self.llm_service._call_llm(messages)
        
        # Parse transformations
        transformations = self._parse_transformations(response["content"])
        
        # Save transformations to database
        saved_transformations = []
        for transform in transformations:
            info_transform = InformationTransformation(
                previous_text=previous_text,
                resulting_text=new_text,
                transformation_type=transform["type"],
                severity=transform["severity"],
                detected_by="ai",
                explanation=transform["explanation"]
            )
            db.add(info_transform)
            saved_transformations.append(info_transform)
        
        db.commit()
        
        return [self._serialize_transformation(t) for t in saved_transformations]
    
    def _parse_transformations(self, response_text: str) -> List[Dict[str, Any]]:
        # Parse LLM response
        # This is simplified - you'd want more robust parsing
        return [
            {
                "type": "alteration",
                "severity": 0.7,
                "explanation": "Key details were changed"
            }
        ]
    
    def _serialize_transformation(self, transform: InformationTransformation) -> Dict[str, Any]:
        return {
            "id": str(transform.id),
            "type": transform.transformation_type,
            "severity": float(transform.severity) if transform.severity else None,
            "explanation": transform.explanation,
            "created_at": transform.created_at.isoformat() if transform.created_at else None
        }
    
    async def _analyze_distortion(
        self,
        db: Session,
        chain_id: str,
        original_text: str,
        final_text: str
    ) -> Dict[str, Any]:
        
        # Get all transmissions
        transmissions = db.query(RelayTransmission).filter(
            RelayTransmission.chain_id == chain_id
        ).order_by(RelayTransmission.position).all()
        
        # Get transformations
        transformations = db.query(InformationTransformation).filter(
            InformationTransformation.id.in_(
                [t.id for t in transmissions if t.position > 0]
            )
        ).all()
        
        # Analyze distortion using LLM
        analysis_prompt = f"""Analyze the distortion in this chain of information transmission:

Original: {original_text}

All transmissions:
{json.dumps([{'position': t.position, 'text': t.text} for t in transmissions], indent=2)}

Provide:
1. Summary of how the information changed
2. Key transformations identified
3. Distortion score (0-100)
4. What was lost, added, or changed
5. What remained consistent

Provide a structured analysis."""

        messages = [
            {"role": "system", "content": "You are an information distortion analyst."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        response = await self.llm_service._call_llm(messages)
        
        # Parse analysis
        analysis_result = self._parse_distortion_analysis(response["content"])
        
        return analysis_result
    
    def _parse_distortion_analysis(self, response_text: str) -> Dict[str, Any]:
        # Parse LLM response
        return {
            "summary": "Summary of information distortion",
            "key_transformations": [
                {"type": "omission", "description": "Removed key details"},
                {"type": "addition", "description": "Added new information"}
            ],
            "distortion_score": 65,
            "changes": {
                "lost": ["Detail 1", "Detail 2"],
                "added": ["New detail 1"],
                "changed": ["Changed detail 1"]
            },
            "consistent_elements": ["Core message"]
        }
    
    async def get_chain(
        self,
        db: Session,
        chain_id: str
    ) -> Dict[str, Any]:
        
        chain = db.query(RelayChain).filter(RelayChain.id == chain_id).first()
        if not chain:
            raise Exception("Chain not found")
        
        # Get all transmissions
        transmissions = db.query(RelayTransmission).filter(
            RelayTransmission.chain_id == chain_id
        ).order_by(RelayTransmission.position).all()
        
        # Get transformations if chain is completed
        transformations = []
        if chain.status == 'completed':
            # Get transformations for this chain
            # This is simplified - you'd need to link transformations to chain
            pass
        
        # Generate distortion analysis if completed
        distortion_analysis = None
        if chain.status == 'completed' and len(transmissions) > 1:
            distortion_analysis = await self._analyze_distortion(
                db,
                chain_id,
                chain.original_text,
                transmissions[-1].text if transmissions else ""
            )
        
        return {
            "id": str(chain.id),
            "scenario_id": str(chain.scenario_id) if chain.scenario_id else None,
            "original_text": chain.original_text,
            "max_links": chain.max_links,
            "status": chain.status,
            "created_at": chain.created_at.isoformat() if chain.created_at else None,
            "completed_at": chain.completed_at.isoformat() if chain.completed_at else None,
            "transmissions": [
                {
                    "id": str(t.id),
                    "position": t.position,
                    "user_id": str(t.user_id) if t.user_id else None,
                    "text": t.text,
                    "elapsed_time_ms": t.elapsed_time_ms,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                }
                for t in transmissions
            ],
            "transformations": transformations,
            "distortion_analysis": distortion_analysis
        }
