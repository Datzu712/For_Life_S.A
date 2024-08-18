from flask import blueprints

from .auth import auth_bp
from .dashboard import dashboard_bp

app_bp = blueprints.Blueprint('app', __name__, url_prefix='/')

app_bp.register_blueprint(auth_bp)
app_bp.register_blueprint(dashboard_bp)