from flask import Flask, render_template, request, redirect, session
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
from joblib import load
from datetime import datetime
import numpy as np

app = Flask(__name__)
app.secret_key = "secret123"

# ======== PATHS ========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

# ======== LOAD ML MODELS ========
clf = load(os.path.join(MODEL_DIR, "crop_model.joblib"))
reg = load(os.path.join(MODEL_DIR, "yield_model.joblib"))
scaler = load(os.path.join(MODEL_DIR, "scaler.joblib"))
le = load(os.path.join(MODEL_DIR, "label_encoder.joblib"))


# ======== DB FUNCTIONS ========
def get_conn():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    """Create required tables if not exist."""
    print("Using DB:", DATABASE_PATH)
    conn = get_conn()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # History table
    c.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            crop TEXT,
            yield_val REAL,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ======== ROUTES ========
@app.route("/")
def home():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/login")


# ---------- AUTH ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        if not u or not p:
            msg = "Fields required"
        else:
            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username=?", (u,))
            res = c.fetchone()
            conn.close()

            if res and check_password_hash(res[0], p):
                session["user"] = u
                return redirect("/")
            else:
                msg = "Invalid credentials"
    return render_template("login.html", msg=msg)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    msg = ""
    if request.method == "POST":
        u = (request.form.get("username") or "").strip()
        p = request.form.get("password") or ""
        cp = request.form.get("cpassword") or ""

        if not u or not p:
            msg = "Username and password required"
        elif p != cp:
            msg = "Passwords do not match"
        else:
            try:
                conn = get_conn()
                c = conn.cursor()
                c.execute("INSERT INTO users(username,password) VALUES (?,?)",
                          (u, generate_password_hash(p)))
                conn.commit()
                conn.close()
                msg = "Account created. Login now!"
            except sqlite3.IntegrityError:
                msg = "Username already exists"
    return render_template("signup.html", msg=msg)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect("/login")

    msg = ""
    if request.method == "POST":
        old = request.form.get("old")
        new = request.form.get("new")

        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (session["user"],))
        res = c.fetchone()

        if res and check_password_hash(res[0], old):
            c.execute("UPDATE users SET password=? WHERE username=?",
                      (generate_password_hash(new), session["user"]))
            conn.commit()
            msg = "Password changed successfully!"
        else:
            msg = "Old password incorrect."
        conn.close()

    return render_template("change_password.html", msg=msg)


# ---------- RECOMMEND ----------
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if "user" not in session:
        return redirect("/login")

    if request.method == "GET":
        return render_template("recommend.html")

    try:
        # Extract inputs safely
        temp = float(request.form.get("temp", 0))
        humidity = float(request.form.get("humidity", 0))
        ph = float(request.form.get("ph", 0))
        rainfall = float(request.form.get("rainfall", 0))
        n = float(request.form.get("n", 0))
        p = float(request.form.get("p", 0))
        k = float(request.form.get("k", 0))
        soil_moisture = float(request.form.get("soil_moisture", 0))
        market_signal = int(request.form.get("market_signal", 1))

        # Combine features (match model training order)
        X = [[n, p, k, temp, humidity, ph, rainfall, soil_moisture, market_signal]]
        Xs = scaler.transform(X)

        crop_idx = clf.predict(Xs)[0]
        crop_name = le.inverse_transform([crop_idx])[0]

        # Predict yield & confidence
        yield_pred = round(reg.predict(Xs)[0], 2)
        proba = clf.predict_proba(Xs)[0]
        confidence = round(float(np.max(proba) * 100), 2)

        # Store in history
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO history(username, date, crop, yield_val, confidence)
            VALUES (?,?,?,?,?)
        """, (session["user"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              crop_name, yield_pred, confidence))
        conn.commit()
        conn.close()

        return render_template("result.html",
                               crop=crop_name,
                               yield_val=yield_pred,
                               confidence=confidence)

    except Exception as e:
        return render_template("recommend.html", msg=f"Error: {e}")


# ---------- HISTORY ----------
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT date, crop, yield_val, confidence
        FROM history WHERE username=? ORDER BY id DESC
    """, (session["user"],))
    data = c.fetchall()
    conn.close()

    return render_template("history.html", records=data)


# ---------- MARKET TRENDS ----------
@app.route("/trends")
def trends():
    if "user" not in session:
        return redirect("/login")

    # Placeholder — later connect to API or chart data
    trend_data = [
        {"crop": "Rice", "trend": "↑ Rising"},
        {"crop": "Wheat", "trend": "→ Stable"},
        {"crop": "Cotton", "trend": "↓ Falling"},
    ]
    return render_template("trends.html", trends=trend_data)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
