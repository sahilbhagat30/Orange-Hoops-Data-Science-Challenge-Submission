import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def load_data():
    try:
        # Try reading with a specific encoding and engine
        injury_history = pd.read_csv('Injury/Data/injury_history(injury_history).csv', 
                                   encoding='ISO-8859-1',
                                   engine='python')
        muscle_imbalance = pd.read_csv('Injury/Data/injury_history(muscle_imbalance_data).csv', 
                                     encoding='ISO-8859-1',
                                     engine='python')
        sessions = pd.read_csv('Injury/Data/injury_history(player_sessions).csv', 
                             encoding='ISO-8859-1',
                             engine='python')
        
        # Convert dates and ensure proper data types for injury_history
        injury_history['Injury Date'] = pd.to_datetime(injury_history['Injury Date'])
        injury_history['Recovery Time (days)'] = pd.to_numeric(injury_history['Recovery Time (days)'], errors='coerce')
        injury_history['Severity'] = injury_history['Severity'].astype(str)
        
        # Convert Date Recorded to datetime for muscle_imbalance
        muscle_imbalance['Date Recorded'] = pd.to_datetime(muscle_imbalance['Date Recorded'])
        # Add Month column for monthly analysis
        muscle_imbalance['Month'] = muscle_imbalance['Date Recorded'].dt.month

        
        return muscle_imbalance, sessions, injury_history
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None