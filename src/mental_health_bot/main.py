#!/usr/bin/env python3
"""
Main orchestrator for Mental Health Agent System
"""

import asyncio
import sys
from src.agents.crisis_detector import CrisisDetectionAgent
from src.agents.emotion_analyzer import EmotionAnalysisAgent
from src.utils.config import Config

class MentalHealthOrchestrator:
    """Main system orchestrator"""
    
    def __init__(self):
        self.agents = {
            'crisis_detector': CrisisDetectionAgent(),
            'emotion_analyzer': EmotionAnalysisAgent()
        }
        Config.validate_config()
    
    async def process_message(self, message: str) -> Dict:
        """Process user message through all agents"""
        print(f"🔍 Processing: {message}")
        
        # Run agents in parallel
        tasks = []
        for agent_name, agent in self.agents.items():
            task = asyncio.create_task(agent.analyze(message))
            tasks.append((agent_name, task))
        
        # Collect results
        results = {}
        for agent_name, task in tasks:
            try:
                result = await task
                results[agent_name] = result
                print(f"✅ {agent_name} completed")
            except Exception as e:
                print(f"❌ {agent_name} failed: {e}")
        
        return self._synthesize_response(results)
    
    def _synthesize_response(self, agent_results: Dict) -> Dict:
        """Synthesize final response from all agents"""
        crisis_data = agent_results.get('crisis_detector', {})
        emotion_data = agent_results.get('emotion_analyzer', {})
        
        # Determine appropriate response
        if crisis_data.get('crisis_level') == 'high':
            response = "🚨 I'm deeply concerned about your safety. Please contact emergency services or a crisis hotline immediately. You are not alone."
        else:
            response = f"🤗 I understand you're feeling {', '.join(emotion_data.get('detected_emotions', []))}. I'm here to support you."
        
        return {
            "response": response,
            "crisis_level": crisis_data.get('crisis_level', 'low'),
            "emotions": emotion_data.get('detected_emotions', []),
            "support_actions": emotion_data.get('support_needs', []),
            "comprehensive_analysis": True
        }

async def main():
    """Main function for command line usage"""
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = input("How are you feeling today? ")
    
    orchestrator = MentalHealthOrchestrator()
    result = await orchestrator.process_message(message)
    
    print(f"\n🎯 SYSTEM RESPONSE:")
    print(f"Response: {result['response']}")
    print(f"Crisis Level: {result['crisis_level'].upper()}")
    print(f"Detected Emotions: {', '.join(result['emotions'])}")

if __name__ == "__main__":
    asyncio.run(main())
