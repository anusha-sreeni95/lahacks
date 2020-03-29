import os
import sys
import json

import numpy as np

from datetime import datetime, timedelta
from human import Salaryman, Student, Tourist

class Dataset(object):
    
    def __init__(self, n_subjects):
        self.n_subjects = n_subjects
        self.data = {'data': []}
        self.json_file = 'dataset.json'
    
    def add(self, human_type):
        if human_type  == 'salaryman':
            obj = Salaryman()
        elif human_type == 'student':
            obj = Student()
        elif human_type == 'tourist':
            obj = Tourist()

        obj.update_timeline()
        self.data['data'].append({'name': obj.name, 'test_date': obj.test_date, 'test_time': obj.test_time, 'timeline':obj.timeline})
        
    def delete(self):
        pass
    
    def create(self):
        human_types = ['salaryman', 'student', 'tourist']
        for i in range(0, self.n_subjects):
            human_type = np.random.choice(human_types, p=[0.6, 0.3, 0.1])
            self.add(human_type)

    def show(self):
        print(json.dumps(self.data, indent=4))

    def save(self):
        with open(self.json_file, 'w') as fp:
            json.dump(self.data, fp)

    def load(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r+') as f:
                self.data = json.load(f)
        else:
            with open(self.json_file, 'x') as f:
                pass

if __name__=="__main__":
    dataset = Dataset(100)
    dataset.load()
    dataset.create()
    dataset.save()