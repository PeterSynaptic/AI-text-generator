# 🤖 Gemini Pro AI Text Generator
A Streamlit-based web application powered by Google's Gemini Pro AI for generating text content in real-time. 
Users can input prompts, receive AI-generated responses, and manage conversation history.
## Key Features
* Natural Language Processing: Leverages Google's Gemini Pro model for high-quality text generation.
* Conversation History: Automatically saves interactions in the sidebar for reference.
* Real-Time Generation: Streamlined interface with loading states for smooth user experience.
* Secure API Integration: Securely handles Gemini API keys via environment variables.
* Customizable UI: Responsive design with options to clear prompts/responses or reset conversations.
* User-friendly interface: The streamlit interface is designed to be intuative and easy to use.
## Requirements
* Python 3.6 or later
* Streamlit library ( pip install streamlit)
* Google Generative AI library ( pip install google-generativeai )
* A valid Google Generative API key
### Instructions
1. Install Dependencies:
- pip install streamlit google-generativeai
2. Obtain a Google Generative AI API Key:
  - Create a Google Cloud project and enable the Generative AI API.
  - Follow the instructions to create an API key and store it securely as an environment variable named API_KEY.
3. Run the App:
  - Navigate to the directory containing the app files
  - Run the following command in your terminal:
    - streamlit run app.py
### Usage
* Enter a propmpt or question in the text area box.
* Clic the "🚀 Generate Response" button.
* The AI model will generate a creative text response based on your prompt.
* The generated response will be displayed in the response section.
* You can view the conversation history in the sidebar.
* Use the buttons in the sidebar to clear the prompt and response, or reset the conversation history.
## Customization
 The app.py file includes comments and configurations for customizing the appearance and behavior of the app. You can modify the CSS styles and explore the GenAI library documentation for advanced configuration options.
## Privacy Policy
 This application utilizes Google Generative AI, and by using this app, you agree to Google's Privacy Policy.
## Disclaimer
 The AI-generated text may not always be factually accurate or complete. It is recommended to use this app for entertainment and creative exploration purposes.
  
