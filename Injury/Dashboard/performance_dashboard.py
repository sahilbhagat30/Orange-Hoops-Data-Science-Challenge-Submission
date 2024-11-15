import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from filters import performance_filters

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
        filtered_data = performance_data[performance_data['Shooter'].isin(selected_shooters)]
        
        # Display KPIs in a row
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            total_shots = filtered_data['Shots Attempted'].sum()
            st.metric(label="Total Shots Attempted", value=total_shots)
        
        with kpi_col2:
            avg_accuracy = filtered_data['Shot Accuracy'].mean() * 100  # Assuming Shot Accuracy is a decimal
            st.metric(label="Average Shot Accuracy", value=f"{avg_accuracy:.2f}%")
        
        with kpi_col3:
            top_shooter = filtered_data.groupby('Shooter')['Points'].sum().idxmax()
            top_points = filtered_data.groupby('Shooter')['Points'].sum().max()
            st.metric(label="Top Shooter", value=top_shooter, delta=f"{top_points} points")
        
        with kpi_col4:
            avg_points_per_game = filtered_data['Points'].mean()
            st.metric(label="Average Points per Game", value=f"{avg_points_per_game:.1f}")
        
        # Create two rows with two columns each for visualizations
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        # Shot Accuracy Distribution
        with row1_col1:
            st.subheader("Shot Accuracy Distribution")
            fig1 = plt.figure(figsize=(5, 4))
            sns.histplot(filtered_data['Shot Accuracy'], bins=10, kde=True)
            plt.xlabel("Shot Accuracy")
            plt.ylabel("Frequency")
            plt.title("Distribution of Shot Accuracy")
            st.pyplot(fig1)
            plt.close()
        
        # Points by Shooter
        with row1_col2:
            st.subheader("Points by Shooter")
            fig2 = plt.figure(figsize=(5, 4))
            points_by_shooter = filtered_data.groupby('Shooter')['Points'].sum().sort_values(ascending=False)
            sns.barplot(x=points_by_shooter.index, y=points_by_shooter.values)
            plt.xlabel("Shooter")
            plt.ylabel("Total Points")
            plt.title("Total Points by Shooter")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
            plt.close()
        
        # Shooting Accuracy Over Time
        with row2_col1:
            st.subheader("Shooting Accuracy Over Time")
            fig3 = plt.figure(figsize=(5, 4))
            filtered_data['Game Date'] = pd.to_datetime(filtered_data['Game Date'])
            accuracy_over_time = filtered_data.groupby('Game Date')['Shot Accuracy'].mean()
            plt.plot(accuracy_over_time.index, accuracy_over_time.values, marker='o')
            plt.xlabel("Game Date")
            plt.ylabel("Average Shot Accuracy")
            plt.title("Shot Accuracy Over Time")
            plt.xticks(rotation=45)
            st.pyplot(fig3)
            plt.close()
        
        # Points per Game Distribution
        with row2_col2:
            st.subheader("Points per Game Distribution")
            fig4 = plt.figure(figsize=(5, 4))
            sns.boxplot(x='Shooter', y='Points', data=filtered_data)
            plt.xlabel("Shooter")
            plt.ylabel("Points per Game")
            plt.title("Points per Game Distribution by Shooter")
            plt.xticks(rotation=45)
            st.pyplot(fig4)
            plt.close()
        
        # Display detailed performance table
        st.subheader("Performance Details")
        st.dataframe(
            filtered_data[['Shooter', 'Game Date', 'Points', 'Shot Accuracy', 'Shots Attempted']],
            use_container_width=True
        )
    except Exception as e:
        st.error(f"An error occurred in render_performance_tab: {str(e)}")