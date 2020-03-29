from .models import LocationData


def add_location(request, location):
    # TODO: Write code to convert geographical location to lat long
    latitutde = 0
    longitude = 0
    timestamp = "03-13-2020"
    row = LocationData(email_address=request.session['email_address'], longitude=longitude, latitutde=latitutde, timestamp=timestamp)
    row.save()
