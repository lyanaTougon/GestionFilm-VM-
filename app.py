from flask import Flask, render_template, session, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "TON_SECRET_KEY"  # nécessaire pour utiliser session

# Config MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/filmsdb"
mongo = PyMongo(app)

# Page d'accueil (index)
@app.route("/")
def index():
    films = list(mongo.db.films.find().limit(6))
    return render_template("index.html", films=films)

# Page "Tous les films"
@app.route('/films')
def films_page():
    films = list(mongo.db.films.find())
    return render_template('film.html', films=films)

# Page "Mes notes"
@app.route('/mesnotes')
def mesnotes():
    return render_template('mesnotes.html')

# Dashboard admin
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))  # redirige vers page de connexion
    films = list(mongo.db.films.find())
    return render_template("admin/dashboard.html", films=films)

# Page client
@app.route("/client")
def client_home():
    if session.get("role") != "client":
        return redirect(url_for("login"))  # redirige vers page de connexion
    films = list(mongo.db.films.find())
    return render_template("client/films.html", films=films)

# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Page de connexion (exemple minimal)
@app.route("/login")
def login():
    return render_template("login.html")  # Crée login.html dans templates

# Lancer l'app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
