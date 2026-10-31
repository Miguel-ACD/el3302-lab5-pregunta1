"""Capa de negocio: carga inicial y validación de predicciones."""
import os
import requests
from . import data


SAMPLE_MATCHES = [
    {"id": 1, "home": "Real Madrid", "away": "Manchester City", "played_at": "2026-11-03 20:00 UTC"},
    {"id": 2, "home": "Barcelona", "away": "Bayern Munich", "played_at": "2026-11-04 20:00 UTC"},
    {"id": 3, "home": "Liverpool", "away": "Paris Saint-Germain", "played_at": "2026-11-05 20:00 UTC"},
]


def startup():
    data.initialize()
    # La API simulada entrega JSON por HTTP desde el servicio source.
    url = os.environ.get("MATCHES_API_URL")
    matches = requests.get(url, timeout=10).json() if url else SAMPLE_MATCHES
    data.save_matches(matches)


def predict(form):
    match_id = int(form["match_id"])
    matches = {m["id"]: m for m in data.all_matches()}
    if match_id not in matches:
        raise ValueError("El partido no existe")
    home_goals, away_goals = int(form["home_goals"]), int(form["away_goals"])
    if not (0 <= home_goals <= 20 and 0 <= away_goals <= 20):
        raise ValueError("Los goles deben estar entre 0 y 20")
    outcome = "Empate" if home_goals == away_goals else (matches[match_id]["home"] if home_goals > away_goals else matches[match_id]["away"])
    data.add_prediction(match_id, outcome, home_goals, away_goals)
