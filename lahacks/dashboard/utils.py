from .models import LocationData


def add_location(request, latitude, longitude, timestamp):
    row = LocationData(email_address=request.session['email_address'], longitude=longitude, latitutde=latitude, timestamp=timestamp)
    row.save()
