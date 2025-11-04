from gemini_client import stream_gemini_response
import uuid
from logger import logger

def generate_diet_plan(client, age, weight, goal, diet_preference, target_weight, time_frame):
    """
    Generate a personalized diet plan using Gemini AI.
    """

    request_id = str(uuid.uuid4())

    prompt = f"""
    You are a professional fitness and nutrition coach.
    Design a complete, personalized diet plan for the following user.

    Age: {age} years
    Current Weight: {weight} kg
    Target Weight: {target_weight} kg
    Goal: {goal}
    Diet Preference: {diet_preference}
    Duration to achieve goal: {time_frame} weeks

    The plan should include:
    - Daily calorie target (based on goal and weight)
    - Macronutrient breakdown (protein, carbs, fats)
    - Sample meals for breakfast, lunch, snacks, and dinner
    - Water intake recommendation
    - Additional lifestyle/nutrition tips
    Return the answer in a neat, structured format with headings.
    """

    try:
        response = stream_gemini_response(client, prompt, [], request_id=request_id)
        logger.info(f"[{request_id}] Diet plan generated successfully for Goal={goal}, Diet={diet_preference}")
        return response
    except Exception as e:
        logger.error(f"[{request_id}] Error generating diet plan: {e}")
        return "⚠️ Sorry, something went wrong while generating your diet plan. Please try again."
