from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
import json

from ..deps import get_current_user, get_db_dep
from ... import crud, schemas, models
from ...db.session import SessionLocal

router = APIRouter()

@router.post("/", response_model=schemas.MessageOut)
def send_message(payload: schemas.MessageCreate, db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    receiver = crud.get_user(db, payload.receiver_id)
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    m = crud.send_message(db, sender_id=current_user.id, receiver_id=payload.receiver_id, content=payload.content)
    return m

@router.get("/conversations/{user_id}", response_model=List[schemas.MessageOut])
def get_conversation(user_id: int, db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    other = crud.get_user(db, user_id)
    if not other:
        raise HTTPException(status_code=404, detail="User not found")
    msgs = crud.list_conversation(db, current_user.id, user_id)
    return msgs

# Simple WebSocket manager for real-time messaging (development)
class ConnectionManager:
    def __init__(self):
        # maps user_id -> websocket
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        # accept connection and register
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            try:
                del self.active_connections[user_id]
            except KeyError:
                pass

    async def send_personal_message(self, message: str, user_id: int):
        ws = self.active_connections.get(user_id)
        if ws:
            try:
                await ws.send_text(message)
            except Exception:
                # ignore send errors for now
                pass

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket endpoint for simple real-time messaging (development).
    Protocol:
      - Connect to ws://host/messages/ws/{your_user_id}
      - Send JSON text messages like: {"to": 2, "msg": "hello"}
      - Server will persist messages and attempt to forward to the `to` user if connected.
    Note: This endpoint does not authenticate the token. In production you should pass and verify JWT.
    """
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                to = int(payload.get("to"))
                msg = str(payload.get("msg"))
            except Exception:
                await websocket.send_text(json.dumps({"error": "invalid payload, expected JSON {to:int, msg:str}"}))
                continue

            # store message in DB (use a new session for the websocket thread)
            db: Session = SessionLocal()
            try:
                crud.send_message(db, sender_id=user_id, receiver_id=to, content=msg)
            finally:
                db.close()

            # attempt to deliver to recipient if connected
            await manager.send_personal_message(json.dumps({"from": user_id, "msg": msg}), to)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception:
        # on unexpected error, ensure disconnect cleanup
        manager.disconnect(user_id)
        try:
            await websocket.close()
        except Exception:
            pass