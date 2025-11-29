import sys
import os

# Add src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import streamlit as st
import asyncio
from mental_health_bot.ai_orchestrator import AIAgentOrchestrator

# Initialize orchestrator
orchestrator = AIAgentOrchestrator()

st.set_page_config(page_title="MindMate AI", page_icon="🧠")

st.title("🧠 MindMate - Mental Health Support AI")
st.write("Talk to me — I'm here to listen and support you ❤️")

# User input
user_input = st.text_area("How are you feeling today?", height=150)

# Button click
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Run asyncio orchestrator
        result = asyncio.run(orchestrator.process(user_input))

        # Display outputs
        st.subheader("🎭 Detected Emotions")
        st.write(result["emotions"])

        if result["crisis_level"] == "high":
            st.error("⚠️ Crisis Situation Detected")

        st.subheader("🤖 MindMate AI Response")
        st.write(result["response"])
