import asyncio
from typing import Dict
from datetime import datetime

class EmotionAnalysisAgent:
    """Specialized agent for emotion analysis and sentiment understanding"""
    
    def __init__(self):
        self.emotion_patterns = {
            'anxiety': ['anxious', 'worried', 'nervous', 'panic'],
            'depression': ['sad', 'depressed', 'hopeless', 'empty'],
            'anger': ['angry', 'furious', 'mad', 'frustrated'],
            'calm': ['calm', 'peaceful', 'relaxed', 'content']
        }
    
    async def analyze(self, text: str, context: Dict = None) -> Dict:
        """Analyze emotional content of text"""
        await asyncio.sleep(0.1)
        
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, patterns in self.emotion_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                detected_emotions.append(emotion)
        
        return {
            "detected_emotions": detected_emotions or ['neutral'],
            "emotional_intensity": self._calculate_intensity(text),
            "support_needs": self._determine_support_needs(detected_emotions),
            "agent_type": "emotion_analysis",
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_intensity(self, text: str) -> float:
        """Calculate emotional intensity from text features"""
        intensity_indicators = text.count('!') + text.count('very')
        return min(intensity_indicators / 10, 1.0)
    
    def _determine_support_needs(self, emotions: List[str]) -> List[str]:
        """Determine support needs based on emotions"""
        needs_mapping = {
            'anxiety': ['grounding_techniques', 'breathing_exercises'],
            'depression': ['emotional_support', 'activity_planning'],
            'anger': ['anger_management', 'emotional_regulation']
        }
        
        needs = []
        for emotion in emotions:
            needs.extend(needs_mapping.get(emotion, []))
        
        return list(set(needs)) or ['general_support']
