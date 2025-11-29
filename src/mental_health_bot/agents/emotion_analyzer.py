from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class EmotionAnalysisAgent:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def analyze_emotions(self, text: str) -> Dict[str, Any]:
        """Analyze emotions from text"""
        if self.model:
            try:
                prompt = f"""
                Analyze the emotional content of this text and return a JSON with:
                - primary_emotion: main emotion detected
                - secondary_emotions: list of other emotions
                - intensity: low/medium/high
                - support_needs: list of support types needed
                
                Text: {text}
                """
                response = self.model.generate_content(prompt)
                return self._parse_response(response.text)
            except Exception as e:
                return self._fallback_analysis(text)
        else:
            return self._fallback_analysis(text)
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response - simplified version"""
        return {
            "primary_emotion": "concern",
            "secondary_emotions": ["anxiety", "stress"],
            "intensity": "medium", 
            "support_needs": ["emotional_support", "coping_strategies"]
        }
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback analysis when AI is unavailable"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['sad', 'depressed', 'hopeless']):
            return {
                "primary_emotion": "sadness",
                "secondary_emotions": ["hopelessness", "loneliness"],
                "intensity": "high",
                "support_needs": ["emotional_support", "crisis_check"]
            }
        elif any(word in text_lower for word in ['anxious', 'worried', 'panic']):
            return {
                "primary_emotion": "anxiety", 
                "secondary_emotions": ["fear", "uncertainty"],
                "intensity": "medium",
                "support_needs": ["grounding_techniques", "anxiety_management"]
            }
        else:
            return {
                "primary_emotion": "neutral",
                "secondary_emotions": [],
                "intensity": "low",
                "support_needs": ["general_support"]
            }
    
    def _determine_support_needs(self, emotions: List[str]) -> List[str]:
        """Determine support needs based on emotions"""
        support_map = {
            "sadness": ["emotional_support", "validation"],
            "anxiety": ["grounding_techniques", "breathing_exercises"],
            "anger": ["anger_management", "safe_expression"],
            "hopelessness": ["crisis_check", "hope_building"]
        }
        
        needs = []
        for emotion in emotions:
            if emotion in support_map:
                needs.extend(support_map[emotion])
        
        return list(set(needs))  # Remove duplicates
