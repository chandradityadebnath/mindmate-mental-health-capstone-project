import streamlit as st
import asyncio
import time
from datetime import datetime
import nest_asyncio
import google.generativeai as genai
import os
import random

# Apply nest_asyncio to handle async in Streamlit
nest_asyncio.apply()

# =============================================
# 🧠 GEMINI AI INTEGRATION - SIMPLIFIED & FIXED
# =============================================

class GeminiAIIntegration:
    """Gemini AI Integration - SIMPLIFIED AND WORKING"""
    
    def __init__(self):
        self.model = None
        self.fallback_mode = True
        self.api_key = None
        
    def configure_ai(self, api_key: str):
        """Configure AI with user-provided API key - SIMPLIFIED"""
        if not api_key or not api_key.strip():
            st.error("❌ Please enter a valid API key")
            return False
            
        try:
            # Clean the API key
            api_key = api_key.strip()
            
            # Configure with the API key
            genai.configure(api_key=api_key)
            
            # Try the most common working models
            models_to_try = [
                'gemini-pro',  # Most reliable
                'gemini-1.0-pro',
                'gemini-1.5-flash-latest',
                'gemini-1.5-pro-latest'
            ]
            
            for model_name in models_to_try:
                try:
                    st.write(f"🔄 Trying model: {model_name}...")
                    self.model = genai.GenerativeModel(model_name)
                    
                    # Simple test - don't use content that might trigger filters
                    test_response = self.model.generate_content("Say hello in one word")
                    
                    # If we get here, the model works
                    self.fallback_mode = False
                    self.api_key = api_key
                    
                    # Store in session state
                    st.session_state.api_key_connected = True
                    st.session_state.api_key = api_key
                    st.session_state.ai_model = model_name
                    
                    st.success(f"✅ Connected to: {model_name}")
                    return True
                    
                except Exception as e:
                    st.write(f"❌ {model_name} failed: {str(e)[:100]}...")
                    continue
                    
            # If no models work
            st.error("❌ All models failed. Please check your API key and try again.")
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
            
        except Exception as e:
            st.error(f"❌ API configuration failed: {str(e)}")
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
    
    async def analyze_with_ai(self, text: str) -> dict:
        """Analyze text with real Gemini AI"""
        print(f"🔍 Analyzing: '{text}'")
        
        # Check if we should use real AI
        use_real_ai = (self.model is not None and 
                      not self.fallback_mode and 
                      st.session_state.get('api_key_connected', False))
        
        if use_real_ai:
            try:
                # Simple, safe prompt that won't trigger content filters
                prompt = f"""
                User message: "{text}"
                
                As a supportive listener, provide a compassionate response to this message.
                Keep it warm, understanding, and helpful.
                """
                
                response = self.model.generate_content(prompt)
                response_text = response.text
                
                return {
                    'emotions': 'ai_analyzed',
                    'urgency': 'medium', 
                    'needs': 'ai_determined',
                    'response': response_text,
                    'ai_generated': True
                }
                
            except Exception as e:
                print(f"❌ AI Error: {e}")
                st.warning("⚠️ AI temporarily unavailable, using advanced simulated responses")
                return self._simulated_analysis(text)
        else:
            return self._simulated_analysis(text)
    
    def _simulated_analysis(self, text: str) -> dict:
        """Advanced simulated AI analysis with varied responses"""
        text_lower = text.lower()
        
        # Crisis detection
        if any(word in text_lower for word in ['kill myself', 'suicide', 'end my life', 'want to die', 'not worth living']):
            return {
                'emotions': 'desperate, hopeless, suicidal',
                'urgency': 'high',
                'needs': 'crisis_intervention',
                'response': """🚨 **Urgent Support Needed**

I hear the depth of your pain. When someone considers ending their life, it means they're carrying an unbearable weight.

**Please reach out now:**
• 📞 Call 988 - Suicide & Crisis Lifeline (24/7)
• 📱 Text HOME to 741741 - Crisis Text Line
• 🚑 Call 911 - Emergency Services

You don't have to face this alone. Professional help is available right now.""",
                'ai_generated': False
            }
        
        # Sad/Depressed responses - VARIED
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless', 'miserable', 'unhappy']):
            responses = [
                """I hear the weight in your words. That heavy feeling can make everything seem difficult.

What's one small thing that might bring a moment of relief, even if temporary?""",
                
                """Thank you for sharing that you're feeling sad. It takes courage to acknowledge when we're struggling.

Would you like to talk about what's been contributing to these feelings?""",
                
                """I understand that sad, empty feeling. It can make the world seem gray.

Remember that feelings, even intense ones, are temporary visitors. What might help you get through this moment?"""
            ]
            return {
                'emotions': 'sad, depressed, hopeless',
                'urgency': 'medium', 
                'needs': 'emotional_support',
                'response': random.choice(responses),
                'ai_generated': False
            }
        
        # Happy/Positive responses - VARIED
        elif any(word in text_lower for word in ['happy', 'good', 'great', 'awesome', 'excited', 'joy']):
            responses = [
                """That's wonderful to hear! It's important to celebrate positive moments too.

What's bringing you this happiness right now?""",
                
                """I'm glad you're feeling good! Positive emotions deserve attention and appreciation.

How does this happiness feel in your body?""",
                
                """It's beautiful to hear about your happiness. These moments remind us of life's brightness.

Would you like to explore what's creating these positive feelings?"""
            ]
            return {
                'emotions': 'happy, content, positive',
                'urgency': 'low',
                'needs': 'celebration',
                'response': random.choice(responses),
                'ai_generated': False
            }
        
        # Angry/Frustrated responses
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'rage', 'frustrated']):
            return {
                'emotions': 'angry, frustrated, resentful',
                'urgency': 'medium',
                'needs': 'anger_management',
                'response': """I feel the intensity in your words. Anger often signals that something important to us feels threatened.

What's beneath this anger? There's usually hurt or fear waiting to be heard.""",
                'ai_generated': False
            }
        
        # Default varied responses
        else:
            responses = [
                """Thank you for sharing. I'm here to listen and understand what you're experiencing.

What would be most helpful for you right now?""",
                
                """I hear you. Sometimes putting our experiences into words can help us understand them better.

What's on your mind?""",
                
                """I'm listening. Every person's experience is unique, and I want to understand yours.

Would you like to tell me more?"""
            ]
            return {
                'emotions': 'reflective, engaged',
                'urgency': 'low',
                'needs': 'connection',
                'response': random.choice(responses),
                'ai_generated': False
            }

# =============================================
# 🧠 MENTAL HEALTH AGENT
# =============================================

class MentalHealthAgent:
    """Mental Health Agent"""
    
    def __init__(self):
        self.ai = GeminiAIIntegration()
        
        # Initialize session state
        if 'api_key_connected' not in st.session_state:
            st.session_state.api_key_connected = False
        if 'api_key' not in st.session_state:
            st.session_state.api_key = None
        if 'ai_model' not in st.session_state:
            st.session_state.ai_model = None
    
    def configure_ai(self, api_key: str) -> bool:
        """Configure the AI with user API key"""
        return self.ai.configure_ai(api_key)
    
    async def chat(self, message: str, user_id: str = "anonymous") -> dict:
        """Main chat method"""
        start_time = time.time()
        
        # Use AI analysis
        ai_analysis = await self.ai.analyze_with_ai(message)
        
        processing_time = time.time() - start_time
        
        return {
            'user_id': user_id,
            'processing_time_seconds': round(processing_time, 2),
            'final_response': {
                "response_text": ai_analysis['response'],
                "crisis_level": ai_analysis['urgency'],
                "emotions": ai_analysis['emotions'],
                "ai_used": ai_analysis['ai_generated'],
                "agents_involved": 4,
            },
            'timestamp': datetime.now().isoformat()
        }

# =============================================
# 🎨 STREAMLIT APP
# =============================================

# Initialize the agent
mental_health_agent = MentalHealthAgent()

# Streamlit app configuration
st.set_page_config(
    page_title="MindMate - AI Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .ai-active {
        background-color: #e6f7f2;
        color: #00cc96;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #00cc96;
        margin: 1rem 0;
    }
    .ai-simulated {
        background-color: #fff4e6;
        color: #ffa500;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #ffa500;
        margin: 1rem 0;
    }
    .crisis-high {
        border-left: 5px solid #ff4b4b;
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 MindMate AI</div>', unsafe_allow_html=True)

# API Key Section
with st.expander("🔑 Connect Your Google AI API Key", expanded=True):
    st.markdown("""
    **Get your FREE API key:**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with Google account
    3. Click "Create API Key"
    4. Copy and paste below
    """)
    
    api_key = st.text_input(
        "Google AI API Key:",
        type="password",
        placeholder="Paste your API key here...",
        help="Get free API key from https://makersuite.google.com/app/apikey",
        key="api_key_input"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔗 Connect AI", use_container_width=True, type="primary"):
            if api_key:
                with st.spinner("Connecting to AI services..."):
                    success = mental_health_agent.configure_ai(api_key)
                    if success:
                        st.balloons()
                        st.rerun()
            else:
                st.warning("⚠️ Please enter an API key")
    
    with col2:
        if st.session_state.get('api_key_connected', False):
            if st.button("🔓 Disconnect", use_container_width=True):
                st.session_state.api_key_connected = False
                st.session_state.api_key = None
                st.session_state.ai_model = None
                st.rerun()

# AI Status Display
if st.session_state.get('api_key_connected', False):
    st.markdown(f'<div class="ai-active">🤖 REAL AI ACTIVE - Using {st.session_state.get("ai_model", "Gemini")}</div>', unsafe_allow_html=True)
    st.success("✅ Your API key is working! Messages will use real AI.")
else:
    st.markdown('<div class="ai-simulated">🔄 ADVANCED SIMULATED AI ACTIVE</div>', unsafe_allow_html=True)
    st.info("💡 Connect your API key above for real AI responses")

# Main chat interface
st.subheader("💬 Chat with MindMate")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        crisis_level = message.get("crisis_level", "low")
        with st.chat_message("assistant"):
            if crisis_level == "high":
                st.markdown(f'<div class="crisis-high">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
            
            if "ai_used" in message:
                if message["ai_used"]:
                    st.caption("🤖 Generated by Real Gemini AI")
                else:
                    st.caption("🔄 Advanced Simulated Response")

# Chat input
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):
            try:
                result = asyncio.run(mental_health_agent.chat(prompt))
                response_data = result['final_response']
                response_text = response_data['response_text']
                ai_used = response_data['ai_used']
                crisis_level = response_data['crisis_level']
                
                # Display with appropriate styling
                if crisis_level == "high":
                    st.markdown(f'<div class="crisis-high">{response_text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(response_text)
                
                # Show AI usage
                if ai_used:
                    st.caption("🤖 Generated by Real Gemini AI")
                else:
                    st.caption("🔄 Advanced Simulated Response")
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "ai_used": ai_used,
                    "crisis_level": crisis_level
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                fallback = "I'm here to support you. Let's try that again."
                st.markdown(fallback)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": fallback,
                    "ai_used": False,
                    "crisis_level": "low"
                })
    
    st.rerun()

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>🧠 MindMate AI Mental Health Support</strong></p>
    <p><small>Always here to listen 🤗 | For emergencies: Call 988</small></p>
</div>
""", unsafe_allow_html=True)
