from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .database.initialize import initialize
from .database.operation import create_user, get_latest_game_state, reset_game_state
from .game.operation import move_location

app = FastAPI()
initialize()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class CookieManager:
    @staticmethod
    def create_cookie(name: str, value: str, days: int = 1):
        expires = datetime.utcnow() + timedelta(days=days)
        return {
            "name": name,
            "value": value,
            "expires": expires.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

@app.get("/api/v1/maze")
async def get_maze(username: str):
    return JSONResponse(get_latest_game_state(username))

@app.post("/api/v1/move")
async def move(request: Request):
    body = await request.json()
    username = body.get("username")
    direction = body.get("direction", "")

    game_state = get_latest_game_state(username)
    if not game_state:
        return JSONResponse({"message": "User does not exist", "status": 0}, status_code=400)

    game_state = move_location(game_state, direction)
    return JSONResponse(game_state)

@app.get("/api/v1/reset")
async def reset_game(username: str):
    reset_game_state(username)
    return JSONResponse(get_latest_game_state(username))

@app.post("/api/v1/login")
async def login(request: Request, response: Response):
    body = await request.json()
    username = body.get("username", "")

    if username == "":
        return JSONResponse({"message": "Username is empty", "cookies": [], "status": 0})

    create_user(username)
    user_cookie = CookieManager.create_cookie("user", username)

    return JSONResponse({"message": "Login successful", "cookies": [user_cookie], "status": 1})

@app.post("/api/v1/logout")
async def logout():
    return JSONResponse({"message": "Logout successful", "cookies": [], "status": 1})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
