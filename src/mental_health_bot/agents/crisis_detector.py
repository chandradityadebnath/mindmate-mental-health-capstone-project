"""
Crisis Detection Agent
"""

from typing import Dict

class CrisisDetectionAgent:
    """Detects if the user message indicates a crisis"""

    def __init__(self):
        self.crisis_keywords = ["suicide", "kill myself", "end my life", "hopeless", "die"]

    async def analyze(self, message: str) -> Dict:
        message_lower = message.lower()
        for kw in self.crisis_keywords:
            if kw in message_lower:
                return {"crisis_level": "high"}
        return {"crisis_level": "low"}
