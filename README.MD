# Battleship PBKK - FastAPI & Streamlit

A modern, web-based implementation of the classic Battleship board game. This project was built to demonstrate a decoupled architecture using **FastAPI** for a robust backend and **Streamlit** for an interactive, state-driven frontend.

##  Project Features

* **User Authentication:** Secure Registration and Login system using session tokens and cookies.
* **Persistent Database:** Accounts and lifetime scores are saved locally using SQLite (`battleship.db`).
* **Single Player (1P) vs AI:** Play against an automated bot that randomly strikes your board.
* **Local Multiplayer (2P):** A "hot-seat" multiplayer mode featuring a secure **Buffer Screen** to prevent players from peeking at each other's ship placements during turn changes.
* **Global Leaderboard:** Ranks top players based on total points accumulated across all games.

---

##  Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit, Python | Handles the UI, game boards, tabs, and session states. |
| **Backend** | FastAPI, Uvicorn | Manages game logic, turn validation, and AI moves. |
| **Database** | SQLite3 | Built-in Python SQL library for persistent user storage. |

---

##  Project Structure

```text
Battle-Ship-streamlit-project/
├── backend/
│   ├── api_main.py         # FastAPI application & game logic
│   └── battleship.db       # SQLite database (auto-generated)
├── streamlit/
│   ├── main.py             # Streamlit entry point
│   ├── pages/              # UI Pages (login, register, game, leaderboard)
│   ├── components/         # Reusable UI (board, scoreboard)
│   ├── services/           # API connection logic (requests)
│   ├── utils/              # Auth & cookie management
│   └── assets/             # CSS styling
└── README.md
```text

##  How to Run the Project Locally

To run this project, you will need two separate terminal windows—one for the backend server and one for the frontend app.

1. Setup the Virtual Environment

First, ensure you are in the root directory of the project and create a clean Python environment.
Bash

```text
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic streamlit requests pandas streamlit-cookies-manager
```text

2. Start the FastAPI Backend

Open Terminal 1, activate the environment, and start the API server.
Bash

```text
source venv/bin/activate
cd backend
uvicorn api_main:app --reload --port 8000
```text

The backend is now running at http://localhost:8000

3. Start the Streamlit Frontend

Open Terminal 2, activate the environment, and start the Streamlit app.
Bash

```text
source venv/bin/activate
cd streamlit
streamlit run main.py
```text

The game is now playable at http://localhost:8501

## How to Play

    Register & Login: Create a new account or log in to an existing one.

    Choose a Mode: Select either 1P (Lawan Bot) or 2P (Multiplayer Local).

    Take Your Turn: Click on the Peta Target (Musuh) to fire a shot.

         Red / Hit: You struck an enemy ship! (+100 points)

         Gray / Miss: You hit empty water. (-10 points)

    Win Condition: The game ends when one player's Sisa Kapal (Remaining Ships) reaches 0.