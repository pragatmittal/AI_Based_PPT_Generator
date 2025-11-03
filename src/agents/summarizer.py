# summarizer_gemini.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

# Configure Gemini
genai.configure(api_key=api_key)

class Summarizer:
    def __init__(self, model_name="models/gemini-flash-latest"):
        self.model = genai.GenerativeModel(model_name)

    def summarize_text(self, text):
        prompt = (
            "Summarize the following text into concise bullet points "
            "that would be suitable for a PowerPoint presentation:\n\n" + text
        )

        response = self.model.generate_content(prompt)
        return response.text


if __name__ == "__main__":
    sample_text = """Your extracted content goes here. This text will be summarized into concise points suitable for a PowerPoint presentation. The summarization will focus on key information and main ideas to ensure clarity and effectiveness in conveying the message. The goal is to create a summary that is easy to understand and highlights the most important aspects of the content. This will help in creating engaging and informative slides for the presentation. The summary should be brief yet comprehensive, capturing the essence of the original text while omitting unnecessary details. The final output should be a set of bullet points that can be directly used in a PowerPoint slide deck."""
    
    summarizer = Summarizer()
    summary = summarizer.summarize_text(sample_text)
    print("\nSummary:\n", summary)
