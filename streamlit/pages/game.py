import streamlit as st
from services.api import start_game, get_game_state
from components.scoreboard import render_scoreboard
from components.board import render_board

if "game_id" not in st.session_state:
    st.session_state.game_id = None
if "mode" not in st.session_state:
    st.session_state.mode = None
if "ready_player" not in st.session_state:
    st.session_state.ready_player = None

# Cek apakah user sudah login
if not st.session_state.get("token"):
    st.warning("Silakan login terlebih dahulu.", icon=":material/lock:")
    st.stop()

# HEADER
col_title, col_quit = st.columns([8, 2])

with col_title:
    st.title("Battleship")

if st.session_state.game_id:
    with col_quit:
        st.write("")
        if st.button("Quit Game", icon=":material/logout:", use_container_width=True):
            st.session_state.game_id = None
            st.session_state.ready_player = None
            st.switch_page("pages/home.py")

# AUTO-START GAME
if not st.session_state.game_id:
    selected_mode = st.session_state.get("game_mode", "1p")
    
    with st.spinner("Mempersiapkan area pertempuran..."):
        data = start_game(selected_mode, st.session_state.token)
        st.session_state.game_id = data.get("game_id")
        st.session_state.mode = selected_mode
        
        st.session_state.ready_player = "player1" if selected_mode == "1p" else None
        st.rerun()

# PHASE 2: GAMEPLAY
else:
    game_state = get_game_state(st.session_state.game_id, st.session_state.token)
    current_turn = game_state["turn"]

    st.markdown(f"### Giliran Saat Ini: **{current_turn.upper()}**")
    st.divider()

    #  MODE 2P 
    if st.session_state.mode == "2p":
        
        # Buffer screen
        if st.session_state.ready_player != current_turn:
            st.warning(f"Giliran telah berganti. Silahkan berikan perangkat ke **{current_turn.upper()}**.")
            
            if st.button(f"Saya {current_turn.upper()} siap bermain!", icon=":material/check_circle:", use_container_width=True):
                st.session_state.ready_player = current_turn
                st.rerun()
                
        else:
            me = current_turn
            enemy = "player2" if me == "player1" else "player1"
            
            col_s1, col_space_s, col_s2 = st.columns([10, 1.5, 10])
            with col_s1:
                render_scoreboard(f"{me.upper()} (Kamu)", game_state[me]["score"], game_state[me]["remaining_ships"])
            with col_s2:
                render_scoreboard(f"{enemy.upper()} (Musuh)", game_state[enemy]["score"], game_state[enemy]["remaining_ships"])
            
            st.write("")
            
            col_b1, col_space_b, col_b2 = st.columns([10, 1.5, 10])
            with col_b1:
                st.markdown("#### Peta Kapal Kamu")
                render_board(game_state[me]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role=f"{me}_defense", token=st.session_state.token)
            with col_b2:
                st.markdown(f"#### Peta Target (Serang {enemy.upper()})")
                render_board(game_state[me]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role=me, token=st.session_state.token)

    # MODE 1P 
    else:
        col_score1, col_space_s, col_score2 = st.columns([10, 1.5, 10])
        with col_score1:
            render_scoreboard("Player 1", game_state["player1"]["score"], game_state["player1"]["remaining_ships"])
        with col_score2:
            render_scoreboard("AI Bot", game_state["player2"]["score"], game_state["player2"]["remaining_ships"])

        st.write("")

        col_board1, col_space_b, col_board2 = st.columns([10, 1.5, 10])
        with col_board1:
            st.markdown("#### Peta Kapal Kamu")
            st.caption("Lihat posisi kapalmu dan tembakan musuh.")
            render_board(game_state["player1"]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role="1p_defense", token=st.session_state.token)
        with col_board2:
            st.markdown("#### Peta Target (Musuh)")
            st.caption("Klik kordinat untuk menembak!")
            render_board(game_state["player1"]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)