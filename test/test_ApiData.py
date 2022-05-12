import unittest
from Data_Collection_Pipeline import API_Data
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import boto3
import warnings
import json


class APITestCase(unittest.TestCase):
    os.chdir('/home/loum/Api_Data_collection/raw_data/') # change to your dir
    
    def setUp(self):
        self.api = API_Data()
        self.api.session.headers.update(self.api.headers)
        self.response = self.api.session.get(self.api.url, params=self.api.parameters)     
        self.id = '1'
        # self.dir='/home/loum/Api_Data_collection/raw_data/'
        self.dir = self.api.dir

    def test_api(self):
        res = self.response.status_code
        self.assertEqual(res, 200)

    def test_data(self):

        data = json.loads(self.response.text) 
        datapoint = data['data'][0]['id']
        self.assertTrue(datapoint, self.id)
      
    def test_file(self):
        
        for root, dir, files in os.walk(os.getcwd()):
            for file in files:
                if file == 'data.json':
                    with open(f'{root}/{file}','r') as handle_file: 
                        length = len(handle_file.read())
                        self.assertTrue(length > 2)
                                            
    def tearDown(self):
        
        self.api.session.close()
         
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        # boto3 connection will still be running
        # for a few  minutes then closes automatically

    def test_image_retriever(self):
        for root, dir, file in os.walk(os.getcwd()):
            if 'Images' in dir:
                count1 = len(os.listdir(root+'/Images/'))
                self.assertTrue(count1 > 30)
     
    def test_s3_upload(self):
        os.chdir('/home/loum/Api_Data_collection') # change to your dir
        s3 = boto3.client('s3')
        iname = 'BTC.png'
        # Of course, change the names of the files to match your own.
        s3.download_file('forthbucket', '08f2166f-819a-4b49-8d93-b5c2988470c5/Images/1.png', f'{iname}')
        if iname in os.listdir(os.getcwd()):
            iexist = True
        else:
            iexist = False
        self.assertTrue(iexist)
    
    def test_RDS_Connection(self):
        from sqlalchemy import create_engine
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        # Change it for your AWS endpoint
        ENDPOINT = 'database-1.c3v3xzshpy9w.us-east-1.rds.amazonaws.com' 
        USER = 'postgres'
        PASSWORD = 'postgres'
        PORT = 5432
        DATABASE = 'postgres'
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        try:

            engine.connect()
            self.assertTrue(True)
        except(ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

