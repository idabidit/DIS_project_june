from flask import Blueprint, render_template, request, redirect, url_for, session
import psycopg2
import os
import re

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
        phone = request.form["phone"]
        area_id = request.form["area"]

        if not is_valid_username(username):
            error = "Username can only contain letters, numbers, spaces, and underscores (2–30 characters)."
        elif not is_valid_password(password):
            error = "Password can only contain letters, numbers, spaces, and underscores (2–30 characters)."
        elif not is_valid_name(name):
            error = "Name can only contain letters and spaces (2–30 characters)."
        else:
            try:
                cur.execute(
                    "INSERT INTO caretakers (username, name, password, phone, area) VALUES (%s, %s, %s, %s, %s)",
                    (username, name, password, phone, area_id)
                )
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for("main.login_caretaker"))
            except UniqueViolation:
                conn.rollback()
                error = f"The username <strong>{username}</strong> is already in use. Please choose a different one."

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

        if not is_valid_username(username):
            error = "Username can only contain letters, numbers, spaces, and underscores (2–30 characters)."
            cur.close()
            conn.close()
        elif not is_valid_password(password):
            error = "Password can only contain letters, numbers, spaces, and underscores (2–30 characters)."
            cur.close()
            conn.close()
        else:
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

        if not is_valid_name(name):
            return "Pet name can only contain letters and spaces (2–30 characters).", 400
        elif not is_valid_description(description):
            return "Description can only contain letters, numbers, spaces, and the characters !?() æøåÆØÅ (2–30 characters).", 400
        else:
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

@bp.route("/edit_preferences/<int:pet_id>", methods=["GET", "POST"])
def edit_preferences(pet_id):
    if "caretaker_id" not in session:
        return redirect(url_for("main.login_caretaker"))

    caretaker_id = session["caretaker_id"]
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch current preferences + basic pet info to verify ownership
    cur.execute("""
        SELECT pets.id, pets.name,
               sp.id AS pref_species,
               g.id AS pref_gender
        FROM pets
        LEFT JOIN species_pref ON pets.id = species_pref.pet_id
        LEFT JOIN species AS sp ON species_pref.species_id = sp.id
        LEFT JOIN gender_pref ON pets.id = gender_pref.pet_id
        LEFT JOIN gender AS g ON gender_pref.gender_id = g.id
        WHERE pets.id = %s AND pets.caretaker_id = %s
    """, (pet_id, caretaker_id))

    pet = cur.fetchone()
    if pet is None:
        cur.close()
        conn.close()
        return "Pet not found or unauthorized", 404

    cur.execute("SELECT id, name FROM species")
    species = cur.fetchall()
    cur.execute("SELECT id, name FROM gender")
    gender = cur.fetchall()

    if request.method == "POST":
        pref_species = request.form.get("pref_species")
        pref_gender = request.form.get("pref_gender")

        # Clear old preferences
        cur.execute("DELETE FROM species_pref WHERE pet_id = %s", (pet_id,))
        cur.execute("DELETE FROM gender_pref WHERE pet_id = %s", (pet_id,))

        # Insert new preferences if provided
        if pref_species:
            cur.execute("INSERT INTO species_pref (pet_id, species_id) VALUES (%s, %s)", (pet_id, pref_species))
        if pref_gender:
            cur.execute("INSERT INTO gender_pref (pet_id, gender_id) VALUES (%s, %s)", (pet_id, pref_gender))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("main.view_owned_pets"))

    cur.close()
    conn.close()
    return render_template("edit_preferences.html", pet=pet, species=species, gender=gender)

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
        cur.execute("DELETE FROM species_pref WHERE pet_id = %s", (pet_id,))
        cur.execute("DELETE FROM gender_pref WHERE pet_id = %s", (pet_id,))
        cur.execute("DELETE FROM age_pref WHERE pet_id = %s", (pet_id,))
        cur.execute("DELETE FROM owns WHERE pet_id = %s AND caretaker_id = %s", (pet_id, session["caretaker_id"]))
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
        SELECT 
            pets.id, 
            pets.name, 
            pets.age, 
            pets.description, 
            pets.image_url,
            gender.name AS pet_gender, 
            species.name AS pet_species, 
            G.name AS pref_gender,
            SP.name AS pref_species
        FROM pets
        JOIN species ON pets.species = species.id
        JOIN gender ON pets.gender = gender.id
        LEFT JOIN species_pref ON pets.id = species_pref.pet_id
        LEFT JOIN species AS SP ON species_pref.species_id = SP.id
        LEFT JOIN gender_pref ON pets.id = gender_pref.pet_id
        LEFT JOIN gender AS G ON gender_pref.gender_id = G.id
        WHERE pets.caretaker_id = %s
    """, (caretaker_id,))
    pets = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "view_owned_pets.html",
        pets=pets
    )

@bp.route("/find_matches/<int:pet_id>")
def find_matches(pet_id):
    if "caretaker_id" not in session:
        return redirect(url_for("main.login_caretaker"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Get pet's preferences and caretaker_id for exclusion
    cur.execute("""
        SELECT pets.caretaker_id,
               sp.id AS pref_species,
               g.id AS pref_gender
        FROM pets
        LEFT JOIN species_pref ON pets.id = species_pref.pet_id
        LEFT JOIN species AS sp ON species_pref.species_id = sp.id
        LEFT JOIN gender_pref ON pets.id = gender_pref.pet_id
        LEFT JOIN gender AS g ON gender_pref.gender_id = g.id
        WHERE pets.id = %s
    """, (pet_id,))

    pet_info = cur.fetchone()
    if not pet_info:
        cur.close()
        conn.close()
        return "Pet not found", 404

    pet_caretaker_id, pref_species, pref_gender = pet_info

    # Build query for matching pets
    query = """
        SELECT pets.id, pets.name, pets.age, pets.description, pets.image_url,
               species.name AS pet_species, gender.name AS pet_gender,
               caretakers.username
        FROM pets
        JOIN species ON pets.species = species.id
        JOIN gender ON pets.gender = gender.id
        JOIN caretakers ON pets.caretaker_id = caretakers.id
        WHERE pets.caretaker_id != %s
    """

    params = [pet_caretaker_id]

    # Add preference filters if set
    if pref_species:
        query += " AND pets.species = %s"
        params.append(pref_species)
    if pref_gender:
        query += " AND pets.gender = %s"
        params.append(pref_gender)

    cur.execute(query, tuple(params))
    matches = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("matches.html", matches=matches, pet_name=pet_id)

def is_valid_username(username):
    return re.fullmatch(r"^[a-zA-Z0-9_ æøåÆØÅ]{2,30}$", username) is not None

def is_valid_password(password):
    return re.fullmatch(r"^[a-zA-Z0-9_ æøåÆØÅ]{2,30}$", password) is not None

def is_valid_description(description):
    return re.fullmatch(r"^[a-zA-Z0-9 æøåÆØÅ.,!?()'\-]{2,300}$", description) is not None

def is_valid_name(name):
    return re.fullmatch(r"^[a-zA-Z æøåÆØÅ]{2,30}$", name) is not None

