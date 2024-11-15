import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained Random Forest model
with open('../Injury/Injury Prediction/rf_best_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the input features required by the model
features = [
    'Average_Recovery_Time',
    'Severity_Score',
    'Baseline_Exertion',
    'Muscle_Imbalance',
    'trimp',
    'Days_Since_Last_Injury'
]

# Set up Streamlit app
st.set_page_config(page_title="Basketball Player Injury Prediction", page_icon="🏀", layout="centered")

# App title and description
st.title("🏀 Basketball Player Injury Prediction")
st.markdown("### Predict the likelihood of injury for basketball players based on training and health metrics.")
st.write("Please enter the player's details below to assess injury risk.")

# Create sidebar for user inputs
st.sidebar.header("Player Information")

# Collect user inputs
average_recovery_time = st.sidebar.slider("Average Recovery Time (days)", 0, 60, 15)
severity_score = st.sidebar.slider("Injury Severity Score", 0.0, 10.0, 5.0)
baseline_exertion = st.sidebar.slider("Baseline Exertion Level", 0, 100, 50)
muscle_imbalance = st.sidebar.slider("Muscle Imbalance Level", 0.0, 10.0, 5.0)
trimp = st.sidebar.slider("TRIMP Score (Training Impulse)", 0, 300, 150)
days_since_last_injury = st.sidebar.slider("Days Since Last Injury", 0, 365, 90)

# Prepare data for prediction
input_data = pd.DataFrame({
    'Average_Recovery_Time': [average_recovery_time],
    'Severity_Score': [severity_score],
    'Baseline_Exertion': [baseline_exertion],
    'Muscle_Imbalance': [muscle_imbalance],
    'trimp': [trimp],
    'Days_Since_Last_Injury': [days_since_last_injury]
})

# Prediction and display results
if st.button("Predict Injury Risk"):
    probabilities = model.predict_proba(input_data)[0][1] * 100
    prediction = "High Risk" if probabilities >= 50 else "Low Risk"
    
    st.markdown("### Prediction Results")
    st.write(f"**Injury Risk Level:** {prediction}")
    st.write(f"**Injury Probability:** {probabilities:.2f}%")

    # Display recommendation
    st.markdown("### Recommendation")
    if prediction == "High Risk":
        st.write("⚠️ **Recommendation**: Consider reducing training intensity and implementing preventive measures.")
    else:
        st.write("✅ **Recommendation**: Player is in a safe training zone. Continue with the current approach.")

# Footer
st.markdown("---")
st.write("**Disclaimer:** This tool is designed to provide an injury risk assessment based on inputted metrics. Always consult with a medical professional for comprehensive health advice.")
