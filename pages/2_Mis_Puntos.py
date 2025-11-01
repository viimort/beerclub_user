import streamlit as st
import pandas as pd
from shared.utils_common.firebase_conn import read

st.title("📊 Mis Puntos")

usuarios = read("usuarios", default={}) or {}
if not usuarios:
    st.warning("No hay usuarios en Firebase.")
    st.stop()

uid = st.selectbox("Seleccioná tu usuario", options=list(usuarios.keys()), format_func=lambda u: usuarios[u].get("nombre", u))

ops = read("operaciones", default={}) or {}
rows = []
for k, v in (ops or {}).items():
    if v.get("uid") == uid:
        rows.append(v)

if not rows:
    st.info("Todavía no hay historial.")
else:
    df = pd.DataFrame(rows).sort_values(by="timestamp", ascending=False, ignore_index=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
