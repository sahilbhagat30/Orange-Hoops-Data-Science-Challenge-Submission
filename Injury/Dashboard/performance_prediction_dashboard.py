import streamlit as st
import numpy as np
import pickle

def render_performance_prediction_tab():
    st.header("Performance Prediction")

    # Load the pre-trained model
    try:
        with open('Performance/winning_shot_model.pkl', 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'winning_shot_model.pkl' is in the correct directory.")
        return

    # Input form for prediction
    with st.form("performance_prediction_form"):
        st.markdown("### Input Player Performance Metrics")
        
        shooting_success_rate = st.slider("Shooting Success Rate", 0.0, 1.0, 0.5)
        recent_performance = st.slider("Recent Performance", 0.0, 1.0, 0.5)
        win_prob_gap = st.slider("Win Probability Gap", 0.0, 1.0, 0.1)
        possession_length = st.slider("Possession Length", 0, 100, 30)
        scoring_streak = st.slider("Scoring Streak", 0, 10, 0)
        time_remaining = st.slider("Time Remaining (seconds)", 0, 300, 120)
        
        # Use descriptive labels for binary options
        home_team_advantage = st.radio("Home Team Advantage", ["No", "Yes"], index=0)
        high_pressure = st.radio("High Pressure", ["No", "Yes"], index=0)
        possession_change = st.radio("Possession Change", ["No", "Yes"], index=0)
        
        clutch_5min_success_rate = st.slider("5-Min Clutch Success Rate", 0.0, 1.0, 0.5)
        clutch_2min_success_rate = st.slider("2-Min Clutch Success Rate", 0.0, 1.0, 0.5)
        final_shot_success_rate = st.slider("Final Shot Success Rate", 0.0, 1.0, 0.5)
        
        submitted = st.form_submit_button("Predict")
    
    if submitted:
        # Convert descriptive labels back to binary values
        home_team_advantage = 1 if home_team_advantage == "Yes" else 0
        high_pressure = 1 if high_pressure == "Yes" else 0
        possession_change = 1 if possession_change == "Yes" else 0

        # Prepare input data for prediction
        input_data = np.array([[
            shooting_success_rate, recent_performance, win_prob_gap, possession_length,
            scoring_streak, time_remaining, home_team_advantage, high_pressure,
            possession_change, clutch_5min_success_rate, clutch_2min_success_rate,
            final_shot_success_rate
        ]])
        
        # Predict the winning shot player
        prediction = model.predict(input_data)
        
        # Display the predicted player
        if prediction[0] == 1:
            st.success("The recommended player for the winning shot is: Judah Mintz")
        else:
            st.warning("No player was predicted as the best choice for the winning shot.")