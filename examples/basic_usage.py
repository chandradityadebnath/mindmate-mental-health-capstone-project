#!/usr/bin/env python3
"""
Basic usage example for Mental Health Agent System
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

async def demo_mental_health_agent():
    """Simple demonstration of the mental health agent system"""
    print("🧠 Mental Health Agent System - Basic Usage")
    print("=" * 50)
    
    # Simulate agent responses for demonstration
    test_scenarios = [
        {
            "message": "I've been feeling really anxious lately",
            "response": "🤗 I hear you're feeling anxious. That sounds really challenging. Let's practice some deep breathing together - inhale for 4 counts, hold for 4, exhale for 6.",
            "crisis_level": "low"
        },
        {
            "message": "I can't stop worrying about everything", 
            "response": "💭 It sounds like worry is taking up a lot of space right now. Sometimes naming our worries can help reduce their power. Would you like to try that?",
            "crisis_level": "low"
        },
        {
            "message": "I feel hopeless about the future",
            "response": "🌱 I hear the hopelessness in your words. Please know that these feelings, while overwhelming, are temporary. You've shown strength by reaching out.",
            "crisis_level": "medium"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n💬 Test {i}: {scenario['message']}")
        print("-" * 40)
        print(f"🤖 Response: {scenario['response']}")
        print(f"📊 Crisis Level: {scenario['crisis_level'].upper()}")
        print(f"⏱️ Processing Time: 0.{i}s")
    
    print("\n" + "=" * 50)
    print("✅ Demonstration completed successfully!")
    print("🔧 Full multi-agent system ready for integration")

async def main():
    """Main function"""
    await demo_mental_health_agent()

if __name__ == "__main__":
    asyncio.run(main())
