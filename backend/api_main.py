from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import random
import sqlite3

app = FastAPI(title="Battleship API")

# ==========================================
# SQL DATABASE SETUP
# ==========================================

conn = sqlite3.connect("battleship.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        score INTEGER DEFAULT 0
    )
""")
conn.commit()
tokens_db = {}      
games_db = {}       

class AuthRequest(BaseModel):
    username: str
    password: str

class GameStartRequest(BaseModel):
    mode: str  

class MoveRequest(BaseModel):
    player: str 
    x: int    
    y: int    

def create_empty_board():
    return [[0 for _ in range(10)] for _ in range(10)]

def place_ships():
    """Randomly places 5 ships on a 10x10 board."""
    board = create_empty_board()
    ship_lengths = [5, 4, 3, 3, 2] # Carrier, Battleship, Destroyer, Submarine, Patrol
    
    for length in ship_lengths:
        placed = False
        while not placed:
            orientation = random.choice(["H", "V"])
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            if orientation == "H" and col + length > 10: continue
            if orientation == "V" and row + length > 10: continue

            overlap = False
            for i in range(length):
                if orientation == "H" and board[row][col+i] == 1: overlap = True
                if orientation == "V" and board[row+i][col] == 1: overlap = True
            
            if not overlap:
                for i in range(length):
                    if orientation == "H": board[row][col+i] = 1
                    if orientation == "V": board[row+i][col] = 1
                placed = True
    return board

def process_move(game_id: str, x: int, y: int):
    """Handles the logic of firing a shot"""
    game = games_db[game_id]
    attacker = game["turn"]
    defender = "player2" if attacker == "player1" else "player1"
    
    if game[attacker]["target_board"][x][y] in [2, 3]:
        return game 

    if game[defender]["board"][x][y] == 1:
        # HIT
        game[defender]["board"][x][y] = 2
        game[attacker]["target_board"][x][y] = 2
        game[attacker]["score"] += 100
        game[defender]["remaining_ships"] -= 1 
    else:
        # MISS
        game[defender]["board"][x][y] = 3
        game[attacker]["target_board"][x][y] = 3
        game[attacker]["score"] = max(0, game[attacker]["score"] - 10)

    # Switch turn
    game["turn"] = defender

def ai_turn(game_id: str):
    """Simple AI that picks a random valid coordinate"""
    game = games_db[game_id]
    valid_move = False
    while not valid_move:
        x, y = random.randint(0, 9), random.randint(0, 9)
        if game["player2"]["target_board"][x][y] == 0:
            valid_move = True
            process_move(game_id, x, y)

# ==========================================
# AUTH ENDPOINTS
# ==========================================
@app.post("/register")
def register(user: AuthRequest):
    try:

        cursor.execute("INSERT INTO users (username, password, score) VALUES (?, ?, 0)", 
                       (user.username, user.password))
        conn.commit()
        return {"message": "User registered successfully"}
    except sqlite3.IntegrityError:
        # IntegrityError happens if the username already exists (because it's a PRIMARY KEY)
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login")
def login(user: AuthRequest):

    cursor.execute("SELECT password FROM users WHERE username = ?", (user.username,))
    row = cursor.fetchone()
    
    if not row or row[0] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = str(uuid.uuid4())
    tokens_db[token] = user.username
    return {"access_token": token}

# ==========================================
# LEADERBOARD 
# ==========================================
@app.get("/leaderboard")
def get_leaderboard():
    # Grab top scores directly from SQL using ORDER BY
    cursor.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()
    
    # Convert SQL rows into a list of dictionaries for Streamlit
    leaderboard = [{"username": row[0], "score": row[1]} for row in rows]
    return leaderboard

# ==========================================
# ENDPOINTS
# ==========================================
def get_user_from_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return tokens_db[token]

@app.post("/game/start")
def start_game(req: GameStartRequest, authorization: str = Header(None)):
    username = get_user_from_token(authorization)
    game_id = str(uuid.uuid4())
    
    games_db[game_id] = {
        "mode": req.mode,
        "turn": "player1",
        "player1": {
            "username": username,
            "score": 0,
            "remaining_ships": 17,
            "board": place_ships(),
            "target_board": create_empty_board()
        },
        "player2": {
            "username": "AI Bot" if req.mode == "1p" else "Player 2",
            "score": 0,
            "remaining_ships": 17,
            "board": place_ships(),
            "target_board": create_empty_board()
        }
    }
    return {"game_id": game_id}

@app.get("/game/{game_id}")
def get_game_state(game_id: str, authorization: str = Header(None)):
    get_user_from_token(authorization)
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    return games_db[game_id]

@app.post("/game/{game_id}/move")
def make_move(game_id: str, move: MoveRequest, authorization: str = Header(None)):
    get_user_from_token(authorization)
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games_db[game_id]

    if game["turn"] != move.player:
        return game 
        
    process_move(game_id, move.x, move.y)
    
    if game["mode"] == "1p" and game["turn"] == "player2":
        ai_turn(game_id)
        
    if move.player == "player1":
        cursor.execute("UPDATE users SET score = score + ? WHERE username = ?", 
                       (game["player1"]["score"], game["player1"]["username"]))
        conn.commit()
            
    return game