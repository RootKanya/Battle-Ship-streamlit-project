##  How to Run the Project Locally

To run this project, you will need two separate terminal windows—one for the backend server and one for the frontend app.

### 1. Setup the Virtual Environment

First, ensure you are in the root directory of the project and create a clean Python environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic streamlit requests pandas streamlit-cookies-manager

2. Start the FastAPI Backend

Open Terminal 1, activate the environment, and start the API server.
Bash

source venv/bin/activate
cd backend
uvicorn api_main:app --reload --port 8000

The backend is now running at http://localhost:8000
3. Start the Streamlit Frontend

Open Terminal 2, activate the environment, and start the Streamlit app.
Bash

source venv/bin/activate
cd streamlit
streamlit run main.py

The game is now playable at http://localhost:8501

How to Play

    Register & Login: Create a new account or log in to an existing one.

    Choose a Mode: Select either 1P (Lawan Bot) or 2P (Multiplayer Local).

    Take Your Turn: Click on the Peta Target (Musuh) to fire a shot.

        Red / Hit: You struck an enemy ship! (+100 points)

        Gray / Miss: You hit empty water. (-10 points)

    Win Condition: The game ends when one player's Sisa Kapal (Remaining Ships) reaches 0.