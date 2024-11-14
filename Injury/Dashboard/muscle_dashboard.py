import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from filters import muscle_filters

def calculate_risk_score(row):
    risk_score = 0
    
    # H/Q Ratio (ideal: 0.6-0.8)
    hq_ratio = row['Hamstring To Quad Ratio']
    if hq_ratio < 0.6:
        risk_score += (0.6 - hq_ratio) * 10
    elif hq_ratio > 0.8:
        risk_score += (hq_ratio - 0.8) * 10
    
    # Muscle imbalances (ideal: -5 to +5)
    imbalance_cols = ['Quad Imbalance Percent', 'HamstringImbalance Percent', 
                      'Calf Imbalance Percent', 'Groin Imbalance Percent']
    
    for col in imbalance_cols:
        imbalance = abs(row[col])
        if imbalance > 5:
            risk_score += (imbalance - 5) * 0.5
            
    return risk_score

def render_muscle_tab(muscle_data, filter_col):
    try:
        # Ensure we have valid data
        if muscle_data is None or len(muscle_data) == 0:
            st.error("No valid muscle imbalance data available")
            return
            
        # Get filter selections
        selected_players, selected_metrics = muscle_filters(muscle_data, filter_col)
        
        # Filter data based on selections
        filtered_data = muscle_data[
            (muscle_data['Player Name'].isin(selected_players))
        ]
        
        # Calculate risk scores
        filtered_data['Risk Score'] = filtered_data.apply(calculate_risk_score, axis=1)
        
        # Display KPIs in a row
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric(
                label="Total Assessments",
                value=len(filtered_data)
            )
        
        with kpi_col2:
            avg_hq_ratio = filtered_data['Hamstring To Quad Ratio'].mean()
            st.metric(
                label="Avg H/Q Ratio",
                value=f"{avg_hq_ratio:.2f}",
                delta="Ideal: 0.6-0.8"
            )
        
        with kpi_col3:
            high_risk = len(filtered_data[filtered_data['Risk Score'] > 20])
            st.metric(
                label="High Risk Players",
                value=high_risk,
                delta=f"{(high_risk/len(filtered_data)*100):.1f}% of total"
            )
        
        with kpi_col4:
            avg_risk = filtered_data['Risk Score'].mean()
            st.metric(
                label="Average Risk Score",
                value=f"{avg_risk:.1f}",
                delta=f"Max: {filtered_data['Risk Score'].max():.1f}"
            )

        # Define the list of metrics to plot
        metrics = [
            'Hamstring To Quad Ratio',
            'Quad Imbalance Percent', 
            'HamstringImbalance Percent', 
            'Calf Imbalance Percent', 
            'Groin Imbalance Percent'
        ]

        # Iterate over metrics in pairs to ensure a two-column layout
        for i in range(0, len(metrics), 2):
            cols = st.columns(2)  # Create two columns
            for j, metric in enumerate(metrics[i:i + 2]):  # Process two metrics at a time
                with cols[j]:  # Place each plot in a separate column
                    st.subheader(f"Distribution of {metric}")
                    fig, ax = plt.subplots(figsize=(4, 3))
                    sns.histplot(filtered_data[metric], kde=True, color='blue', ax=ax)
                    if metric == 'Hamstring To Quad Ratio':
                        ax.axvline(x=0.6, color='green', linestyle='--', label='Ideal Min')
                        ax.axvline(x=0.8, color='green', linestyle='--', label='Ideal Max')
                    else:
                        ax.axvline(x=-5, color='green', linestyle='--', label='Ideal Min')
                        ax.axvline(x=5, color='green', linestyle='--', label='Ideal Max')
                    ax.set_xlabel(metric)
                    ax.set_ylabel('Frequency')
                    ax.legend()
                    st.pyplot(fig)
        
        # Trends in H/Q Ratio Over Time
        st.subheader("Trends in H/Q Ratio Over Time")
        fig, ax = plt.subplots(figsize=(4, 3))
        for player in filtered_data['Player Name'].unique():
            player_data = filtered_data[filtered_data['Player Name'] == player]
            sns.lineplot(x='Date Recorded', y='Hamstring To Quad Ratio', data=player_data, label=player, ax=ax)
        ax.axhline(y=0.6, color='green', linestyle='--', label='Ideal Min')
        ax.axhline(y=0.8, color='green', linestyle='--', label='Ideal Max')
        ax.set_xlabel("Date")
        ax.set_ylabel("H/Q Ratio")
        ax.legend()
        st.pyplot(fig)
        
        # Correlation Heatmap for Muscle Imbalance Metrics
        st.subheader("Correlation Between Key Imbalance Metrics")
        corr = filtered_data[['Hamstring To Quad Ratio', 'Quad Imbalance Percent', 'HamstringImbalance Percent', 'Calf Imbalance Percent', 'Groin Imbalance Percent']].corr()
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(corr, annot=True, cmap='coolwarm', cbar=True, ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)
        
        # Display detailed muscle imbalance table
        st.subheader("Muscle Imbalance Details")
        st.dataframe(
            filtered_data[['Player Name', 'Date Recorded', 'Hamstring To Quad Ratio', 'Risk Score']],
            use_container_width=True
        )
            
    except Exception as e:
        st.error(f"An error occurred in render_muscle_tab: {str(e)}")
