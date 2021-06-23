#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def return_places_by_city_id(city_id):
    """Return places in a city
    """
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
    """Return a place by city_id
    """
    elements = storage.get(Place, place_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete place
    """
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
    """Create place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
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
    """Update place
    """
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


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """Search for places
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)
    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)
    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]
    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)
    return jsonify(places)
