from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trakt API credentials
TRAKT_CLIENT_ID = "your_trakt_client_id"
TRAKT_CLIENT_SECRET = "your_trakt_client_secret"
REDIRECT_URI = "http://localhost:3000/auth/callback"

# OAuth2 scheme
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://api.trakt.tv/oauth/authorize",
    tokenUrl="https://api.trakt.tv/oauth/token"
)

# Store access tokens (in-memory for simplicity)
access_tokens = {}

# Redirect user to Trakt OAuth2 authorization page
@app.get("/auth/trakt")
def trakt_auth():
    auth_url = f"https://api.trakt.tv/oauth/authorize?response_type=code&client_id={TRAKT_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return {"auth_url": auth_url}

# Handle OAuth2 callback
@app.get("/auth/callback")
def trakt_callback(code: str):
    token_url = "https://api.trakt.tv/oauth/token"
    data = {
        "code": code,
        "client_id": TRAKT_CLIENT_ID,
        "client_secret": TRAKT_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to authenticate")

    access_token = response.json()["access_token"]
    access_tokens[access_token] = True  # Store the token
    return {"access_token": access_token}

# Fetch recommendations
async def fetch_recommendations(access_token: str, genres=None, start_year=None, end_year=None, limit=100, language=None, popularity=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "trakt-api-version": "2",
        "trakt-api-key": TRAKT_CLIENT_ID
    }
    url = "https://api.trakt.tv/recommendations/movies"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations")

    data = response.json()

    # Apply genre filter
    if genres and "All" not in genres:
        data = [item for item in data if any(genre in item.get("genres", []) for genre in genres)]

    # Apply year range filter
    if start_year and end_year:
        data = [item for item in data if start_year <= int(item.get("year", 0)) <= end_year]

    # Apply language filter
    if language:
        data = [item for item in data if item.get("language", "").lower() == language.lower()]

    # Apply popularity filter
    if popularity:
        data = [item for item in data if item.get("popularity", 0) >= popularity]

    # Apply item limit
    return data[:limit]

# Create a Trakt list
async def create_trakt_list(access_token: str, name: str, description: str, items: list[int]):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "trakt-api-version": "2",
        "trakt-api-key": TRAKT_CLIENT_ID
    }
    list_data = {
        "name": name,
        "description": description,
        "privacy": "private"
    }
    list_url = "https://api.trakt.tv/users/me/lists"
    list_response = requests.post(list_url, json=list_data, headers=headers)
    if list_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create list")

    list_id = list_response.json()["ids"]["trakt"]
    items_url = f"https://api.trakt.tv/users/me/lists/{list_id}/items"
    items_data = {"movies": [{"ids": {"trakt": item}} for item in items]}
    requests.post(items_url, json=items_data, headers=headers)

    return {"status": "success", "list_id": list_id}

# Schedule daily updates
scheduler = BackgroundScheduler()
scheduler.add_job(create_trakt_list, "interval", days=1, args=["list_id"])
scheduler.start()

# API endpoints
@app.get("/recommendations")
async def get_recommendations(access_token: str = Depends(oauth2_scheme), genres: str = None, start_year: int = None, end_year: int = None, limit: int = 100, language: str = None, popularity: int = None):
    genres_list = genres.split(",") if genres else None
    return await fetch_recommendations(access_token, genres_list, start_year, end_year, limit, language, popularity)

@app.post("/create-list")
async def create_list(name: str, description: str, items: list[int], access_token: str = Depends(oauth2_scheme)):
    list_id = await create_trakt_list(access_token, name, description, items)
    return {"status": "success", "list_id": list_id}from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trakt API credentials
TRAKT_CLIENT_ID = "your_trakt_client_id"
TRAKT_CLIENT_SECRET = "your_trakt_client_secret"
REDIRECT_URI = "http://localhost:3000/auth/callback"

# OAuth2 scheme
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://api.trakt.tv/oauth/authorize",
    tokenUrl="https://api.trakt.tv/oauth/token"
)

# Store access tokens (in-memory for simplicity)
access_tokens = {}

# Redirect user to Trakt OAuth2 authorization page
@app.get("/auth/trakt")
def trakt_auth():
    auth_url = f"https://api.trakt.tv/oauth/authorize?response_type=code&client_id={TRAKT_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return {"auth_url": auth_url}

# Handle OAuth2 callback
@app.get("/auth/callback")
def trakt_callback(code: str):
    token_url = "https://api.trakt.tv/oauth/token"
    data = {
        "code": code,
        "client_id": TRAKT_CLIENT_ID,
        "client_secret": TRAKT_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to authenticate")

    access_token = response.json()["access_token"]
    access_tokens[access_token] = True  # Store the token
    return {"access_token": access_token}

# Fetch recommendations
async def fetch_recommendations(access_token: str, genres=None, start_year=None, end_year=None, limit=100, language=None, popularity=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "trakt-api-version": "2",
        "trakt-api-key": TRAKT_CLIENT_ID
    }
    url = "https://api.trakt.tv/recommendations/movies"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations")

    data = response.json()

    # Apply genre filter
    if genres and "All" not in genres:
        data = [item for item in data if any(genre in item.get("genres", []) for genre in genres)]

    # Apply year range filter
    if start_year and end_year:
        data = [item for item in data if start_year <= int(item.get("year", 0)) <= end_year]

    # Apply language filter
    if language:
        data = [item for item in data if item.get("language", "").lower() == language.lower()]

    # Apply popularity filter
    if popularity:
        data = [item for item in data if item.get("popularity", 0) >= popularity]

    # Apply item limit
    return data[:limit]

# Create a Trakt list
async def create_trakt_list(access_token: str, name: str, description: str, items: list[int]):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "trakt-api-version": "2",
        "trakt-api-key": TRAKT_CLIENT_ID
    }
    list_data = {
        "name": name,
        "description": description,
        "privacy": "private"
    }
    list_url = "https://api.trakt.tv/users/me/lists"
    list_response = requests.post(list_url, json=list_data, headers=headers)
    if list_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create list")

    list_id = list_response.json()["ids"]["trakt"]
    items_url = f"https://api.trakt.tv/users/me/lists/{list_id}/items"
    items_data = {"movies": [{"ids": {"trakt": item}} for item in items]}
    requests.post(items_url, json=items_data, headers=headers)

    return {"status": "success", "list_id": list_id}

# Schedule daily updates
scheduler = BackgroundScheduler()
scheduler.add_job(create_trakt_list, "interval", days=1, args=["list_id"])
scheduler.start()

# API endpoints
@app.get("/recommendations")
async def get_recommendations(access_token: str = Depends(oauth2_scheme), genres: str = None, start_year: int = None, end_year: int = None, limit: int = 100, language: str = None, popularity: int = None):
    genres_list = genres.split(",") if genres else None
    return await fetch_recommendations(access_token, genres_list, start_year, end_year, limit, language, popularity)

@app.post("/create-list")
async def create_list(name: str, description: str, items: list[int], access_token: str = Depends(oauth2_scheme)):
    list_id = await create_trakt_list(access_token, name, description, items)
    return {"status": "success", "list_id": list_id}
