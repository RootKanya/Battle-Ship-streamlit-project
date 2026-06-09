import streamlit as st

def render_scoreboard(player_name, score, remaining_ships):
    st.markdown(f"### {player_name}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", score)
    with col2:
        st.metric("Sisa Kapal", remaining_ships)
    
    st.divider()