from flask import Blueprint, render_template, request, redirect, url_for, session
from pymongo import MongoClient

connexion_bp = Blueprint("connexion", __name__)

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.filmapp

@connexion_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Cherche l'utilisateur dans MongoDB
        user = db.users.find_one({"username": username, "password": password})

        if user:
            # Stocke les infos dans la session
            session["user"] = user["username"]
            session["role"] = user["role"]

            # Redirection selon le rôle
            if user["role"] == "admin":
                return redirect("/admin/dashboard")
            elif user["role"] == "client":
                return redirect("/client")

        # Si mauvais identifiants
        return render_template("login.html", error="Identifiants incorrects")

    return render_template("login.html")
