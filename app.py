import streamlit as st
import pandas as pd
from gemini_client import get_gemini_client, stream_gemini_response
from utils.diet_utils import generate_diet_plan
from utils.workout_utils import generate_workout_plan
from logger import logger
import uuid  # For unique request IDs

# ---------------- Initialize Client ----------------
client = get_gemini_client()

st.set_page_config(page_title="AI Health Coach", page_icon="🏋️‍♀️", layout="wide")
st.title("🏋️‍♀️ Personalized Health & Fitness Coach (AI Agent)")
st.markdown("#### Your AI-powered health companion for personalized diet and workouts.")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("🧍‍♂️ Your Profile")
    
    # Using a form to reduce spacing
    with st.form("profile_form", clear_on_submit=False):
        name = st.text_input("Name", value="Manu")
        age = st.number_input("Age", 10, 80, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", 30, 200, 70)
        height = st.number_input("Current Height (cm)", 100, 250, 175)
        target_height = st.number_input("Target Height (cm)", 100, 250, 175)
        goal = st.selectbox("Goal 🎯", ["Lose Weight", "Gain Muscle", "Stay Fit"])
        time_frame = st.number_input("Time Frame (weeks)", 1, 52, 12)
        diet_preference = st.selectbox("Diet Preference 🍽️", ["Vegan", "Vegetarian", "Non-Veg"])
        
        st.form_submit_button("Save Profile")

st.divider()

# ---------------- Tabs ----------------
tabs = st.tabs(["💬 AI Coach Chat", "🥗 Diet Plan", "🏋️ Workout Plan"])

# ---------------- Chat ----------------
with tabs[0]:
    st.subheader("💬 Chat with your AI Fitness Coach")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous chat messages above input
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**Coach:** {chat['content']}")

    user_prompt = st.text_area("Type your message here...", height=80)

    if st.button("Ask Coach"):
        if not user_prompt.strip():
            st.warning("⚠️ Please enter a question before asking the coach.")
        else:
            request_id = str(uuid.uuid4())
            with st.spinner("Thinking..."):
                context = (
                    f"User details: Name={name}, Age={age}, Weight={weight}, Goal={goal}, "
                    f"Diet={diet_preference}, Target Height={target_height}, Time Frame={time_frame} weeks."
                )
                prompt = f"{context}\nQuestion: {user_prompt}"

                response = stream_gemini_response(client, prompt, st.session_state.chat_history)

                # Save in session
                st.session_state.chat_history.append({"role": "user", "content": user_prompt})
                st.session_state.chat_history.append({"role": "model", "content": response})

                # Display latest response immediately
                st.markdown(f"**Coach:** {response}")

                # Logging
                logger.info(
                    f"[{request_id}] User: {user_prompt[:100]}... | Response length: {len(response)} | "
                    f"Age: {age}, Weight: {weight}, Goal: {goal}, Diet: {diet_preference}, "
                    f"Target Height: {target_height}, Time Frame: {time_frame} weeks"
                )

# ---------------- Diet Plan ----------------
with tabs[1]:
    st.subheader("🥗 Personalized Diet Plan")
    if st.button("Generate Diet Plan"):
        request_id = str(uuid.uuid4())
        with st.spinner("Preparing your personalized diet plan..."):
            plan = generate_diet_plan(client, age, weight, goal, diet_preference, target_height, time_frame)
        st.success("✅ Diet Plan Generated!")
        st.write(plan)
        logger.info(f"[{request_id}] Diet plan generated | Age: {age}, Weight: {weight}, Goal: {goal}, Diet: {diet_preference}")

# ---------------- Workout Plan ----------------
with tabs[2]:
    st.subheader("🏋️ Workout Plan")
    if st.button("Generate Workout Plan"):
        request_id = str(uuid.uuid4())
        with st.spinner("Creating your custom workout routine..."):
            workout = generate_workout_plan(client, age, goal, target_height, time_frame)
        st.success("✅ Workout Plan Ready!")
        st.write(workout)
        logger.info(f"[{request_id}] Workout plan generated | Age: {age}, Goal: {goal}")
