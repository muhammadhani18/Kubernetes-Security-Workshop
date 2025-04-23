from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "testdb"),
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "password")
    )
    return conn

@app.route("/data", methods=["GET"])
def fetch_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM dummy_data;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": row[0], "name": row[1]} for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
