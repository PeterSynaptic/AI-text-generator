from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Gemini Pro - AI Text Generator",
    page_icon=":robot_face:",  # Emoji for page icon
    #layout="centered"  # Centered layout
    layout="wide"
)

# NEW: Custom CSS for full-width display and sidebar adjustments
st.markdown("""
    <style>
        .main-container {
            max-width: 100% !important;
            padding: 0 1rem !important;
        }
        .stTextArea, .stButton, .stMarkdown {
            max-width: 100% !important;
        }
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Check for API key
api_key = st.secrets["API_KEY"]
if not api_key:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if not api_key:
        st.warning("Please enter your API key to proceed.")
        st.stop()

# Configure the generative AI API key
genai.configure(api_key=api_key)

# Initialize the Gemini-Pro model
model = genai.GenerativeModel('gemini-1.5-pro')

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Streamlit App Title
st.title("🤖 Gemini Pro - AI Text Generator")

# User Instructions
st.markdown(
    """
    <p style="font-size:16px; color:#666;">
        Enter your prompt below and let Gemini Pro generate content for you!
    </p>
    """,
    unsafe_allow_html=True
)

# NEW: Callback functions to handle state changes
def clear_prompt():
    st.session_state.prompt_input = ""  # Reset the text area value

def reset_conversation():
    st.session_state.conversation = []

# Buttons FIRST (before text area)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    generate_btn = st.button("Generate Response")
with col2:
    clear_btn = st.button("Clear Prompt", on_click=clear_prompt)  # FIX: Added callback
with col3:
    reset_btn = st.button("Reset Conversation", on_click=reset_conversation)

# Text area AFTER buttons
with st.container():
    user_prompt = st.text_area("Type your prompt here", value="", key="prompt_input", height=150)

# Handle generation
if generate_btn:
    if user_prompt.strip():
        with st.spinner("Generating..."):
            try:
                response = model.generate_content(user_prompt)
                ai_response = response.text.strip()
                st.session_state.conversation.extend([
                    {"role": "User", "text": user_prompt},
                    {"role": "AI", "text": ai_response}
                ])
                
                st.subheader("Generated Response:")
                st.markdown(f'<div style="padding:15px;background:#f0f2f6;border-radius:8px">{ai_response}</div>', 
                           unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt!")

# Sidebar history
with st.sidebar:
    st.subheader("📝 History")
    if st.session_state.conversation:
        for entry in st.session_state.conversation:
            st.markdown(f"**{entry['role']}:** {entry['text']}")
    else:
        st.info("No history yet")

# Footer
st.markdown(
    "<p style='text-align:center; font-size:14px; color:#666;'>Powered by <b>Gemini Pro AI</b></p>",
    unsafe_allow_html=True
)
