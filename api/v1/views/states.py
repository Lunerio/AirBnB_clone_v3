#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models.state import State
from models import storage


@app_views.route('/states/<state_id>', strict_slashes=False)
@app_views.route('/states', strict_slashes=False)
def return_state_id(state_id=None):
    if state_id is None:
        states = storage.all(State)
        new_list = []
        for state in states.values():
            new_list.append(state.to_dict())
        return jsonify(new_list)

    elements = storage.get(State, state_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/states/<state_id>', methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    elements = storage.get(State, state_id)
    if elements is None:
        abort(404)
    else:
        storage.delete(elements)
        storage.save()
        return jsonify({})


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_state():
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'name' not in body.keys():
        abort(400, "Missing name")
    state = State(**body)
    state.save()
    state_dict = state.to_dict()
    return jsonify(state_dict), 201


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    elements = storage.get(State, state_id)
    if elements is None:
        abort(404)

    element_dict = elements.to_dict()
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key in body:
        if key != "id" and key != "updated_at" and key != "created_at":
            element_dict[key] = body[key]
    storage.delete(elements)
    state = State(**element_dict)
    state.save()
    return jsonify(state.to_dict()), 200
