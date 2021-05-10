#!/usr/bin/python3
""" Handle every RESTapi actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def return_reviews_by_place_id(place_id):
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    reviews = storage.all(Review)
    review_place = []
    for elements in reviews.values():
        if place_id in elements.to_dict().values():
            review_place.append(elements.to_dict())
    return jsonify(review_place)


@app_views.route('/reviews/<review_id>', methods=["GET"],
                 strict_slashes=False)
def return_review(review_id):
    elements = storage.get(Review, review_id)
    if elements is None:
        abort(404)
    else:
        return jsonify(elements.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    elements = storage.get(Review, review_id)
    if elements is None:
        abort(404)
    else:
        storage.delete(elements)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'user_id' not in body.keys():
        abort(400, "Missing user_id")
    if storage.get(User, body['user_id']) is None:
        abort(404)
    if 'text' not in body.keys():
        abort(400, "Missing text")
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    review_dict = review.to_dict()
    return jsonify(review_dict), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    elements = storage.get(Review, review_id)
    if elements is None:
        abort(404)

    element_dict = elements.to_dict()
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key in body:
        if key != "id" and key != "updated_at"\
                and key != "created_at" and key != "user_id"\
                and key != "place_id":
            element_dict[key] = body[key]
    storage.delete(elements)
    review = Review(**element_dict)
    review.save()
    return jsonify(review.to_dict()), 200
