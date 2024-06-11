#!/usr/bin/python3
""" Creates a new view for State objects that handles all
default RestFul API actions """
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves the list of all Users objects """
    data = storage.all(User)
    users_list = []
    for obj in data.values():
        users_list.append(obj.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    """ Retrieves an User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes an User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    else:
        user.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a user object"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    json_data = request.get_json()
    new_user = User(**json_data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Updates a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    json_data = request.get_json()
    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    storage.save()
    return make_response(user.to_dict(), 200)
