import google.generativeai as genai

# Configure Gemini Flash
genai.configure(api_key="AQ.Ab8RN6KPXbGC1I-BTKEGXw1CvMoypTsOHgWfmcIk6wgdlE0a9A")

def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"Give a concise nutrition or recovery tip for someone with the goal: {goal}."
    model = genai.GenerativeModel("gemini-flash")
    response = model.generate_content(prompt)
    return response.text
