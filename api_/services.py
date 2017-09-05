from googleplaces import GooglePlaces, lang
from .models import Place

GOOGLE_PLACES_API_KEY = 'AIzaSyBqPlR1NaPECU18YOlbFgA3a5pWwxAWIT8'

google_places = GooglePlaces(GOOGLE_PLACES_API_KEY)


def get_place_from_google_places(place_id: str):
    try:
        place = google_places.get_place(place_id=place_id, sensor=False, language=lang.PORTUGUESE_BRAZIL)
    except Exception:
        return None
    if place:
        return Place(
            id=place.place_id,
            formatted_address=place.formatted_address,
            latitude=float(place.geo_location['lat']),
            longitude=float(place.geo_location['lng']),
        )
    return None
