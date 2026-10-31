"""Capa de acceso a datos: todas las consultas SQL viven aquí."""
import os
import psycopg
from psycopg.rows import dict_row


def connection():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)


def initialize():
    with connection() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY, home TEXT NOT NULL, away TEXT NOT NULL,
            played_at TEXT NOT NULL)""")
        db.execute("""CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            match_id INTEGER NOT NULL REFERENCES matches(id),
            outcome TEXT NOT NULL, home_goals INTEGER NOT NULL,
            away_goals INTEGER NOT NULL, created_at TIMESTAMPTZ DEFAULT now())""")


def save_matches(matches):
    with connection() as db:
        for match in matches:
            db.execute("""INSERT INTO matches (id, home, away, played_at)
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET
                home=EXCLUDED.home, away=EXCLUDED.away, played_at=EXCLUDED.played_at""",
                (match["id"], match["home"], match["away"], match["played_at"]))


def all_matches():
    with connection() as db:
        return db.execute("SELECT * FROM matches ORDER BY id").fetchall()


def add_prediction(match_id, outcome, home_goals, away_goals):
    with connection() as db:
        db.execute("""INSERT INTO predictions (match_id, outcome, home_goals, away_goals)
            VALUES (%s, %s, %s, %s)""", (match_id, outcome, home_goals, away_goals))


def all_predictions():
    with connection() as db:
        return db.execute("""SELECT p.id, p.outcome, p.home_goals, p.away_goals,
            p.created_at, m.home, m.away FROM predictions p
            JOIN matches m ON m.id=p.match_id ORDER BY p.id DESC""").fetchall()
