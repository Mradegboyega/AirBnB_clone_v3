from flask import Blueprint

# Create a Blueprint instance for version 1 of the API
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views to register routes
from api.v1.views import *
