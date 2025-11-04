from gemini_client import stream_gemini_response
import uuid
from logger import logger

def generate_workout_plan(
    client,
    age,
    goal,
    experience="Beginner",
    workout_time=45,
    equipment=None,
    focus_areas=None
):
    """
    Generate a 7-day personalized workout routine using Gemini AI.
    """

    if equipment is None:
        equipment = ["None"]
    if focus_areas is None:
        focus_areas = ["Full Body"]

    request_id = str(uuid.uuid4())

    prompt = f"""
    You are a certified fitness coach.
    Create a 7-day personalized workout plan for a {age}-year-old whose goal is to {goal.lower()}.

    Details:
    - Experience Level: {experience}
    - Daily Workout Duration: {workout_time} minutes
    - Available Equipment: {', '.join(equipment)}
    - Target Areas: {', '.join(focus_areas)}

    Requirements:
    - Include warm-up, main workout, and cool-down sections.
    - Mention sets, reps, and rest time for each exercise.
    - Include at least one rest/recovery day.
    - Keep the tone motivational and concise.
    - Return results in clean structured markdown format with Day 1–Day 7 breakdown.
    """

    try:
        response = stream_gemini_response(client, prompt, [], request_id=request_id)
        logger.info(
            f"[{request_id}] Workout plan generated successfully | Goal={goal}, Experience={experience}, Time={workout_time} mins"
        )
        return response
    except Exception as e:
        logger.error(f"[{request_id}] Error generating workout plan: {e}")
        return "⚠️ Sorry, something went wrong while generating your workout plan. Please try again."
