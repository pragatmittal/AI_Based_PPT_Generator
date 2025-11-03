# check_gemini_models.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("AIzaSyBrOemHbnhorfZGh7ADgq-ox1EfCTIQh_o"))

# List all available models
models = genai.list_models()
print("Available Gemini models:\n")
for model in models:
    print(model)
