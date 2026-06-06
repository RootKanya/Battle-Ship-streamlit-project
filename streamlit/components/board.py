import streamlit as st
from services.api import make_move

def render_board(board_data, is_interactive, game_id, player_role, token):
    
    # State 0 (Kosong) sengaja tidak dimasukkan agar tidak dirender
    icons = {
        1: ":material/directions_boat:",       
        2: ":material/local_fire_department:",
        3: ":material/close:"                  
    }
    
    for r in range(10):
        cols = st.columns(10)
        for c in range(10):
            cell_val = board_data[r][c]
            
            icon_code = icons.get(cell_val, None) 
            
            with cols[c]:
                label = "\u200b" 
                
                # Jika interaktif (board musuh) dan belum ditembak (0 atau 1)
                if is_interactive and cell_val in [0, 1]: 
                    if st.button(label, icon=icon_code, key=f"btn_{player_role}_{r}_{c}"):
                        make_move(game_id, player_role, r, c, token)
                        st.rerun()
                else:
                    st.button(label, icon=icon_code, key=f"stat_{player_role}_{r}_{c}", disabled=True)