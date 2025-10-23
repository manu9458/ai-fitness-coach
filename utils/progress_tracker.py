import pandas as pd
import plotly.express as px

def get_progress_chart():
    """
    Displays mock progress chart (can be connected to fitness data later).
    """
    data = pd.DataFrame({
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Weight (kg)": [70, 69, 68, 67]
    })
    fig = px.line(data, x="Week", y="Weight (kg)", title="Your Weight Progress Over Time", markers=True)
    fig.update_layout(template="plotly_white")
    return fig
