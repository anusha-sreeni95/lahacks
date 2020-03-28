import os
import sys
import names
import requests
import json

import numpy as np

from datetime import date, datetime, timedelta
from utils import is_weekday, generate_random_location

class Human(object):

    buckets = {
        'work': ['accounting', 'bank', 'city_hall', 'courthouse', 'dentist', 'doctor', 'electrician', 'embassy', 'fire_station',
                 'insurance_agency', 'lawyer', 'local_government_office', 'locksmith', 'painter', 'physiotherapist', 'plumber',
                 'police', 'post_office', 'real_estate_agency', 'roofing_contractor', 'moving_company'],
        'home': ['neighbourhood'],
        'fitness': ['gym'],
        'food': ['bakery', 'cafe', 'meal_takeaway', 'restaurant'],
        'party': ['bar', 'night_club'],
        'entertainment': ['amusement_park', 'bowling_alley', 'movie_rental', 'movie_theater', 'museum', 'park', 'stadium',
                          'zoo'],
        'stay': ['lodging'],
        'tourist_spot': ['aquarium', 'art_gallery', 'tourist_attraction'],
        'transport': ['airport', 'bus_station', 'car_rental', 'car_repair', 'light_rail_station', 'subway_station', 'taxi_stand',
                      'train_station', 'transit_station'],
        'regular_stores': ['department_store'],
        'occasional_stores': ['bicycle_store', 'book_store', 'clothing_store', 'convenience_store', 'drugstore', 'electronics_store',
                   'furniture_store', 'hardware_store', 'home_goods_store', 'jewelry_store', 'liquor_store', 'florist', 'pet_store',
                   'pharmacy', 'shoe_store', 'shopping_mall', 'store', 'car_dealer'],
        'personal': ['atm', 'hair_care', 'hospital', 'spa', 'veterinary_care', 'beauty_salon',
                     'gas_station', 'laundry', 'library'],
        'worship': ['cemetery', 'church', 'hindu_temple', 'mosque', 'synagogue'],
        'university': ['university']
    }


    def __init__(self):
        self.name = names.get_full_name()
        self.test_date = self.get_test_date()
        self.test_time = self.get_test_time()
        self.timeline = self.initiate_timeline()

        with open("API_key.txt", r+) as f:
            self.api_key = f.read()

    def get_test_date(self):
        n_days = np.random.randint(90)
        test_date = datetime.today() - timedelta(days=n_days)
        return test_date.strftime('%m-%d-%Y')
        
    def get_test_time(self):
        start = datetime.combine(date.today(), datetime.min.time())
        min_per_day = 24*60
        test = start + timedelta(minutes=np.random.randint(min_per_day))
        return test.strftime('%H:%M:%S')

    def initiate_timeline(self):
        timeline = dict()
        test_date_datetime = datetime.strptime(self.test_date, '%m-%d-%Y')
        for i in range(1, 15):
            date_str = (test_date_datetime - timedelta(days=i)).strftime('%m-%d-%Y')
            timeline[date_str] = []
        return timeline

    def query(self, location_str, radius, location_type):
        
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        params = [('location', location_str),
                    ('radius', radius),
                    ('name', 'cruise'), 
                    ('types', location_type), 
                    ('key', self.api_key)]

        res = requests.get(url, params = params)
        results = json.loads(res.content)
        #results = json.dumps(results, indent=4)
        return results


    def edit_timeline(self, bucket, intial_location_str, radius):
        
        location_type = np.random.choice(self.buckets[bucket])
        print(location_type)
        response = self.query(intial_location_str, radius, location_type)
        
        pruned_results = list(np.random.choice(response['results'], self.places[bucket]))
        
        if len(pruned_results)==0:
            return {}

        if self.events[bucket] == 'everyday':
            for key in self.timeline.keys():
                location = np.random.choice(pruned_results)['geometry']['location']
                self.timeline[key].append(location)
        
        elif self.events[bucket] == 'weekday':
            for key in self.timeline.keys():
                if is_weekday(key):
                    location = np.random.choice(pruned_results)['geometry']['location']
                    self.timeline[key].append(location)
                else:
                    continue
        
        elif self.events[bucket] == 'regular':
            random_number = np.random.randint(7, 10)
            chosen_keys = np.random.choice(list(self.timeline.keys()), random_number)
            for key in chosen_keys:
                location = np.random.choice(pruned_results)['geometry']['location']
                self.timeline[key].append(location)
        
        elif self.events[bucket] == 'occasional':
            random_number = np.random.randint(4, 7)
            chosen_keys = np.random.choice(list(self.timeline.keys()), random_number)
            for key in chosen_keys:
                location = np.random.choice(pruned_results)['geometry']['location']
                self.timeline[key].append(location)
        
        elif self.events[bucket] == 'rare':
            random_number = np.random.randint(0, 3)
            chosen_keys = np.random.choice(list(self.timeline.keys()), random_number)
            for key in chosen_keys:
                location = np.random.choice(pruned_results)['geometry']['location']
                self.timeline[key].append(location)
        
        return np.random.choice(pruned_results)['geometry']['location']
        
        

    def update_timeline(self):
        
        home_location = self.edit_timeline('home', generate_random_location(), 20000)
        home_location_str = str(home_location['lat']) + ', ' + str(home_location['lng'])

        print("Home Location: {}".format(home_location_str))

        work_location = self.edit_timeline('work', home_location_str, 20000)
        work_location_str = str(work_location['lat']) + ', ' + str(work_location['lng'])

        print("Work Location: {}".format(work_location_str))

        _ = self.edit_timeline('fitness', home_location_str, 50000)
        _ = self.edit_timeline('food', work_location_str, 50000)
        _ = self.edit_timeline('party', work_location_str, 50000)
        _ = self.edit_timeline('entertainment', home_location_str, 100000)
        _ = self.edit_timeline('stay', generate_random_location(), 50000)
        _ = self.edit_timeline('tourist_spot', generate_random_location(), 50000)
        _ = self.edit_timeline('regular_stores', home_location_str, 50000)
        _ = self.edit_timeline('occasional_stores', home_location_str, 100000)
        _ = self.edit_timeline('personal', home_location_str, 100000)
        _ = self.edit_timeline('worship', home_location_str, 100000)
        _ = self.edit_timeline('university', home_location_str, 100000)
            
        

        print(self.timeline)
    

class Salaryman(Human):
    
    def __init__(self):
        Human.__init__(self)
        self.places = {
            'work': 1,
            'home': 1,
            'fitness': 1,
            'food': 10,
            'party': 5,
            'entertainment': 5,
            'stay': 0,
            'tourist_spot': 0,
            'transport': 0,
            'regular_stores': 10,
            'occasional_stores': 30,
            'personal': 10,
            'worship': 3,
            'university': 0
        }

        self.events = {
            'work': 'weekday',
            'home': 'everyday',
            'fitness': 'regular',
            'food': 'occasional',
            'party': 'rare',
            'entertainment': 'rare',
            'stay': 'never',
            'tourist_spot': 'never',
            'transport': 'never',
            'regular_stores': 'rare',
            'occasional_stores': 'rare',
            'personal': 'rare',
            'worship': 'rare',
            'university': 'never'
        }

        

class Student(Human):
    
    def __init__(self):
        Human.__init__(self)
        self.places = {
            'work': 1,
            'home': 1,
            'fitness': 1,
            'food': 10,
            'party': 5,
            'entertainment': 5,
            'stay': 0,
            'tourist_spot': 0,
            'transport': 0,
            'regular_stores': 10,
            'occasional_stores': 30,
            'personal': 10,
            'worship': 3,
            'university': 0
        }

        self.events = {
            'work': 'everyday',
            'home': 'everyday',
            'fitness': 'regular',
            'food': 'occasional',
            'party': 'rare',
            'entertainment': 'rare',
            'stay': 'never',
            'tourist_spot': 'never',
            'transport': 'never',
            'regular_stores': 'rare',
            'occasional_stores': 'rare',
            'personal': 'rare',
            'worship': 'rare',
            'university': 'never'
        }

class Tourist(Human):
    
    def __init__(self):
        Human.__init__(self)
        self.places = {
            'work': 1,
            'home': 1,
            'fitness': 1,
            'food': 10,
            'party': 5,
            'entertainment': 5,
            'stay': 0,
            'tourist_spot': 0,
            'transport': 0,
            'regular_stores': 10,
            'occasional_stores': 30,
            'personal': 10,
            'worship': 3,
            'university': 0
        }

        self.events = {
            'work': 'everyday',
            'home': 'everyday',
            'fitness': 'regular',
            'food': 'occasional',
            'party': 'rare',
            'entertainment': 'rare',
            'stay': 'never',
            'tourist_spot': 'never',
            'transport': 'never',
            'regular_stores': 'rare',
            'occasional_stores': 'rare',
            'personal': 'rare',
            'worship': 'rare',
            'university': 'never'
        }

if __name__=='__main__':
    salaryman = Salaryman()
    print(salaryman.name)
    print(salaryman.test_date)
    print(salaryman.test_time)
    print('\n')
    salaryman.update_timeline()
    
    '''
    student = Student()
    print(student.name)
    print(student.test_date)
    print(student.test_time)
    '''

    '''
    tourist = Tourist()
    print(tourist.name)
    print(tourist.test_date)
    print(tourist.test_time)
    '''