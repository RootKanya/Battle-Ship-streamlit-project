import streamlit as st
from services.api import make_move

def render_board(board_data, is_interactive, game_id, player_role, token):
    # Prefix unik agar CSS dan Streamlit tidak bingung membedakan tombol papan 1 dan papan 2
    key_prefix = f"board_{player_role}"
    
    # --- INJEKSI CSS KHUSUS GRID BERMAIN ---
    st.markdown(f"""
    <style>
        /* Menghilangkan jarak antar kolom agar rapat seperti grid papan catur */
        div[data-testid="column"] {{
            padding: 0 !important;
            gap: 0 !important;
        }}
        /* Mengubah tombol bawaan Streamlit menjadi kotak persegi sempurna */
        div.stButton button[key^="{key_prefix}"] {{
            width: 100% !important;
            height: 45px !important;
            border-radius: 0 !important;
            border: 1px solid #334155 !important;
            padding: 0 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # --- KAMUS IKON MATERIAL STREAMLIT ---
    # Pastikan menggunakan nama ikon yang valid dari Google Material Symbols
    icons = {
        1: ":material/directions_boat:",       # Kapal Anda
        2: ":material/local_fire_department:", # HIT (Kena tembak / Api)
        3: ":material/water_drop:"             # MISS (Meleset / Jatuh ke air)
    }

    # --- RENDER GRID 10x10 ---
    for r in range(10):
        cols = st.columns(10)
        for c in range(10):
            cell_val = board_data[r][c]
            
            # Ambil ikon sesuai nilai sel. Jika 0 (kosong), hasilnya None (tidak ada ikon)
            icon_code = icons.get(cell_val, None) 
            
            # Label kosong menggunakan karakter zero-width space agar ikon tetap di tengah
            label = "\u200b"
            cell_key = f"{key_prefix}_{r}_{c}"
            
            with cols[c]:
                # ⚔️ JIKA INI PAPAN MUSUH (INTERAKTIF UNTUK MENEMBAK)
                if is_interactive:
                    # Jika sel masih 0 (belum ditembak) atau 1 (kapal musuh yang disembunyikan backend)
                    if cell_val in [0, 1]:
                        # Kotak bisa diklik untuk menembak!
                        if st.button(label, icon=icon_code, key=cell_key):
                            make_move(game_id, player_role, r, c, token)
                            st.rerun() # Refresh layar untuk mengambil state terbaru dari FastAPI
                    else:
                        # Jika sudah ditembak (2 = Hit, 3 = Miss), tombol dimatikan agar tidak diklik 2x
                        st.button(label, icon=icon_code, key=cell_key, disabled=True)
                        
                # 🛡️ JIKA INI PAPAN SENDIRI (HANYA TAMPILAN PERTAHANAN)
                else:
                    # Jika itu kapal kita yang utuh (val=1), beri warna berbeda (primary)
                    btn_type = "primary" if cell_val == 1 else "secondary"
                