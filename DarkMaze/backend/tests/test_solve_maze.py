import pytest
import httpx

USERNAME = "TestUser"
RESET_URL = f"http://127.0.0.1:8000/api/v1/reset?username={USERNAME}"
LOGIN_URL = f"http://127.0.0.1:8000/api/v1/login"
MOVE_URL = "http://127.0.0.1:8000/api/v1/move"
game_state = {}

async def login_request():
    """Simulates a frontend login."""
    payload = {"username": USERNAME}
    async with httpx.AsyncClient() as client:
        response = await client.post(LOGIN_URL, json=payload)
    assert response.status_code == 200

async def reset_request():
    """Reset Game state"""
    global game_state
    async with httpx.AsyncClient() as client:
        response = await client.get(RESET_URL)
    assert response.status_code == 200
    game_state = response.json()
    assert game_state["current_position"] == [1, 0]

async def move_request(direction):
    """Simulates a frontend move request."""
    global game_state
    payload = {"username": USERNAME, "direction": direction}
    async with httpx.AsyncClient() as client:
        response = await client.post(MOVE_URL, json=payload)
    assert response.status_code == 200
    game_state = response.json()
    assert game_state["health"] >= 3

@pytest.mark.asyncio
async def test_integration():
    await login_request()
    await reset_request()
    for i in range(5):
        await move_request("down")
    assert game_state["current_position"] == [1, 5]

@pytest.mark.asyncio
async def test_solver():
    await login_request()
    await reset_request()
    moves = [
        "down", "down", "down", "down", "down",
        "right", "down", "right", "right",
        "up", "up", "up", "up",
        "right", "right", "down",
        "right", "right", "down",
        "right", "down"
    ]
    for move in moves:
        await move_request(move)
    assert game_state["health"] == 666
