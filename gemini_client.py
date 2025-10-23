from google import genai
from google.genai import types
from config import GOOGLE_API_KEY, MODEL_NAME
from logger import logger
import time

def get_gemini_client():
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        logger.info("✅ Gemini client initialized successfully.")
        return client
    except Exception as e:
        logger.exception("❌ Error initializing Gemini client")
        return None

def convert_history_for_gemini(st_history):
    converted = []
    for msg in st_history:
        role = msg.get("role")
        content = msg.get("content")
        if content:
            gemini_role = "user" if role == "user" else "model"
            converted.append(
                types.Content(role=gemini_role, parts=[types.Part(text=content)])
            )
    return converted

def stream_gemini_response(client, user_prompt, history, request_id=None):
    """
    Streams response from Gemini LLM using generate_content_stream.
    Logs all events with the same request_id for traceability.
    """
    if client is None:
        logger.error(f"[{request_id}] Gemini client not initialized.")
        return "⚠️ Gemini client not initialized."

    start_time = time.time()
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(
        tools=[grounding_tool],
        system_instruction=(
            "You are a helpful AI Health Coach. "
            "Use GoogleSearch for latest fitness or nutrition data if needed."
        ),
    )

    contents = convert_history_for_gemini(history)
    contents.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

    try:
        response_stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=config
        )

        full_response = ""
        for event in response_stream:
            for candidate in getattr(event, "candidates", []):
                for part in getattr(candidate.content, "parts", []):
                    if part.text:
                        full_response += part.text

        elapsed = time.time() - start_time
        logger.info(f"[{request_id}] ✅ Gemini response generated | "
                    f"Prompt: {user_prompt[:100]}... | Response length: {len(full_response)} | Time: {elapsed:.2f}s")

        return full_response

    except Exception as e:
        logger.exception(f"[{request_id}] ❌ Error during Gemini API call | Prompt: {user_prompt[:100]}...")
        return "⚠️ Sorry, there was an issue generating the response."
