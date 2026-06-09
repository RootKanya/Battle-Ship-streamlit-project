import streamlit as st
import numpy as np

# Daftar armada standar Battleship
FLEET = [
    {"name": "Carrier", "size": 5},
    {"name": "Battleship", "size": 4},
    {"name": "Cruiser", "size": 3},
    {"name": "Submarine", "size": 3},
    {"name": "Destroyer", "size": 2}
]

def init_setup_state():
    if "draft_board" not in st.session_state:
        st.session_state.draft_board = np.zeros((10, 10), dtype=int).tolist()
    if "ships_to_place" not in st.session_state:
        st.session_state.ships_to_place = FLEET.copy()
    if "orientation" not in st.session_state:
        st.session_state.orientation = "Horizontal"

def can_place_ship(board, row, col, size, orientation):
    if orientation == "Horizontal":
        if col + size > 10: return False 
        for c in range(col, col + size):
            if board[row][c] != 0: return False 
    else: 
        if row + size > 10: return False 
        for r in range(row, row + size):
            if board[r][col] != 0: return False 
    return True

def place_ship(row, col):
    if not st.session_state.ships_to_place:
        return 

    current_ship = st.session_state.ships_to_place[0]
    size = current_ship["size"]
    orientation = st.session_state.orientation
    board = st.session_state.draft_board

    if can_place_ship(board, row, col, size, orientation):
        if orientation == "Horizontal":
            for c in range(col, col + size):
                board[row][c] = 1 
        else:
            for r in range(row, row + size):
                board[r][col] = 1

        st.session_state.ships_to_place.pop(0)
    else:
        st.toast("Posisi tidak valid! Menabrak batas atau kapal lain.", icon=":material/warning:")

def render_setup_phase():
    init_setup_state()
    
    st.markdown('<h3 class="text-gray-200">Fase Persiapan: Susun Armadamu!</h3>', unsafe_allow_html=True)
    
    col_ui, col_board = st.columns([1, 2])
    
    with col_ui:
        st.markdown('<h4 class="text-blue-400">Kontrol Panel</h4>', unsafe_allow_html=True)
        
        if st.session_state.ships_to_place:
            current_ship = st.session_state.ships_to_place[0]
            st.info(f"**Sekarang Meletakkan:**\n\n{current_ship['name']} ({current_ship['size']} Kotak)", icon=":material/directions_boat:")
            
            st.session_state.orientation = st.radio(
                "Rotasi Kapal:", 
                ["Horizontal", "Vertical"], 
                horizontal=True
            )
            
            if st.button("Reset Papan", icon=":material/refresh:"):
                del st.session_state.draft_board
                del st.session_state.ships_to_place
                st.rerun()
        else:
            st.success("Semua kapal sudah diposisikan!", icon=":material/check_circle:")
            if st.button("MULAI PERMAINAN", icon=":material/play_arrow:", type="primary", use_container_width=True):
                st.session_state.setup_complete = True
                st.rerun()

    with col_board:
        # CSS untuk menempelkan kotak agar terlihat seperti 1 kapal panjang
        st.markdown("""
        <style>
            div[data-testid="column"] { padding: 0 !important; gap: 0 !important; }
            div.stButton button {
                width: 100% !important; height: 45px !important; border-radius: 0 !important;
                border: 1px solid #334155 !important; padding: 0 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        for r in range(10):
            # Hilangkan gap agar kotak menempel
            cols = st.columns(10)
            for c in range(10):
                is_ship = st.session_state.draft_board[r][c] == 1
                icon_code = ":material/directions_boat:" if is_ship else None
                
                with cols[c]:
                    if is_ship:
                        # Tipe primary memberi warna solid (terlihat seperti 1 blok jika menempel)
                        st.button("\u200b", icon=icon_code, key=f"setup_s_{r}_{c}", type="primary", disabled=True)
                    else:
                        if st.button("\u200b", key=f"setup_e_{r}_{c}"):
                            place_ship(r, c)
                            st.rerun()