import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from filters import performance_filters
from sklearn.ensemble import RandomForestClassifier
import shap
import numpy as np

def render_performance_tab(performance_data, filter_col):
    # Set plot styles
    sns.set_palette("Set2")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelcolor'] = '#333333'
    plt.rcParams['xtick.color'] = '#333333'
    plt.rcParams['ytick.color'] = '#333333'
    plt.rcParams['text.color'] = '#333333'
    plt.rcParams['axes.titlecolor'] = '#333333'
    
    try:
        # Get filter selections
        selected_shooters = performance_filters(performance_data, filter_col)
        
        # Ensure we have valid data
        if performance_data is None or len(performance_data) == 0:
            st.error("No valid performance data available")
            return
            
        # Filter data based on selections
        filtered_data = performance_data[performance_data['shooter'].isin(selected_shooters)]
        
        # Display KPIs in a row
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            total_points = filtered_data['scoring_play'].sum()
            st.metric(label="Total Points", value=total_points)
        
        with kpi_col2:
            shooting_accuracy = (filtered_data['shot_outcome'] == 'made').mean() * 100
            st.metric(label="Shooting Accuracy", value=f"{shooting_accuracy:.2f}%")
        
        with kpi_col3:
            three_point_accuracy = filtered_data[filtered_data['three_pt']]['shot_outcome'].eq('made').mean() * 100
            st.metric(label="Three-Point Accuracy", value=f"{three_point_accuracy:.2f}%")
        
        with kpi_col4:
            free_throw_accuracy = filtered_data[filtered_data['free_throw']]['shot_outcome'].eq('made').mean() * 100
            st.metric(label="Free Throw Accuracy", value=f"{free_throw_accuracy:.2f}%")
        
        # Create two rows with two columns each for visualizations
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        # Shot Accuracy Distribution
        with row1_col1:
            st.subheader("Shot Accuracy Distribution")
            fig1 = plt.figure(figsize=(5, 4))
            sns.histplot(filtered_data['shot_outcome'] == 'made', bins=10, kde=True)
            plt.xlabel("Shot Made")
            plt.ylabel("Frequency")
            plt.title("Distribution of Shot Accuracy")
            st.pyplot(fig1)
            plt.close()
        
        # Shooting Accuracy Over Time
        with row2_col1:
            st.subheader("Shooting Accuracy Over Time")
            fig3 = plt.figure(figsize=(5, 4))
            filtered_data['date'] = pd.to_datetime(filtered_data['date'])
            accuracy_over_time = filtered_data.groupby('date')['shot_outcome'].apply(lambda x: (x == 'made').mean())
            plt.plot(accuracy_over_time.index, accuracy_over_time.values, marker='o')
            plt.xlabel("Date")
            plt.ylabel("Average Shot Accuracy")
            plt.title("Shot Accuracy Over Time")
            plt.xticks(rotation=45)
            st.pyplot(fig3)
            plt.close()
        
        # Game Flow Analysis
        with row1_col2:
            st.subheader("Game Flow Analysis")
            fig2 = plt.figure(figsize=(5, 4))
            score_progression = filtered_data.groupby('date')['scoring_play'].cumsum()
            plt.plot(score_progression.index, score_progression.values, marker='o')
            plt.xlabel("Date")
            plt.ylabel("Cumulative Score")
            plt.title("Score Progression Over Time")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
            plt.close()
        
        # Shot Distribution
        with row2_col2:
            st.subheader("Shot Distribution")
            fig4 = plt.figure(figsize=(5, 4))
            shot_types = filtered_data['shot_outcome'].value_counts(normalize=True)
            sns.barplot(x=shot_types.index, y=shot_types.values)
            plt.xlabel("Shot Outcome")
            plt.ylabel("Proportion")
            plt.title("Distribution of Shot Types")
            st.pyplot(fig4)
            plt.close()
        
        # Winning Shot Prediction
        st.subheader("Predict Winning Shot Player")
        
        # Input form for prediction
        with st.form("prediction_form"):
            shooting_success_rate = st.number_input("Shooting Success Rate", min_value=0.0, max_value=1.0, value=0.5)
            recent_performance = st.number_input("Recent Performance", min_value=0.0, max_value=1.0, value=0.5)
            win_prob_gap = st.number_input("Win Probability Gap", min_value=0.0, max_value=1.0, value=0.1)
            possession_length = st.number_input("Possession Length", min_value=0, max_value=100, value=30)
            scoring_streak = st.number_input("Scoring Streak", min_value=0, max_value=10, value=0)
            time_remaining = st.number_input("Time Remaining", min_value=0, max_value=300, value=120)
            home_team_advantage = st.selectbox("Home Team Advantage", [0, 1])
            high_pressure = st.selectbox("High Pressure", [0, 1])
            possession_change = st.selectbox("Possession Change", [0, 1])
            clutch_5min_success_rate = st.number_input("5-Min Clutch Success Rate", min_value=0.0, max_value=1.0, value=0.5)
            clutch_2min_success_rate = st.number_input("2-Min Clutch Success Rate", min_value=0.0, max_value=1.0, value=0.5)
            final_shot_success_rate = st.number_input("Final Shot Success Rate", min_value=0.0, max_value=1.0, value=0.5)
            
            submitted = st.form_submit_button("Predict")
        
        if submitted:
            # Prepare input data for prediction
            input_data = np.array([[
                shooting_success_rate, recent_performance, win_prob_gap, possession_length,
                scoring_streak, time_remaining, home_team_advantage, high_pressure,
                possession_change, clutch_5min_success_rate, clutch_2min_success_rate,
                final_shot_success_rate
            ]])
            
            # Load or train the model
            model = RandomForestClassifier(random_state=42)
            # Assuming the model is already trained, otherwise train it here
            
            # Predict the winning shot player
            prediction = model.predict(input_data)
            
            # Display the predicted player
            if prediction[0] == 1:
                st.success("The recommended player for the winning shot is: Judah Mintz")
            else:
                st.warning("No player was predicted as the best choice for the winning shot.")
        
    except Exception as e:
        st.error(f"An error occurred in render_performance_tab: {str(e)}")