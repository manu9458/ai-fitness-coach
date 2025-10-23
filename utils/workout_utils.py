from gemini_client import stream_gemini_response

def generate_workout_plan(client, age, goal):
    """
    Generates a 7-day personalized workout routine.
    """
    prompt = f"""
    You are a professional fitness trainer.
    Design a 7-day workout plan for a {age}-year-old aiming to {goal.lower()}.
    Include warm-ups, main workouts, and rest days.
    """
    return stream_gemini_response(client, prompt, [])
