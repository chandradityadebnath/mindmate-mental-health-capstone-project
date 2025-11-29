"""
Chat Agent - Generates AI-style supportive responses
"""

import random
from typing import List

class ChatAgent:
    """Generative-style supportive response"""

    def generate(self, message: str, emotions: List[str], crisis_level: str) -> str:
        if crisis_level == "high":
            return (
                "🚨 I’m deeply concerned about your safety. "
                "Please reach out to someone you trust or a crisis hotline immediately. "
                "You are not alone."
            )

        emotion = emotions[0] if emotions else "neutral"

        templates = {
            "sad": [
                "I'm really sorry you're feeling this way. I'm here with you.",
                "It’s okay to feel sad sometimes. You’re not alone.",
            ],
            "anxious": [
                "It's understandable to feel overwhelmed. Take a deep breath—I'm here.",
                "Anxiety can be tough, but we’ll get through it together.",
            ],
            "angry": [
                "It sounds like something really upset you. I'm listening.",
                "Your anger is valid — want to talk about what triggered it?",
            ],
            "happy": [
                "That's wonderful to hear! Tell me more!",
                "Your positivity really shows — keep it going!",
            ],
            "neutral": [
                "I'm here to listen to anything you’d like to share.",
                "Tell me more about how you're doing.",
            ]
        }

        chosen = random.choice(templates.get(emotion, templates["neutral"]))

        return (
            f"{chosen}\n\n"
            f"From what you said, I sensed emotions like: {', '.join(emotions)}.\n"
            "Feel free to talk more about it."
        )
