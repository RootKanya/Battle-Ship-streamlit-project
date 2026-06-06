import streamlit as st
from services.api import start_game, get_game_state
from components.scoreboard import render_scoreboard
from components.board import render_board

# Cek apakah user sudah login
if not st.session_state.get("token"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.title("Battleship")

# --- PHASE 1: SETUP GAME ---
if not st.session_state.game_id:
    st.subheader("Pilih Mode Permainan")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Pilihan 1P (Lawan Bot AI)", use_container_width=True):
            data = start_game("1p", st.session_state.token)
            st.session_state.game_id = data.get("game_id")
            st.session_state.mode = "1p"
            st.rerun()
    with col2:
        if st.button("Pilihan 2P (Multiplayer Local)", use_container_width=True):
            data = start_game("2p", st.session_state.token)
            st.session_state.game_id = data.get("game_id")
            st.session_state.mode = "2p"
            st.rerun()

# --- PHASE 2: GAMEPLAY ---
else:
    # Ambil state terbaru dari FastAPI
    game_state = get_game_state(st.session_state.game_id, st.session_state.token)
    

    if st.button("Akhiri Game (Quit)"):
        st.session_state.game_id = None
        st.rerun()

    st.markdown(f"### Giliran Saat Ini: **{game_state['turn']}**")

    # Layout: Jika 1P, tampilkan Peta Kita dan Peta Target (Lawan).
    # Jika 2P Local, tampilkan berdasarkan giliran siapa yang main agar pemain lain tidak mengintip (Opsional, tapi ini logika standar multiplayer local).
    
    current_player = "player1" if game_state["turn"] == "player1" else "player2"
    
    col_score1, col_score2 = st.columns(2)
    with col_score1:
        render_scoreboard("Player 1", game_state["player1"]["score"], game_state["player1"]["remaining_ships"])
    with col_score2:
        p2_name = "AI Bot" if st.session_state.mode == "1p" else "Player 2"
        render_scoreboard(p2_name, game_state["player2"]["score"], game_state["player2"]["remaining_ships"])

    st.divider()

    col_board1, col_board2 = st.columns(2)
    
    with col_board1:
        st.markdown("#### 🛡️ Peta Kapal Kamu")
        st.caption("Lihat posisi kapalmu dan tembakan musuh.")
        # Render board milik current player (tidak interaktif)
        render_board(game_state[current_player]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role=f"{current_player}_defense", token=st.session_state.token)
        
    with col_board2:
        st.markdown("#### ⚔️ Peta Target (Musuh)")
        st.caption("Klik kordinat untuk menembak!")
        # Render target board (interaktif)
        render_board(game_state[current_player]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role=current_player, token=st.session_state.token)