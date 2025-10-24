import os
import uuid
import shutil
from datetime import datetime, timedelta
from typing import Optional, List, Dict

import psycopg2
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Form,
    UploadFile,
    File,
    Request,
    Query,
)
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from starlette.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from google.oauth2 import id_token as google_id_token_module
from google.auth.transport import requests as grequests
from google.auth.transport import requests as google_requests

# =====================================================
# CONFIG & SETTINGS
# =====================================================

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
GOOGLE_CLIENT_ID = 

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "unio_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "Ragul@2002"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

config = Config(".env")
oauth = OAuth(config)

# Google OAuth config
oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Microsoft OAuth config
oauth.register(
    name="microsoft",
    client_id=config("MICROSOFT_CLIENT_ID"),
    client_secret=config("MICROSOFT_CLIENT_SECRET"),
    server_metadata_url="https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

app = FastAPI(title="UNIO Backend (OAuth Enhanced)")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# =====================================================
# DATABASE UTILITIES
# =====================================================

def get_db():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        is_admin BOOLEAN DEFAULT FALSE,
        google_sub TEXT UNIQUE,
        microsoft_sub TEXT UNIQUE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS meetings(
        id SERIAL PRIMARY KEY,
        title TEXT,
        created_by INTEGER REFERENCES users(id),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages(
        id SERIAL PRIMARY KEY,
        meeting_id INTEGER REFERENCES meetings(id),
        sender_id INTEGER REFERENCES users(id),
        message TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files(
        id SERIAL PRIMARY KEY,
        meeting_id INTEGER REFERENCES meetings(id),
        filename TEXT,
        path TEXT,
        uploaded_by INTEGER REFERENCES users(id),
        uploaded_at TIMESTAMP DEFAULT NOW()
    );
    """)
    cur.close()
    conn.close()
    print("Database initialized")
init_db()

# =====================================================
# JWT / AUTH HELPERS
# =====================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid auth credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, is_admin FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": row[0], "username": row[1], "email": row[2], "is_admin": row[3]}

# =====================================================
# AUTH ROUTES (Signup, Login, Refresh)
# =====================================================

@app.post("/auth/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s) RETURNING id",
            (username, email, password)
        )
        uid = cur.fetchone()[0]
    except psycopg2.Error:
        raise HTTPException(status_code=400, detail="User already exists or DB error")
    finally:
        cur.close()
        conn.close()
    token = create_access_token({"sub": str(uid)})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=%s", (form_data.username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row or row[1] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(row[0])})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/logout")
def logout():
    return {"message": "Logged out (client should discard token)"}

@app.post("/auth/refresh")
def refresh(current_user=Depends(get_current_user)):
    token = create_access_token({"sub": str(current_user["id"])})
    return {"access_token": token, "token_type": "bearer"}

# =====================================================
# GOOGLE TOKEN LOGIN (using id_token as param)
# =====================================================

@app.post("/auth/google/token-login", summary="Google token login (POST form)")
async def google_token_login_form(id_token_str: str = Form(..., description="Google ID token (id_token)")):
    try:
        # Correct request object
        idinfo = google_id_token_module.verify_oauth2_token(
            id_token_str,
            google_requests.Request(), 
            GOOGLE_CLIENT_ID 
        )
        sub = idinfo["sub"]
        email = idinfo.get("email")
        name = idinfo.get("name", email.split("@")[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Google ID token: {str(e)}")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE google_sub=%s", (sub,))
    row = cur.fetchone()

    if row:
        user_id = row[0]
    else:
        cur.execute(
            "INSERT INTO users (username, email, google_sub) VALUES (%s, %s, %s) RETURNING id",
            (name, email, sub)
        )
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    jwt_token = create_access_token({"sub": str(user_id)})
    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {"id": user_id, "email": email, "name": name}
    }
@app.get("/auth/google/token-login", summary="Google token login (GET query param)")
async def google_token_login_query(id_token_str: str = Query(..., description="Google ID token (id_token)")):
    try:
        idinfo = google_id_token_module.verify_oauth2_token(
            id_token_str,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )
        sub = idinfo["sub"]
        email = idinfo.get("email")
        name = idinfo.get("name", email.split("@")[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Google ID token: {str(e)}")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE google_sub=%s", (sub,))
    row = cur.fetchone()

    if row:
        user_id = row[0]
    else:
        cur.execute(
            "INSERT INTO users (username, email, google_sub) VALUES (%s, %s, %s) RETURNING id",
            (name, email, sub)
        )
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    jwt_token = create_access_token({"sub": str(user_id)})
    return {"access_token": jwt_token, "token_type": "bearer", "user": {"id": user_id, "email": email, "name": name}}

# =====================================================
# MICROSOFT LOGIN (unchanged)
# =====================================================

@app.get("/auth/microsoft/login")
async def ms_login(request: Request):
    redirect_uri = request.url_for("ms_auth_callback")
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)

@app.get("/auth/microsoft")
async def ms_auth_callback(request: Request):
    try:
        token = await oauth.microsoft.authorize_access_token(request)
    except OAuthError as err:
        raise HTTPException(status_code=400, detail=f"OAuth error: {err.error}")

    user_info = await oauth.microsoft.parse_id_token(request, token)
    sub = user_info.get("sub")
    email = user_info.get("email")
    name = user_info.get("name") or user_info.get("preferred_username")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE microsoft_sub=%s", (sub,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
    else:
        cur.execute(
            "INSERT INTO users (username, email, microsoft_sub) VALUES (%s, %s, %s) RETURNING id",
            (name, email, sub)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()

    jwt_token = create_access_token({"sub": str(user_id)})
    return {"access_token": jwt_token, "token_type": "bearer", "user": {"id": user_id, "email": email, "name": name}}

# =====================================================
# USERS / MEETINGS / CHAT / FILES / WS / HEALTH
# =====================================================

@app.get("/users")
def list_users(current_user=Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin required")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]

@app.get("/users/{user_id}")
def get_user(user_id: int, current_user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "username": row[1], "email": row[2]}

@app.post("/meetings")
def create_meeting(title: str = Form(...), current_user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO meetings (title, created_by) VALUES (%s,%s) RETURNING id", (title, current_user["id"]))
    mid = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"meeting_id": mid, "message": "Created"}

@app.post("/chat/send")
def send_message(meeting_id: int = Form(...), message: str = Form(...), current_user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO chat_messages (meeting_id, sender_id, message) VALUES (%s,%s,%s)",
                (meeting_id, current_user["id"], message))
    cur.close()
    conn.close()
    return {"message": "Sent"}

@app.post("/file/upload")
def upload_file(meeting_id: int = Form(...), file: UploadFile = File(...), current_user=Depends(get_current_user)):
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, unique_name)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO files (meeting_id, filename, path, uploaded_by) VALUES (%s,%s,%s,%s)",
                (meeting_id, file.filename, path, current_user["id"]))
    cur.close()
    conn.close()
    return {"message": "Uploaded", "filename": file.filename}

connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/meeting/{meeting_id}")
async def meeting_ws(websocket: WebSocket, meeting_id: str):
    await websocket.accept()
    if meeting_id not in connections:
        connections[meeting_id] = []
    connections[meeting_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in connections[meeting_id]:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        connections[meeting_id].remove(websocket)

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
