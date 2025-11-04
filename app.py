import streamlit as st
import pandas as pd
from gemini_client import get_gemini_client, stream_gemini_response
from utils.diet_utils import generate_diet_plan
from utils.workout_utils import generate_workout_plan
from logger import logger
import uuid  # For unique request IDs

# ---------------- Initialize Client ----------------
client = get_gemini_client()

# ---------------- Page Config ----------------
st.set_page_config(page_title="AI Health Coach", page_icon="🏋️‍♀️", layout="wide")
st.title("🏋️‍♀️ Personalized Health & Fitness Coach (AI Agent)")
st.markdown("#### Your AI-powered health companion for personalized diet and workouts.")

# ---------------- Sidebar: Profile ----------------
with st.sidebar:
    st.header("🧍‍♂️ Your Profile")

    if "profile_saved" not in st.session_state:
        st.session_state.profile_saved = False

    # Profile form
    with st.form("profile_form", clear_on_submit=False):
        name = st.text_input("Name", value=st.session_state.get("name", ""))
        age = st.number_input("Age", 10, 80, st.session_state.get("age", 25))
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(st.session_state.get("gender", "Male"))
        )
        weight = st.number_input("Current Weight (kg)", 30, 200, st.session_state.get("weight", 70))
        target_weight = st.number_input("Target Weight (kg)", 30, 200, st.session_state.get("target_weight", 65))
        goal = st.selectbox(
            "Goal 🎯",
            ["Lose Weight", "Gain Muscle", "Stay Fit"],
            index=["Lose Weight", "Gain Muscle", "Stay Fit"].index(st.session_state.get("goal", "Stay Fit"))
        )
        time_frame = st.number_input("Time Frame (weeks)", 1, 52, st.session_state.get("time_frame", 12))
        diet_preference = st.selectbox(
            "Diet Preference 🍽️",
            ["Vegan", "Vegetarian", "Non-Veg"],
            index=["Vegan", "Vegetarian", "Non-Veg"].index(st.session_state.get("diet_preference", "Vegan"))
        )

        save_clicked = st.form_submit_button("💾 Save Profile")

    if save_clicked:
        st.session_state.update({
            "profile_saved": True,
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "target_weight": target_weight,
            "goal": goal,
            "time_frame": time_frame,
            "diet_preference": diet_preference
        })
        st.rerun()  # Re-render main area (sidebar auto-close effect)

# ---------------- Confirmation Message ----------------
if st.session_state.get("profile_saved", False):
    st.success("✅ Profile saved successfully! Sidebar closed.")

st.divider()

# ---------------- Tabs ----------------
tabs = st.tabs(["💬 AI Coach Chat", "🥗 Diet Plan", "🏋️ Workout Plan"])

# ---------------- Chat ----------------
with tabs[0]:
    st.subheader("💬 Chat with your AI Fitness Coach")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**Coach:** {chat['content']}")

    


    # ChatGPT-style input at bottom
    user_prompt = st.chat_input("Ask your coach about diet, workouts, or fitness goals...")

    if user_prompt:
        if not st.session_state.get("profile_saved", False):
            st.warning("⚠️ Please complete and save your profile before chatting with your coach.")
        else:
            request_id = str(uuid.uuid4())
            with st.spinner("💭 Your coach is thinking..."):
                context = (
                    f"You are an AI Fitness Coach. Provide responses only about health, fitness, diet, and workouts. "
                    f"User details: Name={st.session_state.name}, Age={st.session_state.age}, Gender={st.session_state.gender}, "
                    f"Current Weight={st.session_state.weight}kg, Target Weight={st.session_state.target_weight}kg, "
                    f"Goal={st.session_state.goal}, Time Frame={st.session_state.time_frame} weeks, "
                    f"Diet Preference={st.session_state.diet_preference}."
                )

                prompt = f"{context}\nUser Question: {user_prompt}"
                response = stream_gemini_response(client, prompt, st.session_state.chat_history, request_id=request_id)

                st.session_state.chat_history.append({"role": "user", "content": user_prompt})
                st.session_state.chat_history.append({"role": "model", "content": response})

                st.markdown(f"**Coach:** {response}")

# ---------------- Diet Plan ---------------
# ---------------- Diet Plan ---------------
with tabs[1]:
    st.subheader("🥗 Personalized Diet Plan")

    if st.button("Generate Diet Plan"):
        if not st.session_state.get("profile_saved", False):
            st.warning("⚠️ Please complete and save your profile first.")
        else:
            # ✅ Ensure all required keys exist
            required_keys = ["age", "weight", "goal", "diet_preference", "target_weight", "time_frame"]
            missing = [key for key in required_keys if key not in st.session_state]
            if missing:
                st.error(f"⚠️ Missing required fields: {', '.join(missing)}. Please fill out your profile again.")
            elif client is None:
                st.error("❌ Failed to initialize AI client. Please check your API key or environment setup.")
            else:
                request_id = str(uuid.uuid4())
                try:
                    with st.spinner("Preparing your personalized diet plan..."):
                        plan = generate_diet_plan(
                            client,
                            st.session_state.get("age"),
                            st.session_state.get("weight"),
                            st.session_state.get("goal"),
                            st.session_state.get("diet_preference"),
                            st.session_state.get("target_weight"),
                            st.session_state.get("time_frame"),
                        )

                    if not plan:
                        st.warning("⚠️ No diet plan generated. Please try again later.")
                    else:
                        st.success("✅ Diet Plan Generated Successfully!")
                        st.markdown("### 🍱 Your Personalized Diet Plan")
                        st.write(plan)

                        logger.info(
                            f"[{request_id}] Diet plan generated | "
                            f"Age: {st.session_state.get('age')}, "
                            f"Weight: {st.session_state.get('weight')}, "
                            f"Goal: {st.session_state.get('goal')}, "
                            f"Diet: {st.session_state.get('diet_preference')}"
                        )

                except Exception as e:
                    st.error(f"❌ Error while generating diet plan: {e}")
                    logger.error(f"[{request_id}] Diet plan generation failed: {e}")

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
        if not st.session_state.get("profile_saved", False):
            st.warning("⚠️ Please complete and save your profile first.")
        else:
            request_id = str(uuid.uuid4())
            with st.spinner("Designing your personalized workout routine..."):
                context = (
                    "You are an expert AI Fitness Trainer. Create a personalized workout plan "
                    "based on user details and preferences. Include sets, reps, rest times, "
                    "and ensure safety for user's age and goal. Return cleanly formatted text."
                )

                user_input = (
                    f"User Profile:\n"
                    f"Name: {st.session_state.name}\nAge: {st.session_state.age}\nGender: {st.session_state.gender}\n"
                    f"Weight: {st.session_state.weight} kg\nTarget Weight: {st.session_state.target_weight} kg\n"
                    f"Goal: {st.session_state.goal}\nExperience: {experience}\nWorkout Time: {workout_time} mins\n"
                    f"Equipment: {', '.join(equipment)}\nFocus Areas: {', '.join(workout_focus)}"
                )

                prompt = f"{context}\n\n{user_input}\n\nGenerate a structured plan."
                response = stream_gemini_response(client, prompt, st.session_state.chat_history, request_id=request_id)

            st.success("✅ Workout Plan Generated!")
            st.markdown("### 💪 Your Custom Workout Plan")
            st.write(response)
            logger.info(f"[{request_id}] Workout plan generated | Goal: {st.session_state.goal}, Experience: {experience}, Time: {workout_time}")

            st.markdown("---")
            st.markdown("### 🎥 Exercise Visual Guide")
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
