from flask import Blueprint, request, jsonify
from functions.create_provider import create_provider

# Define a Blueprint for provider-related routes
provider_bp = Blueprint('provider', __name__)

@provider_bp.route('/provider', methods=['POST'])
def provider():
    data = request.get_json()
    if data is None or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON or empty request body"}), 400

    # Call create_provider function and handle its response
    provider, status_code = create_provider(data)
    return jsonify(provider), status_code

# Setup routes by registering the blueprint
def setup_routes(app):
    app.register_blueprint(provider_bp)
