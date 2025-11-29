from typing import List, Dict, Any
import asyncio
import time
from datetime import datetime
from .agents.emotion_analyzer import EmotionAnalysisAgent
from .agents.crisis_detector import CrisisDetectionAgent
from .agents.support_planner import SupportPlanningAgent
from .agents.resource_matcher import ResourceMatchingAgent
from .tools import MENTAL_HEALTH_TOOLS

class ParallelAgentsSystem:
    """Multi-agent system that works in parallel for comprehensive analysis"""
    
    def __init__(self):
        self.crisis_agent = CrisisDetectionAgent()
        self.emotion_agent = EmotionAnalysisAgent()
        self.support_agent = SupportPlanningAgent()
        self.resource_agent = ResourceMatchingAgent()
        
    async def process_message(self, message: str, user_context: Dict) -> Dict:
        """Process message through all parallel agents"""
        print("🔄 Activating parallel agents...")
        
        # Run all agents in parallel
        tasks = [
            asyncio.create_task(self.crisis_agent.detect_crisis(message, user_context)),
            asyncio.create_task(self.emotion_agent.analyze_emotions(message, user_context)),
            asyncio.create_task(self.support_agent.create_support_plan(message, user_context)),
            asyncio.create_task(self.resource_agent.match_resources(message, user_context))
        ]
        
        # Collect results
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        agent_results = {
            'crisis_detector': results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
            'emotion_analyzer': results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
            'support_planner': results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])},
            'resource_matcher': results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])}
        }
        
        # Synthesize final response
        final_response = self.synthesize_responses(agent_results)
        
        return {
            "agent_results": agent_results,
            "final_response": final_response,
            "agents_used": len([r for r in results if not isinstance(r, Exception)]),
            "timestamp": datetime.now().isoformat()
        }
    
    def synthesize_responses(self, agent_results: Dict) -> Dict:
        """Synthesize responses from all agents into final output"""
        crisis_data = agent_results.get('crisis_detector', {})
        emotion_data = agent_results.get('emotion_analyzer', {})
        support_data = agent_results.get('support_planner', {})
        resource_data = agent_results.get('resource_matcher', {})
        
        # Determine primary response based on crisis level
        crisis_level = crisis_data.get('crisis_level', 'low')
        
        if crisis_level == 'high':
            primary_response = crisis_data.get('coping_strategy', 'Please seek immediate help.')
        else:
            primary_response = emotion_data.get('therapeutic_approach', 'I am here to support you.')
        
        # Generate paragraph response
        response_text = self._generate_paragraph_response(crisis_level, emotion_data, crisis_data)
        
        return {
            "response_text": response_text,
            "primary_response": primary_response,
            "crisis_level": crisis_level,
            "emotions": emotion_data.get('emotions_detected', 'processing'),
            "support_plan": support_data.get('support_plan', {}),
            "resources": resource_data.get('matched_resources', {}),
            "comprehensive_analysis": True,
            "agents_involved": len(agent_results)
        }
    
    def _generate_paragraph_response(self, crisis_level: str, emotion_data: Dict, crisis_data: Dict) -> str:
        """Generate paragraph-length response based on crisis level"""
        emotions = emotion_data.get('emotions_detected', 'your feelings')
        strategy = crisis_data.get('coping_strategy', 'deep breathing and mindfulness')
        resources = "Crisis Text Line (Text HOME to 741741)"
        
        if crisis_level == 'high':
            return f"""Thank you for sharing, and please know that your **safety** is the absolute priority right now. It sounds like you are in a moment of extreme distress. **Please use the immediate crisis resource we have provided: {resources}.** Reaching out right now is an act of courage and strength. Remember that these intense feelings are temporary, but the support available to you is permanent. We are here for you; please reach out for help immediately."""
        
        elif crisis_level == 'medium':
            return f"""I hear the intensity of your **{emotions}** and how overwhelming this must feel. It takes immense courage to articulate these feelings, and you are not alone in this. Let's work on grounding ourselves: when you are ready, try the coping strategy of **{strategy}**. Focusing on a physical or mental exercise can help regain a sense of control over your immediate surroundings. Remember to be kind to yourself—you are stronger than you feel right now, and this will pass."""
        
        else:  # low crisis level
            return f"""Thank you for showing the courage to talk about your **{emotions}**. It is completely valid to feel this way, and acknowledging it is the first step toward positive change. We can explore a helpful strategy like **{strategy}** to manage your current feelings. Building connection and finding motivation is a journey, and I am here to listen and help you explore small, manageable steps forward. Take a moment to validate your own strength in reaching out."""

class MentalHealthOrchestrator:
    """Main orchestrator that coordinates all system components"""
    
    def __init__(self):
        self.parallel_agents = ParallelAgentsSystem()
        self.tools = MENTAL_HEALTH_TOOLS
        
    async def process_user_message(self, user_message: str, user_id: str = None, session_id: str = None) -> Dict:
        """Main method to process user messages through entire system"""
        
        # Start timing for performance metrics
        start_time = time.time()
        
        print(f"🎯 Processing message for user: {user_id}")
        
        # Step 1: Initial crisis assessment
        initial_crisis = self.tools.crisis_detector(user_message)
        
        # Step 2: Parallel agent processing
        user_context = {}  # Could be extended with user history
        agent_results = await self.parallel_agents.process_message(user_message, user_context)
        
        # Step 3: Generate comprehensive output
        processing_time = time.time() - start_time
        
        comprehensive_output = {
            'user_id': user_id,
            'session_id': session_id,
            'processing_time_seconds': round(processing_time, 2),
            'crisis_assessment': initial_crisis,
            'agent_analysis': agent_results['agent_results'],
            'final_response': agent_results['final_response'],
            'system_metrics': {
                'agents_used': agent_results['final_response'].get('agents_involved', 0),
                'crisis_detected': initial_crisis['crisis_level'] in ['medium', 'high'],
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Processing complete! Time: {processing_time:.2f}s")
        print(f"📊 Crisis Level: {agent_results['final_response'].get('crisis_level', 'low').upper()}")
        print(f"🤖 Agents Used: {agent_results['final_response'].get('agents_involved', 0)}")
        
        return comprehensive_output
