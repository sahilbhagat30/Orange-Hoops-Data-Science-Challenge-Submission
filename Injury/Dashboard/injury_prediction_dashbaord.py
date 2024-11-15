import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def load_prediction_data():
    # Load or generate your dataset here
    # For demonstration, let's create a dummy dataset
    data = pd.DataFrame({
        'Player Name': ['Player1', 'Player2', 'Player3', 'Player4'],
        'Age': [25, 30, 22, 28],
        'Games Played': [20, 15, 25, 10],
        'Previous Injuries': [1, 3, 0, 2],
        'Training Hours': [10, 8, 12, 7],
        'Injury Risk': [0, 1, 0, 1]  # 0: Low Risk, 1: High Risk
    })
    return data

def train_model(data):
    X = data[['Age', 'Games Played', 'Previous Injuries', 'Training Hours']]
    y = data['Injury Risk']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

def render_prediction_tab():
    st.header("Injury Risk Prediction")

    data = load_prediction_data()
    model, accuracy = train_model(data)

    st.write(f"Model Accuracy: {accuracy:.2f}")

    st.subheader("Predict Injury Risk for a Player")
    age = st.number_input("Age", min_value=15, max_value=40, value=25)
    games_played = st.number_input("Games Played", min_value=0, max_value=50, value=20)
    previous_injuries = st.number_input("Previous Injuries", min_value=0, max_value=10, value=1)
    training_hours = st.number_input("Training Hours per Week", min_value=0, max_value=20, value=10)

    if st.button("Predict"):
        features = np.array([[age, games_played, previous_injuries, training_hours]])
        risk = model.predict(features)[0]
        risk_label = "High Risk" if risk == 1 else "Low Risk"
        st.write(f"The player is at {risk_label} of injury.")