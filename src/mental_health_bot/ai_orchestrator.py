"""
High-level orchestrator for a chatbot-style AI response.
"""

import asyncio
from src.agents.crisis_detector import CrisisDetectionAgent
from src.agents.emotion_analyzer import EmotionAnalysisAgent
from src.agents.chat_agent import ChatAgent


class AIAgentOrchestrator:

    def __init__(self):
        self.crisis_agent = CrisisDetectionAgent()
        self.emotion_agent = EmotionAnalysisAgent()
        self.chat_agent = ChatAgent()

    async def process(self, message: str):
        crisis_task = asyncio.create_task(self.crisis_agent.analyze(message))
        emotion_task = asyncio.create_task(self.emotion_agent.analyze(message))

        crisis_result = await crisis_task
        emotion_result = await emotion_task

        crisis_level = crisis_result.get("crisis_level", "low")
        emotions = emotion_result.get("detected_emotions", [])

        final_response = self.chat_agent.generate(
            message=message,
            emotions=emotions,
            crisis_level=crisis_level
        )

        return {
            "response": final_response,
            "crisis_level": crisis_level,
            "emotions": emotions
        }
