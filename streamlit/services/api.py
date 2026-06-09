import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def login_user(username, password):
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    return response

def register_user(username, password):
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
    return response

def get_leaderboard():
    response = requests.get(f"{BASE_URL}/leaderboard")
    if response.status_code == 200:
        return response.json()
    return []

def start_game(mode, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/game/start", json={"mode": mode}, headers=headers)
    return response.json()

def make_move(game_id, player, x, y, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/game/{game_id}/move", 
        json={"player": player, "x": x, "y": y},
        headers=headers
    )
    return response.json()

def get_game_state(game_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/game/{game_id}", headers=headers)
    return response.json()