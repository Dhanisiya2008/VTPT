import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6KPXbGC1I-BTKEGXw1CvMoypTsOHgWfmcIk6wgdlE0a9A")

def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""
    Here is the original workout plan:
    {original_plan}

    User feedback: {feedback}

    Update the plan accordingly while keeping the 7-day structure.
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
