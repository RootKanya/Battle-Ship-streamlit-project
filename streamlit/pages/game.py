import streamlit as st
from services.api import start_custom_game, get_game_state
from components.scoreboard import render_scoreboard
from components.board import render_board
from components.setup_board import render_setup_phase

# --- INJEKSI TAILWIND, FONTAWESOME, & CUSTOM CSS ---
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* MEMAKSA STREAMLIT FULL WIDTH DARI UJUNG KE UJUNG */
    .block-container {
        max-width: 100% !important;
        padding-top: 6rem !important; /* Menghindari area Deploy */
        padding-right: 3rem !important;
        padding-left: 3rem !important;
        padding-bottom: 2rem !important;
    }

    /* Desain area buffer screen untuk mode 2P */
    .buffer-box {
        background-color: #1e293b; 
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    /* Penyesuaian header papan (Board) */
    .board-header {
        font-size: 1.5rem;
        font-weight: 800;
        color: #60a5fa; 
        margin-bottom: 0.2rem;
    }
    .board-caption {
        color: #94a3b8; 
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SAFE STATE ---
if "game_id" not in st.session_state:
    st.session_state.game_id = None
if "mode" not in st.session_state:
    st.session_state.mode = None
if "ready_player" not in st.session_state:
    st.session_state.ready_player = None
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

# Cek apakah user sudah login
if not st.session_state.get("token"):
    st.warning("Silakan login terlebih dahulu untuk bermain.", icon=":material/lock:")
    st.stop()

# ==========================================
# PHASE 1: SETUP (PENEMPATAN KAPAL MANUAL)
# ==========================================
if not st.session_state.setup_complete:
    render_setup_phase()
    st.stop() # Hentikan eksekusi kode di bawah ini sampai setup selesai

# ==========================================
# PHASE 2: AUTO-START WITH CUSTOM BOARD
# ==========================================
if not st.session_state.game_id:
    selected_mode = st.session_state.get("game_mode", "1p")
    
    with st.spinner("Mengirim formasi ke markas..."):
        # Panggil endpoint FastAPI baru yang bisa menerima custom draft_board
        data = start_custom_game(
            mode=selected_mode, 
            token=st.session_state.token,
            custom_board=st.session_state.draft_board
        )
        st.session_state.game_id = data.get("game_id")
        st.session_state.mode = selected_mode
        st.session_state.ready_player = "player1" if selected_mode == "1p" else None
        st.rerun()

# ==========================================
# PHASE 3: GAMEPLAY
# ==========================================
game_state = get_game_state(st.session_state.game_id, st.session_state.token)
current_turn = game_state["turn"]

# --- HEADER PANEL (Giliran & Tombol Keluar) ---
col_turn, col_quit = st.columns([8, 2])
with col_turn:
    st.markdown(f'<div class="text-4xl font-extrabold text-gray-200 mt-3 mb-2">Giliran Saat Ini: <span class="text-blue-500 uppercase">{current_turn}</span></div>', unsafe_allow_html=True)
with col_quit:
    if st.button("Akhiri Game", icon=":material/cancel:", use_container_width=True):
        st.session_state.game_id = None
        st.session_state.ready_player = None
        st.session_state.setup_complete = False # Reset setup juga
        if "draft_board" in st.session_state:
            del st.session_state.draft_board
            del st.session_state.ships_to_place
        st.switch_page("pages/home.py")

st.divider()

# ==========================================
# MODE 2P (HOT-SEAT / BUFFER SCREEN)
# ==========================================
if st.session_state.mode == "2p":
    if st.session_state.ready_player != current_turn:
        st.markdown(f"""
        <div class="buffer-box">
            <i class="fa-solid fa-hand-paper text-6xl text-yellow-500 mb-4"></i>
            <h2 class="text-4xl font-bold text-gray-200">Pergantian Giliran</h2>
            <p class="text-gray-400 mt-2 text-xl">Jangan mengintip! Silakan berikan perangkat ke <b class="text-blue-400 uppercase">{current_turn}</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_space1, col_btn, col_space2 = st.columns([1, 1.5, 1])
        with col_btn:
            if st.button(f"SAYA {current_turn.upper()}, SAYA SIAP!", icon=":material/check_circle:", type="primary", use_container_width=True):
                st.session_state.ready_player = current_turn
                st.rerun()
    else:
        me = current_turn
        enemy = "player2" if me == "player1" else "player1"
        
        col_s1, col_space_s, col_s2 = st.columns([10, 2, 10])
        with col_s1:
            render_scoreboard(f"{me.upper()} (Kamu)", game_state[me]["score"], game_state[me]["remaining_ships"])
        with col_s2:
            render_scoreboard(f"{enemy.upper()} (Musuh)", game_state[enemy]["score"], game_state[enemy]["remaining_ships"])
        
        st.write("") 
        
        col_b1, col_space_b, col_b2 = st.columns([10, 2, 10])
        with col_b1:
            st.markdown('<div class="board-header"><i class="fa-solid fa-shield-halved mr-2"></i> Peta Kapal Kamu</div>', unsafe_allow_html=True)
            st.markdown('<div class="board-caption">Posisi armada kamu dan riwayat serangan musuh.</div>', unsafe_allow_html=True)
            render_board(game_state[me]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role=f"{me}_defense", token=st.session_state.token)
            
        with col_b2:
            st.markdown(f'<div class="board-header text-red-400"><i class="fa-solid fa-crosshairs mr-2"></i> Peta Target (Serang {enemy.upper()})</div>', unsafe_allow_html=True)
            st.markdown('<div class="board-caption">Klik pada koordinat untuk meluncurkan misil!</div>', unsafe_allow_html=True)
            render_board(game_state[me]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role=me, token=st.session_state.token)

# ==========================================
# MODE 1P (TAMPILAN NORMAL LAWAN AI)
# ==========================================
else:
    col_s1, col_space_s, col_s2 = st.columns([10, 2, 10])
    with col_s1:
        render_scoreboard("Player 1", game_state["player1"]["score"], game_state["player1"]["remaining_ships"])
    with col_s2:
        render_scoreboard("AI Bot", game_state["player2"]["score"], game_state["player2"]["remaining_ships"])

    st.write("") 

    col_b1, col_space_b, col_b2 = st.columns([10, 2, 10])
    with col_b1:
        st.markdown('<div class="board-header"><i class="fa-solid fa-shield-halved mr-2"></i> Peta Kapal Kamu</div>', unsafe_allow_html=True)
        st.markdown('<div class="board-caption">Lihat posisi armada kamu dan pantau tembakan musuh.</div>', unsafe_allow_html=True)
        render_board(game_state["player1"]["board"], is_interactive=False, game_id=st.session_state.game_id, player_role="1p_defense", token=st.session_state.token)
        
    with col_b2:
        st.markdown('<div class="board-header" style="color: #f87171;"><i class="fa-solid fa-crosshairs mr-2"></i> Peta Target (Musuh)</div>', unsafe_allow_html=True)
        st.markdown('<div class="board-caption">Klik koordinat grid musuh untuk meluncurkan serangan!</div>', unsafe_allow_html=True)
        render_board(game_state["player1"]["target_board"], is_interactive=True, game_id=st.session_state.game_id, player_role="player1", token=st.session_state.token)