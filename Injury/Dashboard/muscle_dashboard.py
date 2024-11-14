import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from filters import muscle_filters
from io import BytesIO

# Set a consistent style for the plots and apply custom color palette
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

def calculate_risk_score(row):
    risk_score = 0
    hq_ratio = row['Hamstring To Quad Ratio']
    if hq_ratio < 0.6:
        risk_score += (0.6 - hq_ratio) * 10
    elif hq_ratio > 0.8:
        risk_score += (hq_ratio - 0.8) * 10
    imbalance_cols = ['Quad Imbalance Percent', 'HamstringImbalance Percent', 'Calf Imbalance Percent', 'Groin Imbalance Percent']
    for col in imbalance_cols:
        imbalance = abs(row[col])
        if imbalance > 5:
            risk_score += (imbalance - 5) * 0.5
    return risk_score

def render_muscle_tab(muscle_data, filter_col):
    try:
        selected_players, selected_metrics = muscle_filters(muscle_data, filter_col)
        filtered_data = muscle_data[(muscle_data['Player Name'].isin(selected_players))]
        
        # Calculate Risk Score for each player
        filtered_data['Risk Score'] = filtered_data.apply(calculate_risk_score, axis=1)
        
        # Calculate KPIs
        st.write("### Key Performance Indicators")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            st.metric(label="Total Assessments", value=len(filtered_data))
        with kpi_col2:
            avg_hq_ratio = filtered_data['Hamstring To Quad Ratio'].mean()
            st.metric(label="Avg H/Q Ratio", value=f"{avg_hq_ratio:.2f}", delta="Ideal: 0.6-0.8")
        with kpi_col3:
            # Adjusted threshold for high-risk players
            high_risk = len(filtered_data[filtered_data['Risk Score'] > 10])
            st.metric(label="High Risk Players", value=high_risk, delta=f"{(high_risk / len(filtered_data) * 100):.1f}% of total")
        with kpi_col4:
            avg_risk = filtered_data['Risk Score'].mean()
            st.metric(label="Average Risk Score", value=f"{avg_risk:.1f}", delta=f"Max: {filtered_data['Risk Score'].max():.1f}")

        # Muscle Imbalance Metrics Distributions
        metrics = ['Hamstring To Quad Ratio', 'Quad Imbalance Percent', 'HamstringImbalance Percent', 'Calf Imbalance Percent', 'Groin Imbalance Percent']
        st.write("### Muscle Imbalance Metrics Distributions")
        for i in range(0, len(metrics), 2):
            cols = st.columns(2)
            for j, metric in enumerate(metrics[i:i + 2]):
                with cols[j]:
                    st.subheader(f"Distribution of {metric}")
                    fig, ax = plt.subplots(figsize=(5, 3))
                    sns.histplot(filtered_data[metric], kde=True, color=custom_palette[2], edgecolor="black", alpha=0.8, ax=ax)
                    if metric == 'Hamstring To Quad Ratio':
                        ax.axvline(x=0.6, color=custom_palette[3], linestyle='--', label='Ideal Min')
                        ax.axvline(x=0.8, color=custom_palette[3], linestyle='--', label='Ideal Max')
                    else:
                        ax.axvline(x=-5, color=custom_palette[3], linestyle='--', label='Ideal Min')
                        ax.axvline(x=5, color=custom_palette[3], linestyle='--', label='Ideal Max')
                    ax.set_xlabel(metric)
                    ax.set_ylabel('Frequency')
                    ax.legend()
                    sns.despine(left=True, bottom=True)  # Remove left and bottom borders
                    st.pyplot(fig)

        # Trends in H/Q Ratio Over Time
        st.write("### Trends in H/Q Ratio Over Time")
        fig, ax = plt.subplots(figsize=(6, 4))
        for player in filtered_data['Player Name'].unique():
            player_data = filtered_data[filtered_data['Player Name'] == player]
            sns.lineplot(x='Date Recorded', y='Hamstring To Quad Ratio', data=player_data, label=player, ax=ax)

        ax.axhline(y=0.6, color=custom_palette[3], linestyle='--', label='Ideal Min')
        ax.axhline(y=0.8, color=custom_palette[3], linestyle='--', label='Ideal Max')
        ax.set_xlabel("Date")
        ax.set_ylabel("H/Q Ratio")
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
        sns.despine(left=True, bottom=True)
        st.pyplot(fig)

        # Correlation Heatmap for Muscle Imbalance Metrics
        st.write("### Correlation Between Key Imbalance Metrics")
        corr = filtered_data[['Hamstring To Quad Ratio', 'Quad Imbalance Percent', 'HamstringImbalance Percent', 'Calf Imbalance Percent', 'Groin Imbalance Percent']].corr()
        fig, ax = plt.subplots(figsize=(5.5, 4), dpi=100)
        sns.heatmap(corr, annot=True, cmap='coolwarm', cbar=False, ax=ax, annot_kws={"size": 8}, fmt=".2f", linewidths=0.5)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center', fontsize=8)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=8)
        ax.set_title("Correlation Heatmap", fontsize=10)
        sns.despine(left=True, bottom=True)
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        st.image(buf, use_container_width=True)

        # Muscle Imbalance Details Table
        st.write("### Muscle Imbalance Details")
        st.dataframe(filtered_data[['Player Name', 'Date Recorded', 'Hamstring To Quad Ratio', 'Risk Score']], use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred in render_muscle_tab: {str(e)}")
