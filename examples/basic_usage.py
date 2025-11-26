#!/usr/bin/env python3
"""
Basic usage example for Mental Health Agent System
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import MentalHealthOrchestrator

async def example_usage():
    """Demonstrate basic system usage"""
    print("🧠 Mental Health Agent System - Basic Usage")
    print("=" * 50)
    
    orchestrator = MentalHealthOrchestrator()
    
    # Test messages
    test_messages = [
        "I'm feeling really anxious about my upcoming exam",
        "I had a great day with friends",
        "I don't want to live anymore"
    ]
    
    for message in test_messages:
        print(f"\n💬 User: {message}")
        result = await orchestrator.process_message(message)
        print(f"🤖 System: {result['response']}")
        print(f"📊 Crisis Level: {result['crisis_level']}")
        print(f"🎭 Emotions: {result['emotions']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
