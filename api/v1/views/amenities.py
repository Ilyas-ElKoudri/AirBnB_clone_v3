#!/usr/bin/python3
""" Creates a new view for State objects that handles all
default RestFul API actions """
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def amenities():
    """ Retrieves the list of all amenities objects """
    data = storage.all(Amenity)
    amenities_list = []
    for obj in data.values():
        amenities_list.append(obj.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """ Retrieves an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates an amenity object"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    json_data = request.get_json()
    new_amenity = Amenity(**json_data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    json_data = request.get_json()
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return make_response(amenity.to_dict(), 200)
