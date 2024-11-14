import streamlit as st
from utils import load_data

# Set page config
st.set_page_config(
    page_title="Player Injury Analysis Dashboard",
    page_icon="🏃",
    layout="wide"
)

# Initialize session state for active tab
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # 0 for Injury History, 1 for Muscle Imbalance, 2 for Sessions

def handle_tab_click(tab_index):
    st.session_state.active_tab = tab_index

def main():
    try:
        # Load all data
        muscle_imbalance, sessions, injury_history = load_data()
        
        # Create two columns - left for filters, right for content
        col1, col2 = st.columns([1, 4])
        
        # Right panel - Content
        with col2:
            st.title("Player Injury Analysis Dashboard")
            
            # Create tabs
            tabs = st.tabs(["Injury History", "Muscle Imbalance", "Sessions"])
            
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
            
            # Tab selection buttons
            for i, tab in enumerate(tabs):
                with tab:
                    if st.button("Select", key=f"tab_{i}"):
                        handle_tab_click(i)
                        st.rerun()
                        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()