from flask import Blueprint, render_template, request, redirect, url_for, session
import psycopg2
import os
from .models import view_caretakers, insert_caretaker, view_pets, insert_pet
from .database import init_db


bp = Blueprint("main", __name__)
bp.secret_key = os.getenv("FLASK_SECRET", "secret123")

@bp.route('/create_caretaker', methods=['GET', 'POST'])
def create_caretaker():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            insert_caretaker(username, password)
            return redirect(url_for('main.caretakers'))
        except Exception as e:
            print(f"Error creating caretaker: {e}")
            return render_template('create_caretaker.html', error="Could not create account")
            
    return render_template('create_caretaker.html')
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM caretakers WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            session["caretaker_id"] = result[0]
            session["caretaker_name"] = result[1]  # name used for display
            return redirect(url_for("main.home"))
        else:
            return "Invalid username or password", 401

    return render_template("login.html")

@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("main.home"))

@bp.route('/init-db')
def initialize_db():
    init_db()
    return 'Database initialized!'

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route('/view_pets', methods=['GET', 'POST'])
def pets():
    if request.method == 'POST':
        return redirect(url_for('main.view_pets'))
    pets = view_pets()
    return render_template('view_pets.html', pets=pets)

@bp.route('/view_caretakers', methods=['GET', 'POST'])
def caretakers():
    if request.method == 'POST':
        return redirect(url_for('main.view_caretakers'))
    caretakers = view_caretakers()
    return render_template('view_caretakers.html', caretakers=caretakers)