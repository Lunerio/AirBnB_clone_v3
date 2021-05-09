#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def return_places_by_city_id(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    place_city = []
    for elements in places.values():
        if city_id in elements.to_dict().values():
            place_city.append(elements.to_dict())
    return jsonify(place_city)


@app_views.route('/places/<place_id>', methods=["GET"],
                 strict_slashes=False)
def return_place(place_id):
    elements = storage.get(Place, place_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    elements = storage.get(Place, place_id)
    if elements is None:
        abort(404)
    else:
        storage.delete(elements)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not here")
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'user_id' not in body.keys():
        abort(400, "Missing user_id")
    if storage.get(User, body['user_id']) is None:
        abort(404)
    if 'name' not in body.keys():
        abort(400, "Missing name")
    body['city_id'] = city_id
    place = Place(**body)
    place.save()
    place_dict = place.to_dict()
    return jsonify(place_dict), 201


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    elements = storage.get(Place, place_id)
    if elements is None:
        abort(404)

    element_dict = elements.to_dict()
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key in body:
        if key != "id" and key != "updated_at"\
                and key != "created_at" and key != "user_id"\
                    and key != "city_id":
            element_dict[key] = body[key]
    storage.delete(elements)
    place = Place(**element_dict)
    place.save()
    return jsonify(place.to_dict()), 200
