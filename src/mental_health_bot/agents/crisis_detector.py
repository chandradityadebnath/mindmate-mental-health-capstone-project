import asyncio
from typing import Dict, List
from datetime import datetime

class CrisisDetectionAgent:
    """Specialized agent for crisis detection and emergency response"""
    
    def __init__(self):
        self.crisis_keywords = {
            'suicidal': ['kill myself', 'end it all', 'suicide', 'want to die'],
            'self_harm': ['cut myself', 'self harm', 'hurt myself'],
            'panic': ['panic attack', 'cant breathe', 'heart racing'],
            'depression': ['hopeless', 'empty inside', 'no point']
        }
    
    async def analyze(self, text: str, context: Dict = None) -> Dict:
        """Analyze text for crisis indicators"""
        await asyncio.sleep(0.1)  # Simulate processing
        
        crisis_level = "low"
        detected_issues = []
        text_lower = text.lower()
        
        # Multi-layer crisis detection
        for category, keywords in self.crisis_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_issues.append(category)
                if category in ['suicidal', 'self_harm']:
                    crisis_level = "high"
        
        return {
            "crisis_level": crisis_level,
            "detected_issues": detected_issues,
            "immediate_action_required": crisis_level in ["high", "medium"],
            "agent_type": "crisis_detection",
            "timestamp": datetime.now().isoformat()
        }
