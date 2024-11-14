import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from filters import session_filters

def render_sessions_tab(session_data, filter_col):
    try:
        # Ensure data is available
        if session_data is None or len(session_data) == 0:
            st.error("No valid session data available")
            return

        # Convert 'session_date' to datetime format
        session_data['session_date'] = pd.to_datetime(session_data['session_date'])

        # Get filter selections
        selected_players, filtered_data = session_filters(session_data, filter_col)

        # Filter data based on selections
        filtered_data = filtered_data[filtered_data['name'].isin(selected_players)]

        # KPIs
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric(label="Total Sessions", value=len(filtered_data))
        
        with kpi_col2:
            avg_duration = filtered_data['durations'].mean()
            st.metric(label="Avg Duration (mins)", value=f"{avg_duration:.1f}")
        
        with kpi_col3:
            high_risk_sessions = len(filtered_data[filtered_data['trimp'] > 100])  # Example threshold
            st.metric(label="High Risk Sessions", value=high_risk_sessions)
        
        with kpi_col4:
            unique_players = filtered_data['name'].nunique()
            st.metric(label="Unique Players", value=unique_players)

        # Visualizations
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)

        # Sessions Over Time
        with row1_col1:
            st.subheader("Sessions Over Time")
            sessions_over_time = filtered_data.set_index('session_date').groupby(pd.Grouper(freq='W')).size()
            fig, ax = plt.subplots(figsize=(4, 3))
            sessions_over_time.plot(kind='line', ax=ax)
            ax.set_title("Sessions Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Sessions")
            st.pyplot(fig)

        # Distribution of Durations
        with row1_col2:
            st.subheader("Duration Distribution")
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.histplot(filtered_data['durations'], kde=True, ax=ax, color='purple')
            ax.set_title("Session Duration")
            ax.set_xlabel("Duration (mins)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        # High-Risk Sessions Over Time
        with row2_col1:
            st.subheader("High-Risk Sessions Over Time")
            high_risk_sessions_over_time = filtered_data[filtered_data['trimp'] > 100].set_index('session_date').groupby(pd.Grouper(freq='W')).size()
            fig, ax = plt.subplots(figsize=(4, 3))
            high_risk_sessions_over_time.plot(kind='area', ax=ax, color='red', alpha=0.4)
            ax.set_title("High-Risk Sessions Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("High-Risk Sessions")
            st.pyplot(fig)

        # Player Attendance Distribution
        with row2_col2:
            st.subheader("Player Attendance Distribution")
            attendance_count = filtered_data['name'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.barplot(x=attendance_count.index, y=attendance_count.values, ax=ax, palette="Blues_d")
            ax.set_title("Sessions per Player")
            ax.set_xlabel("Player")
            ax.set_ylabel("Sessions")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

        # Sessions by Day of the Week
        with row3_col2:
            st.subheader("Sessions by Day of the Week")
            filtered_data['Day_of_Week'] = filtered_data['session_date'].dt.day_name()
            day_counts = filtered_data['Day_of_Week'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.barplot(x=day_counts.index, y=day_counts.values, ax=ax, palette="viridis")
            ax.set_title("Sessions by Day of the Week")
            ax.set_xlabel("Day")
            ax.set_ylabel("Sessions")
            st.pyplot(fig)
            
        st.subheader("Session Details")
        st.dataframe(
            filtered_data[['name', 'session_date', 'durations', 'trimp']],
            use_container_width=True
)
            
    except Exception as e:
        st.error(f"An error occurred in render_sessions_tab: {str(e)}")