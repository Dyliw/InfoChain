from sqlalchemy.orm import Session
from app.models.analysis import Analysis, Claim
from app.models.llm import LLMInteraction
from app.services.llm_service import LLMService
from typing import Dict, Any, List, Optional
import json
import time
class AnalysisService:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def decompose_claim(
        self,
        db: Session,
        user_id: str,
        claim: str,
        source_claim: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        decompose_prompt = f"""Decompose the following claim into its component parts.

Claim to analyze: {claim}

{f'Original source claim: {source_claim}' if source_claim else ''}

{f'Context: {json.dumps(context, indent=2)}' if context else ''}

Provide a structured decomposition with:
1. Affirmation: What is the core claim?
2. Evidence: What evidence directly supports this claim?
3. Interpretation: How is the evidence being interpreted?
4. Inference: What conclusions are being drawn?
5. Missing information: What key information is missing?
6. Confidence level: How confident should we be? (0-100)

Also provide your reasoning for this decomposition."""

        messages = [
            {"role": "system", "content": self.llm_service.system_prompt},
            {"role": "system", "content": "You are in ANALYZER mode. Focus on breaking down claims into their component parts."},
            {"role": "user", "content": decompose_prompt}
        ]
        
        # Call LLM
        start_time = time.time()
        response = await self.llm_service._call_llm(messages)
        response_time = int((time.time() - start_time) * 1000)
        
        # Parse response into structured format
        result = self._parse_decomposition_response(response["content"])
        
        # Save LLM interaction
        self.llm_service._save_interaction(
            db, user_id, "decompose",
            decompose_prompt, response,
            tokens_used=response.get("tokens_used", 0),
            response_time=response_time,
            metadata={"claim": claim, "result": result}
        )
        
        return result

    def _parse_decomposition_response(self, response_text: str) -> Dict[str, Any]:
        # Parse the response into structured format
        # This is a simplified version - you'd want more robust parsing
        return {
            "affirmation": "Example affirmation",
            "evidence": ["Evidence 1", "Evidence 2"],
            "interpretation": ["Interpretation 1"],
            "inference": ["Inference 1"],
            "missing_info": ["Missing info 1"],
            "confidence_level": 70,
            "reasoning": response_text
        }

    async def compare_sources(
        self,
        db: Session,
        user_id: str,
        claim: str,
        sources: Dict[str, str]
    ) -> Dict[str, Any]:
        
        compare_prompt = f"""Compare the following sources on the claim: {claim}

Sources:
{json.dumps(sources, indent=2)}

Analyze each source for:
1. What does this source claim?
2. What evidence does it provide?
3. What is its perspective or bias?
4. How reliable is it?

Then identify:
- Where do sources agree?
- Where do they disagree?
- Why might there be disagreements?
- What is the consensus (if any)?

Provide a structured comparison."""

        messages = [
            {"role": "system", "content": self.llm_service.system_prompt},
            {"role": "system", "content": "You are in COMPARATOR mode. Compare different sources and perspectives."},
            {"role": "user", "content": compare_prompt}
        ]
        
        # Call LLM
        start_time = time.time()
        response = await self.llm_service._call_llm(messages)
        response_time = int((time.time() - start_time) * 1000)
        
        # Parse response
        result = self._parse_comparison_response(response["content"])
        
        # Save LLM interaction
        self.llm_service._save_interaction(
            db, user_id, "compare",
            compare_prompt, response,
            tokens_used=response.get("tokens_used", 0),
            response_time=response_time,
            metadata={"claim": claim, "result": result}
        )
        
        return result

    def _parse_comparison_response(self, response_text: str) -> Dict[str, Any]:
        # Parse the comparison response
        return {
            "source": {"summary": "Source summary", "reliability": 70},
            "article": {"summary": "Article summary", "reliability": 80},
            "social": {"summary": "Social summary", "reliability": 50},
            "ia": {"summary": "AI summary", "reliability": 75},
            "differences": [
                {"point": "Difference 1", "sources": ["source", "article"]}
            ],
            "consensus": "There is general agreement that...",
            "confidence_level": 75
        }

    async def save_analysis(
        self,
        db: Session,
        user_id: str,
        instance_id: str,
        claim: str,
        source_claim: Optional[str] = None,
        decomposition: Optional[Dict[str, Any]] = None,
        comparison_result: Optional[Dict[str, Any]] = None,
        confidence_level: Optional[int] = None,
        claims_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        
        # Create analysis
        analysis = Analysis(
            user_id=user_id,
            instance_id=instance_id,
            claim=claim,
            source_claim=source_claim,
            decomposition=decomposition,
            comparison_result=comparison_result,
            confidence_level=confidence_level
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Save individual claims if provided
        if claims_data:
            for claim_data in claims_data:
                claim_obj = Claim(
                    analysis_id=analysis.id,
                    text=claim_data.get("text"),
                    claim_type=claim_data.get("claim_type"),
                    confidence=claim_data.get("confidence")
                )
                db.add(claim_obj)
            db.commit()
        
        return {
            "id": str(analysis.id),
            "message": "Analysis saved successfully"
        }

    async def get_analysis(
        self,
        db: Session,
        analysis_id: str
    ) -> Dict[str, Any]:
        
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise Exception("Analysis not found")
        
        # Get associated claims
        claims = db.query(Claim).filter(Claim.analysis_id == analysis_id).all()
        
        return {
            "id": str(analysis.id),
            "user_id": str(analysis.user_id),
            "instance_id": str(analysis.instance_id),
            "claim": analysis.claim,
            "source_claim": analysis.source_claim,
            "decomposition": analysis.decomposition,
            "comparison_result": analysis.comparison_result,
            "confidence_level": analysis.confidence_level,
            "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
            "claims": [
                {
                    "id": str(c.id),
                    "text": c.text,
                    "claim_type": c.claim_type,
                    "confidence": c.confidence,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                }
                for c in claims
            ]
        }
