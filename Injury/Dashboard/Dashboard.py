import streamlit as st
from utils import load_data
from performance_dashboard import render_performance_tab
from performance_prediction_dashboard import render_performance_prediction_tab
from injury_prediction_dashboard import render_injury_prediction_tab

# Set page config
st.set_page_config(
    page_title="SlamCuse Analytics - Syracuse Basketball Analysis Dashboard",
    page_icon="🏀",
    layout="wide"
)

# Initialize session state for active tab
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # 0 for Injury History, 1 for Muscle Imbalance, 2 for Sessions, 3 for Performance, 4 for Performance Prediction, 5 for Injury Prediction

def handle_tab_click(tab_index):
    st.session_state.active_tab = tab_index

def main():
    try:
        # Load all data
        muscle_imbalance, sessions, injury_history, performance_data = load_data()
        
        # Create two columns - left for filters, right for content
        col1, col2 = st.columns([1, 4])
        
        # Right panel - Content
        with col2:
            st.title("SlamCuse Analytics 🏀")
            st.subheader("Insights-Driven Performance and Health for Syracuse Basketball")
            
            # Introductory description
            st.markdown("""
                Welcome to **SlamCuse Analytics**, the dedicated platform for Syracuse basketball insights.
                Here, data-driven analysis meets elite performance tracking, focusing on injury history,
                muscle balance, and session metrics to provide a complete view of player health and readiness.
                Navigate through the tabs to uncover trends and details that support informed training decisions,
                injury prevention, and overall performance optimization.
            """)
            
            # Create tabs
            tabs = st.tabs(["Injury History", "Muscle Imbalance", "Sessions", "Performance", "Performance Prediction", "Injury Prediction"])
            
            # Clear previous filters
            with col1:
                st.empty()
            
            # Handle tab content and filters based on active tab
            if st.session_state.active_tab == 0:
                with tabs[0]:
                    from injury_dashboard import render_injury_tab
                    render_injury_tab(injury_history, col1)
            elif st.session_state.active_tab == 1:
                with tabs[1]:
                    from muscle_dashboard import render_muscle_tab
                    render_muscle_tab(muscle_imbalance, col1)
            elif st.session_state.active_tab == 2:
                with tabs[2]:
                    from sessions_dashboard import render_sessions_tab
                    render_sessions_tab(sessions, col1)
            elif st.session_state.active_tab == 3:
                with tabs[3]:
                    render_performance_tab(performance_data, col1)
            elif st.session_state.active_tab == 4:
                with tabs[4]:
                    render_performance_prediction_tab()
            elif st.session_state.active_tab == 5:
                with tabs[5]:
                    render_injury_prediction_tab()
            
            # Tab selection buttons
            for i, tab in enumerate(tabs):
                with tab:
                    if st.button("Load Data", key=f"tab_{i}"):
                        handle_tab_click(i)
                        st.rerun()
                        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()