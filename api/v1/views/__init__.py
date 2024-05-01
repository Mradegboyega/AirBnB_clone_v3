#!/usr/bin/python3
"""Defines API views for the v1 version."""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import other view files
from api.v1.views import index
from api.v1.views import states
from api.v1.views import amenities
from api.v1.views import cities
from api.v1.views import users
from api.v1.views import places
from api.v1.views import reviews
from api.v1.views import places_amenities
