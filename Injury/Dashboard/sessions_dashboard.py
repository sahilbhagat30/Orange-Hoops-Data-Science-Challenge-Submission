import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from filters import session_filters

# Set consistent style for plots and custom color palette
sns.set_theme(style="whitegrid")
custom_palette = ["#E74C3C", "#D35400", "#2980B9", "#8E44AD", "#BDC3C7"]
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'axes.labelcolor': '#333333',
    'xtick.color': '#333333',
    'ytick.color': '#333333',
    'axes.edgecolor': '#333333',
    'text.color': '#333333'
})
sns.set_palette(custom_palette)

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

        # Calculate high-risk threshold using the 75th percentile
        high_risk_threshold = filtered_data['trimp'].quantile(0.75)

        # KPIs
        st.write("### Key Performance Indicators")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric(label="Total Sessions", value=len(filtered_data))
        
        with kpi_col2:
            avg_duration = filtered_data['durations'].mean()
            st.metric(label="Avg Duration (mins)", value=f"{avg_duration:.1f}")
        
        with kpi_col3:
            high_risk_sessions = len(filtered_data[filtered_data['trimp'] > high_risk_threshold])
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
            fig, ax = plt.subplots(figsize=(5, 3))
            sessions_over_time.plot(kind='line', ax=ax, color=custom_palette[0])
            ax.set_title("Sessions Over Time", fontsize=16, weight='bold')
            ax.set_xlabel("Date", fontsize=13)
            ax.set_ylabel("Number of Sessions", fontsize=13)
            ax.tick_params(axis='x', rotation=45)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig)

        # Distribution of Durations
        with row1_col2:
            st.subheader("Duration Distribution")
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.histplot(filtered_data['durations'], kde=True, ax=ax, color=custom_palette[1], edgecolor="black", alpha=0.8)
            ax.set_title("Session Duration", fontsize=16, weight='bold')
            ax.set_xlabel("Duration (mins)", fontsize=13)
            ax.set_ylabel("Frequency", fontsize=13)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig)

        # High-Risk Sessions Over Time
        with row2_col1:
            st.subheader("High-Risk Sessions Over Time")
            high_risk_sessions_over_time = filtered_data[filtered_data['trimp'] > high_risk_threshold].set_index('session_date').groupby(pd.Grouper(freq='W')).size()
            fig, ax = plt.subplots(figsize=(5, 3))
            high_risk_sessions_over_time.plot(kind='area', ax=ax, color=custom_palette[2], alpha=0.4)
            ax.set_title("High-Risk Sessions Over Time", fontsize=16, weight='bold')
            ax.set_xlabel("Date", fontsize=13)
            ax.set_ylabel("High-Risk Sessions", fontsize=13)
            ax.tick_params(axis='x', rotation=45)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig)

        # Player Attendance Distribution
        with row2_col2:
            st.subheader("Player Attendance Distribution")
            attendance_count = filtered_data['name'].value_counts()
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.barplot(x=attendance_count.index, y=attendance_count.values, ax=ax, palette=custom_palette)
            ax.set_title("Sessions per Player", fontsize=16, weight='bold')
            ax.set_xlabel("Player", fontsize=13)
            ax.set_ylabel("Sessions", fontsize=13)
            ax.tick_params(axis='x', rotation=45)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig)

        # Sessions by Day of the Week
        with row3_col2:
            st.subheader("Sessions by Day of the Week")
            filtered_data['Day_of_Week'] = filtered_data['session_date'].dt.day_name()
            day_counts = filtered_data['Day_of_Week'].value_counts()
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.barplot(x=day_counts.index, y=day_counts.values, ax=ax, palette=custom_palette)
            ax.set_title("Sessions by Day of the Week", fontsize=16, weight='bold')
            ax.set_xlabel("Day", fontsize=13)
            ax.set_ylabel("Sessions", fontsize=13)
            ax.tick_params(axis='x', rotation=45)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig)
            
        # Display session details table
        st.subheader("Session Details")
        st.dataframe(
            filtered_data[['name', 'session_date', 'durations', 'trimp']],
            use_container_width=True
        )
            
    except Exception as e:
        st.error(f"An error occurred in render_sessions_tab: {str(e)}")
