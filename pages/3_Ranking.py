import streamlit as st
import pandas as pd
from shared.utils_common.firebase_conn import read
from shared.utils_common.levels import load_levels, level_for_points

st.title("🏆 Ranking — Beer League")

usuarios = read("usuarios", default={}) or {}
if not usuarios:
    st.warning("No hay usuarios.")
    st.stop()

rows = []
levels_json = load_levels("shared/data/levels.json")
for uid, u in usuarios.items():
    pts = int(u.get("puntos", 0))
    lvl = level_for_points(levels_json, pts)
    rows.append({
        "Usuario": u.get("nombre", uid),
        "Puntos": pts,
        "Nivel": lvl.get("nombre","-") if lvl else "-",
        "Icono": lvl.get("icono","") if lvl else ""
    })

df = pd.DataFrame(rows).sort_values(by="Puntos", ascending=False, ignore_index=True)
st.dataframe(df, use_container_width=True, hide_index=True)

st.caption("Ranking general. Próximamente: ranking mensual por bar / ciudad.")
