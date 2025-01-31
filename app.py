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

# Main content container - NEW: Added container for better layout control
main_container = st.container()

# Custom height for text area
with main_container:
    user_prompt = st.text_area("Type your prompt here", value="", key="prompt_input", height=150)

# Button container 
col1, col2, col3 = st.columns([1, 1, 1])

# NEW: Separated button logic from response display
generate_btn = False
with col1:
    generate_btn = st.button("Generate Response")
with col2:
    if st.button("Clear Prompt"):
        st.session_state.prompt_input = ""
with col3:
    if st.button("Reset Conversation"):
        st.session_state.conversation = []
        st.success("Conversation history cleared!")

# Handle generation and display - NEW: Moved outside columns
if generate_btn:
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            try:
                response = model.generate_content(user_prompt)
                ai_response = response.text.strip()

                # Store conversation
                st.session_state.conversation.append({"role": "User", "text": user_prompt})
                st.session_state.conversation.append({"role": "AI", "text": ai_response})

                # NEW: Full-width response display
                with main_container:
                    st.subheader("Generated Response:")
                    st.markdown(
                        f'<div style="padding: 15px; border-radius: 8px; background-color: #f0f2f6; width: 100%">{ai_response}</div>',
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt to get a response!")

# Display conversation history in the sidebar
with st.sidebar:
    st.subheader("📝 Conversation History")
    if st.session_state.conversation:
        for entry in st.session_state.conversation:
            st.markdown(f"**{entry['role']}:** {entry['text']}")
    else:
        st.info("No conversation history yet.")


# Custom height for text area
#user_prompt = st.text_area("Type your prompt here", value="", key="prompt_input", height=150)

# Button container (Better UI with columns)
#col1, col2, col3 = st.columns([1, 1, 1])

#with col1:
    #if st.button("Generate Response"):
        #if user_prompt.strip():
            #with st.spinner("Generating response..."):
                #try:
                    #response = model.generate_content(user_prompt)
                    #ai_response = response.text.strip()

                    # Store conversation in session state
                    #st.session_state.conversation.append({"role": "User", "text": user_prompt})
                    #st.session_state.conversation.append({"role": "AI", "text": ai_response})

                    # Display AI response
                    #st.subheader("Generated Response:")
                    #st.write(ai_response)

                #except Exception as e:
                    #st.error(f"An error occurred: {e}")
        #else:
            #st.warning("Please enter a prompt to get a response!")

#with col2:
    #if st.button("Clear Prompt"):
        #st.session_state.prompt_input = ""  # Clears the text area

#with col3:
    #if st.button("Reset Conversation"):
        #st.session_state.conversation = []
        #st.success("Conversation history cleared!")

# Display conversation history in the sidebar
#with st.sidebar:
    #st.subheader("📝 Conversation History")
    #if st.session_state.conversation:
        #for entry in st.session_state.conversation:
            #st.markdown(f"**{entry['role']}**: {entry['text']}")
    #else:
        #st.info("No conversation history yet.")

# Footer
st.markdown(
    "<p style='text-align:center; font-size:14px; color:#666;'>Powered by <b>Gemini Pro AI</b></p>",
    unsafe_allow_html=True
)
