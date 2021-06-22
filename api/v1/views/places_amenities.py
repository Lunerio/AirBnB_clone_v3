#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from os import environ
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def return_place_amenities(place_id):
    """Return the amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
    else:
        for amenity in place.amenity_id:
            amenities.append(storage.get(Amenity, amenity).to_dict())


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenities_ids:
            abort(404)
        place.amenities_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=[POST],
                 strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    """Adds an amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenities_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenities_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
