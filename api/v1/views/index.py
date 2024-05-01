from flask import jsonify
from api.v1.views import app_views
from models import storage

# Route to get stats of each object type
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each object type"""
    classes = {"Amenity": storage.count(Amenity),
               "City": storage.count(City),
               "Place": storage.count(Place),
               "Review": storage.count(Review),
               "State": storage.count(State),
               "User": storage.count(User)}
    return jsonify(classes)
