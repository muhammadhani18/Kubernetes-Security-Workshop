from flask import Flask, jsonify, request
import logging
import os
import socket
import time
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# VULNERABILITY: Hardcoded credentials
ADMIN_KEY = os.environ.get('ADMIN_KEY', 'super-secret-key')

# Sensitive data that should be protected
sensitive_data = {
    "database_credentials": {
        "host": "db-server.internal",
        "username": "admin",
        "password": ADMIN_KEY  
    },
    "api_keys": {
        "payment_gateway": "pk_live_123456789",
        "external_service": "eyJhbGciOiJIUzI1NiJ9..."
    },
    "internal_configs": {
        "debug_mode": True,
        "maintenance_window": "Sundays 2-4 AM UTC"
    }
}

def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
        
    token = auth_header.split(' ')[1]
    # VULNERABILITY: Simple string comparison instead of proper auth
    return token == ADMIN_KEY

@app.route('/api/sensitive-data')
def get_sensitive_data():
    if not authenticate():
        return jsonify({"error": "Unauthorized"}), 401
        
    # Log the request (potential information leak)
    logger.info(f"Sensitive data accessed by: {request.remote_addr}")
    
    # VULNERABILITY: Returns all sensitive data without any filtering
    return jsonify(sensitive_data)

@app.route('/api/system-operations', methods=['POST'])
def system_operations():
    if not authenticate():
        return jsonify({"error": "Unauthorized"}), 401
        
    operation = request.json.get('operation')
    
    # VULNERABILITY: Dangerous operations without proper validation
    if operation == "run_command":
        command = request.json.get('command', '')
        # Simulating command execution (in a real app, this could be very dangerous)
        return jsonify({"result": f"Simulated execution of: {command}"})
        
    elif operation == "update_config":
        # Apply without validation
        changes = request.json.get('changes', {})
        sensitive_data["internal_configs"].update(changes)
        return jsonify({"result": "Configuration updated", "new_config": sensitive_data["internal_configs"]})
        
    return jsonify({"error": "Unknown operation"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# VULNERABILITY: Resource exhaustion
@app.route('/api/heavy-operation')
def heavy_operation():
    if not authenticate():
        return jsonify({"error": "Unauthorized"}), 401
    
    # Simulate CPU-intensive operation
    result = 0
    for i in range(10000000):
        result += i
    
    # Memory usage
    big_list = [i for i in range(1000000)]
    
    return jsonify({"result": "Heavy operation completed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)