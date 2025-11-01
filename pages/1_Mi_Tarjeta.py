import streamlit as st
from shared.utils_common.firebase_conn import read
from shared.utils_common.qr_utils import generate_qr_png
from shared.utils_common.levels import load_levels, level_for_points

st.title("🎫 Mi Tarjeta")

usuarios = read("usuarios", default={}) or {}
if not usuarios:
    st.warning("No hay usuarios en Firebase.")
    st.stop()

uid = st.selectbox("Seleccioná tu usuario", options=list(usuarios.keys()), format_func=lambda u: usuarios[u].get("nombre", u))
user = usuarios.get(uid, {})
puntos = int(user.get("puntos", 0))
qr_id = user.get("qr_id", uid)

levels_json = load_levels("shared/data/levels.json")
lvl = level_for_points(levels_json, puntos) or {}
nivel_nombre = lvl.get("nombre","-")
nivel_icono = lvl.get("icono","")
beneficios = lvl.get("beneficios", [])

col1, col2 = st.columns([1,1], vertical_alignment="center")
with col1:
    st.subheader(user.get("nombre", uid))
    st.write(f"**Nivel:** {nivel_icono} {nivel_nombre}")
    st.write(f"**Puntos:** {puntos}")
    if beneficios:
        st.markdown("**Beneficios actuales:**")
        for b in beneficios:
            st.markdown(f"- {b}")
with col2:
    st.image(generate_qr_png(qr_id), caption="Mostrá este QR en el bar", width=220)

st.caption("Tip: agregá esta página a tu pantalla de inicio para usarla como app.")
