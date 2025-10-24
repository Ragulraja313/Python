"""
UNIO Backend API – FastAPI + PostgreSQL + JWT + WebSocket + File Upload + Chat
Run with: uvicorn unio_backend:app --reload
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Optional
import psycopg2, os, shutil, uuid, json

# ---------- CONFIG ----------
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DB_CONFIG = {
    "dbname": "unio_db",
    "user": "postgres",
    "password": "Ragul@2002",
    "host": "localhost",
    "port": 5432,
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- INIT ----------
app = FastAPI(title="UNIO Backend API", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DATABASE ----------
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
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
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
init_db()

# ---------- AUTH HELPERS ----------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, is_admin FROM users WHERE id=%s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": user[0], "username": user[1], "email": user[2], "is_admin": user[3]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

# ---------- AUTH ROUTES ----------
@app.post("/auth/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s) RETURNING id", (username, email, password))
        uid = cur.fetchone()[0]
        return {"message": "User created", "user_id": uid}
    except psycopg2.Error:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        cur.close()
        conn.close()

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=%s", (form_data.username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user or user[1] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user[0])})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/logout")
def logout():
    return {"message": "Logout successful (client should discard token)"}

@app.post("/auth/refresh")
def refresh_token(current_user: dict = Depends(get_current_user)):
    token = create_access_token({"sub": str(current_user["id"])})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/google")
def google_login(token: str = Form(...)):
    return {"message": "Mock Google OAuth login successful", "google_token": token}

@app.post("/auth/microsoft")
def microsoft_login(token: str = Form(...)):
    return {"message": "Mock Microsoft OAuth login successful", "microsoft_token": token}

# ---------- USER MANAGEMENT ----------
@app.get("/users")
def list_users(current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": u[0], "username": u[1], "email": u[2]} for u in users]

@app.get("/users/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user[0], "username": user[1], "email": user[2]}

@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = Form(None), email: str = Form(None), current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username=COALESCE(%s, username), email=COALESCE(%s, email) WHERE id=%s",
                (username, email, user_id))
    cur.close()
    conn.close()
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    cur.close()
    conn.close()
    return {"message": "User deleted"}

# ---------- MEETINGS ----------
@app.post("/meetings")
def create_meeting(title: str = Form(...), current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO meetings (title, created_by) VALUES (%s,%s) RETURNING id", (title, current_user["id"]))
    mid = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"meeting_id": mid, "message": "Meeting created"}

@app.get("/meetings")
def list_meetings(current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, created_at FROM meetings WHERE created_by=%s", (current_user["id"],))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": m[0], "title": m[1], "created_at": m[2]} for m in data]

@app.get("/meetings/{meeting_id}")
def get_meeting(meeting_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, created_by, created_at FROM meetings WHERE id=%s", (meeting_id,))
    m = cur.fetchone()
    cur.close()
    conn.close()
    if not m:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"id": m[0], "title": m[1], "created_by": m[2], "created_at": m[3]}

@app.delete("/meetings/{meeting_id}")
def delete_meeting(meeting_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM meetings WHERE id=%s", (meeting_id,))
    cur.close()
    conn.close()
    return {"message": "Meeting deleted"}

@app.get("/meetings/history")
def meeting_history(current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, created_at FROM meetings WHERE created_by=%s ORDER BY created_at DESC", (current_user["id"],))
    meetings = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": m[0], "title": m[1], "created_at": m[2]} for m in meetings]

# ---------- CHAT ----------
@app.post("/chat/send")
def send_message(meeting_id: int = Form(...), message: str = Form(...), current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO chat_messages (meeting_id, sender_id, message) VALUES (%s,%s,%s)",
                (meeting_id, current_user["id"], message))
    cur.close()
    conn.close()
    return {"message": "Sent"}

@app.get("/chat/messages/{meeting_id}")
def get_messages(meeting_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.username, c.message, c.created_at
        FROM chat_messages c JOIN users u ON c.sender_id = u.id
        WHERE meeting_id=%s ORDER BY c.created_at
    """, (meeting_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [{"sender": d[0], "message": d[1], "time": d[2]} for d in data]

# ---------- FILE UPLOAD/DOWNLOAD ----------
@app.post("/file/upload")
def upload_file(meeting_id: int = Form(...), file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO files (meeting_id, filename, path, uploaded_by) VALUES (%s,%s,%s,%s)",
                (meeting_id, file.filename, file_path, current_user["id"]))
    cur.close()
    conn.close()
    return {"message": "File uploaded", "filename": file.filename}

@app.get("/file/download/{file_id}")
def download_file(file_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT path, filename FROM files WHERE id=%s", (file_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if not data:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(data[0], filename=data[1])

# ---------- WEBSOCKET (SIGNALING) ----------
connections = {}

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

# ---------- HEALTH CHECK ----------
@app.get("/health")
def health_check():
    return {"status": "ok", "time": str(datetime.utcnow())}

# ---------- MAIN ----------
if __name__ == "__main__":
    uvicorn.run("unio_backend:app", host="0.0.0.0", port=8000, reload=True)
