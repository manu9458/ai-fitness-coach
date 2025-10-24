# 🧠 AI Fitness Coach

An interactive **AI-powered fitness and nutrition assistant** built with **Streamlit**, leveraging **Google Gemini AI** for personalized coaching.  
It provides smart **diet plans, workout routines**, and conversational **AI chat support** — all in one sleek interface.

---

## 🚀 Features

### 💬 Smart AI Chat
- Chat naturally with your AI fitness coach.  
- Ask for workout tips, nutrition advice, or lifestyle guidance.  
- Real-time, streaming responses powered by **Gemini API**.

### 🍽️ Personalized Diet Plans
- Generates customized diet plans based on your input (goals, weight, gender, etc.).
- Uses smart logic for calorie balancing and macronutrient ratios.

### 🏋️ Workout Recommendations
- Suggests full-body, strength, or endurance-based workout routines.
- Adjusts difficulty level according to fitness goals.

### ⚡ Real-Time Interaction
- Chat-style UI with input box at the bottom and dynamic response area on top.
- “Typing…” animation for a realistic chat experience.

### 💾 Data Upload (Optional)
- Upload your fitness data or progress logs (CSV/Excel).
- Analyze progress and visualize it using Plotly charts (optional module).

---

## 🧠 How It Works

1. The user enters a query (like *"Create a 7-day muscle gain plan"*).  
2. The system detects the intent (Diet/Workout/Chat).  
3. Based on the intent, it calls:
   - `generate_diet_plan()` → for nutrition guidance  
   - `generate_workout_plan()` → for exercise routines  
   - `stream_gemini_response()` → for general chat  

4. The app displays the result above the input box in a friendly chat layout.

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-fitness-coach.git
   cd ai-fitness-coach
