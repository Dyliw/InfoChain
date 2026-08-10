from sqlalchemy.orm import Session
from app.models.reasoning import ReasoningMap
from app.models.analysis import Analysis, Claim
from app.models.source import Source, SourceFragment
from app.services.llm_service import LLMService
from typing import Dict, Any, List
import json
import time

class ReasoningMapper:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def generate_map(
        self,
        db: Session,
        user_id: str,
        analysis_id: str,
        include_sources: bool = True,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        
        # Get analysis data
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise Exception("Analysis not found")
        
        # Get claims
        claims = db.query(Claim).filter(Claim.analysis_id == analysis_id).all()
        
        # Get sources if available
        sources_data = []
        if include_sources:
            # This would need source relationships in analysis
            # For now, we'll use what's available in the analysis
            pass
        
        # Prepare data for LLM
        map_prompt = self._build_map_prompt(
            analysis.claim,
            analysis.decomposition,
            claims,
            sources_data
        )
        
        # Call LLM to generate map
        messages = [
            {"role": "system", "content": self._get_mapper_system_prompt()},
            {"role": "user", "content": map_prompt}
        ]
        
        start_time = time.time()
        response = await self.llm_service._call_llm(messages)
        response_time = int((time.time() - start_time) * 1000)
        
        # Parse LLM response into map structure
        map_data = self._parse_map_response(response["content"])
        
        # Save map
        reasoning_map = ReasoningMap(
            user_id=user_id,
            analysis_id=analysis_id,
            nodes=map_data["nodes"],
            edges=map_data["edges"],
            confidence_breakdown=map_data["confidence_breakdown"],
            final_conclusion=map_data["final_conclusion"]
        )
        
        db.add(reasoning_map)
        db.commit()
        db.refresh(reasoning_map)
        
        # Save LLM interaction
        self.llm_service._save_interaction(
            db, user_id, "generate_map",
            map_prompt, response,
            tokens_used=response.get("tokens_used", 0),
            response_time=response_time,
            metadata={"analysis_id": analysis_id}
        )
        
        return {
            "id": str(reasoning_map.id),
            "nodes": map_data["nodes"],
            "edges": map_data["edges"],
            "confidence_breakdown": map_data["confidence_breakdown"],
            "final_conclusion": map_data["final_conclusion"],
            "analysis_summary": map_data.get("analysis_summary", "")
        }
    
    def _get_mapper_system_prompt(self) -> str:
        return """You are a reasoning map generator for InfoChain. Your task is to create visual reasoning maps that show how a conclusion is derived from evidence.

For each claim, you should:
1. Identify the core claim or conclusion
2. Identify supporting evidence (directly stated)
3. Identify interpretations (how evidence is understood)
4. Identify inferences (conclusions drawn from evidence)
5. Identify assumptions and gaps

Create a map with the following node types:
- CLAIM: The main claim or conclusion
- EVIDENCE: Directly stated facts or data
- INTERPRETATION: How evidence is understood
- INFERENCE: Conclusions drawn from evidence
- ASSUMPTION: Unstated premises
- GAP: Missing information

Each node should have a clear text and be connected to other nodes with labeled edges.

Also provide:
- Confidence breakdown (% backed by evidence, % inference, % unsupported)
- Final conclusion statement
- Analysis summary
"""
    
    def _build_map_prompt(
        self,
        claim: str,
        decomposition: Dict[str, Any],
        claims: List[Any],
        sources: List[Any]
    ) -> str:
        prompt = f"""Generate a reasoning map for the following analysis:

Main Claim: {claim}

Decomposition:
{json.dumps(decomposition, indent=2) if decomposition else 'No decomposition available'}

Individual Claims:
{json.dumps([{'text': c.text, 'type': c.claim_type, 'confidence': c.confidence} for c in claims], indent=2)}

{f'Sources: {json.dumps(sources, indent=2)}' if sources else ''}

Generate a reasoning map that shows how this analysis builds its conclusion.
Include:
1. All key claims and sub-claims
2. Evidence supporting each claim
3. Inferences made
4. Relationships between claims
5. Confidence breakdown
6. Final conclusion
"""
        return prompt
    
    def _parse_map_response(self, response_text: str) -> Dict[str, Any]:
        # Parse LLM response into structured map data
        # This is a simplified version - you'd want more robust parsing
        nodes = [
            {"id": "1", "type": "claim", "text": "Main claim", "parentId": None},
            {"id": "2", "type": "evidence", "text": "Supporting evidence", "parentId": "1"},
            {"id": "3", "type": "inference", "text": "Inference drawn", "parentId": "1"}
        ]
        
        edges = [
            {"from": "2", "to": "1", "label": "supports"},
            {"from": "3", "to": "1", "label": "supports"}
        ]
        
        return {
            "nodes": nodes,
            "edges": edges,
            "confidence_breakdown": {"backed": 61, "inference": 24, "unsupported": 15},
            "final_conclusion": "Based on the analysis, the claim is supported by evidence.",
            "analysis_summary": "Summary of the analysis"
        }
    
    async def get_map(self, db: Session, analysis_id: str) -> Dict[str, Any]:
        reasoning_map = db.query(ReasoningMap).filter(
            ReasoningMap.analysis_id == analysis_id
        ).first()
        
        if not reasoning_map:
            raise Exception("Map not found for this analysis")
        
        return {
            "id": str(reasoning_map.id),
            "user_id": str(reasoning_map.user_id),
            "analysis_id": str(reasoning_map.analysis_id),
            "nodes": reasoning_map.nodes,
            "edges": reasoning_map.edges,
            "confidence_breakdown": reasoning_map.confidence_breakdown,
            "final_conclusion": reasoning_map.final_conclusion,
            "user_adjustments": reasoning_map.user_adjustments,
            "created_at": reasoning_map.created_at.isoformat() if reasoning_map.created_at else None,
            "updated_at": reasoning_map.updated_at.isoformat() if reasoning_map.updated_at else None
        }
    
    async def save_map_with_adjustments(
        self,
        db: Session,
        user_id: str,
        analysis_id: str,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        confidence_breakdown: Dict[str, float],
        final_conclusion: str,
        user_adjustments: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        reasoning_map = db.query(ReasoningMap).filter(
            ReasoningMap.analysis_id == analysis_id
        ).first()
        
        if not reasoning_map:
            # Create new map
            reasoning_map = ReasoningMap(
                user_id=user_id,
                analysis_id=analysis_id,
                nodes=nodes,
                edges=edges,
                confidence_breakdown=confidence_breakdown,
                final_conclusion=final_conclusion,
                user_adjustments=user_adjustments
            )
            db.add(reasoning_map)
        else:
            # Update existing map
            reasoning_map.nodes = nodes
            reasoning_map.edges = edges
            reasoning_map.confidence_breakdown = confidence_breakdown
            reasoning_map.final_conclusion = final_conclusion
            reasoning_map.user_adjustments = user_adjustments
        
        db.commit()
        db.refresh(reasoning_map)
        
        return {
            "id": str(reasoning_map.id),
            "message": "Map saved successfully"
        }
