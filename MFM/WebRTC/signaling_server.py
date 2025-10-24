# signaling_server.py
import logging
import os
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import socketio
import uvicorn
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signaling-server")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()

# Serve static HTML and uploaded files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Combine FastAPI + Socket.IO
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# In-memory store
rooms: Dict[str, Dict[str, Dict[str, Any]]] = {}

# ------------------ Helper Functions ------------------
async def add_to_room(room: str, sid: str, info: Dict[str, Any]):
    rooms.setdefault(room, {})[sid] = info
    logger.info(f"Added sid={sid} to room={room}")

async def remove_from_room(room: str, sid: str):
    if room in rooms and sid in rooms[room]:
        del rooms[room][sid]
        if not rooms[room]:
            del rooms[room]

def peers_in_room(room: str, sid: str):
    if room not in rooms:
        return []
    return [peer_sid for peer_sid in rooms[room].keys() if peer_sid != sid]

# ------------------ Socket.IO Events ------------------
@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")
    for room, members in list(rooms.items()):
        if sid in members:
            info = members[sid]
            await remove_from_room(room, sid)
            for peer_sid in peers_in_room(room, sid):
                await sio.emit("peer-left", {"sid": sid, "user": info}, to=peer_sid)

@sio.on("join-room")
async def join_room(sid, data):
    room = data.get("room")
    user = data.get("user", {})
    if not room:
        await sio.emit("join-error", {"error": "Room required"}, to=sid)
        return
    await add_to_room(room, sid, user)
    peers = [{"sid": psid, "user": meta} for psid, meta in rooms[room].items() if psid != sid]
    await sio.emit("join-ack", {"ok": True, "peers": peers}, to=sid)
    for peer_sid in peers_in_room(room, sid):
        await sio.emit("peer-joined", {"sid": sid, "user": user}, to=peer_sid)

@sio.on("leave-room")
async def leave_room(sid, data):
    room = data.get("room")
    if room and room in rooms and sid in rooms[room]:
        user = rooms[room][sid]
        await remove_from_room(room, sid)
        for peer_sid in peers_in_room(room, sid):
            await sio.emit("peer-left", {"sid": sid, "user": user}, to=peer_sid)
    await sio.emit("leave-ack", {"ok": True}, to=sid)

# ------------------ WebRTC ------------------
async def forward(event, from_sid, data):
    target = data.get("to")
    room = data.get("room")
    payload = {**data, "from": from_sid}
    if target:
        await sio.emit(event, payload, to=target)
    elif room:
        for peer_sid in peers_in_room(room, from_sid):
            await sio.emit(event, payload, to=peer_sid)

@sio.on("offer")
async def on_offer(sid, data): await forward("offer", sid, data)

@sio.on("answer")
async def on_answer(sid, data): await forward("answer", sid, data)

@sio.on("ice-candidate")
async def on_ice_candidate(sid, data): await forward("ice-candidate", sid, data)

# ------------------ Chat ------------------
@sio.on("chat-message")
async def on_chat_message(sid, data):
    room = data.get("room")
    message = data.get("message")
    user = data.get("user", {})
    if not room or not message:
        return
    payload = {"from": sid, "user": user, "message": message}
    for peer_sid in peers_in_room(room, sid):
        await sio.emit("chat-message", payload, to=peer_sid)

# ------------------ File Upload ------------------
@app.post("/upload")
async def upload_file(room: str = Form(...), username: str = Form(...), file: UploadFile = File(...)):
    """Handle file upload and notify peers in the room."""
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        file_url = f"/uploads/{file.filename}"

        # Notify peers about uploaded file
        payload = {
            "type": "file",
            "file_name": file.filename,
            "file_url": file_url,
            "user": {"username": username},
            "room": room
        }
        for sid in peers_in_room(room, ""):
            await sio.emit("file-shared", payload, to=sid)

        return JSONResponse({"success": True, "file_url": file_url})
    except Exception as e:
        logger.exception(e)
        return JSONResponse({"error": str(e)}, status_code=500)

# ------------------ Run ------------------
if __name__ == "__main__":
    uvicorn.run("signaling_server:socket_app", host="0.0.0.0", port=8000, reload=True)
