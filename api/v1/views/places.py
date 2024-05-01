#!/usr/bin/python3
"""Defines API routes for Place objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place, City, User

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places based on JSON request"""
    try:
        req_data = request.get_json()
        if not req_data:
            return jsonify([place.to_dict() for place in storage.all(Place).values()])

        states = req_data.get("states", [])
        cities = req_data.get("cities", [])
        amenities = req_data.get("amenities", [])

        place_ids = set()
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    place_ids.update([city.id for city in state.cities])

        if cities:
            place_ids.update(cities)

        if amenities:
            amenity_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
            place_ids.intersection_update(set(place.id for place in Place.all() if all(amenity in place.amenities for amenity in amenity_objs)))

        places = [place.to_dict() for place in storage.all(Place).values() if place.id in place_ids]

        return jsonify(places)

    except Exception as e:
        abort(400, str(e))



@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})
