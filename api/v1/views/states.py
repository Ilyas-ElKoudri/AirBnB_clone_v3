#!/usr/bin/python3
""" Creates a new view for State objects that handles all
default RestFul API actions """
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    data = storage.all(State)
    states_list = []
    for obj in data.values():
        states_list.append(obj.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_by_id(state_id):
    """ Retrieves a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State object"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    json_data = request.get_json()
    new_state = State(**json_data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return make_response(state.to_dict(), 200)
