import json, os

def load_levels(path):
    if not os.path.exists(path):
        return {"levels": []}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def level_for_points(levels_json, puntos: int):
    levels = levels_json.get("levels", [])
    for lvl in levels:
        rmin, rmax = lvl.get("rango_puntos", [0, 0])
        if rmin <= puntos <= rmax:
            return lvl
    return levels[-1] if levels else None
