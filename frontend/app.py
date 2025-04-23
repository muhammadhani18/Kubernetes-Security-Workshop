# --- frontend/app.py ---
from flask import Flask, render_template, request, jsonify
import os
import requests
import logging
import socket

app = Flask(__name__)

# Vulnerable configuration - hardcoded credentials and URLs
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend-api:5000')
ADMIN_URL = os.environ.get('ADMIN_URL', 'http://admin-api:5000')  # Should not be accessible
ADMIN_KEY = os.environ.get('ADMIN_KEY', 'super-secret-key')  # Should not be here

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    return f"""
    <h1>Frontend Service</h1>
    <p>Hostname: {hostname}</p>
    <h2>Regular User Actions</h2>
    <button onclick="fetchData()">Get User Data (via Backend)</button>
    <div id="userData"></div>
    
    <h2>Security Vulnerability Demo</h2>
    <button onclick="adminAccess()">Access Admin API Directly</button>
    <div id="adminData"></div>
    
    <script>
    function fetchData() {{
        fetch('/api/user-data')
            .then(response => response.json())
            .then(data => {{
                document.getElementById('userData').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }});
    }}
    
    function adminAccess() {{
        fetch('/api/admin-data')
            .then(response => response.json())
            .then(data => {{
                document.getElementById('adminData').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }});
    }}
    </script>
    """

@app.route('/api/user-data')
def user_data():
    # Proper access through backend API
    try:
        response = requests.get(f"{BACKEND_URL}/api/data")
        return jsonify(response.json())
    except Exception as e:
        logger.error(f"Error fetching backend data: {e}")
        return jsonify({"error": "Backend service unavailable"}), 500

@app.route('/api/admin-data')
def admin_data():
    # VULNERABILITY: Frontend should never access admin API directly
    # This demonstrates the network segmentation issue
    try:
        # Using the hardcoded admin key from environment variables
        response = requests.get(
            f"{ADMIN_URL}/api/sensitive-data",
            headers={"Authorization": f"Bearer {ADMIN_KEY}"}
        )
        return jsonify({"admin_data": response.json(), "message": "Security vulnerability: Direct access to admin API!"})
    except Exception as e:
        logger.error(f"Error accessing admin API: {e}")
        return jsonify({"error": "Admin API access failed", "message": "But the attempt itself shows a security issue!"}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# VULNERABILITY: Debug endpoint that could leak information
@app.route('/debug')
def debug():
    env_vars = dict(os.environ)
    # This leaks sensitive information like keys and internal URLs
    return jsonify({"environment": env_vars, "hostname": socket.gethostname()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)