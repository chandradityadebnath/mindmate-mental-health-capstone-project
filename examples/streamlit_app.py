import streamlit as st
from mental_health_bot.agent import MentalHealthAgent

agent = MentalHealthAgent()

st.title("🧠 MindMate – Mental Health AI Agent")

user_text = st.text_area("How are you feeling today?")

if st.button("Submit"):
    response = agent.get_response(user_text)
    st.write("### 🤖 Agent Response:")
    st.write(response)
