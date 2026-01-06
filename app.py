from flask import Flask, render_template, session, redirect, url_for
from pymongo import MongoClient
from connexion import connexion_bp

app = Flask(__name__)
app.secret_key = "super_secret_key"  # nécessaire pour session

# Enregistrer le Blueprint connexion
app.register_blueprint(connexion_bp)

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.filmapp

@app.route("/")
def index():
    films = list(db.films.find().limit(6))
    return render_template("index.html", films=films)

# Dashboard admin
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("connexion.login"))  # renvoie vers login si pas admin
    films = list(db.films.find())
    return render_template("admin/dashboard.html", films=films)

# Page client
@app.route("/client")
def client_home():
    if session.get("role") != "client":
        return redirect(url_for("connexion.login"))  # renvoie vers login si pas client
    films = list(db.films.find())
    return render_template("client/films.html", films=films)

# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("connexion.login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
