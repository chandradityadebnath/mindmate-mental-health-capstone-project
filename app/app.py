# app/app.py

import sys
import os
import asyncio
import streamlit as st

# Fix for Streamlit Cloud module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from mental_health_bot.ai_orchestrator import AIAgentOrchestrator

# Initialize orchestrator
orchestrator = AIAgentOrchestrator()

# Streamlit page config
st.set_page_config(page_title="MindMate AI", page_icon="🧠")

st.title("🧠 MindMate - Mental Health Support AI")
st.write("Talk to me — I'm here to listen and support you ❤️")

# User input
user_input = st.text_area("How are you feeling today?", height=150)

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Use asyncio.run to handle async processing
        result = asyncio.run(orchestrator.process(user_input))

        # Display emotions
        st.subheader("🎭 Detected Emotions")
        if result["emotions"]:
            st.write(", ".join(result["emotions"]))
        else:
            st.write("No strong emotions detected.")

        # Crisis alert
        if result["crisis_level"] == "high":
            st.error("⚠️ Crisis Situation Detected")

        # AI Response
        st.subheader("🤖 MindMate AI Response")
        st.write(result["response"])
