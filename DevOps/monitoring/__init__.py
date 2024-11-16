
from flask import Blueprint
from .routes import monitor_bp

def init_monitoring(app):
    app.register_blueprint(monitor_bp)
