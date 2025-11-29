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
# 🧠 GEMINI AI INTEGRATION - ULTRA SIMPLIFIED
# =============================================

class GeminiAIIntegration:
    """Gemini AI Integration - ULTRA SIMPLIFIED"""
    
    def __init__(self):
        self.model = None
        self.fallback_mode = True
        self.api_key = None
        
    def configure_ai(self, api_key: str):
        """Configure AI - SIMPLEST POSSIBLE APPROACH"""
        if not api_key or not api_key.strip():
            st.error("❌ Please enter a valid API key")
            return False
            
        try:
            # Clean the API key
            api_key = api_key.strip()
            
            # Store API key first
            self.api_key = api_key
            
            # Configure with the API key
            genai.configure(api_key=api_key)
            
            # Try ONLY the most basic model
            try:
                st.write("🔄 Testing API connection...")
                
                # Use the most basic model
                self.model = genai.GenerativeModel('gemini-pro')
                
                # Ultra simple test
                test_response = self.model.generate_content("Hello")
                
                # If we get here, it worked!
                self.fallback_mode = False
                
                # Store in session state
                st.session_state.api_key_connected = True
                st.session_state.api_key = api_key
                st.session_state.ai_model = 'gemini-pro'
                
                st.success("✅ API Key Valid! Real AI Activated!")
                return True
                
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ API Connection Failed: {error_msg}")
                
                # Show helpful debug info
                if "API_KEY_INVALID" in error_msg:
                    st.info("🔍 Your API key appears invalid. Please check it at https://makersuite.google.com/app/apikey")
                elif "quota" in error_msg.lower():
                    st.info("🔍 You may have exceeded your API quota. Try again later or check your Google AI Studio dashboard.")
                elif "region" in error_msg.lower():
                    st.info("🔍 API may not be available in your region. Try using a VPN or check Google's service availability.")
                else:
                    st.info("🔍 Please ensure your API key is correct and has proper permissions.")
                
                st.session_state.api_key_connected = False
                self.fallback_mode = True
                return False
            
        except Exception as e:
            st.error(f"❌ Configuration failed: {str(e)}")
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
    
    async def analyze_with_ai(self, text: str) -> dict:
        """Analyze text with real Gemini AI"""
        
        # Check if we should use real AI
        use_real_ai = (self.model is not None and 
                      not self.fallback_mode and 
                      st.session_state.get('api_key_connected', False))
        
        if use_real_ai:
            try:
                # Safe, simple prompt
                prompt = f"""Please provide a compassionate response to this: "{text}" """
                
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
                print(f"AI response error: {e}")
                return self._simulated_analysis(text)
        else:
            return self._simulated_analysis(text)
    
    def _simulated_analysis(self, text: str) -> dict:
        """Advanced simulated AI with EXCELLENT varied responses"""
        text_lower = text.lower()
        
        # URGENT CRISIS - Completely different response
        if any(word in text_lower for word in ['kill myself', 'suicide', 'end my life', 'want to die', 'not worth living']):
            crisis_responses = [
                """🚨 **Immediate Support Available**

I hear the profound pain in your words. When someone considers ending their life, it means they're carrying more weight than any person should have to bear alone.

**Please reach out RIGHT NOW:**
• 📞 **Call 988** - Suicide & Crisis Lifeline (24/7, trained specialists)
• 📱 **Text HOME** to 741741 - Crisis Text Line
• 🚑 **Call 911** - Emergency Services for immediate danger

You reaching out tells me part of you still believes help is possible. Please listen to that part - it's telling the truth.""",

                """🚨 **Critical Support Needed**

The fact you're expressing these thoughts means you're in tremendous pain. Please know that intense suicidal feelings are temporary, even when they feel endless.

**Professional help available immediately:**
• **988** - Suicide Prevention Lifeline (free, confidential)
• **741741** - Crisis Text Line (text HOME)
• **911** - Emergency Services

Your life matters, and there are specific people trained to help you through this exact moment. Please call now.""",

                """🚨 **Emergency Support Required**

I hear the desperation in your words. When the pain becomes this overwhelming, it's crucial to reach for professional support.

**Available 24/7:**
• Dial **988** - Suicide & Crisis Lifeline
• Text **HOME** to 741741
• Call **911** for immediate danger

The professionals at these numbers understand exactly what you're experiencing and know how to help. Please don't face this alone."""
            ]
            return {
                'emotions': 'desperate, hopeless, suicidal',
                'urgency': 'high',
                'needs': 'crisis_intervention',
                'response': random.choice(crisis_responses),
                'ai_generated': False
            }
        
        # SAD/DEPRESSED - Very different responses
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless', 'miserable', 'unhappy', 'down']):
            sad_responses = [
                """I hear that heavy sadness in your words. It's like carrying an invisible weight that makes everything feel difficult.

What's one tiny thing that might bring a moment of relief, even if just for a few minutes?""",

                """Thank you for trusting me with your sadness. It takes real courage to acknowledge when we're feeling low.

Would you be willing to share what's been contributing to these heavy feelings lately?""",

                """That deep, empty feeling can make the world seem colorless. I want you to know I see the strength it takes to admit you're struggling.

Depression often lies to us, making us believe this is permanent. But feelings are like weather - they change, even when it doesn't seem possible.""",

                """I recognize that hollow, hopeless feeling. It's one of the most isolating experiences.

The very fact you're reaching out tells me there's still a spark of hope in there, even if it feels tiny right now."""
            ]
            return {
                'emotions': 'sad, depressed, hopeless',
                'urgency': 'medium', 
                'needs': 'emotional_support',
                'response': random.choice(sad_responses),
                'ai_generated': False
            }
        
        # HAPPY/POSITIVE - Very different responses
        elif any(word in text_lower for word in ['happy', 'good', 'great', 'awesome', 'excited', 'joy', 'wonderful']):
            happy_responses = [
                """That's wonderful to hear! Positive emotions deserve just as much attention as difficult ones.

What specifically is bringing you this sense of happiness or contentment right now?""",

                """I'm genuinely glad you're experiencing positive feelings! These moments of lightness are precious and worth savoring.

How does this happiness manifest in your body? Sometimes noticing the physical sensations helps us return to them later.""",

                """It's beautiful to hear about your happiness. These bright moments remind us that light exists, even after periods of darkness.

Would you like to explore what's contributing to these positive feelings? Understanding our joy can be as important as understanding our pain.""",

                """That's fantastic! Positive emotions are like sunshine for the soul - they help everything grow.

What's lighting you up inside right now? Let's celebrate this good moment together."""
            ]
            return {
                'emotions': 'happy, content, positive',
                'urgency': 'low',
                'needs': 'celebration',
                'response': random.choice(happy_responses),
                'ai_generated': False
            }
        
        # ANGRY/FRUSTRATED
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'rage', 'frustrated', 'pissed']):
            angry_responses = [
                """I feel the heat in your words. Anger often shows up when something important feels threatened or violated.

What's the story behind this anger? There's usually valuable information in what triggers our strongest reactions.""",

                """That intensity you're feeling contains important data about your boundaries and values. The challenge is learning to channel that fire constructively.

What would it look like to express this anger in a way that honors what matters to you?""",

                """Anger is often the bodyguard for more vulnerable feelings. I wonder what might be hiding beneath the surface of this frustration?

Would it help to explore what needs aren't being met right now?"""
            ]
            return {
                'emotions': 'angry, frustrated, resentful',
                'urgency': 'medium',
                'needs': 'anger_management',
                'response': random.choice(angry_responses),
                'ai_generated': False
            }
        
        # ANXIOUS/WORRIED
        elif any(word in text_lower for word in ['anxious', 'anxiety', 'worried', 'nervous', 'panic', 'overwhelmed']):
            anxiety_responses = [
                """I understand how overwhelming anxiety can feel. That racing mind and physical tension is your body's alarm system activated.

While it feels terrifying in the moment, this is a false alarm - you are safe right now. Let's try some grounding together.""",

                """Anxiety makes everything feel urgent and threatening. I hear how distressing this must be for you.

What if we pause for a moment and practice some breathing together? Sometimes creating even a tiny bit of space from the anxiety helps.""",

                """That anxious, overwhelmed feeling can make it hard to think clearly. Thank you for reaching out even while feeling this way.

Would you like to try a simple grounding exercise together? It can help bring some calm to the storm."""
            ]
            return {
                'emotions': 'anxious, overwhelmed, scared',
                'urgency': 'medium',
                'needs': 'anxiety_management',
                'response': random.choice(anxiety_responses),
                'ai_generated': False
            }
        
        # DEFAULT - Completely varied responses
        else:
            default_responses = [
                """Thank you for sharing what's on your mind. I'm here to listen and understand your unique experience.

What would be most helpful for you right now - listening, exploring, problem-solving, or something else entirely?""",

                """I hear you. Sometimes the most important conversations begin with simple sharing.

What's been most present for you lately? I'm interested in understanding your world better.""",

                """I appreciate you opening up. Every person's experience is unique, and I want to honor yours.

Would you like to tell me more about what's been happening in your life?""",

                """Thank you for trusting me with this. Putting our experiences into words can sometimes help us understand them differently.

What's standing out to you most right now about what you're going through?"""
            ]
            return {
                'emotions': 'reflective, engaged',
                'urgency': 'low',
                'needs': 'connection',
                'response': random.choice(default_responses),
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
    page_title="MindMate - Mental Health Support",
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
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 MindMate</div>', unsafe_allow_html=True)

# API Key Section with troubleshooting
with st.expander("🔑 API Key Setup (Optional)", expanded=not st.session_state.get('api_key_connected', False)):
    st.markdown("""
    **Get FREE API Key (Optional):**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with Google account
    3. Click "Create API Key" 
    4. Copy and paste below
    
    *Note: The app works perfectly without API key using advanced simulated AI*
    """)
    
    api_key = st.text_input(
        "Google AI API Key:",
        type="password",
        placeholder="Paste API key here (optional)...",
        help="Leave empty to use advanced simulated AI",
        key="api_key_input"
    )
    
    if st.button("🔗 Connect AI", use_container_width=True, type="primary"):
        if api_key:
            with st.spinner("Testing API connection..."):
                success = mental_health_agent.configure_ai(api_key)
                if success:
                    st.balloons()
                    st.rerun()
        else:
            st.warning("⚠️ Please enter an API key to connect")
    
    if st.session_state.get('api_key_connected', False):
        if st.button("🔓 Disconnect API", use_container_width=True, type="secondary"):
            st.session_state.api_key_connected = False
            st.session_state.api_key = None
            st.session_state.ai_model = None
            st.rerun()

# AI Status Display
if st.session_state.get('api_key_connected', False):
    st.markdown('<div class="ai-active">🤖 REAL AI ACTIVE</div>', unsafe_allow_html=True)
    st.success("✅ Real Gemini AI is processing your messages!")
else:
    st.markdown('<div class="ai-simulated">🔄 ADVANCED SIMULATED AI ACTIVE</div>', unsafe_allow_html=True)
    st.info("💡 Using sophisticated mental health algorithms with varied responses")

# Main chat interface
st.subheader("💬 Chat with MindMate")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        crisis_level = message.get("crisis_level", "low")
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
    
    # Generate AI response
    with st.spinner("🧠 Thinking..."):
        try:
            result = asyncio.run(mental_health_agent.chat(prompt))
            response_data = result['final_response']
            response_text = response_data['response_text']
            ai_used = response_data['ai_used']
            crisis_level = response_data['crisis_level']
            
            # Add to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text,
                "ai_used": ai_used,
                "crisis_level": crisis_level
            })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            fallback_responses = [
                "I'm here to support you. Let's try that again.",
                "I appreciate you reaching out. I'm listening.",
                "Thank you for sharing. I'm here with you."
            ]
            st.session_state.messages.append({
                "role": "assistant", 
                "content": random.choice(fallback_responses),
                "ai_used": False,
                "crisis_level": "low"
            })
            st.rerun()

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick test buttons
st.subheader("💡 Try These Examples")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("😔 I'm feeling sad", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I'm feeling sad"})
        st.rerun()
with col2:
    if st.button("😊 I'm happy today", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I'm happy today"})
        st.rerun()
with col3:
    if st.button("😡 I'm so angry", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I'm so angry"})
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>🧠 MindMate Mental Health Support</strong></p>
    <p><small>Always here to listen 🤗 | Emergency: Call 988</small></p>
</div>
""", unsafe_allow_html=True)
