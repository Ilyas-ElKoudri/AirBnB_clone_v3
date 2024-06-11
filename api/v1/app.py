#!/usr/bin/python3
""" a script that starts a Flask web application """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views.index import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """a method to handle app teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON-formatted 404 status code"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host_flask = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port_flask = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host_flask, port=port_flask, threaded=True, debug=True)
