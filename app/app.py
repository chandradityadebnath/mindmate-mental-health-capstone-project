# app.py
import streamlit as st
import asyncio
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import google.generativeai as genai
import os
from typing import Dict, List, Any
import uuid
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="MindMate - Mental Health Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .crisis-high {
        background-color: #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        border-left: 5px solid #ff0000;
    }
    .crisis-medium {
        background-color: #ffd93d;
        padding: 1rem;
        border-radius: 10px;
        color: black;
        border-left: 5px solid #ffa500;
    }
    .crisis-low {
        background-color: #6bcf7f;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        border-left: 5px solid #2e8b57;
    }
    .agent-response {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .user-message {
        background-color: #e6f3ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4d94ff;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🧠 MindMate - Mental Health Agent System</h1>', unsafe_allow_html=True)
st.markdown("### *Because everyone deserves a listening ear 🤗 and support system*")

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{str(uuid.uuid4())[:8]}"
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{str(uuid.uuid4())[:8]}"
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False

# Mental Health Tools (from your Kaggle notebook)
class MentalHealthTools:
    def __init__(self):
        self.crisis_keywords = {
            'suicidal': ['kill myself', 'end it all', 'suicide', 'want to die', 'not worth living'],
            'self_harm': ['cut myself', 'self harm', 'hurt myself', 'bleeding'],
            'panic': ['panic attack', 'cant breathe', 'heart racing', 'losing control'],
            'depression': ['hopeless', 'empty inside', 'no point', 'cant get out of bed']
        }
        
    def crisis_detector(self, text: str) -> Dict:
        text_lower = text.lower()
        crisis_level = "low"
        detected_issues = []
        
        for category, keywords in self.crisis_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_issues.append(category)
                if category in ['suicidal', 'self_harm']:
                    crisis_level = "high"
                elif crisis_level != "high" and category in ['panic']:
                    crisis_level = "medium"
        
        emotional_intensity = self.analyze_emotional_intensity(text)
        if emotional_intensity > 0.8 and crisis_level == "low":
            crisis_level = "medium"
            
        risk_score = self.calculate_risk_score(text, detected_issues)
        
        return {
            "crisis_level": crisis_level,
            "detected_issues": detected_issues,
            "risk_score": risk_score,
            "emotional_intensity": emotional_intensity,
            "immediate_action_required": crisis_level in ["high", "medium"]
        }
    
    def analyze_emotional_intensity(self, text: str) -> float:
        intensity_indicators = [
            len([w for w in text.split() if w in ['very', 'extremely', 'really', 'so', 'too']]),
            text.count('!'),
            len([w for w in text.split() if len(w) > 8]),
            text.count(' not ')
        ]
        
        intensity = sum(intensity_indicators) / (len(text.split()) + 1)
        return min(intensity, 1.0)
    
    def calculate_risk_score(self, text: str, issues: List[str]) -> float:
        base_score = 0.0
        issue_weights = {'suicidal': 1.0, 'self_harm': 0.9, 'panic': 0.7, 'depression': 0.6}
        for issue in issues:
            base_score += issue_weights.get(issue, 0.5)
            
        if 'help' in text.lower():
            base_score += 0.3
        if 'alone' in text.lower() or 'lonely' in text.lower():
            base_score += 0.2
            
        return min(base_score, 1.0)
    
    def generate_coping_strategy(self, crisis_data: Dict) -> str:
        issues = crisis_data['detected_issues']
        
        strategies = {
            'suicidal': """🚨 **CRITICAL**: Please contact crisis support immediately:
• Call 988 (Suicide Prevention)
• Text HOME to 741741
• You are not alone - help is available NOW""",
            
            'panic': """💨 **Panic Attack Protocol**:
1. 5-4-3-2-1 Grounding Technique
2. Deep breathing: 4-4-6 pattern
3. Focus on one safe object in your environment""",
            
            'depression': """🤗 **Depression Support**:
• Break tasks into tiny steps
• Reach out to one person today  
• Remember: feelings aren't facts""",
            
            'default': """🌱 **General Wellness**:
• Practice mindfulness for 5 minutes
• Connect with nature or pets
• Engage in gentle physical activity"""
        }
        
        if 'suicidal' in issues:
            return strategies['suicidal']
        elif 'panic' in issues:
            return strategies['panic']
        elif 'depression' in issues:
            return strategies['depression']
        else:
            return strategies['default']

# AI Integration (Simplified for Streamlit)
class StreamlitAIIntegration:
    def __init__(self):
        self.api_key = None
        self.model = None
        self.setup_gemini()
    
    def setup_gemini(self):
        """Setup Gemini AI with API key from secrets or input"""
        try:
            # Try to get API key from Streamlit secrets
            self.api_key = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            st.success("✅ Gemini AI Connected!")
            return True
        except:
            st.warning("🔧 Gemini AI not configured - using advanced simulated responses")
            return False
    
    async def analyze_with_ai(self, text: str, context: Dict = None) -> Dict:
        """AI analysis with fallback to simulated responses"""
        if self.model:
            try:
                prompt = f"""
                MENTAL HEALTH ANALYSIS:
                User Message: "{text}"
                
                Please provide:
                1. Primary emotions detected
                2. Urgency level (low/medium/high)
                3. Key support needs
                4. A compassionate, therapeutic response
                
                Format as JSON:
                {{
                    "emotions": "comma separated emotions",
                    "urgency": "low/medium/high", 
                    "needs": "key support needs",
                    "response": "compassionate therapeutic response"
                }}
                """
                
                response = self.model.generate_content(prompt)
                return self._parse_ai_response(response.text)
            except Exception as e:
                st.error(f"AI Analysis Failed: {e}")
        
        # Fallback to simulated analysis
        return self._simulated_ai_analysis(text, context)
    
    def _parse_ai_response(self, ai_text: str) -> Dict:
        """Parse AI response"""
        try:
            # Try to extract JSON from response
            start = ai_text.find('{')
            end = ai_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = ai_text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback parsing
        return {
            "emotions": "concerned, attentive",
            "urgency": "medium",
            "needs": "emotional_support", 
            "response": "I hear you and I'm here to support you through this.",
            "ai_generated": True
        }
    
    def _simulated_ai_analysis(self, text: str, context: Dict) -> Dict:
        """Advanced simulated AI responses"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['die', 'suicide', 'kill myself']):
            return {
                "emotions": "desperate, hopeless, suicidal",
                "urgency": "high",
                "needs": "crisis_intervention",
                "response": "🚨 I'm deeply concerned about what you're sharing. Your life is precious. Please call 988 now. I'm here with you - you don't have to face this alone.",
                "ai_generated": False
            }
        elif any(word in text_lower for word in ['anxious', 'panic', 'overwhelmed']):
            return {
                "emotions": "anxious, overwhelmed, scared",
                "urgency": "medium", 
                "needs": "anxiety_management",
                "response": "💨 I understand anxiety can feel overwhelming. Let's breathe together: Inhale for 4 counts, hold for 4, exhale for 6. You're safe right here, right now.",
                "ai_generated": False
            }
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless']):
            return {
                "emotions": "sad, depressed, hopeless", 
                "urgency": "medium",
                "needs": "emotional_support",
                "response": "🤗 I hear you're feeling really low. That sounds incredibly difficult. Remember that these feelings, while overwhelming, are temporary. Would you like to talk about what's been weighing on you?",
                "ai_generated": False
            }
        else:
            return {
                "emotions": "concerned, attentive",
                "urgency": "low",
                "needs": "emotional_connection", 
                "response": "🤗 Thank you for sharing that with me. I'm here to listen and support you through whatever you're experiencing. It takes courage to reach out.",
                "ai_generated": False
            }

# Parallel Agents System (Adapted for Streamlit)
class StreamlitAgentsSystem:
    def __init__(self):
        self.tools = MentalHealthTools()
        self.ai_integration = StreamlitAIIntegration()
    
    async def process_message(self, message: str) -> Dict:
        """Process message through all agents"""
        # Crisis detection
        crisis_data = self.tools.crisis_detector(message)
        coping_strategy = self.tools.generate_coping_strategy(crisis_data)
        
        # Emotion analysis
        emotion_data = await self.ai_integration.analyze_with_ai(message)
        
        # Support planning
        support_plan = {
            "immediate_actions": [
                "Practice grounding techniques",
                "Contact support network", 
                "Use coping strategies"
            ],
            "short_term_goals": [
                "Daily check-ins",
                "Mood tracking",
                "Small achievable tasks"
            ]
        }
        
        # Resource matching
        resources = {
            "crisis": {
                "988 Suicide Prevention": "Call 988",
                "Crisis Text Line": "Text HOME to 741741",
                "Emergency": "Call 911"
            },
            "therapy": {
                "BetterHelp": "Online therapy platform",
                "Open Path Collective": "Affordable therapy"
            }
        }
        
        # Synthesize final response
        final_response = self.synthesize_responses(
            crisis_data, emotion_data, support_plan, resources
        )
        
        return {
            "crisis_data": crisis_data,
            "emotion_data": emotion_data, 
            "support_plan": support_plan,
            "resources": resources,
            "final_response": final_response,
            "processing_time": time.time(),
            "agents_used": 4
        }
    
    def synthesize_responses(self, crisis_data, emotion_data, support_plan, resources):
        """Synthesize all agent responses"""
        crisis_level = crisis_data['crisis_level']
        
        if crisis_level == 'high':
            primary_response = crisis_data.get('coping_strategy', 'Please seek immediate help.')
        else:
            primary_response = emotion_data.get('response', 'I am here to support you.')
        
        return {
            "primary_response": primary_response,
            "crisis_level": crisis_level,
            "emotions": emotion_data.get('emotions', 'processing'),
            "support_plan": support_plan,
            "resources": resources,
            "comprehensive_analysis": True
        }

# Initialize systems
@st.cache_resource
def initialize_systems():
    tools = MentalHealthTools()
    agents = StreamlitAgentsSystem()
    return tools, agents

# Main chat interface
def main():
    # Sidebar
    with st.sidebar:
        st.header("🧠 System Info")
        st.write(f"**Session ID:** {st.session_state.session_id}")
        st.write(f"**User ID:** {st.session_state.user_id}")
        st.write(f"**Messages:** {len(st.session_state.conversation_history)}")
        
        st.header("🔧 Configuration")
        if st.button("Initialize System"):
            st.session_state.tools, st.session_state.agents = initialize_systems()
            st.session_state.system_initialized = True
            st.success("System Initialized!")
        
        st.header("📊 Quick Actions")
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()
        
        if st.button("Test Crisis Response"):
            test_message = "I'm feeling extremely suicidal right now"
            st.session_state.test_input = test_message
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Mental Health Support Chat")
        
        # System status
        if not st.session_state.get('system_initialized', False):
            st.warning("⚠️ Please initialize the system from the sidebar first!")
        else:
            st.success("✅ System Ready - You can start chatting!")
        
        # Chat input
        user_input = st.text_area(
            "Share what you're feeling:",
            placeholder="I'm feeling...",
            key="user_input",
            height=100
        )
        
        col1_1, col1_2 = st.columns([1, 1])
        with col1_1:
            if st.button("Send Message", type="primary", use_container_width=True):
                if user_input.strip():
                    process_user_message(user_input)
        with col1_2:
            if st.button("Emergency Help", use_container_width=True):
                show_emergency_resources()
        
        # Display conversation history
        display_conversation_history()
    
    with col2:
        st.header("📈 System Analytics")
        
        if st.session_state.conversation_history:
            # Crisis level summary
            crisis_levels = [msg.get('crisis_level', 'low') 
                           for msg in st.session_state.conversation_history 
                           if msg.get('type') == 'response']
            
            if crisis_levels:
                current_crisis = crisis_levels[-1]
                st.subheader("Current Status")
                
                if current_crisis == 'high':
                    st.markdown('<div class="crisis-high">🚨 HIGH CRISIS - Immediate attention required</div>', 
                               unsafe_allow_html=True)
                elif current_crisis == 'medium':
                    st.markdown('<div class="crisis-medium">🟡 MEDIUM CRISIS - Close monitoring needed</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown('<div class="crisis-low">🟢 LOW CRISIS - Stable condition</div>', 
                               unsafe_allow_html=True)
            
            # Statistics
            st.subheader("Session Stats")
            total_messages = len(st.session_state.conversation_history)
            user_messages = len([m for m in st.session_state.conversation_history 
                               if m.get('type') == 'user'])
            
            st.metric("Total Messages", total_messages)
            st.metric("Your Messages", user_messages)
            
            # Recent emotions
            if st.session_state.conversation_history:
                recent_emotions = [msg.get('emotions', '') 
                                 for msg in st.session_state.conversation_history[-3:] 
                                 if msg.get('type') == 'response']
                if recent_emotions:
                    st.subheader("Recent Emotions")
                    for emotion in recent_emotions:
                        st.write(f"• {emotion}")
        
        else:
            st.info("💡 Start a conversation to see analytics here!")

def process_user_message(user_input):
    """Process user message through the agent system"""
    if not st.session_state.get('system_initialized', False):
        st.error("System not initialized! Please click 'Initialize System' in the sidebar.")
        return
    
    # Add user message to history
    st.session_state.conversation_history.append({
        'type': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    })
    
    # Show processing indicator
    with st.spinner("🤖 Multiple agents analyzing your message..."):
        # Process through agents
        result = asyncio.run(st.session_state.agents.process_message(user_input))
        
        # Add agent response to history
        st.session_state.conversation_history.append({
            'type': 'response',
            'content': result['final_response']['primary_response'],
            'crisis_level': result['final_response']['crisis_level'],
            'emotions': result['final_response']['emotions'],
            'agents_used': result['agents_used'],
            'timestamp': datetime.now().isoformat(),
            'full_analysis': result
        })
    
    # Rerun to update display
    st.rerun()

def display_conversation_history():
    """Display the conversation history"""
    for i, message in enumerate(st.session_state.conversation_history):
        if message['type'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display crisis level indicator
            crisis_level = message.get('crisis_level', 'low')
            crisis_icons = {'high': '🚨', 'medium': '🟡', 'low': '🟢'}
            
            st.markdown(f"""
            <div class="agent-response">
                <strong>{crisis_icons.get(crisis_level, '🤖')} MindMate:</strong><br>
                {message['content']}
                <br><br>
                <small><i>Detected emotions: {message.get('emotions', 'processing')} | 
                Crisis level: {crisis_level.upper()} | 
                Agents used: {message.get('agents_used', 0)}</i></small>
            </div>
            """, unsafe_allow_html=True)
            
            # Show detailed analysis on expansion
            with st.expander("View Detailed Analysis"):
                full_analysis = message.get('full_analysis', {})
                if full_analysis:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Crisis Assessment")
                        crisis_data = full_analysis.get('crisis_data', {})
                        st.write(f"Level: **{crisis_data.get('crisis_level', 'low').upper()}**")
                        st.write(f"Risk Score: {crisis_data.get('risk_score', 0):.2f}")
                        st.write(f"Detected Issues: {', '.join(crisis_data.get('detected_issues', []))}")
                    
                    with col2:
                        st.subheader("Emotion Analysis")
                        emotion_data = full_analysis.get('emotion_data', {})
                        st.write(f"Emotions: {emotion_data.get('emotions', 'processing')}")
                        st.write(f"Urgency: {emotion_data.get('urgency', 'low').upper()}")
                        st.write(f"Needs: {emotion_data.get('needs', 'emotional_support')}")

def show_emergency_resources():
    """Display emergency resources"""
    st.markdown("""
    <div class="crisis-high">
        <h3>🚨 IMMEDIATE CRISIS SUPPORT</h3>
        <p><strong>National Suicide Prevention Lifeline:</strong> Call 988</p>
        <p><strong>Crisis Text Line:</strong> Text HOME to 741741</p>
        <p><strong>Emergency Services:</strong> Call 911</p>
        <p><strong>Veterans Crisis Line:</strong> Call 988 then press 1</p>
        <br>
        <p><strong>You are not alone. Help is available right now.</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
