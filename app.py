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
    layout="centered"  # Centered layout
)

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

# Title for the app
st.title("🤖 Gemini Pro - AI Text Generator")

# Instructions for the user
st.markdown("""
    <style>
        .instruction {
            font-size: 16px;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
    <div class="instruction">
        Enter your prompt below and let Gemini Pro generate content for you!
    </div>
""", unsafe_allow_html=True)

# Input box for user prompt
user_prompt = st.text_input("Type your prompt here", value="The opposite of hot is")

# Clear button
if st.button("Clear Prompt"):
    user_prompt = ""

# Button to trigger the API call
if st.button("Generate Response"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            try:
                response = model.generate_content(user_prompt)
                # Add user prompt and AI response to conversation history
                st.session_state.conversation.append({"role": "user", "text": user_prompt})
                st.session_state.conversation.append({"role": "AI", "text": response.text})
                # Display the AI response
                st.subheader("Generated Response:")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt to get a response!")

# Reset conversation button
if st.button("Reset Conversation"):
    st.session_state.conversation = []
    st.success("Conversation history cleared!")

# Display conversation history in the sidebar
with st.sidebar:
    st.subheader("Conversation History")
    for entry in st.session_state.conversation:
        st.write(f"**{entry['role'].capitalize()}:** {entry['text']}")

# Footer
st.markdown("Powered by Gemini Pro AI")
