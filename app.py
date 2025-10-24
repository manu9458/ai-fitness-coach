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
# ---------------- Workout Plan ----------------
with tabs[2]:
    st.subheader("🏋️ Personalized Workout Plan")

    # User preferences
    experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
    workout_time = st.selectbox("Workout Duration (minutes)", [30, 45, 60, 90])
    equipment = st.multiselect(
        "Available Equipment",
        ["None", "Dumbbells", "Resistance Bands", "Barbell", "Bench", "Pull-up Bar", "Machine"],
        default=["None"]
    )
    workout_focus = st.multiselect(
        "Target Areas",
        ["Full Body", "Upper Body", "Lower Body", "Core", "Cardio", "Arms", "Legs", "Back"],
        default=["Full Body"]
    )

    if st.button("🏋️ Generate Workout Plan"):
        request_id = str(uuid.uuid4())
        with st.spinner("Designing your personalized workout routine..."):
            context = (
                "You are an expert AI Fitness Trainer. Create a personalized workout plan "
                "based on user details and preferences. Include sets, reps, rest times, "
                "and ensure safety for user's age and goal. Return cleanly formatted text."
            )

            user_input = (
                f"User Profile:\n"
                f"Name: {name}\nAge: {age}\nGender: {gender}\n"
                f"Weight: {weight} kg\nHeight: {height} cm\nGoal: {goal}\n"
                f"Experience: {experience}\nWorkout Time: {workout_time} mins\n"
                f"Equipment: {', '.join(equipment)}\nFocus Areas: {', '.join(workout_focus)}"
            )

            prompt = f"{context}\n\n{user_input}\n\nGenerate a structured plan."

            response = stream_gemini_response(client, prompt, st.session_state.chat_history, request_id=request_id)

        st.success("✅ Workout Plan Generated!")
        st.markdown("### 💪 Your Custom Workout Plan")
        st.write(response)
        logger.info(f"[{request_id}] Workout plan generated | Goal: {goal}, Experience: {experience}, Time: {workout_time}")

    st.markdown("---")
    st.markdown("### 🎥 Exercise Visual Guide (Optional)")
    st.write("Here are some reference exercise videos for your selected focus areas:")

    video_links = {
        "Full Body": "https://www.youtube.com/watch?v=UItWltVZZmE",
        "Upper Body": "https://www.youtube.com/watch?v=xv4YhX4rK-U",
        "Lower Body": "https://www.youtube.com/watch?v=2tM1LFFxeKg",
        "Core": "https://www.youtube.com/watch?v=1fbU_MkV7NE",
        "Cardio": "https://www.youtube.com/watch?v=ml6cT4AZdqI",
        "Arms": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "Legs": "https://www.youtube.com/watch?v=8QgSAFdDff0",
        "Back": "https://www.youtube.com/watch?v=iaBVSJm78ko",
    }

    for focus in workout_focus:
        if focus in video_links:
            st.video(video_links[focus])
