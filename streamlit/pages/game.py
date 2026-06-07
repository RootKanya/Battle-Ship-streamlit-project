import streamlit as st
from services.api import start_game, get_game_state
from components.scoreboard import render_scoreboard
from components.board import render_board

# --- INITIALIZE SAFE STATE ---
if "game_id" not in st.session_state:
    st.session_state.game_id = None
if "mode" not in st.session_state:
    st.session_state.mode = None

# Cek apakah user sudah login
if not st.session_state.get("token"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.title("Battleship")

# --- PHASE 1: SETUP GAME ---
if not st.session_state.game_id:
    st.subheader("Pilih Mode Permainan")
# ... (lanjutkan dengan kode yang sama seperti sebelumnya) ...

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

    st.markdown(f"### Giliran Saat Ini: **{game_state['turn'].upper()}**")
    st.divider()

    # ==========================================
    # LOGIKA UNTUK MODE 2P (MENGGUNAKAN TABS)
    # ==========================================
    if st.session_state.mode == "2p":
        tab1, tab2 = st.tabs(["👤 Layar Player 1", "👤 Layar Player 2"])
        
        # --- TAB PLAYER 1 ---
        with tab1:
            st.info("Jangan mengintip tab lawan! (Honor System)")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                render_scoreboard("Player 1 (Kamu)", game_state["player1"]["score"], game_state["player1"]["remaining_ships"])
            with col_s2:
                render_scoreboard("Player 2 (Musuh)", game_state["player2"]["score"], game_state["player2"]["remaining_ships"])
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.markdown("#### 🛡️ Peta Kapal Kamu")
                render_board(game_state["player1"]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)
            with col_b2:
                st.markdown("#### ⚔️ Peta Target (Serang P2)")
                # Papan target hanya bisa diklik jika ini giliran Player 1
                is_p1_turn = (game_state["turn"] == "player1")
                render_board(game_state["player1"]["target_board"], is_interactive=is_p1_turn, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)

        # --- TAB PLAYER 2 ---
        with tab2:
            st.info("Jangan mengintip tab lawan! (Honor System)")
            col_s3, col_s4 = st.columns(2)
            with col_s3:
                render_scoreboard("Player 2 (Kamu)", game_state["player2"]["score"], game_state["player2"]["remaining_ships"])
            with col_s4:
                render_scoreboard("Player 1 (Musuh)", game_state["player1"]["score"], game_state["player1"]["remaining_ships"])
            
            col_b3, col_b4 = st.columns(2)
            with col_b3:
                st.markdown("#### 🛡️ Peta Kapal Kamu")
                render_board(game_state["player2"]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role="player2", token=st.session_state.token)
            with col_b4:
                st.markdown("#### ⚔️ Peta Target (Serang P1)")
                # Papan target hanya bisa diklik jika ini giliran Player 2
                is_p2_turn = (game_state["turn"] == "player2")
                render_board(game_state["player2"]["target_board"], is_interactive=is_p2_turn, game_id=st.session_state.game_id, player_role="player2", token=st.session_state.token)

    # ==========================================
    # LOGIKA UNTUK MODE 1P (TAMPILAN NORMAL 1 LAYAR)
    # ==========================================
    else:
        col_score1, col_score2 = st.columns(2)
        with col_score1:
            render_scoreboard("Player 1", game_state["player1"]["score"], game_state["player1"]["remaining_ships"])
        with col_score2:
            render_scoreboard("AI Bot", game_state["player2"]["score"], game_state["player2"]["remaining_ships"])

        col_board1, col_board2 = st.columns(2)
        
        with col_board1:
            st.markdown("#### 🛡️ Peta Kapal Kamu")
            st.caption("Lihat posisi kapalmu dan tembakan musuh.")
            render_board(game_state["player1"]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)
            
        with col_board2:
            st.markdown("#### ⚔️ Peta Target (Musuh)")
            st.caption("Klik kordinat untuk menembak!")
            # Di mode 1P, board ini selalu interaktif (kecuali game over, tapi kita belum set game over)
            render_board(game_state["player1"]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)