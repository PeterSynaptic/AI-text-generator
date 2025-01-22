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
api_key = st.secrets("API_KEY")
if not api_key:
    st.error("API key is not set. Please check your environment variables.")
    st.stop()

# Configure the generative AI API key
genai.configure(api_key=api_key)

# Initialize the Gemini-Pro model
model = genai.GenerativeModel('gemini-1.5-pro')

# Title for the app
st.title("🤖 Gemini Pro - AI Text Generator")

# Instructions for the user
st.markdown("Enter your prompt below and let Gemini Pro generate content for you!")

# Input box for user prompt
user_prompt = st.text_input("Type your prompt here", value="The opposite of hot is")

# Button to trigger the API call
if st.button("Generate Response"):
    if user_prompt.strip():
        # Call the Gemini-Pro model with the user's prompt
        response = model.generate_content(user_prompt)

        # Display the AI response
        st.subheader("Generated Response:")
        st.write(response.text)
    else:
        st.warning("Please enter a prompt to get a response!")

# Footer
st.markdown("Powered by Gemini Pro AI")
