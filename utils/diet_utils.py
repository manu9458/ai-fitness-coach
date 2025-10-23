from gemini_client import stream_gemini_response

def generate_diet_plan(client, age, weight, goal):
    """
    Generates a 7-day personalized diet plan.
    """
    prompt = f"""
    You are a certified nutritionist.
    Create a 7-day Indian diet plan for a {age}-year-old weighing {weight}kg 
    whose goal is to {goal.lower()}.
    Include meals for breakfast, lunch, dinner, and snacks with calorie values.
    """
    return stream_gemini_response(client, prompt, [])
