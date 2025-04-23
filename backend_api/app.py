from flask import Flask, jsonify, request
import logging
import os
import socket
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample database (in-memory)
users = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"},
]

@app.route('/api/data')
def get_data():
    logger.info(f"Data request from: {request.remote_addr}")
    return jsonify({"users": users})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# VULNERABILITY: No authentication or rate limiting
@app.route('/api/users', methods=['POST'])
def create_user():
    user = request.json
    if user:
        users.append(user)
        return jsonify({"success": True, "user_id": len(users)}), 201
    return jsonify({"error": "Invalid user data"}), 400

if __name__ == '__main__':
    # VULNERABILITY: Debug mode in production
    app.run(host='0.0.0.0', port=5000, debug=True)
