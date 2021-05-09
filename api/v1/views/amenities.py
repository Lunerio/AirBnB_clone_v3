#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
@app_views.route('/amenities', strict_slashes=False)
def return_amenity_id(amenity_id=None):
    if amenity_id is None:
        amenities = storage.all(Amenity)
        new_list = []
        for amenity in amenities.values():
            new_list.append(amenity.to_dict())
        return jsonify(new_list)

    elements = storage.get(Amenity, amenity_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    elements = storage.get(Amenity, amenity_id)
    if elements is None:
        abort(404)
    else:
        storage.delete(elements)
        storage.save()
        return jsonify({})


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'name' not in body.keys():
        abort(400, "Missing name")
    amenity = Amenity(**body)
    amenity.save()
    amenity_dict = amenity.to_dict()
    return jsonify(amenity_dict), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    elements = storage.get(Amenity, amenity_id)
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
    amenity = Amenity(**element_dict)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
