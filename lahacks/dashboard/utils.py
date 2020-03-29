from .models import LocationData


def add_location(request, latitude, longitude, timestamp):
    row = LocationData(email_address="joshuayoung22@ucla.edu", longitude=longitude, latitutde=latitude, timestamp=timestamp)
    row.save()
