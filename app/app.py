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
# 🧠 GEMINI AI INTEGRATION - FIXED MODEL NAMES
# =============================================

class GeminiAIIntegration:
    """Gemini AI Integration - FIXED WITH CORRECT MODEL NAMES"""
    
    def __init__(self):
        self.model = None
        self.fallback_mode = True
        self.api_key = None
        
    def configure_ai(self, api_key: str):
        """Configure AI with user-provided API key"""
        if not api_key:
            return False
            
        try:
            genai.configure(api_key=api_key)
            
            # **FIXED: CORRECT Gemini model names**
            models_to_try = [
                'gemini-1.5-flash',      # Latest fast model
                'gemini-1.5-pro',        # Latest high-quality model
                'gemini-1.0-pro',        # Stable version
                'gemini-pro',            # Alternative name
            ]
            
            for model_name in models_to_try:
                try:
                    print(f"🧪 Testing model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    # Quick test
                    test_response = self.model.generate_content("Say 'AI Ready'")
                    self.fallback_mode = False
                    self.api_key = api_key
                    
                    # Store in session state
                    st.session_state.api_key_connected = True
                    st.session_state.api_key = api_key
                    st.session_state.ai_model = model_name
                    
                    print(f"✅ AI Connected to: {model_name}")
                    return True
                except Exception as e:
                    print(f"❌ Model {model_name} failed: {str(e)}")
                    continue
            
            # If we get here, try to discover available models
            print("🔍 Discovering available models...")
            try:
                available_models = genai.list_models()
                print("Available models:")
                for model in available_models:
                    if 'generateContent' in model.supported_generation_methods:
                        print(f"   ✅ {model.name}")
                        # Try this model
                        try:
                            self.model = genai.GenerativeModel(model.name)
                            test_response = self.model.generate_content("Test")
                            self.fallback_mode = False
                            self.api_key = api_key
                            st.session_state.api_key_connected = True
                            st.session_state.api_key = api_key
                            st.session_state.ai_model = model.name
                            print(f"✅ Connected to discovered model: {model.name}")
                            return True
                        except:
                            continue
            except Exception as e:
                print(f"❌ Model discovery failed: {e}")
                    
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
            
        except Exception as e:
            print(f"❌ API config failed: {e}")
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
    
    async def analyze_with_ai(self, text: str) -> dict:
        """Analyze text with real Gemini AI"""
        print(f"🔍 Analyzing: '{text}'")
        print(f"🤖 AI Status: Model={self.model is not None}, Fallback={self.fallback_mode}")
        
        # Check if we should use real AI
        use_real_ai = (self.model is not None and 
                      not self.fallback_mode and 
                      st.session_state.get('api_key_connected', False))
        
        print(f"🎯 Use Real AI: {use_real_ai}")
        
        if use_real_ai:
            try:
                # Better prompt for mental health support
                prompt = f"""
                You are a compassionate mental health support assistant. The user said: "{text}"
                
                Please provide a supportive, empathetic response that:
                - Validates their feelings
                - Offers specific, helpful suggestions
                - Shows genuine care and understanding
                - Avoids generic phrases
                - Is tailored to their specific message
                
                Keep it conversational and warm.
                """
                
                print("🚀 Sending to Gemini AI...")
                response = self.model.generate_content(prompt)
                response_text = response.text
                print(f"🤖 RAW AI RESPONSE: {response_text}")
                
                return {
                    'emotions': 'ai_analyzed',
                    'urgency': 'medium', 
                    'needs': 'ai_determined',
                    'response': response_text,
                    'ai_generated': True
                }
                
            except Exception as e:
                print(f"❌ AI Error: {e}")
                st.error(f"AI Error: {str(e)}")
                return self._simulated_analysis(text)
        else:
            print("🔄 Using simulated AI (real AI not available)")
            return self._simulated_analysis(text)
    
    def _simulated_analysis(self, text: str) -> dict:
        """Advanced simulated AI analysis - VARIED RESPONSES"""
        text_lower = text.lower()
        print(f"🔍 Simulated analysis for: '{text_lower}'")
        
        # More varied responses based on content
        if any(word in text_lower for word in ['kill myself', 'suicide', 'end my life', 'want to die', 'not worth living']):
            crisis_responses = [
                """🚨 **I hear the depth of your pain**

When someone considers ending their life, it means they're carrying an unbearable weight. Please know there are specific people trained to help right now.

**Immediate support:**
• Call 988 - Suicide & Crisis Lifeline (24/7)
• Text HOME to 741741 - Crisis Text Line
• Call 911 - Emergency Services

You reaching out tells me part of you still believes help is possible. Please listen to that part.""",
                
                """🚨 **Your safety is the priority**

I can hear the hopelessness in your words. When pain feels endless, it's hard to see any other way. But there are people who understand exactly what you're experiencing.

**Right now:**
• 988 - Suicide Prevention (24/7)
• 741741 - Crisis Text Line
• 911 - Immediate emergency

The fact you're sharing this means part of you wants help. Please reach out now.""",
                
                """🚨 **I'm deeply concerned**

When someone talks about ending their life, it means the pain has become overwhelming. There are specific resources for exactly this moment.

**Please contact:**
• 988 - They understand and can help
• Text HOME to 741741 - For when talking is hard
• 911 - If you're in immediate danger

You don't have to face this alone. Help is available right now."""
            ]
            return {
                'emotions': 'desperate, hopeless, suicidal',
                'urgency': 'high',
                'needs': 'crisis_intervention',
                'response': random.choice(crisis_responses),
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless', 'miserable', 'unhappy']):
            sad_responses = [
                """I recognize that heavy sadness. It's like carrying invisible weights everywhere you go. 

What if we just acknowledge this feeling together? Sometimes naming the weight is the first step toward lightening it.

Has there been any moment, even a brief one, where the heaviness felt slightly less intense?""",
                
                """That deep sadness can make the world feel gray. I want you to know I see the courage it takes to admit you're feeling this way.

Depression often tells us lies about permanence, but feelings are always changing. They're visitors, not residents.

What's one small thing that sometimes brings you a moment of relief, even temporarily?""",
                
                """I hear the emptiness in what you're sharing. That hollow, nothing-matters feeling is one of the most isolating experiences.

You're not broken - you're responding to something painful. The very fact you're reaching out tells me there's still hope present.

Could we explore what that hopeful part might need right now?"""
            ]
            return {
                'emotions': 'sad, depressed, hopeless',
                'urgency': 'medium', 
                'needs': 'emotional_support',
                'response': random.choice(sad_responses),
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['happy', 'good', 'great', 'awesome', 'excited', 'joy']):
            happy_responses = [
                """That's wonderful to hear! Positive emotions deserve just as much attention as difficult ones.

What's creating this sense of happiness for you? Understanding our joy can be as important as understanding our pain.

Let's celebrate this good moment together.""",
                
                """I'm genuinely glad you're experiencing positive feelings! These moments of lightness are precious and worth savoring.

What does this happiness feel like physically? Noticing the bodily sensations can help us return to them later.

Would you like to explore what's contributing to these good feelings?""",
                
                """It's beautiful to hear about your happiness! These moments remind us that light exists, even after periods of darkness.

What aspects of this positive experience stand out most to you? Sometimes articulating our joy helps us appreciate it more deeply."""
            ]
            return {
                'emotions': 'happy, content, positive',
                'urgency': 'low',
                'needs': 'celebration',
                'response': random.choice(happy_responses),
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'rage', 'annoyed']):
            anger_responses = [
                """I feel the intensity in your words. Anger often shows up when something important has been threatened or violated.

That fire you're feeling contains valuable information about your boundaries and values. The energy isn't the problem - it's about learning to channel it constructively.

What's the story behind this anger?""",
                
                """Anger can feel like a storm inside. It often points to places where our boundaries have been crossed or our values challenged.

This intensity contains important data about what matters to you. How might we honor that information while finding constructive outlets?

What triggered this feeling for you?"""
            ]
            return {
                'emotions': 'angry, frustrated, resentful',
                'urgency': 'medium',
                'needs': 'anger_management',
                'response': random.choice(anger_responses),
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['anxious', 'worried', 'nervous', 'panic', 'overwhelmed']):
            anxiety_responses = [
                """I understand how overwhelming anxiety can feel. That racing mind and physical tension is your body's alarm system activated.

While it feels terrifying, this is a false alarm - you are safe in this moment. Let's try some grounding together.

**Breathe with me**: Inhale 4 counts, hold 4, exhale 6. Let's do this 3 times.""",
                
                """Anxiety can make everything feel urgent and threatening. I want you to know that what you're feeling is your protective system working overtime.

You're not in danger right now, even though it feels that way. Let's practice being present together.

**5-4-3-2-1 Grounding**: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you can taste."""
            ]
            return {
                'emotions': 'anxious, overwhelmed, scared',
                'urgency': 'medium',
                'needs': 'anxiety_management', 
                'response': random.choice(anxiety_responses),
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['no', 'nothing', 'dont know', 'not sure', 'idk']):
            uncertain_responses = [
                """Sometimes "no" or "I don't know" is the most honest place to be. There's no pressure to have everything figured out.

We can just sit in this space of not-knowing together. What's it like for you to not have an answer right now?""",
                
                """I hear your uncertainty. Not knowing what to say or feel is actually a very authentic place to be.

You don't need to perform or have everything sorted out. We can explore this space of ambiguity together.

What's present for you in this moment of hesitation?"""
            ]
            return {
                'emotions': 'uncertain, contemplative',
                'urgency': 'low',
                'needs': 'exploration',
                'response': random.choice(uncertain_responses),
                'ai_generated': False
            }
        else:
            general_responses = [
                """I'm listening carefully to what you're sharing. There's often more beneath the surface of our words.

What's the texture of this experience for you? Sometimes describing the quality of a feeling helps us understand it better.""",
                
                """Thank you for trusting me with this. Every person's experience is unique, and I want to understand yours specifically.

What's been most present for you lately?""",
                
                """I hear you. Sometimes the most important conversations start with simple sharing.

What would be most helpful for you right now - listening, exploring, or something else entirely?""",
                
                """I appreciate you sharing what's on your mind. Each person's journey is different, and I'm here to understand yours.

Where would you like to begin with this?"""
            ]
            return {
                'emotions': 'reflective, engaged',
                'urgency': 'low',
                'needs': 'connection',
                'response': random.choice(general_responses),
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
        
        # Always use AI analysis
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
        border-left: 6px solid #ff4b4b;
        background-color: #ffe6e6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .crisis-medium {
        border-left: 6px solid #ffa500;
        background-color: #fff4e6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .crisis-low {
        border-left: 6px solid #00cc96;
        background-color: #e6f7f2;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
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
    2. Click "Create API Key" 
    3. Copy and paste below
    4. It's **FREE** for limited use
    """)
    
    api_key = st.text_input(
        "Google AI API Key:",
        type="password",
        placeholder="Enter your API key here...",
        help="Get free API key from https://makersuite.google.com/app/apikey",
        key="api_key_input"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔗 Connect AI", use_container_width=True, type="primary"):
            if api_key:
                with st.spinner("Testing AI connection..."):
                    success = mental_health_agent.configure_ai(api_key)
                    if success:
                        st.success("✅ AI Connected Successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Connection failed. Please check your API key and try again.")
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
        css_class = f"crisis-{crisis_level}"
        with st.chat_message("assistant"):
            st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)
            if message.get("ai_used"):
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
                # Proper async handling
                result = asyncio.run(mental_health_agent.chat(prompt))
                response_data = result['final_response']
                response_text = response_data['response_text']
                ai_used = response_data['ai_used']
                crisis_level = response_data.get('crisis_level', 'low')
                
                # Display with appropriate styling
                css_class = f"crisis-{crisis_level}"
                st.markdown(f'<div class="{css_class}">{response_text}</div>', unsafe_allow_html=True)
                
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>🧠 MindMate AI Mental Health Support</strong></p>
    <p><small>Always here to listen 🤗</small></p>
</div>
""", unsafe_allow_html=True)
