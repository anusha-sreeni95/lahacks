import os
import sys
import json
import requests
import numpy as np

from datetime import datetime, timedelta


def is_weekday(dt_str):
    dt = datetime.strptime(dt_str, '%m-%d-%Y')
    if dt.weekday()<5:
        return True
    else:
        return False

def generate_random_location(bounds=[33.75, 34.20, -118.50, -118.00]):
    
    mu = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2]
    sigma = [(bounds[1]-bounds[0])/6, (bounds[3]-bounds[2])/6]
    
    random_lat = np.random.normal(mu[0], sigma[0])
    random_lon = np.random.normal(mu[1], sigma[1])

    random_location_str = str(random_lat) + ', ' + str(random_lon)
    
    return random_location_str

def update_timestamp(location_dict, date_string):
    dt = datetime.strptime(date_string, '%m-%d-%Y')
    final_dict = location_dict.copy()
    dt_final = dt + timedelta(np.random.randint(24*60))
    final_dict.update({'timestamp': dt_final.timestamp()})

    return final_dict

def test_query(location_str, radius, location_type):

    with open("API_key.txt", 'r+') as f:
            api_key = f.read()

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    params = [('location', location_str),
                ('radius', radius),
                ('name', 'cruise'), 
                ('types', location_type), 
                ('key', api_key)]

    res = requests.get(url, params = params)
    results = json.loads(res.content)
    results = json.dumps(results, indent=4)
    return results

if __name__=='__main__':
    results=test_query(generate_random_location(), 5000, 'gym')
    print(results)

'''
campground
meal_delivery
parking
primary_school
rv_park
school
secondary_school
storage
travel_agency
'''


'''
buckets = {
        'work': ['accounting', 'bank', 'city_hall', 'courthouse', 'dentist', 'doctor', 'electrician', 'embassy', 'fire_station',
                 'insurance_agency', 'lawyer', 'local_government_office', 'locksmith', 'painter', 'physiotherapist', 'plumber',
                 'police', 'post_office', 'real_estate_agency', 'roofing_contractor', 'moving_company'],
        'home': ['neighbourhood'],
        'fitness': ['gym'],
        'food': ['bakery', 'cafe', 'meal_takeaway', 'restaurant'],
        'party': ['bar', 'night_club'],
        'entertainment': ['amusement_park', 'bowling_alley', 'casino', 'movie_rental', 'movie_theater', 'museum', 'park', 'stadium',
                          'zoo'],
        'stay': ['lodging'],
        'tourist_spot': ['aquarium', 'art_gallery', 'tourist_attraction'],
        'transport': ['airport', 'bus_station', 'car_rental', 'car_repair', 'light_rail_station', 'subway_station', 'taxi_stand',
                      'train_station', 'transit_station'],
        'regular_stores': ['grocery_or_supermarket', 'department_store', 'supermarket'],
        'occasional_stores': ['bicycle_store', 'book_store', 'clothing_store', 'convenience_store', 'drugstore', 'electronics_store',
                   'furniture_store', 'hardware_store', 'home_goods_store', 'jewelry_store', 'liquor_store', 'florist', 'pet_store',
                   'pharmacy', 'shoe_store', 'shopping_mall', 'store', 'car_dealer'],
        'personal': ['atm', 'hair_care', 'hospital', 'spa', 'veterinary_care', 'beauty_salon', 'car_wash', 'funeral_home',
                     'gas_station', 'laundry', 'library'],
        'worship': ['cemetery', 'church', 'hindu_temple', 'mosque', 'synagogue'],
        'university': ['university']
'''

'''
Useless Tags:
'grocery_or_supermarket', 'supermarket'

'casino'

'car_wash', 'funeral_home'

'lodging'
'''