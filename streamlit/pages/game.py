import streamlit as st
from services.api import start_game, get_game_state
from components.scoreboard import render_scoreboard
from components.board import render_board

# --- INITIALIZE SAFE STATE ---
if "game_id" not in st.session_state:
    st.session_state.game_id = None
if "mode" not in st.session_state:
    st.session_state.mode = None
if "ready_player" not in st.session_state:
    st.session_state.ready_player = None

if not st.session_state.get("token"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

# --- HEADER & QUIT BUTTON ---
col_title, col_quit = st.columns([8, 2])
with col_title:
    st.title("Battleship")

if st.session_state.game_id:
    with col_quit:
        st.write("")
        if st.button("Quit Game", use_container_width=True):
            st.session_state.game_id = None
            st.session_state.ready_player = None
            st.rerun()

# --- PHASE 1: SETUP GAME ---
if not st.session_state.game_id:
    st.subheader("Pilih Mode Permainan")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Pilihan 1P (Lawan Bot AI)", use_container_width=True):
            data = start_game("1p", st.session_state.token)
            st.session_state.game_id = data.get("game_id")
            st.session_state.mode = "1p"
            st.session_state.ready_player = "player1" # Langsung siap untuk 1p
            st.rerun()
    with col2:
        if st.button("Pilihan 2P (Multiplayer Local)", use_container_width=True):
            data = start_game("2p", st.session_state.token)
            st.session_state.game_id = data.get("game_id")
            st.session_state.mode = "2p"
            st.session_state.ready_player = None # Paksa masuk buffer screen
            st.rerun()

# --- PHASE 2: GAMEPLAY ---
else:

    game_state = get_game_state(st.session_state.game_id, st.session_state.token)
    
    if "player1" not in game_state or "turn" not in game_state:
        st.error("⚠️ Sesi permainan hilang (server backend baru saja di-restart).")
        if st.button("Buat Game Baru", use_container_width=True):
            st.session_state.game_id = None
            st.session_state.ready_player = None
            st.rerun()
        st.stop() 
        
    # ==========================================
    # GAME OVER / WIN CHECK
    # ==========================================
    p1_ships = game_state["player1"]["remaining_ships"]
    p2_ships = game_state["player2"]["remaining_ships"]
    
    if p1_ships == 0 or p2_ships == 0:
        st.markdown("<h1 style='text-align: center;'>🏆 GAME OVER 🏆</h1>", unsafe_allow_html=True)
        st.divider()
        
        if p2_ships == 0:
            st.success(f"🎉 SELAMAT! **{game_state['player1']['username'].upper()}** Menang!")
            st.balloons() 
        elif p1_ships == 0:
            st.error(f"💀 DEFEAT! **{game_state['player2']['username'].upper()}** Menang!")
            
        st.write("") 
        if st.button("Kembali ke Menu Utama", use_container_width=True):
            st.session_state.game_id = None
            st.session_state.ready_player = None
            st.rerun()
            
        st.stop() 

    # ==========================================
    # RENDER NORMAL GAME
    # ==========================================
    current_turn = game_state["turn"]

    st.markdown(f"### Giliran Saat Ini: **{current_turn.upper()}**")
    st.divider()

    if st.session_state.mode == "2p":
        
        if st.session_state.ready_player != current_turn:
            st.error("🛑  **Selamat Datang di Buffer Screen** 🛑")
            st.warning(f"Giliran telah berganti. Silakan berikan perangkat ke **{current_turn.upper()}**.")
            
            if st.button(f"✅  Saya  {current_turn.upper()}, saya siap bermain!", use_container_width=True):
                st.session_state.ready_player = current_turn
                st.rerun()
                
        else:
            me = current_turn
            enemy = "player2" if me == "player1" else "player1"
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                render_scoreboard(f"{me.upper()} (Kamu)", game_state[me]["score"], game_state[me]["remaining_ships"])
            with col_s2:
                render_scoreboard(f"{enemy.upper()} (Musuh)", game_state[enemy]["score"], game_state[enemy]["remaining_ships"])
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.markdown("#### 🛡️ Peta Kapal Kamu")
                render_board(game_state[me]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role=f"{me}_defense", token=st.session_state.token)
            with col_b2:
                st.markdown(f"#### ⚔️ Peta Target (Serang {enemy.upper()})")
                render_board(game_state[me]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role=me, token=st.session_state.token)

    # MODE 1P (TAMPILAN NORMAL)
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
            render_board(game_state["player1"]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role="1p_defense", token=st.session_state.token)
        with col_board2:
            st.markdown("#### ⚔️ Peta Target (Musuh)")
            st.caption("Klik kordinat untuk menembak!")
            render_board(game_state["player1"]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)