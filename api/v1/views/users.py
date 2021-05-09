!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models.user import User
from models import storage


@app_views.route('/users/<user_id>', strict_slashes=False)
@app_views.route('/users', strict_slashes=False)
def return_user_id(user_id=None):
    if user_id is None:
        users = storage.all(User)
        new_list = []
        for user in users.values():
            new_list.append(user.to_dict())
        return jsonify(new_list)

    elements = storage.get(User, user_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    elements = storage.get(User, user_id)
    if elements is None:
        abort(404)
    else:
        storage.delete(elements)
        storage.save()
        return jsonify({})


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'email' not in body.keys():
        abort(400, "Missing email")
    if 'password' not in body.keys():
        abort(400, "Missing password")
    user = User(**body)
    user.save()
    user_dict = user.to_dict()
    return jsonify(user_dict), 201


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    elements = storage.get(User, user_id)
    if elements is None:
        abort(404)

    element_dict = elements.to_dict()
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key in body:
        if key != "id" and key != "updated_at"\
                and key != "created_at" and key != "email":
            element_dict[key] = body[key]
    storage.delete(elements)
    user = User(**element_dict)
    user.save()
    return jsonify(user.to_dict()), 200
