import os
from flask import Flask, render_template, request, redirect, url_for
import random
import string
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = "db.sqlite"

# Création de la base SQLite si elle n'existe pas
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keys (
        key TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# Générer une clé aléatoire
def generate_key(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return redirect(url_for('unlock'))

@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    if request.method == "POST":
        # Ici, tu peux vérifier que l'utilisateur a bien vu les pubs via un paramètre ou une API
        # Pour l'exemple on génère directement la clé

        new_key = generate_key()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO keys (key) VALUES (?)", (new_key,))
        conn.commit()
        conn.close()

        return render_template("unlock.html", key=new_key)
    else:
        return render_template("unlock.html", key=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
