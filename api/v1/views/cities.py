#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def return_cities_by_state_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    city_state = []
    for elements in cities.values():
        if state_id in elements.to_dict().values():
            city_state.append(elements.to_dict)
    return jsonify(city_state)


@app_views.route('/cities/<city_id>', methods=["GET"],
                 strict_slashes=False)
def return_city(city_id):
    elements = storage.get(City, city_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    elements = storage.get(City, city_id)
    if elements is None:
        abort(404)
    else:
        storage.delete(elements)
        storage.save()
        return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'name' not in body.keys():
        abort(400, "Missing name")
    city = City(**body)
    city.save()
    city_dict = city.to_dict()
    return jsonify(city_dict), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    elements = storage.get(City, city_id)
    if elements is None:
        abort(404)

    element_dict = elements.to_dict()
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key in body:
        if key != "id" and key != "updated_at"\
                and key != "created_at" and key != "state_id":
            element_dict[key] = body[key]
    storage.delete(elements)
    city = City(**element_dict)
    city.save()
    return jsonify(city.to_dict()), 200
