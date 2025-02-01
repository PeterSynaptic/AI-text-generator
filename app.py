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
    layout="centered"
)

# Custom CSS improvements
st.markdown("""
    <style>
        /* Main content styling */
        .main-content { max-width: 900px; margin: 0 auto; 
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) { 
            .main-content { 
                max-width: 90vw; 
            }
            
        /* Text area styling */
        .stTextArea textarea { 
            min-height: 150px; 
            border-radius: 8px;
            #padding: 1rem !important;
        }
        
        /* Response styling */
        .response-box {
            padding: 1rem;
            border-radius: 8px;
            #background: black;
            border: 1px solid #dee2e6;
            margin: 1rem 0;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 20px;
            padding: 0.5rem 1.5rem;
            transition: all 0.3s ease;
        }
        
        /* Sidebar adjustments */
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

# Callback functions
def clear_prompt():
    st.session_state.prompt_input = ""
    st.session_state.generated_response = None

def reset_conversation():
    st.session_state.conversation = []
    st.session_state.generated_response = None

# Main content container
with st.container():
    st.title("🤖 Gemini Pro - AI Text Generator")
    st.markdown("### Start your AI-powered conversation")

    # Text input section
    user_prompt = st.text_area(
        "Type your prompt here:", 
        value="", 
        key="prompt_input", 
        height=200,
        placeholder="Enter your question or request here..."
    )

    # Generate button - centered below text area
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate_btn = st.button("🚀 Generate Response", use_container_width=True)

    # Response section
    if 'generated_response' in st.session_state and st.session_state.generated_response:
        st.markdown("---")
        st.markdown("### Generated Response")
        st.markdown(
            f'<div class="response-box">{st.session_state.generated_response}</div>',
            unsafe_allow_html=True
        )
        
        # Clear prompt button below response
        st.button("🧹 Clear Prompt & Response", on_click=clear_prompt, type="secondary")

# Sidebar section
with st.sidebar:
    st.subheader("⚙️ Settings")
    st.button("🔄 Reset Conversation History", on_click=reset_conversation, type="primary")
    
    st.markdown("---")
    st.subheader("📜 History")
    if st.session_state.conversation:
        for entry in reversed(st.session_state.conversation):
            st.markdown(f"**{entry['role']}:** {entry['text']}")
            st.markdown("---")
    else:
        st.info("No conversation history yet")

# Generation logic
if generate_btn and user_prompt.strip():
    try:
        with st.spinner("✨ Generating response..."):
            response = model.generate_content(user_prompt)
            ai_response = response.text.strip()
            
            # Store in session state
            st.session_state.conversation.append({"role": "User", "text": user_prompt})
            st.session_state.conversation.append({"role": "AI", "text": ai_response})
            st.session_state.generated_response = ai_response
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
elif generate_btn:
    st.warning("⚠️ Please enter a prompt before generating!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; margin-top: 2rem;'>"
    "Powered by Gemini Pro AI • "
    "<a href='https://ai.google/' target='_blank'>Privacy Policy</a></div>",
    unsafe_allow_html=True
)
