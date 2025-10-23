import streamlit as st
import pandas as pd
import plotly.express as px
from gemini_client import get_gemini_client, stream_gemini_response
from utils.diet_utils import generate_diet_plan
from utils.workout_utils import generate_workout_plan
from utils.progress_tracker import get_progress_chart
from logger import logger
import time
import uuid  # For unique request IDs

# ---------------- Initialize Client ----------------
client = get_gemini_client()

st.set_page_config(page_title="AI Health Coach", page_icon="🏋️‍♀️", layout="wide")
st.title("🏋️‍♀️ Personalized Health & Fitness Coach (AI Agent)")
st.markdown("#### Your AI-powered health companion for personalized diet, workouts, and progress tracking.")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("🧍‍♂️ Your Profile")
    name = st.text_input("Name", value="Manu")
    age = st.number_input("Age", 10, 80, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 250, 175)
    goal = st.selectbox("Goal 🎯", ["Lose Weight", "Gain Muscle", "Stay Fit"])

st.divider()
tabs = st.tabs(["💬 AI Coach Chat", "🥗 Diet Plan", "🏋️ Workout Plan", "📊 Progress Tracker"])

# ---------------- Chat ----------------
with tabs[0]:
    st.subheader("💬 Chat with your AI Fitness Coach")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_prompt = st.text_area("Ask anything about your fitness, diet, or workout:", height=100)

    if st.button("Ask Coach"):
        if not user_prompt.strip():
            st.warning("⚠️ Please enter a question before asking the coach.")
        else:
            request_id = str(uuid.uuid4())  # Generate unique request ID
            with st.spinner("Thinking..."):
                context = f"User details: Name={name}, Age={age}, Weight={weight}, Goal={goal}."
                prompt = f"{context}\nQuestion: {user_prompt}"

                response = stream_gemini_response(client, prompt, st.session_state.chat_history)

                # Save in session
                st.session_state.chat_history.append({"role": "user", "content": user_prompt})
                st.session_state.chat_history.append({"role": "model", "content": response})

                # Display response
                st.markdown("#### 🤖 Coach Response:")
                st.write(response)

                # Structured logging with request ID
                logger.info(f"[{request_id}] User: {user_prompt[:100]}... | Response length: {len(response)} | "
                            f"Age: {age}, Weight: {weight}, Goal: {goal}")

# ---------------- Diet Plan ----------------
with tabs[1]:
    st.subheader("🥗 Personalized Diet Plan")
    if st.button("Generate Diet Plan"):
        request_id = str(uuid.uuid4())
        with st.spinner("Preparing your personalized diet plan..."):
            plan = generate_diet_plan(client, age, weight, goal)
        st.success("✅ Diet Plan Generated!")
        st.write(plan)
        logger.info(f"[{request_id}] Diet plan generated | Age: {age}, Weight: {weight}, Goal: {goal}")

# ---------------- Workout Plan ----------------
with tabs[2]:
    st.subheader("🏋️ Workout Plan")
    if st.button("Generate Workout Plan"):
        request_id = str(uuid.uuid4())
        with st.spinner("Creating your custom workout routine..."):
            workout = generate_workout_plan(client, age, goal)
        st.success("✅ Workout Plan Ready!")
        st.write(workout)
        logger.info(f"[{request_id}] Workout plan generated | Age: {age}, Goal: {goal}")

# ---------------- Progress Tracker ----------------
with tabs[3]:
    st.subheader("📊 Progress Tracker")
    st.write("Simulated weight tracking chart (replace with wearable data later).")
    st.plotly_chart(get_progress_chart(), use_container_width=True)
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Progress chart displayed")
