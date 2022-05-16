import unittest
from Data_Collection_Pipeline import API_Data
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import boto3
import warnings
import json
from sqlalchemy import create_engine


class APITestCase(unittest.TestCase):
    # os.chdir('/raw_data/') # change to your dir
    
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
        # boto3 connection will still be running but
        # after a few  minutes it will closes automatically

    def test_image_retriever(self):
        for root, dir, file in os.walk(os.getcwd()):
            if 'Images' in dir:
                count1 = len(os.listdir(root+'/Images/'))
                self.assertTrue(count1 > 30)
     
    def test_s3_upload(self):
        
        s3 = boto3.client('s3')
        iname = '1.png'
        bucket = 'forthbucket'
        # To get the folder name in s3 type:
        result = s3.list_objects(Bucket=bucket, Delimiter='/')
        for o in result.get('CommonPrefixes'):
            folder_name = o.get('Prefix')
            # Of course, change the names of the files to match your own.
            # To download object from s3
            s3.download_file(bucket, f'{folder_name}', f'{iname}')
            # image download in your dir and checks if it exists
            if iname in os.listdir(os.getcwd()):
                iexist = True
            else:
                iexist = False
            self.assertTrue(iexist)
    
    def test_RDS_Connection(self):

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

unittest.main(argv=[''], verbosity=0, exit=False)