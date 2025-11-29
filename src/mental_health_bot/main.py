from typing import List, Dict, Any
from .simple_orchestrator import simple_orchestrator

class MentalHealthAgent:
    """Main class for the mental health agent system"""
    
    def __init__(self):
        self.orchestrator = simple_orchestrator
    
    async def chat(self, message: str, user_id: str = "anonymous") -> Dict:
        """Main chat interface for the mental health agent"""
        return await self.orchestrator.process_user_message(message, user_id)

# Global instance
mental_health_agent = MentalHealthAgent()
