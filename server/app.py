from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
import time

app = Flask(__name__)

# משתנים של בסיס הנתונים
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mysecret")
DB_NAME = os.getenv("DB_NAME", "recipes_db")
CONTAINER_NAME = os.getenv("FLASK_INSTANCE", "flask-default")


def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.Error:
            retries -= 1
            time.sleep(3)
    raise Exception("DB connection failed")


def init_db():
    """יוצר את הטבלה recipes אם היא לא קיימת"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            ingredients TEXT,
            instructions TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/whoami")
def whoami():
    user_ip = request.remote_addr
    return f"Container: {CONTAINER_NAME}, User IP: {user_ip}"


@app.route("/recipes", methods=["GET"])
def get_recipes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, ingredients, instructions FROM recipes")
    recipes = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in recipes:
        r["ingredients"] = r["ingredients"].split(",") if r["ingredients"] else []

    return jsonify(recipes)


@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.json
    name = data.get("name")
    ingredients = ",".join(data.get("ingredients", []))
    instructions = data.get("instructions")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, ingredients, instructions) VALUES (%s, %s, %s)",
        (name, ingredients, instructions)
    )
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"id": last_id, "message": "Recipe added"}), 201


@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id=%s", (recipe_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recipe deleted"}), 200


@app.route("/recipes/<int:recipe_id>", methods=["PATCH"])
def update_recipe(recipe_id):
    data = request.json
    ingredients = ",".join(data.get("ingredients", [])) if "ingredients" in data else None
    instructions = data.get("instructions") if "instructions" in data else None

    if not ingredients and not instructions:
        return jsonify({"message": "No fields to update"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    if ingredients is not None:
        fields.append("ingredients=%s")
        values.append(ingredients)
    if instructions is not None:
        fields.append("instructions=%s")
        values.append(instructions)
    
    values.append(recipe_id)
    sql = f"UPDATE recipes SET {', '.join(fields)} WHERE id=%s"
    cursor.execute(sql, tuple(values))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Recipe updated"}), 200


if __name__ == "__main__":
    init_db()  # ודא שהטבלה קיימת לפני הפעלת השרת
    app.run(host="0.0.0.0", port=5000)
