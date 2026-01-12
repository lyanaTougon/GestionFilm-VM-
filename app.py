from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "TON_SECRET_KEY"

# Config MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/filmsdb"
mongo = PyMongo(app)

# ------------------------------
# Route login
# ------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Cherche l'utilisateur dans MongoDB
        user = mongo.db.users.find_one({"username": username, "password": password})

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]

            # 🔹 Redirection vers mesnotes.html
            return redirect(url_for("mesnotes"))

        # Si mauvais identifiants
        return render_template("login.html", error="Identifiants incorrects")

    return render_template("login.html")


# ------------------------------
# Déconnexion
# ------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ------------------------------
# Page d'accueil
# ------------------------------
@app.route("/")
def index():
    films = list(mongo.db.films.find().limit(6))
    return render_template("index.html", films=films)

# ------------------------------
# Tous les films
# ------------------------------
@app.route("/films")
def films_page():
    films = list(mongo.db.films.find())
    return render_template("films.html", films=films)

# ------------------------------
# Mes notes
# ------------------------------
@app.route("/mesnotes")
def mesnotes():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("mesnotes.html")

# ------------------------------
# Dashboard Admin
# ------------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    films = list(mongo.db.films.find())
    return render_template("admin/dashboard.html", films=films)

# ------------------------------
# Page Client
# ------------------------------
@app.route("/client")
def client_home():
    if session.get("role") != "client":
        return redirect(url_for("login"))
    films = list(mongo.db.films.find())
    return render_template("client/films.html", films=films)

# ------------------------------
# Lancer l'application
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
