import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load variables from .env
load_dotenv()
# Configure Gemini Pro
genai.configure(api_key=os.getenv("AQ.Ab8RN6KPXbGC1I-BTKEGXw1CvMoypTsOHgWfmcIk6wgdlE0a9A"))
genai.configure(api_key="AQ.Ab8RN6KPXbGC1I-BTKEGXw1CvMoypTsOHgWfmcIk6wgdlE0a9A")

def generate_workout_gemini(goal: str, intensity: str) -> str:
    prompt = f"""
    Create a structured 7-day workout plan for {goal} at {intensity} intensity.
    Each day should include:
    - Warm-up (5–10 mins)
    - Main workout (exercise details, sets, reps)
    - Cooldown or recovery tip
    Format clearly by day.
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
