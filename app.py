from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pathlib import Path
import sqlite3
import csv
import io
from datetime import datetime
from predictor import predict_risk, MODEL_NOTE

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "motosense.db"

app = Flask(__name__)
app.secret_key = "change-this-for-production"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS motorcycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_name TEXT NOT NULL,
                motorcycle_model TEXT NOT NULL,
                odometer_km REAL NOT NULL,
                days_since_service INTEGER NOT NULL,
                engine_temp_c REAL NOT NULL,
                vibration_mm_s REAL NOT NULL,
                service_notes TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


@app.route("/")
def index():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM motorcycles ORDER BY id DESC").fetchall()
    items = []
    for row in rows:
        item = dict(row)
        result = predict_risk(
            odometer_km=item["odometer_km"],
            days_since_service=item["days_since_service"],
            engine_temp_c=item["engine_temp_c"],
            vibration_mm_s=item["vibration_mm_s"],
        )
        item.update(result)
        items.append(item)
    total = len(items)
    high = sum(1 for x in items if x["risk_level"] == "High")
    medium = sum(1 for x in items if x["risk_level"] == "Medium")
    low = sum(1 for x in items if x["risk_level"] == "Low")
    return render_template("index.html", items=items, total=total, high=high, medium=medium, low=low,
                           model_note=MODEL_NOTE)


@app.route("/add", methods=["GET", "POST"])
def add_motorcycle():
    if request.method == "POST":
        try:
            owner_name = request.form["owner_name"].strip()
            motorcycle_model = request.form["motorcycle_model"].strip()
            odometer_km = float(request.form["odometer_km"])
            days_since_service = int(request.form["days_since_service"])
            engine_temp_c = float(request.form["engine_temp_c"])
            vibration_mm_s = float(request.form["vibration_mm_s"])
            service_notes = request.form.get("service_notes", "").strip()
            if not owner_name or not motorcycle_model:
                raise ValueError("Owner name and motorcycle model are required.")
            if odometer_km < 0 or days_since_service < 0 or not (0 <= engine_temp_c <= 200) or vibration_mm_s < 0:
                raise ValueError("Please enter valid non-negative values and a reasonable engine temperature.")
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO motorcycles
                    (owner_name, motorcycle_model, odometer_km, days_since_service, engine_temp_c,
                     vibration_mm_s, service_notes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (owner_name, motorcycle_model, odometer_km, days_since_service, engine_temp_c,
                      vibration_mm_s, service_notes, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
            flash("Motorcycle record added successfully.", "success")
            return redirect(url_for("index"))
        except (ValueError, KeyError) as exc:
            flash(str(exc) or "Please check the submitted values.", "error")
    return render_template("add.html")


@app.route("/record/<int:record_id>/delete", methods=["POST"])
def delete_record(record_id):
    with get_db() as conn:
        conn.execute("DELETE FROM motorcycles WHERE id = ?", (record_id,))
        conn.commit()
    flash("Record deleted.", "success")
    return redirect(url_for("index"))


@app.route("/export")
def export_csv():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM motorcycles ORDER BY id DESC").fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Owner", "Model", "Odometer km", "Days since service", "Engine temp C",
                     "Vibration mm/s", "Service notes", "Created at", "Estimated risk"])
    for row in rows:
        result = predict_risk(row["odometer_km"], row["days_since_service"],
                              row["engine_temp_c"], row["vibration_mm_s"])
        writer.writerow([row["id"], row["owner_name"], row["motorcycle_model"], row["odometer_km"],
                         row["days_since_service"], row["engine_temp_c"], row["vibration_mm_s"],
                         row["service_notes"], row["created_at"], result["risk_level"]])
    mem = io.BytesIO(output.getvalue().encode("utf-8-sig"))
    mem.seek(0)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="motosense_records.csv")


@app.route("/about")
def about():
    return render_template("about.html", model_note=MODEL_NOTE)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
