#!/usr/bin/python3
""" Creates a new view for City objects that handles all
default RestFul API actions """
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all Cities objects """
    data = storage.all(City)
    cities_list = []
    for obj in data.values():
        if obj.state_id == state_id:
            cities_list.append(obj.to_dict())
    if len(cities_list) == 0:
        return jsonify([]), 404
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_by_id(city_id):
    """ Retrieves a State object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Creates a City object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    json_data = request.get_json()
    new_city = City(state_id=state_id, **json_data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Updates a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
