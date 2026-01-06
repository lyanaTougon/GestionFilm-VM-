#!/bin/bash

# Aller dans le dossier du projet
cd "$(dirname "$0")"

# Activer le venv si il existe
if [ -d "venv" ]; then
    echo "Activation de l'environnement virtuel..."
    source venv/bin/activate
else
    echo "Aucun venv trouvé ! Création..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Lancer l'application Flask
echo "Lancement de Flask..."
python3 app.py
