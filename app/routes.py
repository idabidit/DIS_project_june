from flask import Blueprint, render_template, request, redirect, url_for, session
import psycopg2
import os

bp = Blueprint("main", __name__)
bp.secret_key = os.getenv("FLASK_SECRET", "secret123")

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "pet_tinder"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password")
    )
    return conn

@bp.route("/")
def home():
    return render_template("home.html")

from psycopg2.errors import UniqueViolation

@bp.route("/register_caretaker", methods=["GET", "POST"])
def register_caretaker():
    conn = get_db_connection()
    cur = conn.cursor()
    error = None

    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        area_id = request.form["area"]

        try:
            cur.execute(
                "INSERT INTO caretakers (username, name, password, area) VALUES (%s, %s, %s, %s)",
                (username, name, password, area_id)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("main.login_caretaker"))

        except UniqueViolation:
            conn.rollback()
            error = f"❗ The username <strong>{username}</strong> is already in use. Please choose a different one."

    # Fetch areas again for the form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM areas")
    areas = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("register_caretaker.html", areas=areas, error=error)

@bp.route("/login_caretaker", methods=["GET", "POST"])
def login_caretaker():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM caretakers WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            user_id, name = user
            session["caretaker_id"] = user_id
            session["caretaker_name"] = name
            return redirect(url_for("main.home"))
        else:
            error = "Wrong username or password"

    return render_template("login_caretaker.html", error=error)

@bp.route("/logout_caretaker")
def logout_caretaker():
    session.clear()
    return redirect(url_for("main.home"))

import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"

@bp.route("/register_pet", methods=["GET", "POST"])
def register_pet():
    if "caretaker_id" not in session:
        return redirect(url_for("main.login_caretaker"))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        species = request.form["species"]
        gender = request.form["gender"]
        description = request.form["description"]
        caretaker_id = session["caretaker_id"]

        # Handle uploaded file
        file = request.files["image"]
        if not file:
            return "Image required", 400
        
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(file_path)
        image_url = f"/{file_path}"

        cur.execute("""
            INSERT INTO pets (name, age, species, gender, image_url, description, caretaker_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, age, species, gender, image_url, description, caretaker_id))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("main.view_owned_pets"))

    cur.execute("SELECT id, name FROM species")
    species = cur.fetchall()
    cur.execute("SELECT id, name FROM gender")
    gender = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("register_pet.html", species=species, gender=gender)

@bp.route("/delete_pet/<int:pet_id>", methods=["POST"])
def delete_pet(pet_id):
    if "caretaker_id" not in session:
        return redirect(url_for("main.login_caretaker"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Get the image file path before deleting
    cur.execute("SELECT image_url FROM pets WHERE id = %s AND caretaker_id = %s", (pet_id, session["caretaker_id"]))
    result = cur.fetchone()
    if result:
        image_url = result[0]  # e.g. /static/uploads/filename.jpg
        file_path = image_url.lstrip("/")  # remove leading slash

        # Delete the database entry
        cur.execute("DELETE FROM pets WHERE id = %s AND caretaker_id = %s", (pet_id, session["caretaker_id"]))
        conn.commit()
        cur.close()
        conn.close()

        # Delete image file from filesystem
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
    else:
        cur.close()
        conn.close()

    return redirect(url_for("main.view_owned_pets"))

@bp.route("/view_owned_pets")
def view_owned_pets():
    if "caretaker_id" not in session:
        return redirect(url_for("main.login_caretaker"))

    caretaker_id = session["caretaker_id"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT pets.id, pets.name, pets.age, species.name, pets.description, pets.image_url
        FROM pets
        JOIN species ON pets.species = species.id
        WHERE pets.caretaker_id = %s
    """, (caretaker_id,))
    pets = cur.fetchall()
    cur.close()
    conn.close()

    # Convert result to list of dicts
    # pet_list = []
    # for pet in pets:
    #     pet_list.append({
    #         "id": pet[0],
    #         "name": pet[1],
    #         "age": pet[2],
    #         "species": pet[3],
    #         "gender": pet[4],
    #         "description": pet[5],
    #         "image_url": pet[6]
    #     })

    return render_template("view_owned_pets.html", pets=pets)
