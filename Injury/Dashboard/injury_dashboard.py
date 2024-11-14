import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from filters import injury_filters

def render_injury_tab(injury_data, filter_col):
    try:
        # Get filter selections
        selected_players, selected_severity = injury_filters(injury_data, filter_col)
        
        # Ensure we have valid data
        if injury_data is None or len(injury_data) == 0:
            st.error("No valid injury data available")
            return
            
        # Filter data based on selections
        filtered_data = injury_data[
            (injury_data['Name'].isin(selected_players)) &
            (injury_data['Severity'].isin(selected_severity))
        ]
        
        # Display KPIs in a row
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric(
                label="Total Injuries",
                value=len(filtered_data)
            )
            
        with kpi_col2:
            avg_recovery = filtered_data['Recovery Time (days)'].mean()
            st.metric(
                label="Average Recovery Time",
                value=f"{avg_recovery:.1f} days" if not pd.isna(avg_recovery) else "N/A"
            )
            
        with kpi_col3:
            if len(filtered_data) > 0:
                most_common_injury = filtered_data['Injury Type'].mode().iloc[0]
                injury_count = filtered_data['Injury Type'].value_counts().iloc[0]
                st.metric(
                    label="Most Common Injury",
                    value=most_common_injury,
                    delta=f"{injury_count} cases"
                )
            else:
                st.metric(
                    label="Most Common Injury",
                    value="N/A"
                )
                
        with kpi_col4:
            if len(filtered_data) > 0:
                most_affected = filtered_data['Body Part'].mode().iloc[0]
                part_count = filtered_data['Body Part'].value_counts().iloc[0]
                st.metric(
                    label="Most Affected Body Part",
                    value=most_affected,
                    delta=f"{part_count} injuries"
                )
            else:
                st.metric(
                    label="Most Affected Body Part",
                    value="N/A"
                )
        
        # Create two rows with two columns each for visualizations
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        # Injury Type Distribution
        with row1_col1:
            st.subheader("Injury Type Distribution")
            fig1 = plt.figure(figsize=(4, 3))
            sns.countplot(data=filtered_data, x='Injury Type', palette='Set2')
            plt.xticks(rotation=45)
            plt.xlabel('Injury Type')
            plt.ylabel('Count')
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close()
        
        # Recovery Time by Body Part
        with row1_col2:
            st.subheader("Recovery Time by Body Part")
            fig2 = plt.figure(figsize=(4, 3))
            sns.boxplot(data=filtered_data, x='Body Part', y='Recovery Time (days)', palette='Set2')
            plt.xticks(rotation=45)
            plt.xlabel('Body Part')
            plt.ylabel('Recovery Time (days)')
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()
        
        # Injury Frequency Over Time
        with row2_col1:
            st.subheader("Injury Frequency Over Time")
            fig3 = plt.figure(figsize=(4, 3))
            injury_freq = filtered_data.set_index('Injury Date').resample('M')['Injury Type'].count()
            plt.plot(injury_freq.index, injury_freq.values, marker='o')
            plt.xticks(rotation=45)
            plt.xlabel('Date')
            plt.ylabel('Number of Injuries')
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()
            
        # Severity Distribution
        with row2_col2:
            st.subheader("Severity Distribution")
            fig4 = plt.figure(figsize=(4, 3))
            severity_counts = filtered_data['Severity'].value_counts()
            plt.pie(severity_counts.values, 
                   labels=severity_counts.index, 
                   autopct='%1.1f%%',
                   colors=sns.color_palette('Set2'))
            plt.axis('equal')
            st.pyplot(fig4)
            plt.close()
        
        # Display detailed injury table
        st.subheader("Injury Details")
        st.dataframe(
            filtered_data[['Name', 'Injury Date', 'Injury Type', 'Body Part', 'Severity', 'Recovery Time (days)']],
            use_container_width=True
        )
    except Exception as e:
        st.error(f"An error occurred in render_injury_tab: {str(e)}")