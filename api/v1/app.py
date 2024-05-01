from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)

# Register Blueprint instance to the Flask app
app.register_blueprint(app_views)

# Close storage connection on application context teardown
@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

# Enable CORS for all routes with a wildcard origin (0.0.0.0)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

# Handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    # Run Flask application
    app.run(host=host, port=port, threaded=True)
