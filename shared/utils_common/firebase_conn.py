import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

DATABASE_URL = st.secrets.get("database_url", None) or "https://beerclub-beta-default-rtdb.firebaseio.com/"

def init_firebase():
    if 'firebase_initialized' in st.session_state and st.session_state['firebase_initialized']:
        return
    try:
        cred = credentials.Certificate("firebase_config.json")
        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
        st.session_state['firebase_initialized'] = True
    except Exception as e:
        st.session_state['firebase_initialized'] = False
        st.session_state['firebase_error'] = str(e)

def get_ref(path: str):
    init_firebase()
    return db.reference(path)

def read(path: str, default=None):
    try:
        ref = get_ref(path)
        data = ref.get()
        return data if data is not None else default
    except Exception as e:
        st.error(f"Error leyendo {path}: {e}")
        return default

def write(path: str, value):
    try:
        ref = get_ref(path)
        ref.set(value)
        return True
    except Exception as e:
        st.error(f"Error escribiendo {path}: {e}")
        return False

def update(path: str, value: dict):
    try:
        ref = get_ref(path)
        ref.update(value)
        return True
    except Exception as e:
        st.error(f"Error actualizando {path}: {e}")
        return False

def append_operation(uid: str, bar_id: str, puntos: int):
    ref = get_ref("operaciones").push({
        "uid": uid,
        "bar_id": bar_id,
        "puntos": puntos,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
    return ref.key

def increment_user_points(uid: str, puntos: int):
    user = read(f"usuarios/{uid}", default={})
    if not user: return None
    nuevo_total = int(user.get("puntos", 0)) + int(puntos)
    user["puntos"] = nuevo_total
    write(f"usuarios/{uid}", user)
    return nuevo_total
