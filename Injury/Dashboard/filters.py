import streamlit as st

def injury_filters(injury_data, filter_col):
    with filter_col:
        st.header("Injury History Filters")
        
        # Player filter
        st.subheader("Select Players")
        all_players = sorted(injury_data['Name'].unique())
        selected_players = st.multiselect(
            "",
            options=all_players,
            default=all_players[:3] if len(all_players) >= 3 else all_players,
            key="injury_players"
        )
        
        # Severity filter
        st.subheader("Select Severity Levels")
        severity_options = sorted(injury_data['Severity'].unique())
        selected_severity = st.multiselect(
            "",
            options=severity_options,
            default=severity_options,
            key="injury_severity"
        )
        
    return selected_players, selected_severity

def muscle_filters(muscle_data, filter_col):
    with filter_col:
        st.header("Muscle Imbalance Filters")
        
        # Player filter
        st.subheader("Select Players")
        all_players = sorted(muscle_data['Player Name'].unique())
        selected_players = st.multiselect(
            "",
            options=all_players,
            default=all_players[:3] if len(all_players) >= 3 else all_players,
            key="muscle_players"
        )
        
        # Muscle Metrics filter
        st.subheader("Select Muscle Metrics")
        muscle_metrics = ['Quad Imbalance Percent', 'HamstringImbalance Percent', 
                         'Calf Imbalance Percent', 'Groin Imbalance Percent']
        selected_metrics = st.multiselect(
            "",
            options=muscle_metrics,
            default=muscle_metrics,
            key="muscle_metrics"
        )
        
    return selected_players, selected_metrics

def session_filters(session_data, filter_col):
    with filter_col:
        st.header("Session Filters")
        
        # Player filter
        st.subheader("Select Players")
        all_players = sorted(session_data['name'].unique())
        selected_players = st.multiselect(
            "",
            options=all_players,
            default=all_players[:3] if len(all_players) >= 3 else all_players,
            key="session_players"
        )
        
    return selected_players, session_data