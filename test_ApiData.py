from collections import Counter
import unittest
from urllib import response
from requests import Request,Session
import Data_Collection
import tracemalloc
from Data_Collection import API_Data
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import warnings
import json
import os

class APITestCase(unittest.TestCase):




    def setUp(self):
        
        self.api=API_Data()
        
        self.response=self.api.session.get(self.api.url,params=self.api.parameters)       
        self.id='1'
        self.handle=open('/home/loum/Api_Data_collection/raw_data/83305966-ce8d-4c85-82a3-65e958ab50d3/data.json','r')
        #self.dir='/home/loum/Api_Data_collection/raw_data/'
        self.dir=self.api.dir
    def test_api(self):
        res = self.response.status_code
        self.assertEqual(res,200)

    def test_data(self):

        data=json.loads(self.response.text) 
        datapoint=data['data'][0]['id']
        self.assertTrue(datapoint,self.id)
    
    def test_file(self):
        for i,ig in enumerate(os.listdir(self.api.dir)): 
            if i ==0:
                
                with open(self.dir+str(ig)+'/data.json','r') as handle_file:
            
                    length=len(handle_file.read())
                    self.assertTrue(length>2)

    def tearDown(self):
        self.api.session.close()
        
        #warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def test_image_retriever(self):
        for i,ig in enumerate(os.listdir(self.api.dir)):
            if i ==0:
                self.new_dir=os.chdir(self.dir+str(ig)+'/Images/')
                count_ig=Counter(os.listdir(self.new_dir))
                self.assertTrue(len(count_ig)>30)