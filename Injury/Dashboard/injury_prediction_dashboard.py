import streamlit as st
import pandas as pd
import pickle

def render_injury_prediction_tab():
    st.header("Injury Prediction")

    # Load the trained Random Forest model
    try:
        with open('Injury/Injury Prediction/rf_best_model.pkl', 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'rf_best_model.pkl' is in the correct directory.")
        return
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        return

    # Input form for prediction
    with st.form("injury_prediction_form"):
        st.markdown("### Input Player Health Metrics")
        
        # Collect user inputs through sidebar sliders
        average_recovery_time = st.sidebar.slider("Average Recovery Time (days)", 0, 110, 71)
        severity_score = st.sidebar.slider("Injury Severity Score", 0, 3, 3)
        baseline_exertion = st.sidebar.slider("Baseline Exertion Level", 0, 320, 251)
        muscle_imbalance = st.sidebar.slider("Muscle Imbalance Level", 0.0, 24.0, 3.667)
        trimp = st.sidebar.slider("TRIMP Score (Training Impulse)", 0, 300, 195)
        days_since_last_injury = st.sidebar.slider("Days Since Last Injury", -1, 250, 58)
        
        submitted = st.form_submit_button("Predict Injury Risk")
    
    if submitted:
        # Prepare data for prediction
        input_data = pd.DataFrame({
            'Average_Recovery_Time': [average_recovery_time],
            'Severity_Score': [severity_score],
            'Baseline_Exertion': [baseline_exertion],
            'Muscle_Imbalance': [muscle_imbalance],
            'trimp': [trimp],
            'Days_Since_Last_Injury': [days_since_last_injury]
        })

        # Define risk levels and recommendations mapping
        risk_bins = [0, 20, 40, 60, 80, 100]
        risk_labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
        recommendations = {
            'Very Low': "Continue normal training routine",
            'Low': "Monitor and maintain current approach",
            'Moderate': "Consider reducing training intensity",
            'High': "Implement preventive measures immediately",
            'Very High': "Immediate attention required - high risk of injury"
        }
        
        # Calculate probability and detailed risk assessment
        probability = model.predict_proba(input_data)[0][1] * 100
        risk_status = "High Risk" if probability >= 50 else "Low Risk"
        confidence = abs(probability - 50) * 2
    
        # Classify risk level based on probability
        risk_level = pd.cut([probability], bins=risk_bins, labels=risk_labels)[0]
        recommendation = recommendations[risk_level]
    
        st.markdown("### Prediction Results")
        st.write(f"**Injury Probability:** {probability:.2f}%")
        st.write(f"**Risk Status:** {risk_status}")
        st.write(f"**Confidence Level:** {confidence:.2f}%")
    
        # Display recommendation based on risk level
        st.markdown("### Recommendation")
        st.write(f"{recommendation}")

    # Footer
    st.markdown("---")
    st.write("**Disclaimer:** This tool provides an injury risk assessment based on inputted metrics. Consult with a medical professional for comprehensive health advice.")
