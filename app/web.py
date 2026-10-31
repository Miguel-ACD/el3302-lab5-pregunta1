"""Capa de presentación: rutas y HTML."""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from . import data, logic


def create_app():
    app = Flask(__name__)
    app.secret_key = "lab5-demo-key"
    logic.startup()

    @app.get("/")
    def index():
        return render_template("index.html", matches=data.all_matches(), predictions=data.all_predictions())

    @app.post("/predicciones")
    def add_prediction():
        try:
            logic.predict(request.form)
            flash("Predicción guardada")
        except (ValueError, KeyError) as error:
            flash(f"Error: {error}")
        return redirect(url_for("index"))

    @app.get("/api/partidos-fuente")
    def source():
        return jsonify(logic.SAMPLE_MATCHES)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
